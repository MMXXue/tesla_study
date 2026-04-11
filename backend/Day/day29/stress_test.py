import sys
import os
import time

# --- 1. 路径锁定 (确保能找到 SDK) ---
current_dir = os.path.dirname(os.path.abspath(__file__))
# 这里的路径必须指向你生成的 SDK 文件夹名
sdk_dir = os.path.join(current_dir, "tesla-ts-79-diagnostic-api-client")
if sdk_dir not in sys.path:
    sys.path.insert(0, sdk_dir)

# --- 2. 导入 SDK 组件 ---
try:
    from tesla_ts_79_diagnostic_api_client import Client
    from tesla_ts_79_diagnostic_api_client.models import DiagnosticTask, DiagnosticResult, HTTPValidationError
    from tesla_ts_79_diagnostic_api_client.api.diagnosis import analyze_vehicle_v1_analyze_post as api_module
except ImportError as e:
    print(f"❌ 导入失败：请确认 SDK 文件夹名称是否正确！错误信息: {e}")
    sys.exit(1)

# --- 3. 配置与模拟数据 ---
client = Client(base_url="http://127.0.0.1:8000")

# 生成 5 个符合 17 位规范的模拟故障数据
# 这里要保证 VIN 长度正好 17 位，否则会被 Pydantic 校验拒绝
test_cases = [
    {
        "vin": f"TSLA{i:09d}XXXX",  # 4 + 9 + 4 = 17
        "fault_code": f"BMS_a{i}66"
    }
    for i in range(1, 6)
]

for case in test_cases:
    assert len(case["vin"]) == 17, f"VIN 长度错误: {case['vin']} ({len(case['vin'])})"


def run_batch_test():
    print("="*50)
    print("🚀 Tesla 自动化批量诊断测试启动")
    # 把 client.base_url 改成 client._base_url
    print(f"📍 目标地址: {client._base_url}")
    print("="*50)
    
    start_time = time.time()
    success_count = 0

    for case in test_cases:
        # 封装数据模型
        task = DiagnosticTask(
            vin=case["vin"],
            fault_code=case["fault_code"]
        )
        
        print(f"📡 正在发送 VIN: {case['vin']} ...", end=" ", flush=True)
        
        try:
            # 执行同步调用
            # 注意：根据你的 SDK 版本，参数名可能是 body 或 json_body
            response = api_module.sync(client=client, body=task)
            
            # 逻辑判断：SDK 通常会返回 Union[DiagnosticResult, HTTPValidationError]
            if isinstance(response, DiagnosticResult):
                success_count += 1
                status = "✅ 成功"
                detail = f"AI建议: {response.suggestion[:15]}..."
            elif isinstance(response, HTTPValidationError):
                status = "⚠️ 校验失败"
                detail = f"详情: {response.detail}"
            else:
                status = "❓ 未知响应"
                detail = f"类型: {type(response)}"
            
            print(f"{status} | {detail}")

        except Exception as e:
            print(f"❌ 系统异常: {e}")

    # 统计结果
    end_time = time.time()
    duration = end_time - start_time
    print("="*50)
    print(f"✨ 测试完成！")
    print(f"📊 成功率: {success_count}/{len(test_cases)}")
    print(f"⏱️ 总耗时: {duration:.2f} 秒")
    print("="*50)

if __name__ == "__main__":
    run_batch_test()