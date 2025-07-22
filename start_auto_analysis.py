#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TradingAgents 自动化分析快速启动脚本
快速启动自动化分析功能，无需复杂的命令行参数
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 加载环境变量
from dotenv import load_dotenv
load_dotenv()

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt

console = Console()

def main():
    """主函数"""
    console.print(Panel(
        "🚀 TradingAgents 自动化分析快速启动\n\n"
        "本脚本将帮助您快速启动自动化分析功能\n"
        "从MySQL数据库读取股票代码并进行智能分析",
        title="自动化分析快速启动",
        style="bold blue"
    ))
    
    # 检查基本配置
    console.print("\n[yellow]📋 检查配置...[/yellow]")
    
    # 检查环境变量
    mysql_host = os.getenv('MYSQL_HOST')
    mysql_password = os.getenv('MYSQL_PASSWORD')
    mysql_database = os.getenv('MYSQL_DATABASE')
    
    if not all([mysql_host, mysql_password, mysql_database]):
        console.print("[red]❌ MySQL配置不完整[/red]")
        console.print("[yellow]💡 请在.env文件中配置以下变量:[/yellow]")
        console.print("   MYSQL_HOST=localhost")
        console.print("   MYSQL_PASSWORD=your_password")
        console.print("   MYSQL_DATABASE=coredata")
        console.print("\n[cyan]📖 详细配置指南请查看: docs/guides/auto-analysis-guide.md[/cyan]")
        return
    
    console.print("[green]✅ MySQL配置检查通过[/green]")
    
    # 询问分析参数
    try:
        max_workers = IntPrompt.ask(
            "[cyan]请输入并发分析线程数量[/cyan]",
            default=4,
            show_default=True
        )
        
        if max_workers <= 0 or max_workers > 4:
            console.print("[yellow]⚠️ 并发数量限制为1-4之间，已调整为4[/yellow]")
            max_workers = 4
        
        # 确认执行
        console.print(f"\n[bold]📊 分析配置:[/bold]")
        console.print(f"   并发线程数: {max_workers}")
        console.print(f"   数据库: {mysql_host}/{mysql_database}")
        console.print(f"   [green]✨ 将分析所有可用股票（无数量限制）[/green]")
        console.print(f"\n[yellow]⚠️ 注意: 分析过程将消耗LLM API调用次数[/yellow]")
        
        if not Confirm.ask("\n[bold cyan]确认开始自动化分析吗？[/bold cyan]"):
            console.print("[yellow]👋 已取消分析[/yellow]")
            return
        
        # 启动分析
        console.print("\n[green]🚀 启动自动化分析...[/green]")
        
        try:
            from cli.auto_analysis import AutoAnalyzer
            
            analyzer = AutoAnalyzer(max_workers=max_workers)
            analyzer.run_analysis()
            
            console.print("\n[green]🎉 自动化分析完成！[/green]")
            console.print("[cyan]💡 您可以查询数据库response表查看分析结果[/cyan]")
            
        except ImportError as e:
            console.print(f"[red]❌ 导入失败: {e}[/red]")
            console.print("[yellow]💡 请确保已安装依赖: pip install pymysql[/yellow]")
        except Exception as e:
            console.print(f"[red]❌ 分析失败: {e}[/red]")
            console.print("[cyan]📖 请查看日志文件获取详细错误信息[/cyan]")
    
    except KeyboardInterrupt:
        console.print("\n[yellow]👋 用户中断，程序退出[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ 程序异常: {e}[/red]")

if __name__ == "__main__":
    main()