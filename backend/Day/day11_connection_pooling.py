from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import asyncio


app = FastAPI()

# 1. 配置异步引擎 (这里以 PostgreSQL 为例)
# pool_size=2 意味着同时只能有 2 个数据库连接
# 核心修正：用户名设为 postgres，密码设为 password，库名设为 testdb
DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/testdb"

engine = create_async_engine(
    DATABASE_URL,
    pool_size=2,         # 极小的连接池，方便测试调优
    max_overflow=10,      # 不允许溢出
    pool_timeout=30       # 获取连接等待 30 秒超时
)

# 2. 创建异步 Session 工厂
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@app.get("/test-io")
async def test_io():
    async with AsyncSessionLocal() as session:
        # 模拟一个耗时 1 秒的数据库查询 (I/O 耗时)
        # 在 Tesla 的场景中，这可能是查询车辆的历史轨迹数据
        await session.execute(text("SELECT pg_sleep(1)")) 
        return {"status": "success", "message": "Database task finished"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)