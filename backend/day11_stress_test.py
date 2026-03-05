# 压测的核心逻辑其实就是：用代码模拟一堆人同时疯狂点击你的接口
import asyncio
import httpx
import time

# 1. 设置你要测试的接口地址（比如你本地运行的 SQLAlchemy 接口）
URL = "http://127.0.0.1:8000/test-io" 
# 2. 设置并发量（模拟多少个“人”同时访问）
CONCURRENT_USERS = 50

async def call_api(client, user_id):
    """模拟单个用户发起请求"""
    start_time = time.perf_counter()
    try:
        response = await client.get(URL)
        end_time = time.perf_counter()
        print(f"用户 {user_id}: 状态码 {response.status_code}, 耗时 {end_time - start_time:.4f}s")
    except Exception as e:
        print(f"用户 {user_id} 请求失败: {e}")

async def main():
    print(f"🚀 开始压测，模拟 {CONCURRENT_USERS} 个并发请求...")
    
    # 使用异步客户端
    async with httpx.AsyncClient() as client:
        # 创建 50 个任务
        tasks = [call_api(client, i) for i in range(CONCURRENT_USERS)]
        # 同时启动所有任务
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    start_total = time.perf_counter()
    asyncio.run(main())
    print(f"🏁 压测结束，总耗时: {time.perf_counter() - start_total:.2f}s")