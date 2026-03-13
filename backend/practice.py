# import asyncio
# from fastapi import FastAPI
# from fastapi import HTTPException
# from fastapi.responses import StreamingResponse
# from fastapi.responses import HTMLResponse

# async def run_inference(role : str):
#     yield f"---❇️ 正在为{role}生成中---"
#     words = ["I", "wanna", "to", "be", "a", "good", "one!"]
#     for word in words:
#         await asyncio.sleep(1)
#         yield f"{word}\n"
#     yield f"---✅ {role}的任务已经完成---"

# sem = asyncio.Semaphore(1)

# async def smart_scheduler(role : str, current_sem : asyncio.Semaphore):
#     if role == "user":
#         yield f"检测到{role}, 正在准备进入队伍中..."
#         async with current_sem:
#             yield f"📶 {role}正在准备进行推理中..."
#             async for chunk in run_inference(role):
#                 yield(chunk)

#     elif role == "admin":
#         yield f"检测到{role}, 启用绿色通道中...."
#         async for chunk in run_inference(role):
#             yield(chunk)

# app = FastAPI()

# @app.get("/stream")
# async def stream_api(role : str = "user"):
#     if role not in {"user", "admin"}:
#         raise HTTPException(status_code=400, detail="❌ role出现错误! 仅支持 user/admin")
#     return StreamingResponse(smart_scheduler(role, sem), media_type="text/plain; charset=utf-8")

# @app.get("/", response_class = HTMLResponse)
# async def index():
#     return """
#     <!DOCTYPE html>
#     <html>
#         <head>
#             <title>Tesla HTMLResponse test page</title>
#         </head>
#         <body>
#             <h1>🚀 Tesla 边缘计算节点</h1>
#             <div class="status">请输入 User ID (输入 admin 开启 VIP 通道)</div>
#             <input type="text" id="role" value="user">
#             <button onclick="startInference()">开始推理</button>
#             <div id="output">等待指令...</div>

#             <script>
#                 async function startInference(){
#                     const role = document.getElementById('role').value;
#                     const outputDiv = document.getElementById('output');
#                     outputDiv.innerText = "正在连接服务器...\n";

#                     const response = await fetch(`/stream?role=${encodeURIComponent(role)}`);
#                     const reader = response.body.getReader();
#                     const decoder = new TextDecoder();

#                     while (true) {
#                         const { value, done } = await reader.read();
#                         if (done) break;
                        
#                         // 将读取到的二进制块转为文字并显示
#                         const chunk = decoder.decode(value);
#                         outputDiv.innerText += chunk;
#                         outputDiv.scrollTop = outputDiv.scrollHeight; // 自动滚动到底部
#                     }
#                 }
#             </script>
#         </body>
#     </html>
#     """

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)