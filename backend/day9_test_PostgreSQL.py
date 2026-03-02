import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

# 这里的数据库地址必须和刚才 Docker 设置的密码 (tesla_power) 一致
DATABASE_URL = "postgresql+asyncpg://postgres:tesla_power@localhost:5432/postgres"

async def test_connection():
    engine = create_async_engine(DATABASE_URL)
    try:
        async with engine.connect() as conn:
            print("✅ 成功连接到 Docker 里的 PostgreSQL！")
            print("🚀 你现在已经具备了开发高并发异步后端的基础。")
    except Exception as e:
        print(f"❌ 连接失败，原因: {e}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_connection())