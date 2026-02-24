import asyncio
import httpx # 如果没装，执行 pip install httpx

async def send_request(client, i):
    resp = await client.get("http://127.0.0.1:8000/predict", params={"user_id": f"用户_{i}"})
    print(f"请求 {i} 完成: {resp.json()}")

async def main():
    async with httpx.AsyncClient(timeout=30.0) as client:
        # 同时发出 5 个请求
        tasks = [send_request(client, i) for i in range(5)]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())