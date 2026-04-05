import asyncio

class SensorService:
    async def fetch_data(self, sensor_id: int):
        # 模拟真实的网络请求
        await asyncio.sleep(1)
        return {"id": sensor_id, "value": 100}

async def get_all_data(service: SensorService, ids: list):
    tasks = [service.fetch_data(i) for i in ids]
    try:
        # 同时启动所有任务
        results = await asyncio.gather(*tasks)
        return results
    except Exception as e:
        # 如果任何一个任务失败，返回错误提示
        return f"Error occurred: {str(e)}"