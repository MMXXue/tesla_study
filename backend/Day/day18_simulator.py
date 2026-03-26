
# 负责用 for 循环 publish（发布）1000 条消息

import paho.mqtt.client as mqtt
import time
import random

# 1. 初始化 (2.0 规范)
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "Sheldon_Simulator")
client.connect("localhost", 1883)

print("🚀 模拟器启动，正在模拟 1000 个机器人上报...")

try:
    for i in range(1, 1001): # 循环 1 到 1000
        # 动态生成频道名：tesla/factory/robot_001/data ... 到 robot_1000
        topic = f"tesla/factory/robot_{i:03d}/data" 
        
        # 模拟一个随机温度
        temp = round(random.uniform(20, 30), 1)
        message = f"Robot_{i:03d} Temp: {temp}C"
        
        # 发送数据
        client.publish(topic, message)
        
        # 稍微停一下（0.01秒），否则你的屏幕会炸裂
        time.sleep(0.01) 
        
    print("✅ 1000 个数据全部发送完毕！")
except KeyboardInterrupt:
    pass

client.disconnect()