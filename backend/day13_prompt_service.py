import json
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from backend.day13_models import SystemPromptModel

class PromptService:
    def __init__(self, db: AsyncSession, redis: Redis):
        self.db = db
        self.redis = redis

    async def get_system_prompt(self, role: str) -> str:
        # 统一 Key 的名字，方便你在命令行找
        cache_key = f"system_prompt:{role}"

        # --- [Step 1] 查 Redis ---
        cached_data = await self.redis.get(cache_key)
        if cached_data:
            print(f"🔥 Cache Hit: {role}")
            return cached_data

        # --- [Step 2] 查 Postgres ---
        print(f"❄️ Cache Miss: {role}, checking DB...")
        query = select(SystemPromptModel).where(SystemPromptModel.role == role)
        result = await self.db.execute(query)
        prompt_obj = result.scalar_one_or_none()

        # --- [Step 3] 确定内容并回填 ---
        # 这里的逻辑改动：先确定内容，再统一存入 Redis
        final_content = prompt_obj.content if prompt_obj else "You are a helpful assistant."

        # 无论数据库有没有，都存入 Redis，有效期 1 小时
        await self.redis.setex(cache_key, 3600, final_content)
        print(f"✅ Stored in Redis: {cache_key}")
        
        return final_content