import asyncio
from fastapi import FastAPI
from databases import Database
from contextlib import asynccontextmanager
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

# --- 基础配置 ---
DATABASE_URL = "sqlite:///./db/day6_tesla_ai_db.db"  # 本地 SQLite 数据库路径（迁移到 db/ 目录）
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

# --- 核心业务逻辑 ---

async def run_inference(user_id: str):
    """
    模拟 AI 推理过程：调取记忆并生成流式响应
    """
    # 获取最近 6 条对话记录作为上下文
    history = await get_ai_context(user_id, limit=6)
    
    yield f"--- [AI 引擎] 调取了 {len(history)} 条历史记忆 ---\n"
    
    # 格式化并显示历史记录（排除最后一条刚存入的消息）
    if len(history) > 1:
        for h in history[:-1]: 
            yield f"📜 {h}\n"
        yield "--------------------\n"

    # 生成模拟的回复内容
    if len(history) >= 1:
        # 提取用户刚才发送的内容（简单去除前缀）
        last_user_said = history[-1].replace("user: ", "") 
        response_text = f"你刚才是不是说了：'{last_user_said}'？我已经把它存入我的特斯拉大脑数据库了。"
    else:
        response_text = "你好！我是你的特斯拉 AI 助手，这是我们的第一次对话。"

    # 打字机效果：逐字发送字符串，模拟流式输出
    for char in response_text:
        await asyncio.sleep(0.02) # 模拟推理耗时
        yield char

async def _process_request(user_id: str, prompt: str):
    """
    处理请求的中间层：负责保存用户输入、获取 AI 输出并保存 AI回复
    """
    # 1. 记录用户输入到数据库
    await save_chat(user_id, "user", prompt)

    full_ai_reply = "" 
    # 2. 迭代 AI 生成的每一个字符/片段
    async for chunk in run_inference(user_id):
        # 优化：只把真正的回答内容存入数据库，过滤掉 UI 装饰符（如 --- 或 📜）
        if "---" not in chunk and "📜" not in chunk:
            full_ai_reply += chunk
        yield chunk

    # 3. 推理结束，将 AI 的完整回复存入数据库
    if full_ai_reply.strip():
        await save_chat(user_id, "assistant", full_ai_reply.strip())
        yield f"\n\n✅ [记忆存入成功]"

# --- 数据库操作工具函数 ---

async def save_chat(user_id: str, role: str, content: str):
    """将一条消息存入数据库"""
    formatted_msg = f"{role}: {content}"
    try:
        query = "INSERT INTO chat_history(user_id, role, message) VALUES (:u, :r, :m)"
        await database.execute(query=query, values={"u": user_id, "r": role, "m": formatted_msg})
    except Exception as e:
        print(f"⚠️ 数据库写入失败: {e}")

async def get_ai_context(user_id: str, limit: int = 6):
    """从数据库读取最近的 N 条对话历史"""
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
