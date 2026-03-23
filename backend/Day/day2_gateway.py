import asyncio
import random
import time


async def mock_ai_inference(user_id: str, request_text: str, sem: asyncio.Semaphore):
    # 【关键】async with sem: 是信号量的"获取-释放"机制
    # 进入 async with 时会尝试获取信号量：
    #   - 如果信号量还有"名额"（比如 Semaphore(2) 表示最多 2 个），就立即进入
    #   - 如果没有名额，当前协程会在这里"挂起"，等待其他协程释放信号量
    # 退出 async with 时（无论正常退出还是异常），会自动释放信号量，让排队的协程继续
    async with sem:
        # 监控代码：查看当前信号量状态（仅用于调试，生产环境不建议访问私有属性）
        free_slots = sem._value
        waiting_count = len(sem._waiters) if sem._waiters else 0
        print(f"--- [监控进入] | 用户 {user_id} 进入门内 , 当前空位: {free_slots} , 排队人数: {waiting_count} ---")

        #函数 A：模拟 AI 推理，随机耗时 1~4 秒"""
        delay = random.uniform(1, 4)  # 随机生成 1~4 秒的浮点数

        # 这里你加了一个“马斯克就报错”的彩蛋，我保留
        # 【异常处理练习】如果 user_id 是 "3" 或 3，就抛出异常（模拟 GPU 显存溢出）
        # 注意：这里直接 raise，不 try-except，让异常抛给调用方处理
        if user_id == "3" or user_id == 3:
            raise ValueError("GPU 显存溢出！")

        await asyncio.sleep(delay)  # 异步等待 delay 秒，模拟耗时

        # 返回处理结果，这里用 (user_id, request_text) 简单表示
        return user_id, request_text, delay


async def main():
    # 【关键】创建信号量，参数 1 表示：同时最多只有 1 个协程能进入 async with sem 块
    # 如果改成 Semaphore(2)，就是最多 2 个并发；Semaphore(3) 就是最多 3 个并发
    # 这是"限流"的核心：防止无限并发导致资源耗尽
    sem = asyncio.Semaphore(1)
    """函数 B：创建 5 个任务，并使用 asyncio.as_completed 逐个按完成顺序处理"""
    start_time = time.perf_counter()

    # 【关键】创建 5 个协程对象（注意：这里只是创建，还没开始执行）
    # 每个任务都会传入同一个 sem 信号量，它们会"竞争"信号量的名额
    tasks = [
        mock_ai_inference("工厂质检员", "检查 Model 3 车门缝隙", sem),
        mock_ai_inference("自动驾驶组", "识别前方障碍物", sem),
        mock_ai_inference("3", "把火箭发射到火星", sem),  # 这个任务会抛出异常
        mock_ai_inference("HR部门", "筛选 100 份简历", sem),
        mock_ai_inference("车主APP", "开启远程空调", sem),
    ]

    # 【关键】asyncio.as_completed(tasks) 返回一个迭代器，按任务完成顺序（而非创建顺序）返回
    # 这意味着：哪个任务先完成，就先从迭代器里拿到哪个任务的结果
    # 即使任务 3 先完成，也会先处理任务 3，而不是按 1、2、3、4、5 的顺序
    # 【关键】用 try-except 包裹 await，确保一个任务崩了不会影响其他任务
    # 这是"异常隔离"的核心：单个请求失败不应该导致整个服务崩溃
    for finished_task in asyncio.as_completed(tasks):
        try:
            user_id, request_text, delay = await finished_task
            finished_time = time.perf_counter()
            print(
                f"[{finished_time - start_time:5.2f}s] "
                f"用户 {user_id} 的请求「{request_text}」处理完成（耗时约 {delay:.2f} 秒）"
            )
        except ValueError as e:
            # 【关键】捕获异常后，继续循环处理下一个任务，不会中断整个流程
            # 即使任务 3 抛异常，任务 4、5 依然会正常执行和打印结果
            # 这就是"异常隔离"：一个请求崩了，其他请求不受影响
            finished_time = time.perf_counter()
            print(
                f"[{finished_time - start_time:5.2f}s] "
                f"❌ 任务处理失败，错误: {e}（其他任务继续执行）"
            )

    total_time = time.perf_counter() - start_time
    print(f"所有任务都处理完了！总耗时 {total_time:.2f} 秒")


if __name__ == "__main__":
    asyncio.run(main())
