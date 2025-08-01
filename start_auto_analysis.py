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

try:
    import pymysql
except ImportError:
    print("❌ 缺少pymysql依赖，请安装: pip install pymysql")
    sys.exit(1)

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt

console = Console()

def check_and_create_database() -> bool:
    """检查数据库是否存在，如果不存在则创建"""
    try:
        # 获取数据库配置
        config = {
            'host': os.getenv('MYSQL_HOST', 'localhost'),
            'port': int(os.getenv('MYSQL_PORT', 3306)),
            'user': os.getenv('MYSQL_USER', 'root'),
            'password': os.getenv('MYSQL_PASSWORD', ''),
            'charset': 'utf8mb4'
        }
        database_name = os.getenv('MYSQL_DATABASE', 'coredata')
        
        # 先连接到MySQL服务器（不指定数据库）
        connection = pymysql.connect(**config)
        
        try:
            with connection.cursor() as cursor:
                # 检查数据库是否存在
                cursor.execute("SHOW DATABASES LIKE %s", (database_name,))
                result = cursor.fetchone()
                
                if result:
                    console.print(f"[green]✅ 数据库 '{database_name}' 已存在[/green]")
                else:
                    # 创建数据库
                    console.print(f"[yellow]📦 数据库 '{database_name}' 不存在，正在创建...[/yellow]")
                    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name} DEFAULT CHARSET=utf8mb4")
                    connection.commit()
                    console.print(f"[green]✅ 数据库 '{database_name}' 创建成功[/green]")
                
                # 验证数据库连接
                connection.select_db(database_name)
                console.print(f"[green]✅ 成功连接到数据库 '{database_name}'[/green]")
                
        finally:
            connection.close()
            
        return True
        
    except Exception as e:
        console.print(f"[red]❌ 数据库检查或创建失败: {e}[/red]")
        console.print("[yellow]💡 请检查MySQL服务是否运行，以及配置信息是否正确[/yellow]")
        return False

def clear_local_cache():
    """清理本地缓存文件"""
    import shutil
    
    try:
        # 清理Python缓存文件
        cache_patterns = ["__pycache__"]
        total_cleaned = 0
        
        for pattern in cache_patterns:
            cache_dirs = list(project_root.rglob(pattern))
            for cache_dir in cache_dirs:
                try:
                    shutil.rmtree(cache_dir)
                    total_cleaned += 1
                except Exception:
                    pass  # 忽略删除失败的情况
        
        # 清理数据缓存目录
        cache_dirs = [
            project_root / "cache",
            project_root / "data" / "cache", 
            project_root / "tradingagents" / "dataflows" / "data_cache"
        ]
        
        for cache_dir in cache_dirs:
            if cache_dir.exists():
                try:
                    shutil.rmtree(cache_dir)
                    total_cleaned += 1
                except Exception:
                    pass  # 忽略删除失败的情况
        
        if total_cleaned > 0:
            console.print(f"[green]✅ 已清理 {total_cleaned} 个缓存目录[/green]")
        else:
            console.print("[cyan]ℹ️ 没有发现需要清理的缓存[/cyan]")
            
    except Exception as e:
        console.print(f"[yellow]⚠️ 缓存清理过程中出现问题: {e}[/yellow]")

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
    
    # 检查并创建数据库
    console.print("\n[yellow]🔍 检查数据库是否存在...[/yellow]")
    if not check_and_create_database():
        console.print("[red]❌ 数据库检查或创建失败[/red]")
        return
    
    # 清理本地缓存
    console.print("\n[yellow]🧹 清理本地缓存...[/yellow]")
    clear_local_cache()
    
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