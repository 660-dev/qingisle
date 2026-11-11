import os
from dotenv import load_dotenv

load_dotenv(".env.local", override=True)
load_dotenv(".env")

PORT = int(os.getenv("WS_PORT", "3001"))
HOST = os.getenv("WS_HOST", "0.0.0.0")
DATABASE_URL = os.getenv("DATABASE_URL", "")
SESSION_COOKIE = "better-auth.session_token"
MAX_MESSAGE_LENGTH = 2000
RATE_WINDOW_MS = 60_000
RATE_MAX = 30
AI_CONTEXT = 20
HEARTBEAT_SEC = 30
DEV_USER_ID = os.getenv("DEV_USER_ID", "").strip()
DEV_USER_NAME = os.getenv("DEV_USER_NAME", "本地用户")
AGNES_API_KEY = os.getenv("AGNES_API_KEY") or os.getenv("DASHSCOPE_API_KEY") or ""
AGNES_BASE_URL = (os.getenv("AGNES_BASE_URL") or os.getenv("DASHSCOPE_BASE_URL") or "https://api.agnes-ai.cn/v1").rstrip("/")
DASHSCOPE_MODEL = os.getenv("DASHSCOPE_MODEL", "agnes-2.5-flash")
