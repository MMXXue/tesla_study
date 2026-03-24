import grpc
# 导入你刚刚生成的两个“翻译官”文件
import day16_sensor_pb2 as sensor_pb2
import day16_sensor_pb2_grpc as sensor_pb2_grpc

def run():
    # 1. 拨号：尝试连接本地的 50051 端口（就像拿起电话）
    # insecure_channel 表示现在先不加密，方便测试
    with grpc.insecure_channel('localhost:50051') as channel:
        
        # 2. 找接线员：创建一个“存根 (Stub)”，它负责具体的业务对接
        stub = sensor_pb2_grpc.SmartFactoryStub(channel)
        
        print("--- 准备上报数据 ---")
        
        # 3. 填表：按照密码本定义的数据格式填好
        request = sensor_pb2.SensorRequest(
            device_id="Tesla_Robot_01",
            temperature=25.5,
            humidity=40
        )
        
        # 4. 发送：调用 ReportData 方法，就像调用本地函数一样简单
        # 注意：因为我们还没开服务器，这一步现在运行会报错，但这正是我们要观察的！
        try:
            response = stub.ReportData(request)
            print(f"服务器回执: {response.status}")
        except grpc.RpcError as e:
            print(f"发送失败 (意料之中): 因为中央大脑(Server)还没上班呢！错误信息: {e.code()}")

if __name__ == '__main__':
    run()