import redis
import time
import uuid

class RedlockTesla:
    def __init__(self, node_list):
        # 连接所有 Redis 节点
        self.nodes = [redis.Redis(**n) for n in node_list]
        self.quorum = (len(self.nodes) // 2) + 1

    def lock(self, resource_name, ttl=10000):
        unique_id = str(uuid.uuid4())
        start_time = time.time() * 1000 # 毫秒
        
        success_count = 0
        for node in self.nodes:
            # 尝试在每个节点加锁，超时时间设为 50ms
            if node.set(resource_name, unique_id, nx=True, px=ttl):
                success_count += 1
        
        elapsed_time = (time.time() * 1000) - start_time
        # 实际可用时间要减去消耗的时间和时钟漂移补偿
        valid_time = ttl - elapsed_time - (ttl * 0.01 + 2)

        if success_count >= self.quorum and valid_time > 0:
            return unique_id, resource_name
        else:
            # 如果失败，必须在所有节点释放（即使没加锁成功的也要尝试释放）
            self.unlock(resource_name, unique_id)
            return None

    def unlock(self, resource_name, unique_id):
        lua_script = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        else
            return 0
        end
        """
        for node in self.nodes:
            node.eval(lua_script, 1, resource_name, unique_id)

# --- 模拟练习 ---
nodes = [
    {'host': 'localhost', 'port': 6379, 'db': 1},
    {'host': 'localhost', 'port': 6379, 'db': 2},
    {'host': 'localhost', 'port': 6379, 'db': 3},
]

dlm = RedlockTesla(nodes)
lock_res = dlm.lock("fms_model_v12_update", ttl=5000)

if lock_res:
    print(">>> 恭喜！你已获得分布式多数派认证，可以开始更新 Tesla 模型。")
    # ... 执行任务 ...
    dlm.unlock(lock_res[1], lock_res[0])
else:
    print(">>> 获取锁失败，系统保护中。")