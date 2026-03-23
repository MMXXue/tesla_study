from fastapi import FastAPI
from contextlib import asynccontextmanager

# 1. 定义生命周期逻辑
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- 【启动阶段】 ---
    print("正在连接数据库...")
    db_connection = {"status": "connected"} 
    
    # 将资源传递给应用（可选）
    yield {"db": db_connection}
    
    # --- 【关闭阶段】 ---
    print("正在断开数据库...")
    db_connection["status"] = "disconnected"

app = FastAPI(lifespan = lifespan)

@app.get("/")
async def read_root():
    return {"message": "Hello World"}