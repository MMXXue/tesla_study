
# config.py (系统的“调节旋钮”)：规定了你自己系统的运行参数。

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, PostgresDsn, field_validator
from typing import Optional

class Settings(BaseSettings):
    # --- 1. 项目基础信息 ---
    APP_NAME: str = "TS-79-Diagnostic-Expert"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # --- 2. 数据库配置 (使用 Pydantic 的强大类型) ---
    # PostgresDsn 会自动校验字符串是否符合 postgres:// 格式
    DATABASE_URL: Optional[str] = Field(
        default=None, 
        env="DATABASE_URL"
    )

    # --- 3. 业务逻辑参数 (把硬编码参数抽离出来) ---
    TEMP_ALERT_THRESHOLD: float = 80.0  # 默认80度报警
    
    # --- 4. 配置读取规则 ---
    model_config = SettingsConfigDict(
        env_file=".env",              # 优先读这个文件
        env_file_encoding='utf-8',
        case_sensitive=True,          # 环境变量区分大小写
        extra='allow'                 # 允许额外字段
    )

    # --- 5. 进阶：自定义校验 ---
    @field_validator("TEMP_ALERT_THRESHOLD")
    @classmethod
    def validate_threshold(cls, v):
    #                      ↑   ↑
    #              这个车间名   进来的原材料
        if v < 0 or v > 200:
            raise ValueError("报警温度阈值设置不合理")
        return v

# 导出单例，其他文件直接 import settings 即可
settings = Settings()

