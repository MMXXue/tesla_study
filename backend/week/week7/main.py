# main.py
import asyncio
import json
import random
import time
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import redis.asyncio as aioredis  # 引入 Month 1 强调的异步 Redis 驱动

app = FastAPI(
    title="TS-79 Real-time Diagnostic Full-Stack Engine",
    description="对标 Tesla 生产级标准：集成 Redis 分布式限流与全双工任务控制"
)

# 允许跨域：确保 Next.js 前端（通常在 3000 端口）能够跨域建立 WebSocket 长连接
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====================================================================
# 🔌 数据库连接池调优 (温故 Month 1 - Day 11 Connection Pooling)
# ====================================================================
# 连接到你刚刚用 Docker 拉起的 ts79-redis-limiter（宿主机暴露端口为 6379）
REDIS_URL = "redis://localhost:6379/0"
redis_pool = aioredis.ConnectionPool.from_url(
    REDIS_URL, 
    max_connections=10,        # 限制最大连接数，防止高并发下耗尽内存
    decode_responses=True      # 自动将 Redis 返回的 bytes 转换为 string，方便处理
)
redis_client = aioredis.Redis(connection_pool=redis_pool)


# ====================================================================
# 🔍 分布式流量治理 (温故 Month 1 - Day 21 Rate Limiting)
# ====================================================================
async def is_rate_limited(user_id: str, limit: int = 4, window: int = 10) -> bool:
    """
    基于 Redis 计数器实现分布式滑动窗口/固定窗口限流
    策略：限制单个虚拟车辆节点（user_id）在 window（10秒）内，最多只能发送 limit（4次）控制指令
    """
    key = f"rate_limit:diagnostics:{user_id}"
    try:
        # INCR 是原子性操作，天然防止并发冲突
        current_requests = await redis_client.incr(key)
        
        if current_requests == 1:
            # 第一次请求时，必须为该 key 设置过期时间（即窗口大小）
            await redis_client.expire(key, window)
        
        if current_requests > limit:
            return True  # 触发限流
        return False     # 放行
    except Exception as e:
        # 弹性韧性设计 (温故 Day 20): 数据库异常时的降级预案，防止因为 Redis 波动导致整个监控瘫痪
        print(f"[⚠️ LOG RECOVERY] Redis 限流器通信异常: {e}. 自动启用降级放行策略。")
        return False


# ====================================================================
# ⚙️ 核心全双工异步任务生成器 (温故 Month 2 - Day 45~50)
# ====================================================================

async def telemetry_generator(websocket: WebSocket):
    """
    [高频遥测流] 模拟工业车机以 10Hz (每秒10次) 的高频，源源不断推送传感器硬件指标。
    这是前端 ECharts 动态滚动图表（60FPS）的数据源。
    """
    try:
        while True:
            payload = {  # 数据载荷
                "type": "telemetry",  # 告诉前端：这是“遥测数据”，不是“AI说的话”
                "data": {
                    # 模拟 CPU 在 60% 左右上下波动（最低不低于10%，最高不超过95%）
                    "cpu": max(10, min(95, 60 + random.randint(-8, 8))),
                    # 模拟内存占用在 70.0% 到 76.5% 之间随机摇摆
                    "memory": round(random.uniform(70.0, 76.5), 1),
                    # 模拟网络延迟在 10ms 到 30ms 之间跳动
                    "latency": random.randint(10, 30)
                }
            }
            await websocket.send_text(json.dumps(payload)) # 🌟 啪，发一颗炮弹给前端
            await asyncio.sleep(0.1)  # 🌟 严格休息 100 毫秒（0.1 秒） 10HZ的采样率
    except asyncio.CancelledError:
        # 优雅停机 (温故 Day 24 Profiling & Day 30)
        print("[✓ BACKEND] 遥测数据流协程已被安全 cancel，未发生内存泄漏。")
        raise

async def ai_diagnostic_engine(websocket: WebSocket, prompt: str):
    """
    [AI 诊断打字机] 模拟底层大模型（如 DeepSeek）实时解析指令，并流式输出极客感诊断报告。
    """
    try:
        steps = [
            f"\n[🚀 START] 成功捕获外部控制原语: '{prompt}'\n",
            "[🛠️ STAGE 1] 正在调取全链路网络拓扑结构...\n",
            "[📡 STAGE 2] 分布式限流状态校验成功，正在将指令挂载至全双工双向管道...\n",
            "[⚠️ WARN] 检测到底层缓存命中率小幅震荡，建议检查 Day 13 实现的 Redis Cache-Aside 策略。\n",
            "[💡 SUGGEST] 系统整体韧性指标极高。终端保持持续监听。\n",
            "[🏁 DONE] 诊断事务安全提交。\n"
        ]
        for step in steps:
            for char in step:
                await websocket.send_text(json.dumps({"type": "ai_text", "data": char}))
                await asyncio.sleep(0.01)  # 10ms 极速吐字
            await asyncio.sleep(0.3)       # 段落停顿体感
    except asyncio.CancelledError:
        print(f"[-] 任务取消：旧的 AI 诊断任务已被强行熔断。指令: {prompt}")
        raise


# ====================================================================
# 📡 WebSockets 路由入口 (温故 Month 1 - Day 19 WebSocket 状态机)
# ====================================================================

# 流 A（自动连发）：由 telemetry_generator 掌管，像心跳一样，每秒钟雷打不动地往管道里砸 10 次硬件遥测指标（CPU、内存）。

# 流 B（突发事件）：由 ai_diagnostic_engine 掌管，平时闭嘴，一旦被触发，就以 10ms 一个字的速度在同一条管道里疯狂倾泄 AI 诊断报告。


@app.websocket("/ws/diagnostics")
async def diagnostics_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("[+ SYSTEM] 成功握手：一条全新的全双工车载诊断通道已开启。")

    # 模拟从长连接握手中提取的用户或物理设备唯一识别码（例如 Tesla 车辆的 VIN 码）
    mock_vin_code = "TESLA_MODEL_Y_2026_MOCK"

    # 1. 异步并行启动：背景高频遥测任务
    telemetry_task = asyncio.create_task(telemetry_generator(websocket))
    
    # 用于动态追踪并控制当前连接内部正在运行的 AI 打字机任务
    current_ai_task = None

    try:
        while True:
            # 持续监听前端随时可能上报的异步控制原语
            raw_client_data = await websocket.receive_text()
            client_data = json.loads(raw_client_data)
            user_prompt = client_data.get("prompt", "")    #  通过 json.loads 解包，提取出用户的真实意图 user_prompt

            # 节点 A：调用分布式 Redis 限流器
            if await is_rate_limited(user_id=mock_vin_code, limit=4, window=10):
                await websocket.send_text(json.dumps({
                    "type": "system_status",
                    "data": "\n[🚨 REDIS LIMIT] 触发全局分布式限流保护！10秒内同一个 VIN 码最多执行 4 次诊断。\n"
                }))
                continue

            # 节点 B：全双工抢占式中断控制 (温故 Day 24 协程调度)
            if current_ai_task and not current_ai_task.done():
                current_ai_task.cancel()  # 强行杀死正在吐字的旧协程
                await websocket.send_text(json.dumps({
                    "type": "system_status",
                    "data": "\n[⚡ INTERRUPT] 监测到高优先级指令强行霸占通道，旧诊断已被熔断丢弃。\n"
                }))
                try:
                    await current_ai_task  # 等待旧协程抛出 CancelledError 闭环
                except asyncio.CancelledError:
                    pass

            # 节点 C：产生新的诊断任务
            current_ai_task = asyncio.create_task(ai_diagnostic_engine(websocket, user_prompt))

    except WebSocketDisconnect:
        print("[- SYSTEM] 客户端断开连接，长连接生命周期结束。")
    finally:
        # ====================================================================
        # 🛡️ 生产级垃圾回收 (温故 Day 30 Release Engineering)
        # ====================================================================
        print("[* SYSTEM] 正在强制回收长连接所持有的全部后台协程，防止内存泄漏...")
        telemetry_task.cancel()
        if current_ai_task:
            current_ai_task.cancel()
            
        # 并发等待所有残余协程彻底退出销毁
        await asyncio.gather(telemetry_task, return_exceptions=True)
        if current_ai_task:
            await asyncio.gather(current_ai_task, return_exceptions=True)
        print("[✓ SYSTEM] 协程清理完毕，系统硬件资源安全复位。")