# test_main.py
import pytest
from unittest.mock import AsyncMock  # 专门用来模拟异步函数的工具
from main import welcome_user, Database

# 告诉 pytest：这个函数里有 await，请用异步方式运行
@pytest.mark.asyncio
async def test_welcome_user_logic():
    # 【第一步：造假人 (Mock)】
    # 我们不希望测试时真的去连数据库，所以造个假的 Database
    mock_db = AsyncMock(spec=Database)
    
    # 规定：当有人调用 get_user_email 时，直接返回我们要的假数据
    mock_db.get_user_email.return_value = "fake_test@test.com"

    # 【第二步：执行测试】
    # 运行我们要测的 welcome_user，并把“假数据库”传给它
    result = await welcome_user(mock_db, 99)

    # 【第三步：检查结果 (Assert)】
    # 看看结果是不是我们预期的
    assert result == "Welcome, your email is fake_test@test.com"
    
    # 还可以检查：那个假数据库是不是真的被调用了？
    mock_db.get_user_email.assert_called_once_with(99)