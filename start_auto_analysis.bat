@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo TradingAgents 自动化分析启动器
echo ========================================
echo.

REM 检查Python是否可用
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python，请确保Python已安装并添加到PATH
    echo 💡 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python环境检查通过
echo.

REM 检查虚拟环境
if exist ".venv\Scripts\activate.bat" (
    echo 🔄 激活虚拟环境...
    call .venv\Scripts\activate.bat
    echo ✅ 虚拟环境已激活
) else (
    echo ⚠️ 未找到虚拟环境，使用系统Python
)
echo.

REM 检查依赖
echo 🔍 检查依赖包...
python -c "import pymysql" >nul 2>&1
if errorlevel 1 (
    echo ❌ 缺少pymysql依赖
    echo 🔄 正在安装依赖...
    pip install pymysql
    if errorlevel 1 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
)
echo ✅ 依赖检查通过
echo.

REM 运行自动化分析
echo 🚀 启动自动化分析...
echo.
python start_auto_analysis.py

echo.
echo ========================================
echo 程序执行完成
echo ========================================
pause