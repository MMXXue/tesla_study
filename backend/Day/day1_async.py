import time          # 导入 time 模块，用于同步阻塞式 sleep
import asyncio       # 导入 asyncio 模块，用于编写异步协程

# --- 同步部分：像普通人排队 ---
def sync_task(name):                             # 定义一个普通的同步函数，表示一个阻塞的任务
    print(f"同步任务 {name} 开始...")           # 打印当前同步任务开始的信息
    time.sleep(2)                                # 阻塞当前线程 2 秒，这 2 秒内程序什么也干不了
    print(f"同步任务 {name} 完成！")            # 打印当前同步任务完成的信息

# --- 异步部分：像极客并行 ---
async def async_task(name):                      # 定义一个异步协程函数，前面用 async 关键字
    print(f"异步任务 {name} 开始...")           # 打印当前异步任务开始的信息
    # await 的含义：这里要“等待”一个异步操作
    # 在等待的这 2 秒里，事件循环可以去运行别的协程，不会像 time.sleep 那样把线程卡住
    await asyncio.sleep(2)                       # 异步地“睡眠” 2 秒，不阻塞事件循环
    print(f"异步任务 {name} 完成！")            # 打印当前异步任务完成的信息

async def main():                                # 定义主协程，负责组织整体流程
    # 1. 演示同步的低效
    print("\n--- 开始演示【同步】：你会发现是一个接一个跑，总共大约 6 秒 ---")
    start_sync = time.perf_counter()             # 使用高精度计时函数记录同步开始时间
    sync_task("A")                               # 顺序执行第一个同步任务，耗时约 2 秒
    sync_task("B")                               # 顺序执行第二个同步任务，再耗时约 2 秒
    sync_task("C")                               # 顺序执行第三个同步任务，再耗时约 2 秒
    # 这里三个任务是串行执行的，所以总时间大约是 2 + 2 + 2 = 6 秒
    print(f"同步总耗时: {time.perf_counter() - start_sync:.2f} 秒")  # 计算并打印同步总耗时

    # 2. 演示异步的高效（高并发的核心思想）
    print("\n--- 开始演示【异步】：你会发现是 3 个一起跑，总共只要大约 2 秒 ---")
    start_async = time.perf_counter()            # 记录异步部分开始时间
    
    # 【重点】使用 asyncio.gather 同时启动多个协程任务
    # 这一步的含义：把三个协程一起交给事件循环调度，它们会“并发地”等待 2 秒
    # 因为三个 async_task 里都是 await asyncio.sleep(2)，可以重叠等待时间
    await asyncio.gather(
        async_task("任务1"),                     # 创建并调度第一个异步任务
        async_task("任务2"),                     # 创建并调度第二个异步任务
        async_task("任务3")                      # 创建并调度第三个异步任务
    )
    # 三个任务几乎同时开始等待 2 秒，所以总体耗时接近 2 秒，而不是 6 秒
    print(f"异步总耗时: {time.perf_counter() - start_async:.2f} 秒")  # 计算并打印异步总耗时

# 只有当当前文件被“直接运行”时，才执行下面这一段
if __name__ == "__main__":
    # asyncio.run 会创建事件循环，然后运行 main 协程，直到其执行完成
    asyncio.run(main())
