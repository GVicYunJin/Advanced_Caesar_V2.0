# 使用官方 Python 镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt /app/

# 安装依赖
RUN pip install -r requirements.txt

# 复制应用程序代码
COPY . /app/

# 设置 Flask 端口和环境变量
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=3333

# 启动 Flask 应用
CMD ["flask", "run"]
