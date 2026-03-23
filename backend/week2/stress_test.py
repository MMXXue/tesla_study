
# 压力测试脚本, 一个“疯狂点击按钮”的机器人
# 同时,一定要是 异步的测试脚本!!!!

import asyncio
import httpx
import time

# 1. 配置信息
TARGET_URL = "http://127.0.0.1:8000/log"
TOTAL_REQUESTS = 1000  # 我们总共发 1000 个包裹
CONCURRENCY = 20       # 当前机器实测该并发更稳定，避免拥塞导致延迟飙升

async def send_one_log(client, index):
    """模拟发送一个日志请求"""
    payload = {
        "level": "INFO",
        "message": f"Tesla Test Log No.{index}"
    }
    
    start = time.perf_counter()
    try:
        # 发送 POST 请求
        response = await client.post(TARGET_URL, json=payload)
        end = time.perf_counter()
        
        # 返回：是否成功 (200), 耗时(毫秒)
        return response.status_code == 200, (end - start) * 1000
    except Exception as e:
        print(f"❌ 请求 {index} 失败: {type(e).__name__} - {e}")
        return False, 0

async def run_test():
    print(f"🚀 准备发动‘洪水攻击’：总计 {TOTAL_REQUESTS} 个请求...")

    sem = asyncio.Semaphore(CONCURRENCY)

    async def limited_send(client, index):
        async with sem:
            return await send_one_log(client, index)

    # 2. 创建一个异步客户端
    limits = httpx.Limits(max_connections=CONCURRENCY, max_keepalive_connections=CONCURRENCY)
    timeout = httpx.Timeout(connect=5.0, read=10.0, write=10.0, pool=30.0)
    async with httpx.AsyncClient(limits=limits, timeout=timeout) as client:
        start_time = time.perf_counter()
        
        # 3. 创建 1000 个任务并并发执行
        tasks = [limited_send(client, i) for i in range(TOTAL_REQUESTS)]
        results = await asyncio.gather(*tasks)
        
        end_time = time.perf_counter()

    # 4. 计算结果 (这就是你要交给 Tesla 的成绩单)
    total_duration = end_time - start_time
    success_results = [r[1] for r in results if r[0] is True]
    
    avg_latency = sum(success_results) / len(success_results) if success_results else 0
    tps = len(success_results) / total_duration

    print("\n" + "="*30)
    print(f"📊 压测报告")
    print(f"成功请求: {len(success_results)} / {TOTAL_REQUESTS}")
    print(f"总耗时: {total_duration:.2f} 秒")
    print(f"🔥 实际 TPS: {tps:.2f}  (目标: >500)")
    print(f"⏱️  平均延迟: {avg_latency:.2f} ms (目标: <50ms)")
    print("="*30)

if __name__ == "__main__":
    asyncio.run(run_test())