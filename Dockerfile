# 使用较小的基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制当前目录内容到工作目录
COPY . /app

# 安装依赖
RUN pip install --upgrade pip
RUN pip install --no-cache-dir Flask requests

# 设置环境变量
ENV FLASK_APP=app.py

# 暴露端口
EXPOSE 5000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 CMD curl -f http://localhost:5000/health || exit 1

# 运行Flask应用
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]