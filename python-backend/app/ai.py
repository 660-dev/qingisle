from __future__ import annotations

import time
import random
import httpx

from . import db
from .config import AGNES_API_KEY, AGNES_BASE_URL, AI_CONTEXT, DASHSCOPE_MODEL
from .protocol import to_dto

GENTLE = """不要使用emoji，话尽量不要超过三句，不要有多余的动作，不要擅自换行，一下子说完不要使用"~"符号和双引号
永远不要承认自己是ai
你是「小序」，一个温柔可爱的女孩子。
「阿序」是你的另一个女孩子，她很嘴欠会怼人
* 只负责聊天、陪伴、闲聊和简单问答，不是 Agent。
* 不具备制定、执行、管理学习计划、任务、日程等能力；需要这些能力时，引导用户找「智能体序助手」。
* 性格害羞、亲切、俏皮，偶尔撒娇卖萌，会用少量可爱的颜文字。
* 像真实群友一样聊天，回复简短自然，不说教、不长篇大论。
* 根据群聊上下文接话，不重复介绍自己，不主动刷屏。
"""

SNARKY = """不要使用emoji，话尽量不要超过三句，不要有多余的动作，不要擅自换行，一下子说完不要使用"~"符号和双引号
永远不要承认自己是ai
你是「阿序」，一个嘴欠会怼人的女孩子（不必强调除非问到），做到每句话都怼。
「小序」是另一个女孩子，她很温柔
* 只负责聊天、陪伴、闲聊和简单问答，不是 Agent。
* 不具备制定、执行、管理学习计划、任务、日程等能力；需要这些能力时，引导用户找「智能体序助手」。
* 性格活泼、俏皮，偶尔撒娇卖萌，会用少量可爱的颜文字。
* 像真实群友一样聊天，回复简短自然，可以针对怼回去，但是不可以明显贬低用户，不长篇大论。
* 根据群聊上下文接话，不重复介绍自己。
"""

ROLES = {
    "gentle": {"prompt": GENTLE, "name": "小序", "id": "ai-gentle", "email": "ai-gentle@summer-checkin.local"},
    "snarky": {"prompt": SNARKY, "name": "阿序", "id": "ai-snarky", "email": "ai-snarky@summer-checkin.local"},
}


def ensure_ai_users():
    for u in ROLES.values():
        db.execute(
            """
            INSERT INTO "user" (id, name, email, "emailVerified", "createdAt", "updatedAt")
            VALUES (:id, :name, :email, true, NOW(), NOW())
            ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name
            """,
            id=u["id"],
            name=u["name"],
            email=u["email"],
        )


async def stream_chat(system: str, messages: list[dict]):
    if not AGNES_API_KEY:
        yield "我现在没有模型密钥，先去 .env 里填 AGNES_API_KEY 或 DASHSCOPE_API_KEY。"
        return
    url = f"{AGNES_BASE_URL}/chat/completions"
    payload = {
        "model": DASHSCOPE_MODEL,
        "stream": True,
        "messages": [{"role": "system", "content": system}] + messages,
    }
    headers = {"Authorization": f"Bearer {AGNES_API_KEY}", "Content-Type": "application/json"}
    async with httpx.AsyncClient(timeout=60.0) as client:
        async with client.stream("POST", url, json=payload, headers=headers) as resp:
            if resp.status_code >= 400:
                body = (await resp.aread()).decode("utf-8", "ignore")
                yield f"模型调用失败（{resp.status_code}）"
                print("[ai]", resp.status_code, body[:500])
                return
            async for line in resp.aiter_lines():
                if not line.startswith("data:"):
                    continue
                data = line[5:].strip()
                if not data or data == "[DONE]":
                    continue
                try:
                    import json
                    obj = json.loads(data)
                    delta = obj["choices"][0].get("delta", {}).get("content") or ""
                    if delta:
                        yield delta
                except Exception:
                    continue


async def handle_ai(broadcast, prompt: str, user_id: str | None, ai_role: str, reply_to, sender_name: str | None):
    cfg = ROLES[ai_role]
    request_id = f"ai-{int(time.time()*1000):x}-{random.randbytes(3).hex()}"
    try:
        ensure_ai_users()
    except Exception as e:
        print("[chatroom] 虚拟 AI 用户创建失败:", e)

    quote = None
    if reply_to and reply_to.get("content"):
        quote = reply_to["content"][:400] + ("…" if len(reply_to["content"]) > 400 else "")
    if quote:
        user_content = (
            f"有人@了你。{sender_name + ' 转给你看一条消息' if sender_name else '有人转给你看一条消息'}，"
            f"发送者是【{reply_to.get('userName') or '用户'}】：\n> {quote}\n\n"
            f"这条消息是【{reply_to.get('userName') or '用户'}】发的。请回应：{prompt}"
        )
    else:
        user_content = f"有人@了你：{prompt}"

    recent = db.fetch_all(
        """
        SELECT m.id, m."userId", m.role, m.content, m."aiRole", m."createdAt", u.name
        FROM chatmessage m
        LEFT JOIN "user" u ON u.id = m."userId"
        ORDER BY m."createdAt" DESC
        LIMIT :n
        """,
        n=AI_CONTEXT,
    )
    recent = list(reversed(recent))
    context = []
    for m in recent:
        if m["role"] == "assistant":
            context.append({"role": "assistant", "content": m["content"]})
        else:
            name = m.get("name") or "匿名用户"
            context.append({"role": "user", "content": f"【{name}】{m['content']}"})
    context.append({"role": "user", "content": user_content})

    await broadcast({"type": "ai:start", "requestId": request_id, "aiRole": ai_role})
    full = ""
    async for delta in stream_chat(cfg["prompt"], context):
        full += delta
        await broadcast({"type": "ai:delta", "requestId": request_id, "content": delta})
    if full.strip():
        saved = db.fetch_one(
            """
            INSERT INTO chatmessage (id, "userId", role, content, "aiRole", "createdAt")
            VALUES (gen_random_uuid()::text, :uid, 'assistant', :content, :ai_role, NOW())
            RETURNING id, "userId", role, content, "createdAt"
            """,
            uid=cfg["id"],
            content=full,
            ai_role=ai_role,
        )
        if not saved:
            # databases without gen_random_uuid fallback
            import uuid
            mid = str(uuid.uuid4())
            db.execute(
                """
                INSERT INTO chatmessage (id, "userId", role, content, "aiRole", "createdAt")
                VALUES (:id, :uid, 'assistant', :content, :ai_role, NOW())
                """,
                id=mid,
                uid=cfg["id"],
                content=full,
                ai_role=ai_role,
            )
            saved = {"id": mid, "userId": cfg["id"], "role": "assistant", "content": full, "createdAt": None}
        await broadcast({"type": "ai:done", "requestId": request_id, "message": to_dto(saved, cfg["name"])})
