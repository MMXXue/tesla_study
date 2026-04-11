import sys
import os

# 1. 彻底锁定路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 这里的路径必须指向那个包含 __init__.py 的真实代码目录
real_code_dir = os.path.join(current_dir, "tesla-ts-79-diagnostic-api-client")
if real_code_dir not in sys.path:
    sys.path.insert(0, real_code_dir)
                              
# 2. 尝试终极导入逻辑
try:
    # 这里的包名必须是带下划线的那个小文件夹名
    from tesla_ts_79_diagnostic_api_client import Client
    from tesla_ts_79_diagnostic_api_client.models import DiagnosticTask
    # 直接导入那个被 grep 出来的长文件名模块
    from tesla_ts_79_diagnostic_api_client.api.diagnosis import analyze_vehicle_v1_analyze_post as api_module
except Exception as e:
    print(f"❌ 导入包失败，报错信息: {e}")
    print("💡 建议检查：tesla-ts-79-diagnostic-api-client 文件夹里的小文件夹到底叫什么？")
    sys.exit(1)

# 3. 创建客户端
client = Client(base_url="http://127.0.0.1:8000")

def run_test():
    # 4. 构造数据模型
    task = DiagnosticTask(
        vin="5YJ3E1EB123456789",
        fault_code="BMS_a066"
    )

    print("🚀 正在通过 SDK 发送诊断请求...")

    try:
        # 5. 调用你在 grep 中亲眼看到的那个 sync 函数
        response = api_module.sync(client=client, body=task)
        
        if response:
            print("-" * 30)
            print("✅ 恭喜！Day 29 终极通关！")
            # 使用 getattr 安全读取返回字段
            suggestion = getattr(response, 'suggestion', '未定义返回字段')
            print(f"🤖 AI 诊断建议: {suggestion}")
            print("-" * 30)
    except Exception as e:
        print(f"❌ 请求发送成功但处理失败: {e}")

if __name__ == "__main__":
    run_test()