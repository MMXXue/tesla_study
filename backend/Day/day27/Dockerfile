# --- 第一阶段：构建 (Builder) ---
# 这一层包含了所有开发工具（编译器等），但它们最后会被丢弃
FROM python:3.10-slim AS builder

# 设置工作目录
WORKDIR /build

# 1. 拷贝你刚生成的依赖清单
COPY requirements.txt .

# 2. 安装依赖到本地用户的目录下
# --no-cache-dir 告诉 Docker 不要保存下载包的缓存，进一步省空间
RUN pip install --user --no-cache-dir -r requirements.txt


# --- 第二阶段：运行 (Final) ---
# 这一层只包含运行程序所必需的“干净”环境
FROM python:3.10-slim

WORKDIR /app

# 3. 【核心优化】从 builder 阶段只拷贝安装好的“家具”（库），不拿“梯子”（工具）
COPY --from=builder /root/.local /root/.local

# 4. 拷贝你 day27 文件夹下的所有代码
COPY . .

# 5. 配置环境变量，确保系统能找到刚才拷贝过来的库
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# 6. 启动程序 (假设你的主程序是 main.py，如果没有，请改成你实际的文件名)
CMD ["python", "main.py"]