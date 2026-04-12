# 1. 使用轻量级的 Python 镜像，像特斯拉车载系统一样精简
FROM python:3.12-slim

# 2. 设置工作目录
WORKDIR /app

# 3. 先复制清单并安装，利用 Docker 缓存加速
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 复制当前文件夹下的所有代码
COPY . .

# 5. 关键：创建一个空的 log 文件，防止权限问题
RUN touch app.log && chmod 666 app.log

# 6. 暴露 FastAPI 的端口
EXPOSE 8000

# 7. 启动指令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


