import json
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from backend.day13_databases import engine, Base, get_db
from backend.day13_redis_config import get_redis
from backend.day13_prompt_service import PromptService

# --- 生命周期管理 (替换掉弃用的 on_event) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动：创建表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("🚀 系统启动：数据库表已就绪")
    yield
    # 关停：清理资源
    await engine.dispose()
    print("🛑 系统关闭：连接已释放")

app = FastAPI(lifespan=lifespan)

# --- 业务逻辑：获取配置 + 处理 Session ---
@app.get("/ai/chat/{role}")
async def chat_with_context(
    role: str, 
    user_id: int,
    user_message: str,
    db = Depends(get_db), 
    redis = Depends(get_redis)
):
    service = PromptService(db, redis)
    
    # 1. 获取 System Prompt (Cache Aside 策略)
    system_prompt = await service.get_system_prompt(role)
    
    # 2. 处理 Session (Redis 滑动窗口策略) 
    # 这是一种 滑动窗口对话记忆
    session_key = f"session:{user_id}:{role}"
    
    # 将新消息存入 Redis 列表右侧
    new_msg_json = json.dumps({"role": "user", "content": user_message})
    await redis.rpush(session_key, new_msg_json)
    
    # 关键：只保留最近 10 条对话，防止 Token 爆炸 (Day 13 核心)
    # 裁剪窗口 (ltrim)
    await redis.ltrim(session_key, -10, -1)
    
    # 获取完整的历史上下文给 LLM
    # 获取上下文 (lrange)
    history_raw = await redis.lrange(session_key, 0, -1)
    history = [json.loads(m) for m in history_raw]
    
    # 设置过期时间（比如 30 分钟不说话就自动清空上下文）
     # 自动销毁 (expire)
    await redis.expire(session_key, 1800)

    return {
        "system_prompt": system_prompt,
        "history_count": len(history),
        "history": history,
        "status": "Ready to send to LLM"
    }
