
# tenacity + jitter(随机抖动)

import random
import time
from tenacity import retry, stop_after_attempt, wait_exponential, wait_random, after_log
import logging  # 导入 Python 自带的日志管家
import pybreaker  # 熔断机制


#这是进阶的学习内容

# --- 关键修改：先清理之前的配置，确保这次配置生效 ---
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# 1. 设置一个简单的日志记录器（模拟监控系统）
logging.basicConfig(
    filename='backend/day/day20_tesla_debug.log', # <--- 告诉它存入这个文件
    filemode='a',              # 'a' 代表追加模式（不删旧的，只加新的）
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
    )
logger = logging.getLogger(__name__)

# 2. 定义一个重试时的“播报员”
def my_before_sleep(retry_state):
    msg = f"第 {retry_state.attempt_number} 次失败，等待中..."
    print(msg)            # 屏幕显示
    logger.warning(msg)   # 文件记录



# --- 熔断机制 ---

# fail_max: 连续失败 3 次就跳闸（Open）
# reset_timeout: 跳闸 10 秒后尝试进入半开状态（Half-Open）
db_breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=10)





# --- 第一部分：模拟一个“不稳定”的 API 调用 ---
def call_tesla_api():
    # 模拟 70% 的失败概率
    if random.random() < 1:
        print(f"[{time.strftime('%H:%M:%S')}] ❌ 网络连接失败，正在触发重试逻辑...")
        raise Exception("Tesla Cloud Connection Error")
    
    print(f"[{time.strftime('%H:%M:%S')}] ✅ 成功获取路况数据！")
    return "Road Data: Clear"


# --- 第二部分：使用 Tenacity 给函数加“外壳” ---
# multiplier: 初始等待时间基数
# min: 最小等待秒数
# max: 最大等待秒数
@db_breaker # <--- 第一层保护：熔断器
@retry(     # <--- 第二层保护：指数退避重试
    wait=wait_exponential(multiplier=1, min=2, max=10) + wait_random(0, 1), 
    stop=stop_after_attempt(5),
    before_sleep=my_before_sleep  # <--- 加入这个“播报员”
)
def smart_fetch():
    return call_tesla_api()

# --- 第三部分：实际执行并捕获最终结果 ---
if __name__ == "__main__":
    for i in range(15): # 模拟连续发起 15 次任务
        print(f"\n🚀 发起第 {i+1} 组任务:")
        try:
            # 执行受保护的函数
            result = smart_fetch()
            print(f"✅ 结果: {result}")
        except pybreaker.CircuitBreakerError:
            # 如果熔断器跳闸了，会直接抛出这个错误，不再执行函数内部的重试
            logger.error("🔴 熔断器处于开启状态！请求被直接拦截，保护服务器。")
        except Exception as e:
            # 这是重试了 3 次都失败后抛出的最终异常
            logger.warning(f"⚠️ 重试 3 次后依然失败: {e}")
        
        time.sleep(1) # 每组任务间隔 1 秒，方便观察逻辑