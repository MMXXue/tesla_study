
# 这段代码是你的指挥中心。
# 它负责把数据库（Postgres）、缓存（Redis）和 Web 框架（FastAPI）组合在一起，实现一个工业级的数据查询接口。

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import json

# 导入你写的零件 (请确保文件名匹配)
from day13_database import get_db, engine, Base
from day12_models import PerceptionTask
from day13_redis_config import redis_tool
from day13_service import get_task_with_cache

app = FastAPI()

# 自动创建表（如果数据库里还没有 perception_tasks 表，这一行会自动建表）
Base.metadata.create_all(bind=engine)

# --- API 接口 ---
@app.get("/perception/task/{task_id}")
async def read_perception_task(task_id: int, db: Session = Depends(get_db)):
    # 使用刚才定义的带缓存函数
    task = await get_task_with_cache(task_id, db)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    return {
        "status": "success", 
        "data": task,
        "note": "First time slow (DB), second time fast (Redis)"
    }