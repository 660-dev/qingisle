from __future__ import annotations

import hashlib
import hmac
from http.cookies import SimpleCookie
from urllib.parse import unquote

from . import db
from .config import DEV_USER_ID, DEV_USER_NAME, SESSION_COOKIE


def parse_session_cookie(cookie_header: str | None) -> str | None:
    if not cookie_header:
        return None
    jar = SimpleCookie()
    try:
        jar.load(cookie_header)
    except Exception:
        return None
    morsel = jar.get(SESSION_COOKIE) or jar.get(SESSION_COOKIE.replace(".", "_"))
    if not morsel:
        # sometimes better-auth uses prefixed cookie
        for key in jar:
            if "session_token" in key:
                morsel = jar[key]
                break
    if not morsel:
        return None
    return unquote(morsel.value)


def _sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def authenticate(cookie_header: str | None) -> dict | None:
    raw = parse_session_cookie(cookie_header)
    user = None
    if raw:
        candidates = [raw]
        if "." in raw:
            candidates.append(raw.rsplit(".", 1)[0])
        hashed = [_sha256(c) for c in candidates]
        tokens = list(dict.fromkeys(candidates + hashed))
        for token in tokens:
            row = db.fetch_one(
                """
                SELECT u.id, u.name, u.image, s.token, s."expiresAt" AS expires_at
                FROM session s
                JOIN "user" u ON u.id = s."userId"
                WHERE s.token = :token
                  AND s."expiresAt" > NOW()
                LIMIT 1
                """,
                token=token,
            )
            if row:
                user = {"id": row["id"], "name": row["name"], "image": row.get("image")}
                break
    if user:
        return user
    if DEV_USER_ID:
        row = db.fetch_one('SELECT id, name, image FROM "user" WHERE id = :id', id=DEV_USER_ID)
        if row:
            return {"id": row["id"], "name": row["name"], "image": row.get("image")}
        return {"id": DEV_USER_ID, "name": DEV_USER_NAME, "image": None}
    return None
