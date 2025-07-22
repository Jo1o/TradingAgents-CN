#!/usr/bin/env pwsh
# TradingAgents 自动化分析启动器 (PowerShell版本)

# 设置控制台编码为UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 颜色函数
function Write-ColorText {
    param(
        [string]$Text,
        [string]$Color = "White"
    )
    Write-Host $Text -ForegroundColor $Color
}

function Write-Success { param([string]$Text) Write-ColorText "✅ $Text" "Green" }
function Write-Error { param([string]$Text) Write-ColorText "❌ $Text" "Red" }
function Write-Warning { param([string]$Text) Write-ColorText "⚠️ $Text" "Yellow" }
function Write-Info { param([string]$Text) Write-ColorText "🔄 $Text" "Cyan" }

# 主函数
function Start-AutoAnalysis {
    Write-ColorText "========================================" "Blue"
    Write-ColorText "TradingAgents 自动化分析启动器" "Blue"
    Write-ColorText "========================================" "Blue"
    Write-Host ""
    
    # 切换到脚本目录
    $ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    Set-Location $ScriptDir
    Write-Info "工作目录: $ScriptDir"
    Write-Host ""
    
    # 检查Python
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Python环境检查通过: $pythonVersion"
        } else {
            throw "Python未找到"
        }
    } catch {
        Write-Error "未找到Python，请确保Python已安装并添加到PATH"
        Write-Warning "下载地址: https://www.python.org/downloads/"
        Read-Host "按任意键退出"
        return
    }
    
    # 检查并激活虚拟环境
    if (Test-Path ".venv\Scripts\Activate.ps1") {
        Write-Info "激活虚拟环境..."
        try {
            & ".venv\Scripts\Activate.ps1"
            Write-Success "虚拟环境已激活"
        } catch {
            Write-Warning "虚拟环境激活失败，使用系统Python"
        }
    } elseif (Test-Path ".venv\Scripts\activate.bat") {
        Write-Info "激活虚拟环境 (批处理模式)..."
        cmd /c ".venv\Scripts\activate.bat && echo 虚拟环境已激活"
    } else {
        Write-Warning "未找到虚拟环境，使用系统Python"
    }
    Write-Host ""
    
    # 检查依赖
    Write-Info "检查依赖包..."
    try {
        python -c "import pymysql" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Success "依赖检查通过"
        } else {
            throw "pymysql未安装"
        }
    } catch {
        Write-Warning "缺少pymysql依赖"
        Write-Info "正在安装依赖..."
        
        try {
            pip install pymysql
            if ($LASTEXITCODE -eq 0) {
                Write-Success "依赖安装成功"
            } else {
                throw "依赖安装失败"
            }
        } catch {
            Write-Error "依赖安装失败，请手动执行: pip install pymysql"
            Read-Host "按任意键退出"
            return
        }
    }
    Write-Host ""
    
    # 检查配置文件
    if (Test-Path ".env") {
        Write-Success "找到配置文件 .env"
    } else {
        Write-Warning "未找到 .env 配置文件"
        Write-Info "请参考 .env.example 创建配置文件"
    }
    Write-Host ""
    
    # 运行自动化分析
    Write-Info "启动自动化分析..."
    Write-Host ""
    
    try {
        python start_auto_analysis.py
        Write-Host ""
        Write-Success "程序执行完成"
    } catch {
        Write-Host ""
        Write-Error "程序执行失败: $_"
        Write-Info "请检查日志文件获取详细错误信息"
    }
    
    Write-Host ""
    Write-ColorText "========================================" "Blue"
    Write-ColorText "程序执行完成" "Blue"
    Write-ColorText "========================================" "Blue"
    
    # 等待用户输入
    Read-Host "按任意键退出"
}

# 错误处理
trap {
    Write-Error "发生未处理的错误: $_"
    Read-Host "按任意键退出"
}

# 执行主函数
Start-AutoAnalysis