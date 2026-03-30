import asyncio
import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware  # 修复 403 的核心
from contextlib import asynccontextmanager
from manager import manager  # 导入刚才写的收纳盒
from fastapi_mqtt import FastMQTT, MQTTConfig
import json

# # --- 模拟数据工厂：每 3 秒生成一个假传感器数据 ---
# async def mock_sensor_data():
#     while True:
#         await asyncio.sleep(3)
#         # 构造假数据
#         fake_payload = {
#             "device": "Tesla_Model3_Sensor",
#             "speed": 60,
#             "temp": 25.5,
#             "time": datetime.datetime.now().strftime("%H:%M:%S")
#         }
#         # 只有当有人在线时才广播
#         if manager.active_connections:
#             print(f"正在向 {len(manager.active_connections)} 个客户端推送数据...")
#             await manager.broadcast(fake_payload)

## --- 生命周期管理：程序启动时开启“工厂” ---
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     print("系统启动中：开启模拟数据推送...")
#     task = asyncio.create_task(mock_sensor_data())
#     yield
#     print("系统关闭中：正在停止任务...")
#     task.cancel()


# 1. --- MQTT 配置 ---
# 我们连接到一个公共的测试服务器 broker.emqx.io
mqtt_config = MQTTConfig(
    host="broker.emqx.io",
    port=1883,
    keepalive=60
)
fast_mqtt = FastMQTT(config=mqtt_config)

app = FastAPI()

# 2. --- 修复 403 Forbidden 的安全配置 ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. --- MQTT 事件：当连接成功时订阅主题 ---
@fast_mqtt.on_connect()    # 这就是“连接成功”的警报器。
def connect_handler(client, flags, rc, properties):
    # 订阅一个名为 "tesla/sensors" 的主题
    # 既然连上了，赶紧告诉服务器：“我要听 tesla/sensors 频道的消息”
    fast_mqtt.client.subscribe("tesla/sensors")
    print("已成功连接到 MQTT Broker，并订阅了主题: tesla/sensors")

# 4. --- MQTT 事件：核心！当收到真实传感器消息时 ---
@fast_mqtt.on_message()    # 这就是“有新邮件/消息”的警报器。
async def message_handler(client, topic, payload, qos, properties):
    # 收到的是字节，需要解码 把字节变成字符串，比如 '{"temp": 25}'
    raw_data = payload.decode()
    print(f"【MQTT 实时数据】主题: {topic} | 内容: {raw_data}")
    
    # 尝试将字符串转为 JSON (如果发来的是 JSON)
    try:
        data_json = json.loads(raw_data) # 尝试把字符串转成字典
    except:
        data_json = {"raw": raw_data}   # 如果对方发的不是标准 JSON，就原样保存

    # 关键：把从 MQTT 拿到的真实数据，通过 WebSocket 广播出去！
    await manager.broadcast({
        "source": "MQTT_REAL_TIME",
        "topic": topic,
        "payload": data_json
    })

# 5. --- WebSocket 路由 ---
@app.websocket("/ws/monitor")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # 保持连接，监听网页指令
            data = await websocket.receive_text()
            print(f"收到网页端指令: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# 将 MQTT 挂载到 FastAPI
fast_mqtt.init_app(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)