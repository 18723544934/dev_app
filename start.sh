#!/bin/bash

# 今天吃啥 - 快速启动脚本

echo "==================================="
echo "  今天吃啥 - 快速启动"
echo "==================================="
echo ""

# 检查后端依赖
if [ ! -d "backend/venv" ]; then
    echo "📦 安装后端依赖..."
    cd backend
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
fi

# 检查环境配置
if [ ! -f "backend/.env" ]; then
    echo "⚙️  创建环境配置文件..."
    cp backend/.env.example backend/.env
    echo "⚠️  请编辑 backend/.env 文件，配置数据库和高德地图API Key"
    echo ""
fi

# 启动后端服务
echo "🚀 启动后端服务..."
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

echo ""
echo "✅ 后端服务已启动: http://localhost:8000"
echo "📚 API文档: http://localhost:8000/docs"
echo ""
echo "📱 请在另一个终端启动Flutter应用:"
echo "   cd frontend && flutter run"
echo ""
echo "按 Ctrl+C 停止服务"

# 等待后端服务
wait $BACKEND_PID
