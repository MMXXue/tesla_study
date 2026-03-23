import redis
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# --- 1. 配置连接（必须与 Worker 保持一致） ---
DB_URL = "postgresql://postgres:tesla_power@localhost:5432/postgres"
# 注意：这里 host 请确保是你 Redis 容器映射到宿主机的地址（通常是 localhost）
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

engine = create_engine(DB_URL, pool_size=10, max_overflow=20, pool_timeout=30)
SessionLocal = sessionmaker(bind=engine)

def monitor_and_heal():
    print("🔍 [Monitor] 巡检机器人已启动...")
    db = SessionLocal()
    
    try:
        # 1. 纯查询：找出所有正在执行的任务
        # 这里我们不开启事务块，只是简单读取
        query = text("SELECT id, worker_id FROM agent_tasks WHERE status = 'EXECUTING'")
        tasks = db.execute(query).fetchall()
        
        if not tasks:
            print("✨ 系统运行良好，无僵尸任务。")
            return

        for row in tasks:
            task_id, worker_id = row[0], row[1]
            heartbeat_key = f"task:{task_id}:heartbeat"
            
            if not r.exists(heartbeat_key):
                print(f"🚨 [警报] 发现僵尸任务！ID: {task_id}")
                
                # 2. 关键修复：在这里使用一个新的事务块来更新
                # 注意：如果 db.execute 报错，直接在这里处理
                try:
                    # 使用 Session 的独立 execute 来更新，或者手动 commit
                    db.execute(
                        text("UPDATE agent_tasks SET status='PENDING', worker_id=NULL WHERE id=:tid"),
                        {"tid": task_id}
                    )
                    db.commit() # 手动提交这次更新
                    print(f"✅ [救援成功] 任务 {task_id} 已重置为 PENDING。")
                except Exception as update_error:
                    db.rollback() # 出错就回滚
                    print(f"❌ 更新任务 {task_id} 失败: {update_error}")
            else:
                print(f"🟢 任务 {task_id} 正常 (TTL: {r.ttl(heartbeat_key)}s)")
                
    except Exception as e:
        print(f"❌ [Monitor] 巡检过程发生严重错误: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    monitor_and_heal()