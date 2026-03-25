
# 用于给 REST 和 gRPC 掐表比赛的]

import time
import requests  # 用于 REST 测试
import grpc
import sys
import os

# 路径修复（沿用你刚才学会的绝招）
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, "day16"))

import day16.day16_sensor_pb2 as pb2
import day16.day16_sensor_pb2_grpc as pb2_grpc

ITERATIONS = 1000  # 测试 1000 次连续发送

def test_grpc():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = pb2_grpc.SmartFactoryStub(channel)
        request = pb2.SensorRequest(device_id="Robot_01", temperature=25.5, humidity=40)
        
        start_time = time.time()
        for _ in range(ITERATIONS):
            stub.ReportData(request)
        end_time = time.time()
        
        return end_time - start_time

def test_rest():
    payload = {"device_id": "Robot_01", "temperature": 25.5, "humidity": 40}
    
    start_time = time.time()
    for _ in range(ITERATIONS):
        requests.post("http://localhost:8000/report", json=payload)
    end_time = time.time()
    
    return end_time - start_time

if __name__ == "__main__":
    print(f"🚀 开始性能对标测试 (循环 {ITERATIONS} 次)...")
    
    # 注意：运行前确保两个 Server 都已启动！
    grpc_time = test_grpc()
    print(f"✅ gRPC 耗时: {grpc_time:.4f} 秒")
    
    rest_time = test_rest()
    print(f"❌ REST (JSON) 耗时: {rest_time:.4f} 秒")
    
    print(f"\n🔥 结论：gRPC 比 REST 快了 {(rest_time/grpc_time):.2f} 倍！")