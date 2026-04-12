
# 这是你的程序入口。它会把 config 和 schemas 结合在一起。

from fastapi import FastAPI
# TODO: 从你的 config 文件导入 settings
from config import settings
# TODO: 从你的 schemas 文件导入 TS79DiagnosticPayload
from schemas import TS79DiagnosticPayload
from datetime import datetime
from logger import logger # 导入你刚才写的那个对象
import uuid # 顺便导入这个，给每次请求一个 ID

# TODO: Task 2.2 - 初始化 FastAPI 实例
# 提示：使用 settings.APP_NAME 和 settings.APP_VERSION 作为参数
app = FastAPI(title = settings.APP_NAME, version = settings.APP_VERSION)

@app.post("/v1/diagnose")
async def perform_diagnosis(payload: TS79DiagnosticPayload): # TODO: 将 None 替换为你的 Payload 模型
    """
    执行诊断逻辑的工位
    TODO:
    1. 遍历 payload.sensors
    2. 如果 unit 是 "Celsius" 且 value 超过 settings.TEMP_ALERT_THRESHOLD，记录警报
    3. 返回一个包含诊断结果 (Healthy/Critical) 和 警报列表的字典
    """
    trace_id = str(uuid.uuid4())
    # 1. 记录：开始诊断
    logger.info("start_diagnosis", device_id=payload.device_id, trace_id=trace_id)

    alerts = []
    for sensor in payload.sensors:
        if sensor.unit == "Celsius" and sensor.value > settings.TEMP_ALERT_THRESHOLD:
            alerts.append(f"设备 {payload.device_id} 温度过高: {sensor.value}度")
            # 2. 记录：发现严重问题
            logger.error("overheat_detected", device_id=payload.device_id, value=sensor.value)

    # 在 return 之前加上这一行，记录诊断结束的状态
    logger.info("diagnosis_complete", device_id=payload.device_id, is_healthy=len(alerts) == 0)
    return {
        "trace_id": trace_id,
        "message": "诊断完成",
        "is_healthy": len(alerts) == 0,
        "alerts": alerts,
        "server_info": settings.APP_NAME
    }

# TODO: Task 5.2 - 预留健康检查接口，供 Docker 使用
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": settings.APP_VERSION
    }

if __name__ == "__main__":
    import os
    print(f"当前程序的运行路径是: {os.getcwd()}")
    logger.info("checking_file_creation", path="app.log")
    
    import uvicorn
    # TODO: 使用 uvicorn 运行 app，端口 8000
    uvicorn.run(app, host="127.0.0.1", port=8000)