from fastapi import WebSocket
from typing import List

class ConnectionManager:
    def __init__(self):
        # 你的“管子收纳盒”：存放所有活跃的 WebSocket 实例
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        # 1. 接受连接（接通电话）
        await websocket.accept()
        # 2. 存入收纳盒
        self.active_connections.append(websocket)
        print(f"--- 新用户上线！当前在线人数: {len(self.active_connections)} ---")

    def disconnect(self, websocket: WebSocket):
        # 3. 从收纳盒移除
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            print(f"--- 用户下线。当前在线人数: {len(self.active_connections)} ---")

    async def broadcast(self, message: dict):
        # 4. 往收纳盒里所有的管子“灌”数据
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"推送失败，连接可能已失效: {e}")

# 实例化：创建一个真正的收纳盒供全局使用，变量名必须叫 manage
manager = ConnectionManager()