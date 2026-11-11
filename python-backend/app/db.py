from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from .config import DATABASE_URL

_engine: Engine | None = None

def engine() -> Engine:
    global _engine
    if _engine is None:
        if not DATABASE_URL:
            raise RuntimeError("DATABASE_URL is not set")
        _engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_size=5)
    return _engine

def fetch_one(sql: str, **params):
    with engine().connect() as conn:
        row = conn.execute(text(sql), params).mappings().first()
        return dict(row) if row else None

def fetch_all(sql: str, **params):
    with engine().connect() as conn:
        rows = conn.execute(text(sql), params).mappings().all()
        return [dict(r) for r in rows]

def execute(sql: str, **params):
    with engine().begin() as conn:
        result = conn.execute(text(sql), params)
        return result
