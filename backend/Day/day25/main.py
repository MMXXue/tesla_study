# main.py
import asyncio

# 这是一个模拟数据库操作的类
class Database:
    async def get_user_email(self, user_id):
        await asyncio.sleep(1)  # 模拟网络延迟
        return "real_user@example.com"

# 这是我们要测试的核心逻辑
async def welcome_user(db: Database, user_id: int):
    email = await db.get_user_email(user_id)
    return f"Welcome, your email is {email}"