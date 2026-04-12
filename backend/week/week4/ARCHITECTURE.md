# week4 的项目目标
- 本系统通过 FastAPI 接收 TS-79 传感器数据，使用 Pydantic 进行严苛校验。所有关键路径必须携带 Trace ID。最终交付为体积小于 200MB 的 Docker 镜像。

## 数据样本
{
    "device_id": "TS-79-SYD-001",
    "timestamp": "2026-04-12T12:30:00Z",
    "metadata": {
        "firmware_version": "v2.1.0",
        "location": "Sydney_Plant_05"
    },
    "sensors": [
        {"sensor_id": "TEMP_01", "value": 85.5, "unit": "Celsius"},
        {"sensor_id": "VOLT_02", "value": 12.4, "unit": "V"},
        {"sensor_id": "VIB_03", "value": 0.02, "unit": "g"}
    ],
    "status_code": 200
}

