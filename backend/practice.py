import time
import redis
import threading

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

class Tesla_limitation():
    def __init__(self, host='localhost', port=6379):
        self.r = redis.Redis(host=host, port=port, decode_responses=True)
        # 预加载脚本
        self.lua_script = self.r.register_script(LUA_RATE_LIMITER)

    def acquire(self, device_id):
        # 参数：容量10，每秒恢复2个令牌
        now = time.time()
        # 执行脚本：keys=[key], args=[capacity, fill_rate, now, requested]
        return self.lua_script(keys=[f"limiter:{device_id}"], args=[10, 2, now, 1]) == 1

