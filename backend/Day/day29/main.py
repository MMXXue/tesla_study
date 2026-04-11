from fastapi import FastAPI
from pydantic import BaseModel, Field

# 1. 这里的 title 和 description 就是 SDK 的封面
app = FastAPI(
    title="Tesla TS-79 Diagnostic API",
    description="自动生成的车辆诊断服务接口，支持全栈 SDK 自动化集成。",
    version="1.0.0"
)

# 2. 定义【输入模型】：SDK 会根据这个自动生成前端的 Interface/Type
class DiagnosticTask(BaseModel):
    vin: str = Field(..., min_length=17, max_length=17, description="车辆17位唯一识别码", example="5YJ3E1EB...")
    fault_code: str = Field(..., description="传感器捕获的故障码", example="BMS_a066")

# 3. 定义【输出模型】：让前端知道返回的数据长什么样
class DiagnosticResult(BaseModel):
    is_critical: bool = Field(..., description="是否属于致命故障")
    suggestion: str = Field(..., description="AI 给出的维修建议")

@app.post("/v1/analyze", response_model=DiagnosticResult, tags=["diagnosis"])
async def analyze_vehicle(task: DiagnosticTask):
    """
    接收车辆数据，通过 DeepSeek 模型进行自动化故障分析
    """
    # 模拟 AI 逻辑
    return {
        "is_critical": True,
        "suggestion": "检测到电池包温度异常，请立即停车并联系服务中心。"
    }

# http://127.0.0.1:8000/openapi.json