# 导入 redis 客户端库，用来连接 Redis 并执行 set、eval 等命令。
import redis
# 导入 time 模块，用来统计加锁过程消耗了多少毫秒。
import time
# 导入 uuid 模块，用来为每次加锁生成全局唯一的锁标识。
import uuid

# 定义一个简化版的 Redlock 类，用来演示分布式锁的核心思路。
class RedlockTesla:
    # 初始化方法，接收一个 Redis 节点配置列表。
    def __init__(self, node_list):
        # 把每个节点配置转换成 Redis 连接对象，后面会逐个向这些节点申请锁。
        self.nodes = [redis.Redis(**n) for n in node_list]
        # 计算多数派数量，3 个节点时多数派就是 2。
        self.quorum = (len(self.nodes) // 2) + 1

    # 定义加锁方法，resource_name 是锁资源名，ttl 是锁的过期时间，单位毫秒。
    def lock(self, resource_name, ttl=10000):
        # 为这次加锁生成唯一 ID，解锁时必须拿着同一个 ID 才能删锁。
        unique_id = str(uuid.uuid4())
        # 记录开始时间，并换算成毫秒，后面要扣除加锁消耗时间。
        start_time = time.time() * 1000

        # 统计有多少个 Redis 节点成功加锁。
        success_count = 0
        # 依次向所有 Redis 节点发起加锁请求。
        for node in self.nodes:
            # 使用 set nx px 原子加锁：nx 表示键不存在才设置，px 表示毫秒级过期时间。
            if node.set(resource_name, unique_id, nx=True, px=ttl):
                # 如果当前节点加锁成功，就把成功计数加 1。
                success_count += 1

        # 计算整个加锁过程总共花了多少毫秒。
        elapsed_time = (time.time() * 1000) - start_time
        # 计算锁的剩余有效时间，并预留 1% 加 2ms 作为时钟漂移补偿。
        valid_time = ttl - elapsed_time - (ttl * 0.01 + 2)

        # 只有在成功节点数达到多数派且剩余有效时间大于 0 时，才认为真正加锁成功。
        if success_count >= self.quorum and valid_time > 0:
            # 返回唯一锁 ID 和资源名，方便调用方后续解锁。
            return unique_id, resource_name
        else:
            # 如果没有形成多数派或者锁几乎已经过期，就主动清理所有节点上可能写入的锁。
            self.unlock(resource_name, unique_id)
            # 返回 None 表示这次加锁失败。
            return None

    # 定义解锁方法，必须传入资源名和加锁时生成的唯一 ID。
    def unlock(self, resource_name, unique_id):
        # Lua 脚本保证“先比较值、再删除键”两个动作在 Redis 里原子执行。
        lua_script = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        else
            return 0
        end
        """
        # 遍历所有 Redis 节点，对每个节点都尝试执行安全解锁。
        for node in self.nodes:
            # KEYS[1] 对应 resource_name，ARGV[1] 对应 unique_id，只有值匹配时才删除。
            node.eval(lua_script, 1, resource_name, unique_id)

# 下面开始构造一个简单的本地演示环境。
# 定义三个 Redis 节点配置，这里为了练习，使用同一台机器上的不同逻辑库来模拟多个节点。
nodes = [
    # 第一个“节点”使用本地 6379 端口上的 db 1。
    {'host': 'localhost', 'port': 6379, 'db': 1},
    # 第二个“节点”使用本地 6379 端口上的 db 2。
    {'host': 'localhost', 'port': 6379, 'db': 2},
    # 第三个“节点”使用本地 6379 端口上的 db 3。
    {'host': 'localhost', 'port': 6379, 'db': 3},
]

# 用上面的节点配置创建一个分布式锁管理器实例。
dlm = RedlockTesla(nodes)
# 尝试给资源 fms_model_v12_update 加锁，锁的有效期设置为 5000 毫秒。
lock_res = dlm.lock("fms_model_v12_update", ttl=5000)

# 如果 lock_res 有值，说明已经拿到多数派锁。
if lock_res:
    # 打印成功信息，表示当前进程可以安全地执行关键任务。
    print(">>> 恭喜！你已获得分布式多数派认证，可以开始更新 Tesla 模型。")
    # 这里代表真正的业务逻辑，例如模型更新、配置发布或任务调度。
    # ... 执行任务 ...
    # 任务完成后，使用返回的资源名和唯一 ID 释放锁。
    dlm.unlock(lock_res[1], lock_res[0])
else:
    # 如果没有拿到锁，就打印失败信息，表示当前不允许执行关键任务。
    print(">>> 获取锁失败，系统保护中。")