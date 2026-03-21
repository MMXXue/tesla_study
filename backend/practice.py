import uvicorn
from fastapi import FastAPI
import asyncio
from fastapi.responses import StreamingResponse

app = FastAPI()
# Key 是用户 ID，Value 是该用户的对话列表
user_sessions = {}

app.get('/')
async def getStatus():
    return {
        "status": "ready",
        "engine": "Tesla-AI-Core",
        "version": "1.0.0"
    }


async def message_generator(user_id: str, current_prompt: str):
    if user_id not in user_sessions:
        user_sessions[user_id] = []

    history = user_sessions[user_id]
    if history:
        yield f"📜 [记忆回顾] 上次我们聊了: {', '.join(history)}\n"
    else:
        yield f"🆕 [系统提示] 检测到新用户，正在初始化记忆模块...\n"
    
    yield f"正在处理新指令:'{current_prompt}'....\n"
    await asyncio.sleep(2)

    user_sessions[user_id].append(current_prompt)
    yield "✅ 处理完毕！\n"


@app.get('/stream')
async def getStreaming(user_id: str = "guest", prompt: str = "Hello"):
    # 必须返回 StreamingResponse，否则 FastAPI 不知道这是在“流式传输”
    return StreamingResponse(
                                message_generator(user_id, prompt), 
                                media_type="text/plain"
                            )

if __name__ == "__main__":
    uvicorn.run(app, host = "127.0.0.1", port = 8000)