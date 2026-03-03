import time
import redis
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# --- 配置连接 ---
# 注意：如果你在 Docker 里运行，localhost 对应映射出的端口
DB_URL = "postgresql://postgres:tesla_power@localhost:5432/postgres"

# Redis 客户端：用于写入任务心跳，给监控端判断 Worker 是否存活
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# SQLAlchemy 引擎：管理到 PostgreSQL 的底层连接池，常驻 10 个，最大 20 个溢出连接，连接超时 30 秒
# 引擎是整个系统的“动力源”和“调度室”
engine = create_engine(DB_URL, pool_size=10, max_overflow=20, pool_timeout=30)

# Session 工厂：每次 SessionLocal() 都会创建一个新的数据库会话
# 类似于开了一个快递公司的柜台，每个柜台独立处理一个客户的事务
SessionLocal = sessionmaker(bind=engine)

def run_task_with_heartbeat(worker_id):
    # 为本次任务执行创建独立会话（用完后在 finally 里关闭）
    # 类似于雇佣了一个员工来处理这个任务
    db = SessionLocal()
    
    # 提前声明，确保在异常分支或 finally 块中能安全引用
    task_id = None 
    
    try:
        # 第一步：DB 锁抢占 (PostgreSQL)
        # 事务块内完成“选任务 + 改状态”，保证原子性
        # with db.begin() 是一个“原子隔离舱”，要么全成功提交，要么全失败回滚
        with db.begin():
            # 这里的 SKIP LOCKED 是为了让多个 Worker（比如 100 个 Tesla Bot）不互相打架
            # 它会跳过已经被别人锁住的任务，直接找下一个 PENDING 的
            query = text("""
                SELECT id FROM agent_tasks 
                WHERE status = 'PENDING' 
                LIMIT 1 FOR UPDATE SKIP LOCKED
            """)
            
            # fetchone() 只取一条可执行任务
            result = db.execute(query).fetchone()
            
            if not result:
                print(f"🤖 [{worker_id}] 📭 暂时没有 PENDING 任务，休息中...")
                return
            
            task_id = result[0]
            
            # 抢到了！在档案库里写下自己的名字（worker_id）
            # 注意：这个操作在 with 块结束前是暂时的，退出块时会自动 COMMIT（正式刻在硬盘上）
            db.execute(
                text("UPDATE agent_tasks SET status='EXECUTING', worker_id=:wid WHERE id=:tid"),
                {"wid": worker_id, "tid": task_id}
            )
        
        print(f"✅ [{worker_id}] 抢到任务 ID: {task_id}！准备同步 Redis 心跳...")

        # 第二步：开启心跳并模拟执行 (Redis)
        # 我们模拟任务需要执行 15 秒，但心跳每 5 秒刷新一次
        for i in range(3):
            # 设置/刷新心跳，过期时间设为 10 秒（容错时间）
            # 这里的 ex=10 是关键：如果 Worker 猝死，10秒后 Redis 里的这个键会自动消失
            heartbeat_key = f"task:{task_id}:heartbeat"
            r.set(heartbeat_key, "ALIVE", ex=10)
            
            # 模拟干活（比如在处理 FSD 视觉训练图片）
            progress = i * 33
            print(f"⏳ 任务 {task_id} 处理中... (进度 {progress}%)... 心跳已续期 (TTL: {r.ttl(heartbeat_key)}s)")
            time.sleep(5) 

        # 第三步：任务完成，清理现场
        # 将任务状态标记为 COMPLETED（档案库最终确认）
        with db.begin():
            db.execute(
                text("UPDATE agent_tasks SET status='COMPLETED' WHERE id=:tid"),
                {"tid": task_id}
            )
        
        # 任务结束后删除心跳键，避免监控端误判为任务仍在执行
        r.delete(f"task:{task_id}:heartbeat")
        print(f"🎉 任务 {task_id} 圆满完成！")

    except Exception as e:
        # 如果在 with db.begin() 内部出错，SQLAlchemy 会自动触发回滚（Rollback）
        print(f"❌ [{worker_id}] 运行出错: {e}")
    finally:
        # 无论成功失败都关闭会话，释放连接回连接池
        # 相当于柜台窗口关闭，员工下班，但连接（水管）留在池子里给下一个人用
        db.close()

if __name__ == "__main__":
    # 模拟启动一个带“工号”的 Worker
    run_task_with_heartbeat("Tesla_Bot_X1")