from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# 定义和 .proto 相同的数据结构
class SensorData(BaseModel):
    device_id: str
    temperature: float
    humidity: int

@app.post("/report")
async def report_data(data: SensorData):
    # 逻辑与 gRPC Server 完全一致
    return {"status": "OK"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)