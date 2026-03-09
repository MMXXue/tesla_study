from sqlalchemy.orm import Session
from .day12_models import PerceptionTask  # 你的模型文件
from .day13_redis_config import redis_tool # 你的连接文件

async def get_task_with_cache(task_id: int, db: Session):
    # 1. 定义 Redis 里的 Key（加上前缀方便管理）
    cache_key = f"task:detail:{task_id}"
    
    # 2. 尝试从 Redis 拿数据 (调用你写的 get_json)
    cached_task = await redis_tool.get_json(cache_key)
    
    if cached_task:
        print(f"🚀 [Redis Hit] 任务 {task_id} 数据来自缓存")
        return cached_task

    # 3. 缓存没有，查 PostgreSQL (调用你的 PerceptionTask 模型)
    print(f"🐢 [Cache Miss] 正在从硬盘读取任务 {task_id}...")
    task = db.query(PerceptionTask).filter(PerceptionTask.id == task_id).first()
    
    if task:
        # 将模型对象转为字典，准备存入 Redis
        task_data = {
            "id": task.id,
            "video_id": task.video_id,
            "status": task.status,
            "model_version": task.model_version,
            "confidence": task.confidence_score,
        }
        # 4. 存入 Redis (调用你写的 set_json)，设置 10 分钟过期
        await redis_tool.set_json(cache_key, task_data, ex=600)
        return task_data
    
    return None