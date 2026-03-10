# 处理 Postgres (SQLAlchemy)

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# 1. 数据库 URL (使用 asyncpg 驱动)
# 格式: postgresql+asyncpg://用户名:密码@地址:端口/数据库名
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/ai_db"

# 2. 创建异步引擎
# echo=True 可以让你在控制台看到生成的 SQL 语句，方便 Day 13 调试
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True, 
    pool_size=10,       # 连接池大小
    max_overflow=20     # 允许临时溢出的连接数
)

# 3. 创建 Session 工厂
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False, # 异步环境下必须设置为 False
)

# 4. 定义模型基类
class Base(DeclarativeBase):
    pass

# 5. 依赖项：给 FastAPI 注入使用
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()