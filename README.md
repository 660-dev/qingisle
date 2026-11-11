> 本仓库是 **知序 Zhixu**，基于开源项目 https://github.com/gdut4140/summer-checkin 二次开发（原项目 MIT 协议，见 [LICENSE](./LICENSE)，保留原作者版权声明）。演示：https://YOUR_DEMO_URL

<h1 align="center">
  <span style="color:#ffffff;">知</span>
  <span style="color:#d7ef83;">序</span>
</h1>

<p align="center">
  🌱 把每一次专注，都长成一座岛
</p>

<p align="center">
  <strong>全栈学习成长平台</strong> · 小岛打卡 · 计划 · 专注 · AI 智能体 · 知识库 · 聊天室
</p>

<p align="center">

![Next.js](https://img.shields.io/badge/Next.js-16-black?style=for-the-badge&logo=next.js&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Prisma](https://img.shields.io/badge/Prisma-5-2D3748?style=for-the-badge&logo=prisma&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Tailwind](https://img.shields.io/badge/Tailwind%20CSS-v4-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)

</p>

<p align="center">
  <a href="#-功能亮点">功能亮点</a> ·
  <a href="#-相对原项目的主要修改">二次开发说明</a> ·
  <a href="#-功能总览">功能总览</a> ·
  <a href="#-技术架构">技术架构</a> ·
  <a href="#-快速开始">快速开始</a> ·
  <a href="#-部署docker">部署</a> ·
  <a href="#-尚未迁移与待办">未迁移/待办</a> ·
  <a href="#-常见问题">FAQ</a>
</p>

---

## ✨ 功能亮点

| 亮点 | 说明 |
|---|---|
| 🏝️ **学习小岛打卡** | 每日打卡签到，3D 学习岛屿随累计时长成长，连续天数 + 年度热力图实时更新 |
| 🤖 **AI 原生智能体** | 分析学习数据生成个性化计划、文档自动拆任务、长期记忆、每周学习报告 |
| 📚 **知识库 RAG** | 上传 md / pdf / docx / txt，向量检索后基于你的文档回答 |
| 💬 **实时聊天室** | WebSocket 群聊，支持引用回复，`@AI` 唤起 AI 伙伴流式回复（Markdown / 代码高亮）|
| 📊 **周报一键导出** | 统计页按周聚合打卡、专注时长与完成任务，导出 Markdown 周报 |
| 🌿 **多场景主题 + 环境音** | 雨林 / 雪日 / 暖云一键换肤，自动配对应环境音，离开站点自动静音 |
| 📈 **个人统计主页** | 专注时长趋势、年度打卡热力图、最佳科目，进步一目了然 |

## 🌿 相对原项目的主要修改

> 原项目来源：https://github.com/gdut4140/summer-checkin （MIT）。以下为本仓库在其基础上的改动。

- **品牌更名**：产品更名为「知序 Zhixu」，落地页、导航、浏览器标题与主要文案同步替换；AI 伙伴更名为「小序 / 阿序 / 序助手」。品牌名集中配置在 `src/config/brand.ts`。
- **聊天室后端新增 Python 实现**：在保留原 Node sidecar（`server/`）的同时，新增 Python FastAPI 服务 `python-backend/`，可独立替代聊天室 WebSocket 进程（替代范围见下节）。
- **新增周报导出**：统计页「周报导出」按钮，按周聚合打卡 / 专注 / 完成任务并结合 Agent 周报生成逻辑，导出 Markdown（接口 `src/app/api/reports/weekly/route.ts`，实现 `src/lib/reports/weekly-export.ts`）。
- **登录接入 Server Action**：登录表单通过 `src/app/(auth)/actions.ts` 调用 Better Auth 完成。

### Python 后端到底替换了什么（边界说明，勿扩大宣传）

`python-backend/` **只替代原来的聊天室 WebSocket sidecar**（原 `tsx server/index.ts`，端口 3001）。

**已由 Python 承接：**
- 实时聊天 WebSocket 连接与在线状态广播
- Better Auth 会话 cookie 查库鉴权
- `@小序 / @阿序 / @序助手 / @AI` 流式回复
- 引用回复、消息限流、心跳保活与断线清理

**尚未迁移、仍在 Next.js `/api` 中实现：**
- 登录 / 注册（Better Auth）
- 计划 / 待办 / 打卡 / 学习记录
- 知识库 RAG 检索与文档处理
- Agent 智能体工作流
- 阿里云 OSS 预签名直传

> 也就是说，本仓库**不是“全部后端改为 Python”**；除聊天室 WebSocket 外，其余业务后端仍是 Next.js API Routes。页面本身也仍需运行 Next.js 进程。

## 📸 截图

<p align="center">
  <img src="public/start.png" width="85%" alt="产品进入页" />
  <br/>
  <em>产品进入页 · 多场景主题，切换场景整页换色</em>
</p>

## 🧩 功能总览

> 主导航：**小岛** · **计划** · **阅读** · **主页**（个人统计），全局入口含聊天室、智能体、通知铃、音量与环境音。

### 🏝️ 小岛（每日打卡）
- 进入 3D 学习小岛，点按钮记录今日打卡与心情；场景随氛围切换
- 连续打卡天数、最长连续、累计时长驱动岛屿成长
- 年度日历热力图，坚持足迹一目了然

### 📋 计划与任务
- 任务制进度：`已完成任务 / 总任务`，计划、任务、打卡三方联动
- **文档工作室**：Markdown 撰写计划文档，AI 按文档自动拆分任务
- **今日待办**：独立待办清单，AI 智能体可直接增删改查

### 🍅 专注与沉浸
- 番茄钟专注（可自定义时长，默认 25+5），完成自动写入学习记录
- 沉浸模式：全屏无干扰界面，时间 / 鼓励语纯净展示
- 专注时长趋势、日均学习等数据进入个人统计主页

### 🤖 AI 智能体
- 学习计划工作流：先分析学习数据，再生成个性化计划（关键步骤请求确认）
- 文档自动拆解为任务，知识库向量检索 + 基于文档回答
- 长期记忆：AI 自动提取用户偏好注入上下文
- 通知中心：每日总结、每周报告、进度提醒（每日去重）

### 💬 多人聊天室
- WebSocket 实时群聊：所有在线用户共享一条消息流，在线人数实时广播
- **引用回复**：对任意消息回复，对方收到「某某某回复了你」的滚动感知提醒
- `@AI` 唤起 AI 伙伴流式回复，内置「小序」「阿序」等人格，支持 Markdown 与代码高亮
- WebSocket 为独立 sidecar 进程，握手期 Cookie 鉴权，心跳保活 + 断线清理
- AI 以虚拟用户身份入群，读取最近群聊上下文后流式回推，模型池 LOW 档自动降级并做 token 记账 / 限流
- sidecar 有两套可互换实现：Node（`server/`）与 Python FastAPI（`python-backend/`）

### 👤 账号与头像
- Better Auth 注册 / 登录 / 会话管理
- 头像阿里云 OSS 预签名直传，**历史头像可一键回滚**

### ✨ 其他体验
- 雨林 / 雪日 / 暖云三场景，整页配色 + 对应环境音（雨声 / 雪声）
- 首次使用新手引导，带游标逐步介绍核心入口
- 连续操作体验打磨：沉浸聚焦、场景切换动效、3D 岛屿

## 🛠 技术架构

| 层 | 技术 |
|---|---|
| 前端 | Next.js 16（App Router）、React 19、TypeScript、Tailwind CSS v4 |
| 3D / 动效 | Three.js（react-three-fiber）、GSAP、Motion（按需动态加载）|
| 业务后端 | Next.js API Routes、AI SDK、Prisma ORM |
| 实时（二选一） | WebSocket sidecar：Node `server/`（tsx）或 Python FastAPI `python-backend/`（Uvicorn）|
| 数据库 | PostgreSQL 16 + pgvector（向量检索）、Prisma |
| AI | OpenAI 兼容 API，**模型池**多模型可配（默认 Agnes 中国站，Embedding 走阿里百炼）|
| 文件存储 | 阿里云 OSS（头像预签名直传）|
| 可视化 | 自绘热力图 / 统计条（无第三方图表库）|

### 架构概览

```
浏览器
  │
  ├─ HTTP/HTTPS ──► Nginx（反向代理）
  │                    ├─ /            → Next.js 应用（:3000）
  │                    └─ /ws          → WebSocket sidecar（:3001）
  │
  ├─ 头像上传 ──► 阿里云 OSS（预签名直传，不经应用服务器）
  │
  └─ WebSocket ─────► sidecar（聊天室 + AI 流式回复）
                         ├─ Node:  server/index.ts   （原实现，保留）
                         └─ Python: python-backend/  （FastAPI 替代实现）
                                     │
                                     └─ Prisma / SQLAlchemy ──► PostgreSQL 16 + pgvector
```

- **Next.js 应用**：页面、业务 API、AI 智能体、知识库、周报导出
- **WebSocket sidecar**（`server/` 或 `python-backend/`，二选一）：独立进程，只承载多人聊天室与 AI 流式回复
- **PostgreSQL**：主数据 + pgvector 向量检索（文档分块 / 用户记忆）
- **OSS**：头像对象存储，浏览器直传，应用只签发预签名 URL

## 🚀 快速开始

### 环境要求

| 依赖 | 版本 |
|---|---|
| Node.js | 18+ |
| PostgreSQL | 16（建议 `pgvector/pgvector` 镜像，向量检索需要 pgvector 扩展）|
| Python（仅使用 Python sidecar 时） | 3.11+ |

### 本地开发

```bash
# 1. 安装前端依赖
npm install

# 2. 配置环境变量
cp .env.example .env   # 填入真实 API Key 与数据库地址

# 3. 生成 Prisma Client
npx prisma generate

# 4. 初始化数据库（建表 + 写入引导模板等种子数据）
npx prisma db push
npx prisma db seed

# 5. 启动 Next.js 主应用（:3000，页面与业务 API 都在这个进程）
npm run dev
```

### 启动聊天室 WebSocket（二选一）

**方式 A：原 Node sidecar**

```bash
npm run ws:dev        # tsx server/index.ts，监听 :3001
```

**方式 B：Python FastAPI sidecar**

```bash
cd python-backend
python -m venv .venv
# Windows: .venv\Scripts\activate    |    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cd ..
# 在仓库根目录运行（读取根目录 .env）
python -m uvicorn python-backend.app.main:app --host 0.0.0.0 --port 3001
# 或：npm run ws:py
```

> 两个 sidecar 协议与前端聊天室兼容（`ready` / `message` / `ai:*` / `presence` / cookie 鉴权），按机器环境任选其一即可，不要同时占用 3001 端口。

> **数据库升级**：本项目使用手写 SQL 迁移，见 `prisma/*.sql`，已有数据库按需执行对应文件。

## 🔑 环境变量

根目录 `.env.example` 为脱敏模板，复制为 `.env` 后填写；**`.env` 不纳入 git**。

| 变量 | 说明 |
|---|---|
| `DATABASE_URL` | PostgreSQL 连接串（Next.js 与 Python sidecar 共用）|
| `AGNES_API_KEY` / `DASHSCOPE_API_KEY` | AI 对话 API Key（OpenAI 兼容；模型池优先读 `AGNES_*`，`DASHSCOPE_*` 兼容旧配置）|
| `AGNES_BASE_URL` / `DASHSCOPE_BASE_URL` | 对话 API 地址（默认 `https://api.agnes-ai.cn/v1` 中国站）|
| `DASHSCOPE_MODEL` | 对话模型（默认 `agnes-2.5-flash`）|
| `EMBEDDING_API_KEY` / `MODEL` / `BASE_URL` | 向量模型（默认阿里百炼）|
| `AI_TOKEN_LIMIT` | 每用户每日 token 上限（0 = 不限）|
| `BETTER_AUTH_SECRET` | 会话签名密钥（`openssl rand -base64 32`；Python sidecar 校验 cookie 时也读取）|
| `BETTER_AUTH_URL` | 登录回调地址（部署时 = 公网访问地址，不带端口）|
| `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY` | Server Actions 加密密钥（`openssl rand -hex 32`）|
| `OSS_ACCESS_KEY_ID` / `SECRET` | 阿里云 OSS 凭证（头像直传）|
| `OSS_BUCKET` / `REGION` / `PUBLIC_BASE_URL` | OSS Bucket 配置 |
| `CRON_SECRET` | agent 定时接口 Bearer 鉴权（服务器本地维护，勿整包覆盖 .env）|

Python sidecar 额外读取 / 可调项（见 `python-backend/.env.example`）：

| 变量 | 说明 |
|---|---|
| `WS_PORT` | WebSocket 监听端口（默认 `3001`）|
| `WS_HOST` | 监听地址（默认 `0.0.0.0`）|
| `DEV_USER_ID` | **仅本地调试**：无有效登录 cookie 时用该用户 id 进房；生产环境不要设置 |
| `DEV_USER_NAME` | 调试用户名（默认「本地用户」）|

## 📁 项目结构

```
├── src/
│   ├── app/                 # App Router 页面与 API 路由
│   │   ├── (auth)/          # 登录 / 注册（含 actions.ts Server Action）
│   │   ├── (dashboard)/     # 小岛 / 计划 / 阅读 / 统计主页
│   │   ├── agent/           # AI 智能体页
│   │   └── api/             # 后端接口（chat / ai / knowledge / plans / reports…）
│   ├── components/          # UI 组件（聊天室 / 专注室 / 智能体 / 统计 / 岛屿…）
│   ├── lib/                 # 业务逻辑、AI 工具、RAG 检索、记忆、用量、reports 周报
│   ├── config/brand.ts      # 品牌名 / slogan / AI 伙伴名集中配置
│   ├── context/             # 全局状态（场景 / 引导）
│   └── styles/ types/       # 全局样式、共享类型
├── server/                  # 原 Node WebSocket sidecar（聊天室 + AI 流式回复）
├── python-backend/         # Python FastAPI WebSocket sidecar（可替代 server/）
│   ├── app/                 # main / protocol / ai / auth / config / db
│   ├── run.py               # 本地启动入口
│   └── requirements.txt
├── prisma/                  # Schema、种子数据、SQL 迁移
├── scripts/                 # 部署、文档提取、重置密码等工具
└── nginx/                   # 反向代理配置
```

## 🧰 内置脚本工具

| 脚本 | 用途 |
|---|---|
| `scripts/reset-password.ts` | 管理员重置用户密码（scrypt 与 Better Auth 兼容）|
| `scripts/extract_pdf.py` / `extract_docx.py` | 知识库 PDF / Word 文本提取 |
| `scripts/deploy.sh` | Docker 镜像构建与上传部署 |
| `scripts/server-setup.sh` | 新服务器初始化（装 Docker / 开端口）|

## 🗄 数据模型

27 张表，按模块分组：

| 模块 | 表 |
|---|---|
| 用户与认证 | `user` · `session` · `account` · `avatarchange`（头像历史）|
| 学习核心 | `plan` · `plantask` · `todo` · `checkin` · `studyrecord` |
| AI 智能体 | `agentrun` · `agentstep` · `agentapproval` · `agentdecision` · `agenttoolcall` · `usermemory` · `aihistory` · `conversation` · `conversationmessage` · `agentschedule` |
| 聊天室 | `chatmessage` |
| 知识库 / 文档 | `document` · `documentchunk` · `knowledgedoc` · `plantemplate` · `documenttemplate` |
| 其他 | `notification` · `tokenusage` |

> 完整字段见 `prisma/schema.prisma`。

## 🐳 部署（Docker）

```bash
# 一键部署（PostgreSQL + Next.js 应用 + Nginx）
docker compose up -d --build
```

- 需提供 AI 对话、Embedding、Better Auth、OSS 等环境变量（见上文表格）
- `BETTER_AUTH_URL` 设置为服务器的公网地址（不含端口，走 Nginx 80）
- 首次部署后需初始化数据库：`prisma db push` + `prisma db seed`
- 生产环境注意：修改 `docker-compose.yml` 中 PostgreSQL 默认密码；容器内置 Python 仅用于 PDF / Word 文本提取

### 当前容器编排与 Python sidecar 的关系（重要）

- 现有 `Dockerfile` / `docker-entrypoint.sh` / `docker-compose.yml` 打包并启动的 WebSocket sidecar **仍是原 Node 实现**：entrypoint 后台执行 `node tsx server/index.ts &`，Nginx 把 `/ws` 转发到同容器 `app:3001`。
- **Python `python-backend/` 目前尚未接入 Docker 编排**：镜像未安装 Python 依赖、未作为独立服务启动，Nginx upstream 也未指向 Python 进程。若生产环境要使用 Python sidecar，需要自行：在编排中增加 Python 服务（安装 `requirements.txt`、开放 3001）、调整 Nginx upstream 指向，并复用同一套环境变量。
- 容器内自带的 `python3` 只服务于知识库 PDF / Word 文本提取（`scripts/extract_*.py`），**不是** Python WebSocket 后端。

## ⚠️ 尚未迁移与待办

- **业务后端未 Python 化**：除聊天室 WebSocket 外，登录注册、计划 / 待办 / 打卡、知识库 RAG、Agent、OSS 预签名仍在 Next.js `/api`。
- **Python sidecar 未容器化**：见上节，生产 Docker 部署当前仍跑 Node sidecar。
- **占位信息待填**：`src/config/brand.ts` 与 `docs/RESUME.md` 中的 GitHub 用户名、仓库名、演示站 URL 仍为占位（`YOUR_GITHUB_USER` / `YOUR_DEMO_URL`），发布前替换为真实值。
- **沿用原项目路线图**：HTTPS 上线（域名 + Let's Encrypt）、邮件自助找回密码（SMTP）、数据库定期自动备份、更多场景主题与环境音。

## ❓ 常见问题

**忘记密码了怎么办？**
管理员用 `scripts/reset-password.ts` 重置，无需邮件服务，几秒搞定。

**为什么数据库里密码是一串看不懂的字符？**
那是 scrypt 密码哈希（`盐:哈希`），不是明文。密码不可逆，泄露数据库也推不出原密码——这是安全设计。

**纯 HTTP 访问时聊天室发不出消息？**
`crypto.randomUUID()` 只在 HTTPS / localhost（安全上下文）可用，代码已做兜底。长期建议上 HTTPS。

**知识库上传 PDF / Word 报“文本提取失败”？**
容器内置了 Python + PyPDF2 + python-docx，确认部署的镜像包含这些依赖。

**Python sidecar 启动后连不上 / 鉴权失败？**
确认根目录 `.env` 的 `DATABASE_URL`、`BETTER_AUTH_SECRET` 与 Next.js 应用一致；本地无登录 cookie 时可临时设 `DEV_USER_ID` 调试，生产不要保留该项。

## 🗺 路线图

- [ ] Python sidecar 接入 Docker 编排（独立服务 + Nginx upstream）
- [ ] HTTPS 上线（需配置域名 + Let's Encrypt 证书）
- [ ] 忘记密码自助流程（邮件链接重置，需接入 SMTP）
- [ ] 数据库定期自动备份
- [ ] 更多场景主题与专属环境音

## 🙏 致谢

- [Next.js](https://nextjs.org) · [React](https://react.dev) · [Tailwind CSS](https://tailwindcss.com)
- [Prisma](https://www.prisma.io) · [PostgreSQL](https://www.postgresql.org) · [pgvector](https://github.com/pgvector/pgvector)
- [Better Auth](https://better-auth.com) · [AI SDK](https://ai-sdk.dev) · [Three.js](https://threejs.org) · [FastAPI](https://fastapi.tiangolo.com) · [Motion](https://motion.dev)
- 基础项目由 [gdut4140/summer-checkin](https://github.com/gdut4140/summer-checkin) 提供（MIT）。

## 📄 License

[MIT](./LICENSE) — 沿用原项目 MIT 协议与原作者版权声明；二次开发部分同样以 MIT 开源。
