import asyncio
import random
import time

async def get_charger_status(charger_id : str, sem : asyncio.Semaphere):
     async with sem:
        print(f"🔗 正在尝试连接[{charger_id}]....")
        if charger_id == 4:
            raise RuntimeError(f"⚠️ {charger_id}的硬件通讯中断!")
        
        delay = random(1,3)
        await asyncio.sleep(delay)

        return charger_id, random.randint(0, 100)


async def main():
    sem = asyncio.Semaphore(2)
    tasks = [
        asyncio.create_task(get_charger_status(i, sem))
        for i in range(5)
    ]
    
    start_time = time.perf_counter()
    print(f"准备开始处理任务....")

    for finished_task in asyncio.as_completed(tasks):
        try:
            charger_id, battery = await finished_task
            print(f"✅ {charger_id}目前还有{battery}的电量🔋,总耗时{time.perf_counter() - start_time}s")
        except RuntimeError as e:
            print(f"❌ 任务处理失败，错误: {e}（其他任务继续执行）")

    print(f"所有任务都已执行完毕,总耗时{time.perf_counter() - start_time}")

if __name__ == "__main__":
    asyncio.run(main())