import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.responses import HTMLResponse

app = FastAPI()

# 1. 定义资源闸机（电池）
# 限制普通用户并发数为 1
sem = asyncio.Semaphore(1)

# 2. 模拟底层的 AI 推理引擎（水龙头/第一棒）
async def run_inference(user_id: str):
    """模拟 AI 逐字生成结果的过程"""
    yield f"--- [AI 引擎] 开始为用户 {user_id} 生成内容 ---\n"
    words = ["Tesla", "FSD", "V12", "is", "fully", "neural", "network-based."]
    for word in words:
        await asyncio.sleep(1)  # 模拟每 0.5 秒产生一个词
        yield f"{word} "
    yield f"\n--- [AI 引擎] {user_id} 任务完成 ---\n"

# 3. 核心调度器（救护车逻辑/中转站）
# 这里的 current_sem 是外部传进来的插座
async def smart_scheduler(user_id: str, current_sem: asyncio.Semaphore):
    """
    负责判断：你是谁？你该排队还是直接走？
    """
    if user_id == "admin":
        yield "🌟 [调度系统] 识别到管理员身份，启动 VIP 绿色通道，跳过排队！\n"
        # 直接接力数据流，不加 async with sem
        async for chunk in run_inference(user_id):
            yield chunk
    else:
        yield f"⏳ [调度系统] 用户 {user_id} 权限普通，正在进入 GPU 排队队列...\n"
        # 必须占住位置（刷卡进门）
        async with current_sem:
            yield f"✅ [调度系统] 用户 {user_id} 已获取资源，开始推理...\n"
            # 在闸机内部接力数据流，确保占位
            async for chunk in run_inference(user_id):
                yield chunk

# 4. API 路由入口
@app.get("/stream")
async def stream_api(user_id: str = "guest"):
    """
    FastAPI 路由，只负责把全局 sem 传给调度器
    """
    # 这里把全局定义的 sem 像电池一样插进调度器里
    return StreamingResponse(
        smart_scheduler(user_id, sem), 
        media_type="text/plain"
    )

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Tesla AI 推理中心</title>
            <style>
                body { background: #1a1a1a; color: #fff; font-family: sans-serif; padding: 40px; }
                #output { background: #000; padding: 20px; border-radius: 8px; height: 300px; overflow-y: auto; white-space: pre-wrap; border: 1px solid #333; }
                input { padding: 10px; border-radius: 4px; border: none; width: 200px; }
                button { padding: 10px 20px; background: #cc0000; color: white; border: none; border-radius: 4px; cursor: pointer; }
                .status { margin-bottom: 10px; color: #888; }
            </style>
        </head>
        <body>
            <h1>🚀 Tesla 边缘计算节点</h1>
            <div class="status">请输入 User ID (输入 admin 开启 VIP 通道)</div>
            <input type="text" id="userId" value="guest">
            <button onclick="startInference()">开始推理</button>
            <hr style="border: 0.5px solid #333; margin: 20px 0;">
            <div id="output">等待指令...</div>

            <script>
                async function startInference() {
                    const userId = document.getElementById('userId').value;
                    const outputDiv = document.getElementById('output');
                    outputDiv.innerText = "正在连接服务器...\n";

                    // 1. 发起流式请求
                    const response = await fetch(`/stream?user_id=${userId}`);
                    const reader = response.body.getReader();
                    const decoder = new TextDecoder();

                    // 2. 循环读取流数据
                    while (true) {
                        const { value, done } = await reader.read();
                        if (done) break;
                        
                        // 将读取到的二进制块转为文字并显示
                        const chunk = decoder.decode(value);
                        outputDiv.innerText += chunk;
                        outputDiv.scrollTop = outputDiv.scrollHeight; // 自动滚动到底部
                    }
                }
            </script>
        </body>
    </html>
    """


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
