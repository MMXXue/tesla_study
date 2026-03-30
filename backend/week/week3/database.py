from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime # 确保是这样导入的

DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/postgres"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

class SensorLog(Base):
    __tablename__ = "sensor_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String)
    payload = Column(JSON)
    # 修正这里
    created_at = Column(DateTime, default=datetime.utcnow) 

# 别忘了加上这个函数，供 main.py 调用
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("数据库初始化成功！")