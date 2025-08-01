#!/bin/bash
# 数据库升级脚本 - 添加新闻分析师和情绪分析师字段
# Shell脚本用于Linux/macOS环境

echo "=== TradingAgents-CN 数据库升级脚本 ==="
echo "此脚本将为response表添加新闻分析师和情绪分析师字段"
echo ""

# 检查MySQL是否安装
if ! command -v mysql &> /dev/null; then
    echo "❌ 未找到MySQL命令行工具，请确保MySQL已安装并添加到PATH"
    echo "   Ubuntu/Debian: sudo apt-get install mysql-client"
    echo "   CentOS/RHEL: sudo yum install mysql"
    echo "   macOS: brew install mysql-client"
    exit 1
fi

echo "✅ 找到MySQL: $(which mysql)"

# 获取数据库连接信息
read -p "请输入MySQL主机地址 [默认: localhost]: " host
host=${host:-localhost}

read -p "请输入MySQL端口 [默认: 3306]: " port
port=${port:-3306}

read -p "请输入MySQL用户名 [默认: root]: " username
username=${username:-root}

read -s -p "请输入MySQL密码: " password
echo ""
echo ""

echo "连接信息:"
echo "  主机: $host"
echo "  端口: $port"
echo "  用户: $username"
echo ""

# 确认执行
read -p "是否继续执行数据库升级? [y/N]: " confirm
if [[ $confirm != [yY] ]]; then
    echo "❌ 用户取消操作"
    exit 0
fi

echo ""
echo "🔄 开始执行数据库升级..."

# 获取脚本目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
SQL_FILE="$SCRIPT_DIR/upgrade_response_table.sql"

if [[ ! -f "$SQL_FILE" ]]; then
    echo "❌ 未找到升级脚本文件: $SQL_FILE"
    exit 1
fi

# 执行升级脚本
if mysql -h"$host" -P"$port" -u"$username" -p"$password" < "$SQL_FILE"; then
    echo ""
    echo "✅ 数据库升级成功完成!"
    echo "   已为response表添加以下字段:"
    echo "   - news_analysis: 新闻分析师结果"
    echo "   - sentiment_analysis: 情绪分析师结果"
    echo ""
    echo "📝 现在可以重新运行自动分析，新字段将自动填充分析结果"
else
    echo "❌ 数据库升级失败，请检查错误信息"
    exit 1
fi

echo ""
echo "升级完成，按回车键退出..."
read