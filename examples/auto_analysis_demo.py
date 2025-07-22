#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TradingAgents 自动化分析演示
演示如何使用自动化分析功能从MySQL数据库读取股票并进行批量分析
"""

import os
import sys
import datetime
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# 加载环境变量
load_dotenv()

console = Console()

def check_mysql_config():
    """检查MySQL配置"""
    console.print(Panel("🔍 检查MySQL数据库配置", style="bold blue"))
    
    config_table = Table(title="MySQL配置检查")
    config_table.add_column("配置项", style="cyan")
    config_table.add_column("值", style="green")
    config_table.add_column("状态", style="yellow")
    
    configs = {
        "MYSQL_HOST": os.getenv('MYSQL_HOST', 'localhost'),
        "MYSQL_PORT": os.getenv('MYSQL_PORT', '3306'),
        "MYSQL_USER": os.getenv('MYSQL_USER', 'root'),
        "MYSQL_PASSWORD": "***" if os.getenv('MYSQL_PASSWORD') else "未设置",
        "MYSQL_DATABASE": os.getenv('MYSQL_DATABASE', 'coredata')
    }
    
    for key, value in configs.items():
        status = "✅ 已配置" if value and value != "未设置" else "❌ 未配置"
        config_table.add_row(key, str(value), status)
    
    console.print(config_table)
    
    # 检查是否所有必需配置都已设置
    missing_configs = []
    if not os.getenv('MYSQL_HOST'):
        missing_configs.append('MYSQL_HOST')
    if not os.getenv('MYSQL_PASSWORD'):
        missing_configs.append('MYSQL_PASSWORD')
    if not os.getenv('MYSQL_DATABASE'):
        missing_configs.append('MYSQL_DATABASE')
    
    if missing_configs:
        console.print(f"\n[red]❌ 缺少必需的配置项: {', '.join(missing_configs)}[/red]")
        console.print("[yellow]💡 请在.env文件中设置这些配置项[/yellow]")
        return False
    
    console.print("\n[green]✅ MySQL配置检查通过[/green]")
    return True

def show_database_setup_guide():
    """显示数据库设置指南"""
    console.print(Panel("📋 数据库设置指南", style="bold green"))
    
    console.print("[bold yellow]1. 创建数据库和表:[/bold yellow]")
    console.print("""
[cyan]-- 创建数据库
CREATE DATABASE IF NOT EXISTS coredata DEFAULT CHARSET=utf8mb4;

-- 使用数据库
USE coredata;

-- 创建rising_stocks表
CREATE TABLE IF NOT EXISTS rising_stocks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(20) NOT NULL COMMENT '股票代码',
    record_date DATE NOT NULL COMMENT '记录日期',
    INDEX idx_code (code),
    INDEX idx_record_date (record_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 插入示例数据（今日日期）
INSERT INTO rising_stocks (code, record_date) VALUES 
('000001', CURDATE()),
('600036', CURDATE()),
('000002', CURDATE()),
('600519', CURDATE()),
('000858', CURDATE());

-- response表会自动创建，无需手动创建[/cyan]
""")
    
    console.print("[bold yellow]2. 配置环境变量:[/bold yellow]")
    console.print("""
[cyan]# 在.env文件中添加以下配置
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=coredata[/cyan]
""")
    
    console.print("[bold yellow]3. 运行自动化分析:[/bold yellow]")
    console.print("""
[cyan]# 方法1: 使用CLI命令
python -m cli.main auto-analysis

# 方法2: 指定最大分析数量
python -m cli.main auto-analysis --max 3

# 方法3: 试运行模式（暂未实现）
python -m cli.main auto-analysis --dry-run[/cyan]
""")

def show_example_usage():
    """显示使用示例"""
    console.print(Panel("🚀 使用示例", style="bold magenta"))
    
    console.print("[bold yellow]直接运行自动化分析:[/bold yellow]")
    console.print("""
[cyan]from cli.auto_analysis import AutoAnalyzer

# 创建分析器（最多分析5只股票）
analyzer = AutoAnalyzer(max_stocks=5)

# 运行分析
analyzer.run_analysis()[/cyan]
""")
    
    console.print("[bold yellow]查看分析结果:[/bold yellow]")
    console.print("""
[cyan]-- 查询今日分析结果
SELECT 
    stock_code,
    action,
    target_price,
    confidence,
    risk_score,
    reasoning,
    analysis_date,
    created_at
FROM response 
WHERE analysis_date = CURDATE()
ORDER BY created_at DESC;[/cyan]
""")

def main():
    """主函数"""
    console.print(Panel(
        "🤖 TradingAgents 自动化分析演示\n\n"
        "本演示将展示如何配置和使用自动化分析功能",
        title="自动化分析演示",
        style="bold blue"
    ))
    
    # 检查MySQL配置
    if not check_mysql_config():
        console.print("\n[red]❌ 配置检查失败，请先完成MySQL配置[/red]")
        show_database_setup_guide()
        return
    
    # 显示使用示例
    show_example_usage()
    
    # 询问是否运行实际分析
    console.print("\n[bold yellow]是否要运行实际的自动化分析？[/bold yellow]")
    console.print("[dim]注意：这将消耗API调用次数并可能产生费用[/dim]")
    
    try:
        choice = input("输入 'y' 或 'yes' 继续，其他任意键退出: ").lower().strip()
        
        if choice in ['y', 'yes']:
            console.print("\n[green]🚀 启动自动化分析...[/green]")
            
            # 导入并运行自动化分析
            try:
                from cli.auto_analysis import AutoAnalyzer
                
                analyzer = AutoAnalyzer(max_stocks=3)  # 演示模式只分析3只股票
                analyzer.run_analysis()
                
            except ImportError as e:
                console.print(f"[red]❌ 导入失败: {e}[/red]")
                console.print("[yellow]💡 请确保已安装pymysql: pip install pymysql[/yellow]")
            except Exception as e:
                console.print(f"[red]❌ 运行失败: {e}[/red]")
        else:
            console.print("\n[yellow]👋 演示结束，感谢使用！[/yellow]")
            
    except KeyboardInterrupt:
        console.print("\n[yellow]👋 用户中断，演示结束[/yellow]")

if __name__ == "__main__":
    main()