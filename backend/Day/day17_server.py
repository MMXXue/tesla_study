import sys
import os

# 1. 核心补丁：获取当前文件所在的目录 (day)，然后定位到 day16
current_dir = os.path.dirname(os.path.abspath(__file__))
day16_path = os.path.join(current_dir, "day16")

# 2. 把 day16 文件夹加入 Python 的搜索路径
if day16_path not in sys.path:
    sys.path.append(day16_path)



import grpc
import day16.day16_sensor_pb2 as pb2
import day16.day16_sensor_pb2_grpc as pb2_grpc
from concurrent import futures

# 我们定义一个类，它继承自生成的“服务基类”
# 就像是在物业办公室里分配一个具体的办事员
class SmartFactoryServicer(pb2_grpc.SmartFactoryServicer):
    
    # 这个函数名必须和你在 .proto 里定义的 rpc 名字一模一样
    def ReportData(self, request, context):
        # 1. 拿到客户端发来的数据
        device = request.device_id
        temp = request.temperature
        humi = request.humidity
        
        # 2. 模拟处理逻辑（比如打印出来，或者存进你的 PostgreSQL）
        print(f"📡 [Server收到] 设备: {device} | 温度: {temp}°C | 湿度: {humi}%")
        
        # 3. 必须给客户端一个回执（Response）
        # 就像办完事给人家一张回执单
        return pb2.SensorResponse(status="数据已安全送达大脑")
    

def serve():
# 1. 招聘接线员：创建一个线程池，允许同时处理 10 个人打电话进来
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # 2. 分配业务：把我们刚才写的 SmartFactoryServicer 绑定到服务器上
    pb2_grpc.add_SmartFactoryServicer_to_server(SmartFactoryServicer(), server)
    
    # 3. 确定地址：监听本地的 50051 端口
    # '[::]' 表示监听所有 IP 地址，类似于 0.0.0.0
    server.add_insecure_port('[::]:50051')
    
    print("🚀 Tesla 工厂中央大脑已启动，正在 50051 端口待命...")
    
    # 4. 正式运行
    server.start()
    
    # 让程序别关，一直等着
    server.wait_for_termination()

if __name__ == '__main__':
    serve()