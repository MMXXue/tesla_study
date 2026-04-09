import os
from pydantic_settings import BaseSettings, SettingsConfigDict

# 获取当前 config.py 文件所在的文件夹路径
curr_dir = os.path.dirname(os.path.abspath(__file__))
# 拼接出 .env 的绝对路径
env_path = os.path.join(curr_dir, ".env")

class Settings(BaseSettings):
    PROJECT_NAME: str = "Default Name"
    LOG_LEVEL: str = "DEBUG"
    DATABASE_URL: str = "sqlite:///default.db"
    TESLA_API_KEY: str = "default_key_here"

    # 重点：使用精准的绝对路径
    model_config = SettingsConfigDict(
        env_file=env_path, 
        env_file_encoding="utf-8"
    )

settings = Settings()