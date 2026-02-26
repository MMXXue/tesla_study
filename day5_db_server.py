import asyncio
from fastapi import FastAPI
from databases import Database
from contextlib import asynccontextmanager
from fastapi.responses import StreamingResponse

DATABASE_URL = "sqlite:///./my_ai_db.db" 
database = Database(DATABASE_URL)
sem = asyncio.Semaphore(1)  # 限制普通用户的全局并发数为 1

# 1. 定义生命周期管理器
@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect() 
    # 确保表结构包含 role 分类
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

    yield

    await database.disconnect()
    print("🛑 [系统关闭] 数据库已安全断开。")


# 2. 在初始化 app 时传入 lifespan
app = FastAPI(lifespan=lifespan)

# --- 核心业务逻辑 ---
async def run_inference(user_id: str):
    # 获取最近 6 条（包含刚刚存入的那条 user prompt）
    history = await get_ai_context(user_id, limit=6)
    
    yield f"--- [AI 引擎] 调取了 {len(history)} 条历史记忆 ---\n"
    
    # 如果有历史记录，显示除了“最后一条”以外的所有内容
    # 因为最后一条就是用户刚刚发来的，还没形成“历史”
    if len(history) > 1:
        for h in history[:-1]: 
            yield f"📜 {h}\n"
        yield "--------------------\n"

    # 模拟回复
    if len(history) > 1:
        last_user_said = history[-1] # 获取最近一条（还没存成历史的那条）
        response_text = f"你刚才是不是说了：'{last_user_said}'？我已经把它存入我的特斯拉大脑数据库了。"
    else:
        response_text = "你好！我是你的特斯拉 AI 助手，这是我们的第一次对话，我会记住你说的每一句话。"

    for char in response_text:
        await asyncio.sleep(0.02)
        yield char

async def _process_request(user_id: str, prompt: str):
    # --- 步骤 A：存入用户提问 ---
    await save_chat(user_id, "user", prompt)

    full_ai_reply = "" 
    # --- 步骤 B：执行推理 (注意：此时 get_ai_context 会读到刚才存的那个 prompt) ---
    async for chunk in run_inference(user_id):
        # 过滤掉系统提示字符，只收集真正的 AI 回复
        if "---" not in chunk and "📜" not in chunk and "✅" not in chunk:
            full_ai_reply += chunk
        yield chunk

    # --- 步骤 C：等 AI 全部说完，再存入 AI 的回答 ---
    if full_ai_reply.strip():
        await save_chat(user_id, "assistant", full_ai_reply.strip())
        yield f"\n\n✅ [记忆存入成功]"


# 1. 保存对话的函数
async def save_chat(user_id: str, role: str, content: str):
    # 我们把角色(user/assistant)和内容存在一起
    # 存入格式： "user: 你好" 或 "assistant: 我是特斯拉AI"
    formatted_msg = f"{role}: {content}"
    query = "INSERT INTO chat_history(user_id, role, message) VALUES (:u, :r, :m)"
    await database.execute(query=query, values={"u": user_id, "r": role, "m": formatted_msg})

# 2. 获取历史记忆的函数
async def get_ai_context(user_id: str, limit: int = 6):
    # 从数据库捞取最近的几条消息
    query = "SELECT message FROM chat_history WHERE user_id = :u ORDER BY id DESC LIMIT :l"
    rows = await database.fetch_all(query=query, values={"u": user_id, "l": limit})
    
    # 数据库取出来是倒序的，我们要反转回正序
    history = [row["message"] for row in reversed(rows)]
    return history

# @app.post("/chat")
# async def chat_endpoint(user_id: str, role: str, prompt: str):
#     # A. 先存入用户的提问
#     await save_chat(user_id, role, prompt)
    
#     # B. 从数据库获取之前的记忆
#     context = await get_ai_context(user_id)
    
#     # C. 将记忆拼接到大模型的输入中 (这里是关键！)
#     # 模拟把历史记录传给模型
#     full_prompt = "\n".join(context) + f"\nassistant: "
    
#     # ... 执行 AI 生成逻辑 (比如调用 OpenAI 或本地模型) ...
    
#     # D. 假设 AI 回复了 ai_response
#     ai_response = "这是我根据历史记忆给你的回答"
#     await save_chat(user_id, "assistant", ai_response)
    
#     return {"response": ai_response}


@app.get("/chat_stream")
async def chat_stream_endpoint(user_id: str, prompt: str):
    async def event_generator():
        # 这里套用你之前的信号量(sem)逻辑
        if user_id == "admin":
            async for chunk in _process_request(user_id, prompt):
                yield chunk
        else:
            async with sem:
                async for chunk in _process_request(user_id, prompt):
                    yield chunk
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("day5_db_server:app", host="127.0.0.1", port=8000, reload=True)