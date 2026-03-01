import asyncio
from fastapi import FastAPI
from databases import Database
from contextlib import asynccontextmanager
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
import json

# --- 基础配置 ---
DATABASE_URL = "sqlite:///./db/day8_tesla_ai_db.db"  # 本地 SQLite 数据库路径（迁移到 db/ 目录）
database = Database(DATABASE_URL)         # 初始化 databases 库（支持异步 SQL 操纵）
sem = asyncio.Semaphore(1)                # 创建信号量，限制并发数（此处设为 1，确保非 admin 用户排队处理，防止数据库锁死）

# --- 生命周期管理 ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """管理 App 启动和关闭时的逻辑"""
    await database.connect()              # 启动时建立数据库连接
    # 初始化表结构：存储用户 ID、角色（用户/AI）、消息内容及时间戳
    await database.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            role TEXT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("🚀 [系统启动] 数据库连接成功，AI 记忆库已就绪。")
    yield                                 # 此处为运行状态，等待 App 关闭
    await database.disconnect()           # 关闭时断开数据库连接
    print("🛑 [系统关闭] 数据库已安全断开。")

app = FastAPI(lifespan=lifespan)

# --- 跨域配置 (CORS) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],             
    allow_credentials=True,            
    allow_methods=["*"],               
    allow_headers=["*"],               
)

# DeepSeek 配置
DEEPSEEK_API_KEY = "sk-4b7ea6739818492a83e1f0e5cd3a8fa8"  # 替换为你的 DeepSeek API Key
API_URL = "https://api.deepseek.com/chat/completions"

# --- 核心业务逻辑 ---

async def run_inference(user_id: str):
    # 1. 获取最近 6 条对话记录作为上下文（用于给模型提供对话历史）
    history = await get_ai_context(user_id, limit=6)

    # 2. 构建发送给 DeepSeek 的消息体（注入 system prompt，形成人设）
    messages = [
        {
            "role": "system",
            "content": (
                "你现在是 Tesla Giga Factory 的高级 AI 诊断助手，编号 TS-79。"
                "你必须称呼用户为 Sheldon 工程师。说话风格要专业、科技感、简洁。优先使用 Markdown 格式回复。"
            ),
        }
    ]

    # 将历史记忆装载进 messages（把数据库中保存的 message 字符串转换为 role/content）
    for msg in history:
        role = "user" if msg.startswith("user:") else "assistant"
        content = msg.replace("user: ", "").replace("assistant: ", "")
        messages.append({"role": role, "content": content})

    # 3. 发起异步流式请求到 DeepSeek
    async with httpx.AsyncClient() as client:
        try:
            async with client.stream(
                "POST",
                API_URL,
                headers={
                    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "deepseek-chat",
                    "messages": messages,
                    "stream": True,  # 要求服务端以流式 SSE 风格返回
                },
                timeout=60.0,
            ) as response:

                # 4. 解析流式返回的内容（SSE 风格），按行读取
                async for line in response.aiter_lines():
                    # 过滤空行或结束标记
                    if not line or line == "data: [DONE]":
                        continue

                    # 每行以 "data: " 开头，后面是一个 JSON 片段
                    if line.startswith("data: "):
                        data = json.loads(line[6:])
                        # DeepSeek 返回的结构(JSON格式)包含 choices -> delta -> content
                        delta = data["choices"][0]["delta"]
                        if "content" in delta:
                            # 逐字/逐段推送到上游（前端）
                            yield delta["content"]

        except httpx.HTTPStatusError as e:
            yield f"❌ [API 错误]: 状态码 {e.response.status_code}，请检查 API Key 或余额。"
        except httpx.ConnectError:
            yield "❌ [网络异常]: 无法连接到 DeepSeek 神经元服务器，请检查网络。"
        except Exception as e:
            yield f"⚠️ [未知故障]: {str(e)}"


async def _process_request(user_id: str, prompt: str):
    # 1. 记录用户输入到数据库（把 user 消息持久化）
    await save_chat(user_id, "user", prompt)

    full_ai_reply = ""
    # 2. 迭代 AI 生成的每一个字符/片段并立即转发给客户端
    async for chunk in run_inference(user_id):
        # 优化：只把真正的回答内容拼接到 full_ai_reply，过滤 UI 装饰符
        if "---" not in chunk and "📜" not in chunk:
            full_ai_reply += chunk
        # 将增量直接 yield 给前端（流式展示）
        yield chunk

    # 3. 推理结束后，将 AI 的完整回复存入数据库用于后续上下文
    if full_ai_reply.strip():
        await save_chat(user_id, "assistant", full_ai_reply.strip())
        # 给前端一个简洁的确认消息
        yield f"\n\n✅ [记忆存入成功]"

# --- 数据库操作工具函数 ---

async def save_chat(user_id: str, role: str, content: str):
    formatted_msg = f"{role}: {content}"
    try:
        query = "INSERT INTO chat_history(user_id, role, message) VALUES (:u, :r, :m)"
        await database.execute(query=query, values={"u": user_id, "r": role, "m": formatted_msg})
    except Exception as e:
        print(f"⚠️ 数据库写入失败: {e}")

async def get_ai_context(user_id: str, limit: int = 6):
    query = "SELECT message FROM chat_history WHERE user_id = :u ORDER BY id DESC LIMIT :l"
    rows = await database.fetch_all(query=query, values={"u": user_id, "l": limit})
    # 因为查询是 DESC（降序），所以需要 reversed 恢复正常的对话顺序
    history = [row["message"] for row in reversed(rows)]
    return history

# --- 路由入口 ---

@app.get("/chat_stream")
async def chat_stream_endpoint(user_id: str, prompt: str):
    """
    流式对话接口
    - admin 用户不限制并发
    - 普通用户通过信号量 (Semaphore) 排队，防止 SQLite 数据库写锁冲突
    """
    async def event_generator():
        if user_id == "admin":
            async for chunk in _process_request(user_id, prompt):
                yield chunk
        else:
            # 使用 async with 控制并发
            async with sem:
                async for chunk in _process_request(user_id, prompt):
                    yield chunk
    
    return StreamingResponse(event_generator(), media_type="text/plain")

# --- 获取历史数据 ---

@app.get("/get_history")
async def get_history_endpoint(user_id: str):
    # 调用你 Day 5 写的 get_ai_context 函数
    history = await get_ai_context(user_id, limit=20) 
    return {"history": history}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
