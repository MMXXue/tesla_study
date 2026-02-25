import asyncio
from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse, HTMLResponse
import uvicorn

app = FastAPI()

# --- 全局状态管理 ---
# Key: user_id, Value: list of prompts
user_sessions = {}

# 限制普通用户的全局并发数为 1
sem = asyncio.Semaphore(1)

# --- 核心业务逻辑 ---

async def run_inference(user_id: str, history: list):
    """
    模拟 AI 推理引擎。
    history 包含了当前用户最近的对话记录。
    """
    yield f"--- [AI 引擎] 正在调取用户 {user_id} 的记忆 ---\n"
    
    # 1. 回顾历史（不含本次输入）
    if len(history) > 1:
        yield "📜 历史记录回顾：\n"
        for i, msg in enumerate(history[:-1], 1):
            await asyncio.sleep(0.1)  # 稍微快一点的仪式感
            yield f"  {i}. {msg}\n"
        yield "--------------------\n"
    else:
        yield "🆕 首次对话，暂无历史记忆。\n"
    
    # 2. 处理当前问题
    current_prompt = history[-1]
    yield f"✨ 针对新问题 '{current_prompt}'，正在思考：\n"

    words = ["正在", "检索", "知识库", "进行", "逻辑推理...", "生成回答", "完成！"]
    for word in words:
        await asyncio.sleep(0.4) 
        yield f"{word} "
    yield f"\n--- [AI 引擎] 任务完成 ---\n"

async def smart_scheduler(user_id: str, prompt: str):
    """
    核心调度器：处理排队逻辑与记忆登记
    """
    is_admin = (user_id == "admin")

    # 1. 身份预告
    if is_admin:
        yield "🌟 [调度系统] 识别到管理员 VIP 身份，跳过排队...\n"
    else:
        yield f"⏳ [调度系统] 用户 {user_id} 权限普通，正在进入队列...\n"

    # 2. 流量控制逻辑
    # 使用 contextlib 的思想简化逻辑
    if is_admin:
        # VIP 直接进入推理
        async for chunk in _process_request(user_id, prompt):
            yield chunk
    else:
        # 普通用户竞争信号量
        async with sem:
            yield f"✅ [调度系统] 用户 {user_id} 已获取 GPU 资源，开始执行...\n"
            async for chunk in _process_request(user_id, prompt):
                yield chunk

async def _process_request(user_id: str, prompt: str):
    """
    内部方法：负责真正的记忆更新和调用引擎
    """
    # 初始化 session
    if user_id not in user_sessions:
        user_sessions[user_id] = []
    
    # 登记记忆
    user_sessions[user_id].append(prompt)
    
    # 限制长度（保留最近 5 条）
    if len(user_sessions[user_id]) > 5:
        user_sessions[user_id] = user_sessions[user_id][-5:]
    
    # 调用推理引擎
    async for chunk in run_inference(user_id, user_sessions[user_id]):
        yield chunk

# --- API 路由 ---

@app.get("/stream")
async def stream_api(user_id: str = "guest", prompt: str = "Hello"):
    # 传入调度器生成流
    return StreamingResponse(
        smart_scheduler(user_id, prompt), 
        media_type="text/event-stream"
    )

@app.get("/clear")
async def clear_memory(user_id: str):
    if user_id in user_sessions:
        user_sessions[user_id] = []
    return {"status": "success", "message": f"用户 {user_id} 的记忆已清空"}

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="UTF-8">
            <title>Tesla AI 推理中心</title>
            <style>
                body { background: #0f0f0f; color: #e0e0e0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 40px; }
                .container { max-width: 800px; margin: 0 auto; }
                #output { background: #000; padding: 20px; border-radius: 8px; height: 400px; overflow-y: auto; 
                          white-space: pre-wrap; border: 1px solid #333; font-family: monospace; line-height: 1.6; }
                .controls { margin-bottom: 20px; display: flex; gap: 10px; }
                input { padding: 12px; border-radius: 4px; border: 1px solid #444; background: #222; color: #fff; flex: 1; }
                #userId { flex: 0 0 100px; }
                button { padding: 10px 20px; background: #cc0000; color: white; border: none; border-radius: 4px; cursor: pointer; transition: 0.3s; }
                button:disabled { background: #555; cursor: not-allowed; }
                button:hover:not(:disabled) { background: #ff0000; }
                .status-bar { font-size: 0.8em; color: #888; margin-bottom: 5px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Tesla 边缘计算节点</h1>
                <div class="status-bar">提示: 使用 'admin' 作为 User ID 可享受 VIP 通道</div>
                <div class="controls">
                    <input type="text" id="userId" placeholder="User ID" value="guest">
                    <input type="text" id="userPrompt" placeholder="输入您的问题 (回车发送)">
                    <button id="sendBtn" onclick="startInference()">开始推理</button>
                    <button onclick="clearMemory()" style="background: #444;">清空记忆</button>
                </div>
                <div id="output">等待指令...</div>
            </div>

            <script>
                // 支持回车发送
                document.getElementById('userPrompt').addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') startInference();
                });

                async function startInference() {
                    const userId = document.getElementById('userId').value;
                    const promptInput = document.getElementById('userPrompt');
                    const sendBtn = document.getElementById('sendBtn');
                    const outputDiv = document.getElementById('output');
                    
                    const prompt = promptInput.value.trim();
                    if (!prompt) return;

                    // 状态锁定
                    promptInput.value = "";
                    sendBtn.disabled = true;
                    outputDiv.innerHTML += `<div style="color: #00ff00; margin-top: 10px;">> ${prompt}</div>`;

                    try {
                        const response = await fetch(`/stream?user_id=${userId}&prompt=${encodeURIComponent(prompt)}`);
                        const reader = response.body.getReader();
                        const decoder = new TextDecoder();

                        while (true) {
                            const { value, done } = await reader.read();
                            if (done) break;
                            const chunk = decoder.decode(value);
                            outputDiv.innerText += chunk;
                            outputDiv.scrollTop = outputDiv.scrollHeight; 
                        }
                    } catch (e) {
                        outputDiv.innerText += `\n❌ 发生错误: ${e.message}`;
                    } finally {
                        sendBtn.disabled = false;
                        promptInput.focus();
                    }
                }

                async function clearMemory() {
                    const userId = document.getElementById('userId').value;
                    const response = await fetch(`/clear?user_id=${userId}`);
                    const result = await response.json();
                    document.getElementById('output').innerText = `✨ 系统提示: ${result.message}\\n` + "-".repeat(20) + "\\n";
                }
            </script>
        </body>
    </html>
    """

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)