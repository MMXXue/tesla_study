
# 独立运行,且用于批量搬运存在redis中的数据🚛,将他们存进总数据库中(持久化保存)

import asyncio
import redis.asyncio as redis
import asyncpg
import json

async def start_worker():
    redis_client = redis.Redis(host='127.0.0.1', port=6379, decode_responses=False)
    
    # 创建 PostgreSQL 连接池
    pg_pool = await asyncpg.create_pool('postgresql://postgres:password@127.0.0.1:5432/postgres')
    
    print("🚚 Worker 大卡车已启动，并连接到数据库池...")

    async with pg_pool.acquire() as conn:
        while True:
            logs_to_write = []

            raw_logs = await redis_client.lpop("log_queue", count=200)
            if raw_logs:
                for raw_log in raw_logs:
                    try:
                        log_dict = json.loads(raw_log)
                        level = log_dict.get("level", "INFO")
                        message = log_dict.get("message", "Empty Message")
                        logs_to_write.append((level, message))
                    except Exception as e:
                        print(f"❌ 解析错误: {e}")

            if logs_to_write:
                # 批量写入
                await conn.executemany(
                    "INSERT INTO diagnostic_logs(level, message) VALUES($1, $2)",
                    logs_to_write
                )
                print(f"✅ 成功搬运 {len(logs_to_write)} 条日志")
                if len(logs_to_write) == 200:
                    continue
                continue

            await asyncio.sleep(0.2)

if __name__ == "__main__":
    try:
        asyncio.run(start_worker())
    except KeyboardInterrupt:
        print("Worker 已安全停止")