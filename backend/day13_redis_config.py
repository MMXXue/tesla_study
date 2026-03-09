import json
from redis import asyncio as aioredis # 升级为异步库

class RedisCache:
    def __init__(self):
        # 1. 这里就是连接！相当于你之前的 r = redis.Redis(...)
        # 但我们用了从 URL 连接的方式，更简洁
        self.client = aioredis.from_url(
            "redis://localhost:6379", 
            decode_responses=True,
            encoding="utf-8"
        )

    # 2. 封装一个“存”的方法
    async def set_json(self, key: str, value: dict, ex: int = 3600):
        # 工业级习惯：把字典转成 JSON 字符串再存
        await self.client.set(key, json.dumps(value), ex=ex)

    # 3. 封装一个“取”的方法
    async def get_json(self, key: str):
        data = await self.client.get(key)
        return json.loads(data) if data else None

# 创建一个全局变量，让整个 FastAPI 项目都能用这一个连接
redis_tool = RedisCache()