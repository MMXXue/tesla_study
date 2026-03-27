
# 用来接收数据的程序
# 在 MQTT 中，如果发布者发消息时没有订阅者在线，消息通常就丢了(除非设置了特殊标志).所以我们要先让“大脑”蹲守.

import paho.mqtt.client as mqtt


# 1. 定义“听到消息”后要做什么 (Callback)
async def on_message(client, userdata, msg):
    print(f"接收到信号频段: {msg.topic} | 内容: {msg.payload.decoder()}")

# 2. 初始化客户端 (同样要用 2.0 版本的规矩)
brain = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "Sheldon_tesla_brain")
# 3. 绑定“听到消息”的动作
brain.on_message = on_message()
# 4. 连接并订阅频道
brain.connect("127.0.0.1", 1883)
brain.subscribe("tesla/factory/+/data")

print("🧠 大脑已启动，正在监听频道：tesla/factory/robot_01...")

# 5. 开始循环（让程序停在这里，不要运行完就结束）
brain.loop_forever()