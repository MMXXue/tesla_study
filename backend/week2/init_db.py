
# 📜 初始化数据库里需要的表 diagnostic_logs

import asyncio
import asyncpg

async def create_table():
    # 1. 连接到你的 Docker 容器
    conn = await asyncpg.connect('postgresql://postgres:password@localhost:5432/postgres')
    
    print("📡 正在连接数据库...")

    # 2. 编写建表语句 (SQL)
    # id: 自动增长的数字
    # level: 日志级别（INFO/ERROR）
    # message: 日志具体内容
    # created_at: 自动记录存入时间
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS diagnostic_logs (
            id SERIAL PRIMARY KEY,
            level VARCHAR(20),
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    
    await conn.close()
    print("✅ 表 'diagnostic_logs' 已成功创建！")

if __name__ == "__main__":
    asyncio.run(create_table())
