
# 令牌桶,限流

import time
import redis
import threading

# --- 1. Lua 脚本：Redis 内部的原子“公证人” ---
LUA_RATE_LIMITER = """
local key = KEYS[1]
local capacity = tonumber(ARGV[1])
local fill_rate = tonumber(ARGV[2])
local now = tonumber(ARGV[3])
local requested = tonumber(ARGV[4])

-- 获取上次的数据
local data = redis.call("HMGET", key, "tokens", "last_time")
local last_tokens = tonumber(data[1]) or capacity
local last_time = tonumber(data[2]) or now

-- 计算补票数量
local delta = math.max(0, now - last_time) * fill_rate
local new_tokens = math.min(capacity, last_tokens + delta)

if new_tokens >= requested then
    -- 够扣：更新并返回成功(1)
    redis.call("HMSET", key, "tokens", new_tokens - requested, "last_time", now)
    -- 设置过期时间(1分钟没人用就删除，节省空间)
    redis.call("EXPIRE", key, 60)
    return 1
else
    -- 不够扣：返回失败(0)
    return 0
end
"""

class TeslaRateLimiter:
    def __init__(self, host='localhost', port=6379):
        self.r = redis.Redis(host=host, port=port, decode_responses=True)
        # 预加载脚本
        self.lua_script = self.r.register_script(LUA_RATE_LIMITER)

    def acquire(self, device_id):
        # 参数：容量10，每秒恢复2个令牌
        now = time.time()
        # 执行脚本：keys=[key], args=[capacity, fill_rate, now, requested]
        return self.lua_script(keys=[f"limiter:{device_id}"], args=[10, 2, now, 1]) == 1

# --- 3. 验证实验：多线程冲击测试 ---
def task(limiter, device_id, thread_id):
    if limiter.acquire(device_id):
        print(f"线程 {thread_id:02d}: ✅ 成功拿票！")
    else:
        print(f"线程 {thread_id:02d}: ❌ 被限流了...")

if __name__ == "__main__":
    limiter = TeslaRateLimiter()
    device_id = "model_y_001"
    
    # 瞬间启动 20 个线程去抢 10 张票
    print(f"🚀 正在模拟 20 个并发请求冲击限流器 (桶容量 10)...")
    threads = []
    for i in range(20):
        # 分身术,暴冲
        # 告诉 Python：创建一个分身，它的任务（target）是去执行 task 函数
        t = threading.Thread(target=task, args=(limiter, device_id, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()