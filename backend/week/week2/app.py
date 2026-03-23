
# 把log消息放入redis(临时仓库)中,减少等待时间⏳
# API是接收员,相当于快递员🙎, redis就像是空投箱📦一样

import redis.asyncio as redis
from fastapi import FastAPI, Request
import uvicorn
from contextlib import asynccontextmanager

# 1. 使用 lifespan 管理，确保每个进程独立拥有自己的连接池
@asynccontextmanager
async def lifespan(app: FastAPI):
    pool = redis.ConnectionPool.from_url(
        "redis://127.0.0.1:6379",
        max_connections=1000,
        decode_responses=False
    )
    app.state.redis = redis.Redis(connection_pool=pool)
    yield
    await pool.disconnect()

app = FastAPI(lifespan=lifespan)

@app.post("/log")
async def collect_diagnostic_log(request: Request):
    raw_payload = await request.body()
    await app.state.redis.rpush("log_queue", raw_payload)
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, loop="uvloop", http="httptools", log_level="warning")