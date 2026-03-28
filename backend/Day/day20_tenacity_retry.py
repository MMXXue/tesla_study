
# tenacity + jitter(随机抖动)

import random
import time
from tenacity import retry, stop_after_attempt, wait_exponential, wait_random, after_log
import logging  # 导入 Python 自带的日志管家


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





# --- 第一部分：模拟一个“不稳定”的 API 调用 ---
def call_tesla_api():
    # 模拟 70% 的失败概率
    if random.random() < 0.7:
        print(f"[{time.strftime('%H:%M:%S')}] ❌ 网络连接失败，正在触发重试逻辑...")
        raise Exception("Tesla Cloud Connection Error")
    
    print(f"[{time.strftime('%H:%M:%S')}] ✅ 成功获取路况数据！")
    return "Road Data: Clear"

# --- 第二部分：使用 Tenacity 给函数加“外壳” ---
# multiplier: 初始等待时间基数
# min: 最小等待秒数
# max: 最大等待秒数
@retry(
    wait=wait_exponential(multiplier=1, min=2, max=10) + wait_random(0, 1), 
    stop=stop_after_attempt(5),
    before_sleep=my_before_sleep  # <--- 加入这个“播报员”
)
def smart_fetch():
    return call_tesla_api()

# --- 第三部分：实际执行并捕获最终结果 ---
if __name__ == "__main__":
    print("🚀 开始请求 Tesla 云端数据...\n")
    try:
        result = smart_fetch()
        print(f"\n🎉 任务完成！获取到的内容是: {result}")
    except Exception as e:
        print(f"\n⚠️ 最终失败：尝试了 5 次依然无法连接。错误详情: {e}")