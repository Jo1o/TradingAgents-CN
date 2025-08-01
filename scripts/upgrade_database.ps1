# 数据库升级脚本 - 添加新闻分析师和情绪分析师字段
# PowerShell脚本用于Windows环境

Write-Host "=== TradingAgents-CN 数据库升级脚本 ===" -ForegroundColor Green
Write-Host "此脚本将为response表添加新闻分析师和情绪分析师字段" -ForegroundColor Yellow
Write-Host ""

# 检查MySQL是否安装
$mysqlPath = Get-Command mysql -ErrorAction SilentlyContinue
if (-not $mysqlPath) {
    Write-Host "❌ 未找到MySQL命令行工具，请确保MySQL已安装并添加到PATH" -ForegroundColor Red
    Write-Host "   下载地址: https://dev.mysql.com/downloads/mysql/" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ 找到MySQL: $($mysqlPath.Source)" -ForegroundColor Green

# 获取数据库连接信息
$host = Read-Host "请输入MySQL主机地址 [默认: localhost]"
if ([string]::IsNullOrEmpty($host)) { $host = "localhost" }

$port = Read-Host "请输入MySQL端口 [默认: 3306]"
if ([string]::IsNullOrEmpty($port)) { $port = "3306" }

$username = Read-Host "请输入MySQL用户名 [默认: root]"
if ([string]::IsNullOrEmpty($username)) { $username = "root" }

$password = Read-Host "请输入MySQL密码" -AsSecureString
$passwordText = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($password))

Write-Host ""
Write-Host "连接信息:" -ForegroundColor Cyan
Write-Host "  主机: $host" -ForegroundColor White
Write-Host "  端口: $port" -ForegroundColor White
Write-Host "  用户: $username" -ForegroundColor White
Write-Host ""

# 确认执行
$confirm = Read-Host "是否继续执行数据库升级? [y/N]"
if ($confirm -ne 'y' -and $confirm -ne 'Y') {
    Write-Host "❌ 用户取消操作" -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "🔄 开始执行数据库升级..." -ForegroundColor Yellow

# 执行升级脚本
$scriptPath = Join-Path $PSScriptRoot "upgrade_response_table.sql"
if (-not (Test-Path $scriptPath)) {
    Write-Host "❌ 未找到升级脚本文件: $scriptPath" -ForegroundColor Red
    exit 1
}

try {
    # 执行SQL脚本
    $mysqlCmd = "mysql -h$host -P$port -u$username -p$passwordText < `"$scriptPath`""
    Invoke-Expression $mysqlCmd
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ 数据库升级成功完成!" -ForegroundColor Green
        Write-Host "   已为response表添加以下字段:" -ForegroundColor White
        Write-Host "   - news_analysis: 新闻分析师结果" -ForegroundColor White
        Write-Host "   - sentiment_analysis: 情绪分析师结果" -ForegroundColor White
        Write-Host ""
        Write-Host "📝 现在可以重新运行自动分析，新字段将自动填充分析结果" -ForegroundColor Cyan
    } else {
        Write-Host "❌ 数据库升级失败，请检查错误信息" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ 执行过程中发生错误: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "按任意键退出..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")