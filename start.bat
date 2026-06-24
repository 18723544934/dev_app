@echo off
chcp 65001 >nul
echo ===================================
echo   今天吃啥 - 快速启动
echo ===================================
echo.

REM 检查后端依赖
if not exist "backend\venv" (
    echo 📦 安装后端依赖...
    cd backend
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
    cd ..
)

REM 检查环境配置
if not exist "backend\.env" (
    echo ⚙️  创建环境配置文件...
    copy backend\.env.example backend\.env
    echo ⚠️  请编辑 backend\.env 文件，配置数据库和高德地图API Key
    echo.
)

REM 启动后端服务
echo 🚀 启动后端服务...
cd backend
call venv\Scripts\activate.bat
start "后端服务" cmd /k "uvicorn main:app --reload --host 0.0.0.0 --port 8000"
cd ..

echo.
echo ✅ 后端服务已启动: http://localhost:8000
echo 📚 API文档: http://localhost:8000/docs
echo.
echo 📱 请在另一个终端启动Flutter应用:
echo    cd frontend ^&^& flutter run
echo.
echo 按任意键退出...
pause >nul
