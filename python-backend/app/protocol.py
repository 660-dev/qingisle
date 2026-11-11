from datetime import datetime, timezone

def iso(dt) -> str:
    if dt is None:
        return datetime.now(timezone.utc).isoformat()
    if getattr(dt, "tzinfo", None) is None:
        return dt.replace(tzinfo=timezone.utc).isoformat()
    return dt.isoformat()

def to_dto(msg: dict, user_name: str | None, image: str | None = None, reply_to: dict | None = None) -> dict:
    role = msg.get("role") if msg.get("role") in ("assistant", "system", "user") else "user"
    created = msg.get("createdAt") or msg.get("created_at")
    return {
        "id": msg["id"],
        "userId": msg.get("userId") or msg.get("userid"),
        "userName": user_name,
        "image": image,
        "role": role,
        "content": msg["content"],
        "createdAt": iso(created) if not isinstance(created, str) else created,
        "replyTo": reply_to,
    }
