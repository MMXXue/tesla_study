from config import settings

def test_my_config():
    print("-" * 30)
    print(f"🚀 当前项目名: {settings.PROJECT_NAME}")
    print(f"📊 当前日志级别: {settings.LOG_LEVEL}")
    print(f"🔗 数据库地址: {settings.DATABASE_URL}")
    print("-" * 30)

if __name__ == "__main__":
    test_my_config()