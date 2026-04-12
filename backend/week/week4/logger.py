
# 标准化日志表格形式

import structlog
import logging
import sys
from logging.handlers import RotatingFileHandler
import os

def setup_logging():
    # 找到 logger.py 所在的文件夹路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 把路径和文件名拼在一起，形成绝对路径
    log_path = os.path.join(current_dir, "app.log")


    # 第一步：设置“搬运工” (Logging Handlers)
    # 这个搬运工负责把日志写进 app.log 文件，超过 5MB 就换新文件
    file_handler = RotatingFileHandler(
        log_path, maxBytes=5 * 1024 * 1024, backupCount=5, delay=False  # 立刻创建文件
    )

    # 【新增点】强制每一条日志都立刻写入硬盘，不留存缓冲区
    # 这在开发调试阶段非常有用
    file_handler.setFormatter(logging.Formatter('%(message)s'))
    
    # 这个搬运工负责把日志打印到你的屏幕上
    console_handler = logging.StreamHandler(sys.stdout)

    # 第二步：把搬运工交给 Python 核心系统
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # 第三步：配置 structlog 的“加工流水线”
    structlog.configure(
        processors=[
            # 添加时间戳
            structlog.processors.TimeStamper(fmt="iso"),
            # 添加日志级别 (INFO, ERROR 等)
            structlog.processors.add_log_level,
            # 将输出格式化为 JSON
            structlog.processors.JSONRenderer()
        ],
        # 这一行最关键：它告诉 structlog 把加工好的 JSON 字符串交给上面那两个“搬运工”
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

setup_logging()
logger = structlog.get_logger()