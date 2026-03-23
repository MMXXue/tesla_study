# 处理 Redis

import redis.asyncio as redis

# 1. Redis 配置
REDIS_URL = "redis://localhost:6379"

# 2. 创建全局连接池
redis_pool = redis.ConnectionPool.from_url(
    REDIS_URL, 
    decode_responses=True, # 自动把字节转为 Python 字符串
    max_connections=20     # 限制最大并发连接
)

# 3. 创建异步客户端实例
redis_client = redis.Redis(connection_pool=redis_pool)

# 4. 依赖项：给 FastAPI 注入使用
async def get_redis():
    return redis_client