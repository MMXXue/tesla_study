from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        # 记录活跃连接
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"✅ 新用户接入，当前在线人数: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            print(f"❌ 用户离开，当前在线人数: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        # 注意这里：必须传两个参数 (消息, 哪个连接)
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # 1. 建立连接
    await manager.connect(websocket)
    
    try:
        while True:
            # 2. 接收客户端发来的字符串
            data = await websocket.receive_text()
            
            # 【心跳逻辑】收到 ping，回 pong
            if data == "ping":
                await manager.send_personal_message("pong", websocket)
            else:
                # 【业务逻辑】回显收到的内容，并传回当前的 websocket 对象
                # 修复了你刚才报错的地方：增加了第二个参数 websocket
                await manager.send_personal_message(f"服务器已收到: {data}", websocket)
                
    except WebSocketDisconnect:
        # 3. 正常或异常断开
        manager.disconnect(websocket)