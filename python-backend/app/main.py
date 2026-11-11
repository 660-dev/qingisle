from __future__ import annotations

import asyncio
import json
import re
import time
import uuid
from typing import Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, status
from fastapi.responses import PlainTextResponse

from . import db
from .ai import handle_ai
from .auth import authenticate
from .config import HOST, MAX_MESSAGE_LENGTH, PORT, RATE_MAX, RATE_WINDOW_MS
from .protocol import to_dto

app = FastAPI(title="summer-checkin python backend", version="0.1.0")


class Connection:
    def __init__(self, ws: WebSocket, user: dict):
        self.ws = ws
        self.user_id = user["id"]
        self.user_name = user.get("name") or "匿名"
        self.image = user.get("image")
        self.window_start = time.time() * 1000
        self.message_count = 0
        self.seen: set[str] = set()


connections: set[Connection] = set()


async def broadcast(message: dict):
    data = json.dumps(message, ensure_ascii=False)
    dead = []
    for c in list(connections):
        try:
            await c.ws.send_text(data)
        except Exception:
            dead.append(c)
    for c in dead:
        connections.discard(c)


@app.get("/health")
def health():
    return PlainTextResponse("ok")


@app.get("/")
def root():
    return {
        "service": "summer-checkin-python",
        "ws": "/ws",
        "health": "/health",
        "note": "这是 Node sidecar(server/) 的 Python 替代，监听与原来相同的协议。Next.js /api 仍负责页面接口。",
    }


@app.websocket("/ws")
@app.websocket("/")
async def websocket_endpoint(ws: WebSocket):
    cookie = ws.headers.get("cookie")
    user = authenticate(cookie)
    if not user:
        await ws.close(code=status.WS_1008_POLICY_VIOLATION, reason="Unauthorized")
        return
    await ws.accept()
    conn = Connection(ws, user)
    connections.add(conn)
    await broadcast({"type": "presence", "online": len(connections)})
    await ws.send_text(json.dumps({
        "type": "ready",
        "user": {"id": user["id"], "name": user.get("name"), "image": user.get("image")},
    }, ensure_ascii=False))
    try:
        while True:
            raw = await ws.receive_text()
            await handle_raw(conn, raw)
    except WebSocketDisconnect:
        pass
    finally:
        connections.discard(conn)
        await broadcast({"type": "presence", "online": len(connections)})


def check_rate(conn: Connection) -> bool:
    now = time.time() * 1000
    if now - conn.window_start > RATE_WINDOW_MS:
        conn.window_start = now
        conn.message_count = 0
    conn.message_count += 1
    return conn.message_count <= RATE_MAX


def extract_ai(content: str) -> list[dict]:
    results = []
    for m in re.finditer(r"@青青|@屿屿|@屿助手|@AI|^\s*/ai(?=\s|$)", content, flags=re.I | re.M):
        token = m.group(0)
        role = "gentle" if "青青" in token else "snarky"
        after = content[m.end():].strip()
        prompt = after or content[: m.start()].strip()
        if prompt:
            results.append({"prompt": prompt, "aiRole": role})
    uniq = []
    seen = set()
    for r in results:
        if r["aiRole"] not in seen:
            seen.add(r["aiRole"])
            uniq.append(r)
    return uniq


async def send_error(conn: Connection, code: str, reason: str):
    await conn.ws.send_text(json.dumps({"type": "error", "code": code, "reason": reason}, ensure_ascii=False))


async def handle_raw(conn: Connection, raw: str):
    try:
        msg = json.loads(raw)
    except json.JSONDecodeError:
        await send_error(conn, "invalid_json", "消息格式错误")
        return
    typ = msg.get("type")
    if typ == "ping":
        await conn.ws.send_text(json.dumps({"type": "pong"}))
        return
    if typ != "message":
        await send_error(conn, "unknown_type", "未知消息类型")
        return
    content = (msg.get("content") or "").strip()
    if not content:
        return
    if len(content) > MAX_MESSAGE_LENGTH:
        await send_error(conn, "too_long", "消息过长")
        return
    if not check_rate(conn):
        await send_error(conn, "rate_limited", "发送太频繁，稍后再试")
        return
    client_id = msg.get("clientId") or ""
    if client_id:
        if client_id in conn.seen:
            return
        conn.seen.add(client_id)
        if len(conn.seen) > 200:
            conn.seen.pop()
    reply_to = None
    reply_to_id = msg.get("replyToId")
    if reply_to_id:
        target = db.fetch_one(
            """
            SELECT m.id, m."userId", m.content, u.name
            FROM chatmessage m
            LEFT JOIN "user" u ON u.id = m."userId"
            WHERE m.id = :id
            """,
            id=reply_to_id,
        )
        if not target:
            await send_error(conn, "reply_not_found", "回复的消息不存在")
            return
        reply_to = {
            "id": target["id"],
            "userId": target.get("userId"),
            "userName": target.get("name") or "用户",
            "content": target["content"],
        }
    mid = str(uuid.uuid4())
    saved = db.fetch_one(
        """
        INSERT INTO chatmessage (id, "userId", role, content, "replyToId", "createdAt")
        VALUES (:id, :uid, 'user', :content, :reply, NOW())
        RETURNING id, "userId", role, content, "createdAt"
        """,
        id=mid,
        uid=conn.user_id,
        content=content,
        reply=reply_to_id,
    )
    if not saved:
        db.execute(
            """
            INSERT INTO chatmessage (id, "userId", role, content, "replyToId", "createdAt")
            VALUES (:id, :uid, 'user', :content, :reply, NOW())
            """,
            id=mid,
            uid=conn.user_id,
            content=content,
            reply=reply_to_id,
        )
        saved = {"id": mid, "userId": conn.user_id, "role": "user", "content": content, "createdAt": None}
    sender = db.fetch_one('SELECT name, image FROM "user" WHERE id = :id', id=conn.user_id)
    user_name = (sender or {}).get("name") or conn.user_name
    image = (sender or {}).get("image") if sender else conn.image
    conn.user_name = user_name
    conn.image = image
    await broadcast({"type": "message", "message": to_dto(saved, user_name, image, reply_to)})
    for ai in extract_ai(content):
        asyncio.create_task(handle_ai(broadcast, ai["prompt"], conn.user_id, ai["aiRole"], reply_to, user_name))


def run():
    import uvicorn
    print(f"[ws] Python WebSocket 服务启动 :{PORT}")
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=False)


if __name__ == "__main__":
    run()
