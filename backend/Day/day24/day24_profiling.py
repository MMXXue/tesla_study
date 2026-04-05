import cProfile
import pstats
import time
from fastapi import FastAPI

app = FastAPI()

def slow_function():
    # 模拟一个耗时操作
    time.sleep(1) 
    return "Done"


def heavy_computation():
    result = 0
    for i in range(10000000): # 循环一千万次
        result += i
    return result

# # 开始性能分析
# with cProfile.Profile() as pr:
#     slow_function()
#     heavy_computation()

# # 打印结果
# stats = pstats.Stats(pr)
# stats.sort_stats(pstats.SortKey.TIME).print_stats(10) # 打印耗时前10的函数

@app.get("/heavy")
async def heavy():
    # 这是一个 CPU 密集型任务
    result = 0
    for i in range(10000000):
        result += i
    return {"result": result}

@app.get("/ping")
async def ping():
    return {"status": "pong"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


    print("程序开始运行，正在等待录制... (持续 20 秒)")
    start_time = time.time()
    # 让它跑够 20 秒，给你留出启动录制的时间
    while time.time() - start_time < 20:
        slow_function()
        heavy_computation()
    print("运行结束")
