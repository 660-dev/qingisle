# summer-checkin Python 后端

替换原来的 Node sidecar：`tsx server/index.ts`（端口 3001）。

协议与前端聊天室兼容：`ready` / `message` / `ai:*` / `presence` / cookie 鉴权。

## 做了什么、没做什么

已替换：
- 实时聊天 WebSocket
- Better Auth 会话 cookie 查库
- @青青 / @屿屿 / @屿助手 / @AI 流式回复
- 引用回复、限流、心跳由 Uvicorn/WebSocket 保活

未整仓翻译（仍在 Next.js `/api`）：
- 登录注册（better-auth）
- 计划 / 待办 / 打卡 / 知识库 RAG / Agent 智能体
- OSS 预签名

页面应用仍要跑 `npm run dev`。Python 只替代 `npm run ws:dev`。

## 启动

在仓库根目录（与 `.env` 同级）：

```bash
cd python-backend
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt
cd ..
python -m uvicorn python-backend.app.main:app --host 0.0.0.0 --port 3001
```

或：

```bash
cd python-backend
pip install -r requirements.txt
# 把上级目录的 .env 拷过来，或在仓库根运行
set PYTHONPATH=.
python -m app.main
```

环境变量与原项目相同：`DATABASE_URL`、`AGNES_API_KEY` / `DASHSCOPE_*`。

本地没有登录 cookie 时，可在 `.env` 设 `DEV_USER_ID=` 数据库里已有用户的 id。
