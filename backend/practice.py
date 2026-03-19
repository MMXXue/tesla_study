import uvicorn
from fastapi import FastAPI
import asyncio
from fastapi import StreamingResponse

app = FastAPI()
user_session = {}

app.get('/')
async def getStatus():
    return {
        "status": "ready",
        "engine": "Tesla-AI-Core",
        "version": "1.0.0"
    }


async def message_generator():
    messages = ["Tesla", "is", "the", "best", "one."]
    for mes in messages:
        yield f"{mes} "
        await asyncio.sleep(3)

app.get('/stream')
async def getStreaming():
    # 必须返回 StreamingResponse，否则 FastAPI 不知道这是在“流式传输”
    return StreamingResponse(message_generator(), media_type="text/plain")

if __name__ == "__main__":
    uvicorn.run(app, host = "127.0.0.1", port = 8000)