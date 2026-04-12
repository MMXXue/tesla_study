
# schemas.py (数据的“法律”)：规定了外面进来的数据长什么样。

from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import List

# TODO: Task 2.1 - 定义单条传感器数据模型
class SensorReadout(BaseModel):
    # 提示：需要包含 sensor_id (str), value (float), unit (str)
    sensor_id: str
    value: float
    unit: str

# TODO: Task 2.1 - 定义元数据模型
class DeviceMetadata(BaseModel):
    # 提示：需要包含 firmware_version (str), location (str)
    firmware_version: str
    location: str

# TODO: Task 2.1 - 定义主数据模型
class TS79DiagnosticPayload(BaseModel):
    """
    这是你的核心数据合同。
    要求：
    1. 包含 device_id, timestamp, metadata, sensors (列表), status_code
    2. 使用 @field_validator 确保 device_id 必须以 "TS-79-" 开头 (使用 cls, v)
    """
    device_id: str
    timestamp: datetime
    metadata: DeviceMetadata
    sensors: List[SensorReadout]
    status_code: int = 200
    
    @field_validator("device_id")
    @classmethod
    def must_be_ts79(cls, v):
        if not v.startswith("TS-79-"):
            raise ValueError("必须是 TS-79 系列设备")
        return v