import uuid
from fastapi import FastAPI, Request
from structlog.contextvars import bind_contextvars
from day23_logger import log

app = FastAPI()

# 所有访问你 API 的请求，在到达你的业务代码（比如 root 函数）之前，必须先经过这个安检口
@app.middleware("http")
async def add_trace_id_middleware(request: Request, call_next):
    # 为当前请求生成唯一的 Trace ID
    trace_id = str(uuid.uuid4())

    # 将 trace_id 绑定到当前协程上下文
    # 一次绑定，处处生效. “给你戴上“隐形手环”的动作”   别人只需要log.info()就可以知道你是谁了
    bind_contextvars(trace_id=trace_id)
    
    # call_next 的意思其实是：“去运行用户真正想访问的那个函数，不管它是谁。”
    response = await call_next(request)
    
    # 也可以在响应头中返回 trace_id，方便前端排查问题
    response.headers["X-Trace-ID"] = trace_id
    return response

@app.get("/")
async def root():
    log.info("processing_request", action="greet", user="Sheldon")
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)