
# 用于测试的pytest

from fastapi.testclient import TestClient
# 从你的 main.py 导入 app 实例
from main import app
import pytest

# 初始化测试客户端
client = TestClient(app)

def test_diagnosis_healthy():
    """
    场景：设备温度正常（25度），预期返回 Healthy。
    """
    # 1. 准备数据 (Arrange)
    payload = {
        "device_id": "TS-79-SYD-001",
        "timestamp": "2026-04-12T10:00:00",
        "metadata": {"firmware_version": "1.0.1", "location": "Sydney"},
        "sensors": [
            {"sensor_id": "T1", "value": 25.0, "unit": "Celsius"}
        ]
    }

    # 2. 执行请求 (Act)
    response = client.post("/v1/diagnose", json=payload)

    # 3. 验证结果 (Assert)
    assert response.status_code == 200
    result = response.json()
    assert result["is_healthy"] is True
    assert len(result["alerts"]) == 0


def test_diagnosis_overheat():
    """
    场景：设备温度过高（95度），预期返回 Critical 且包含警报信息。
    """
    # 1. 准备数据 (Arrange)
    payload = {
        "device_id": "TS-79-SYD-002",
        "timestamp": "2026-04-12T10:05:00",
        "metadata": {"firmware_version": "1.0.1", "location": "Sydney"},
        "sensors": [
            {"sensor_id": "T2", "value": 95.0, "unit": "Celsius"}
        ]
    }

    # 2. 执行请求 (Act)
    response = client.post("/v1/diagnose", json=payload)

    # 3. 验证结果 (Assert)
    assert response.status_code == 200
    result = response.json()
    assert result["is_healthy"] is False
    # 检查是否包含我们预期的错误文案
    assert "温度过高" in result["alerts"][0]


def test_health_check_endpoint():
    """
    场景：检查服务器基础健康状态。
    """
    # 执行 GET 请求
    response = client.get("/health")
    
    # 验证
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"