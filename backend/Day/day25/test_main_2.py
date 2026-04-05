import pytest
from unittest.mock import AsyncMock
from main_2 import SensorService, get_all_data

@pytest.mark.asyncio
async def test_get_all_data_success():
    # 创建 Mock 
    mock_service = AsyncMock(spec=SensorService)
    # 模拟返回数据
    mock_service.fetch_data.side_effect = [
        {"id": 1, "value": 10},
        {"id": 2, "value": 20},
        {"id": 3, "value": 30}
    ]

    ids = [1, 2, 3]
    results = await get_all_data(mock_service, ids)

    # 断言：结果数量对不对？
    assert len(results) == 3
    assert results[0]["value"] == 10
    # 断言：是否真的并发调用了 3 次？
    assert mock_service.fetch_data.call_count == 3

@pytest.mark.asyncio
async def test_get_all_data_partial_failure():
    mock_service = AsyncMock(spec=SensorService)
    
    # 模拟：前两个成功，第三个突然抛出异常（比如传感器断开）
    mock_service.fetch_data.side_effect = [
        {"id": 1, "value": 10},
        {"id": 2, "value": 20},
        Exception("Sensor 3 Disconnected")
    ]

    ids = [1, 2, 3]
    result = await get_all_data(mock_service, ids)

    # 断言：程序没有崩溃，而是返回了错误字符串
    assert "Error occurred" in result
    assert "Sensor 3 Disconnected" in result