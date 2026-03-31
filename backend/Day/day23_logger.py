import structlog
import logging
import sys

def configure_logger():
    structlog.configure(
        processors=[
            # 提取日志级别 (告诉系统这条日志是 INFO（正常）、WARNING（警告）还是 ERROR（错误）)
            structlog.stdlib.add_log_level,
            # 注入时间戳
            structlog.processors.TimeStamper(fmt="iso"),
            # 允许传入上下文变量（如 trace_id） 开始去翻“隐形口袋”了
            structlog.contextvars.merge_contextvars,
            # 如果是终端环境则彩色输出，否则输出 JSON
            structlog.processors.JSONRenderer() if not sys.stderr.isatty() else structlog.dev.ConsoleRenderer()
        ],
        logger_factory=structlog.PrintLoggerFactory(),
    )

# 这是生产线的出口
log = structlog.get_logger()