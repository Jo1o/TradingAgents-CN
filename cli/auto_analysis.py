#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TradingAgents 自动化分析模块
从MySQL数据库读取股票代码并进行自动化分析
"""

import os
import sys
import time
import datetime
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any, Optional
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 第三方库导入
try:
    import pymysql
except ImportError:
    print("❌ 缺少pymysql依赖，请安装: pip install pymysql")
    sys.exit(1)

from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, TaskID
from rich.panel import Panel

# 项目内部导入
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.utils.logging_manager import get_logger
from tradingagents.default_config import DEFAULT_CONFIG

# 导入频率限制器统计
try:
    from tradingagents.dataflows.rate_limiter import get_api_statistics, reset_api_statistics
    RATE_LIMITER_AVAILABLE = True
except ImportError:
    RATE_LIMITER_AVAILABLE = False

# 加载环境变量
load_dotenv()

# 初始化日志和控制台
logger = get_logger("auto_analysis")
console = Console()

class MySQLManager:
    """MySQL数据库管理器"""
    
    def __init__(self):
        self.connection = None
        self.config = {
            'host': os.getenv('MYSQL_HOST', 'localhost'),
            'port': int(os.getenv('MYSQL_PORT', 3306)),
            'user': os.getenv('MYSQL_USER', 'root'),
            'password': os.getenv('MYSQL_PASSWORD', ''),
            'database': os.getenv('MYSQL_DATABASE', 'coredata'),
            'charset': 'utf8mb4'
        }
        
    def connect(self) -> bool:
        """连接到MySQL数据库"""
        try:
            self.connection = pymysql.connect(**self.config)
            logger.info(f"✅ 成功连接到MySQL数据库: {self.config['host']}:{self.config['port']}/{self.config['database']}")
            return True
        except Exception as e:
            logger.error(f"❌ 连接MySQL数据库失败: {e}")
            console.print(f"[red]❌ 数据库连接失败: {e}[/red]")
            return False
    
    def disconnect(self):
        """断开数据库连接"""
        if self.connection:
            self.connection.close()
            logger.info("🔌 已断开MySQL数据库连接")
    
    def get_today_stocks(self) -> List[str]:
        """获取今日的股票代码列表"""
        if not self.connection:
            return []
        
        today = datetime.date.today().strftime('%Y-%m-%d')
        
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT DISTINCT code FROM rising_stocks WHERE record_date = %s"
                cursor.execute(sql, (today,))
                results = cursor.fetchall()
                
                stock_codes = [row[0] for row in results]
                logger.info(f"📊 从数据库获取到 {len(stock_codes)} 只今日股票: {stock_codes}")
                return stock_codes
                
        except Exception as e:
            logger.error(f"❌ 查询股票代码失败: {e}")
            console.print(f"[red]❌ 查询股票代码失败: {e}[/red]")
            return []
    
    def create_response_table(self):
        """创建response表（如果不存在）"""
        if not self.connection:
            return False
        
        try:
            with self.connection.cursor() as cursor:
                sql = """
                CREATE TABLE IF NOT EXISTS response (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    stock_code VARCHAR(20) NOT NULL COMMENT '股票代码',
                    action VARCHAR(50) DEFAULT NULL COMMENT '投资动作',
                    target_price DECIMAL(10,2) DEFAULT NULL COMMENT '目标价格',
                    confidence DECIMAL(3,2) DEFAULT NULL COMMENT '置信度',
                    risk_score DECIMAL(3,2) DEFAULT NULL COMMENT '风险评分',
                    reasoning TEXT DEFAULT NULL COMMENT '分析推理',
                    news_analysis TEXT DEFAULT NULL COMMENT '新闻分析师结果',
                    sentiment_analysis TEXT DEFAULT NULL COMMENT '情绪分析师结果',
                    analysis_date DATE NOT NULL COMMENT '分析日期',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                    INDEX idx_stock_code (stock_code),
                    INDEX idx_analysis_date (analysis_date)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='股票分析结果表'
                """
                cursor.execute(sql)
                self.connection.commit()
                logger.info("✅ response表已创建或已存在")
                return True
                
        except Exception as e:
            logger.error(f"❌ 创建response表失败: {e}")
            console.print(f"[red]❌ 创建response表失败: {e}[/red]")
            return False
    
    def save_analysis_result(self, stock_code: str, result: Dict[str, Any]) -> bool:
        """保存分析结果到数据库"""
        if not self.connection:
            return False
        
        try:
            with self.connection.cursor() as cursor:
                sql = """
                INSERT INTO response (
                    stock_code, action, target_price, confidence, 
                    risk_score, reasoning, news_analysis, sentiment_analysis, analysis_date
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                values = (
                    stock_code,
                    result.get('action'),
                    result.get('target_price'),
                    result.get('confidence'),
                    result.get('risk_score'),
                    result.get('reasoning'),
                    result.get('news_analysis'),
                    result.get('sentiment_analysis'),
                    datetime.date.today()
                )
                
                cursor.execute(sql, values)
                self.connection.commit()
                
                logger.info(f"✅ 股票 {stock_code} 分析结果已保存到数据库")
                return True
                
        except Exception as e:
            logger.error(f"❌ 保存分析结果失败 {stock_code}: {e}")
            console.print(f"[red]❌ 保存分析结果失败 {stock_code}: {e}[/red]")
            return False

class AutoAnalyzer:
    """自动化分析器"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.db_manager = MySQLManager()
        self.trading_graph = None
        
        # 重置API统计信息
        if RATE_LIMITER_AVAILABLE:
            reset_api_statistics()
            logger.info(f"📊 已重置API频率限制器统计信息")
        
        logger.info(f"📊 自动分析器初始化完成 (并发数: {max_workers})")
        logger.info(f"📊 API频率限制: {'已启用' if RATE_LIMITER_AVAILABLE else '未启用'}")
        
    def initialize(self) -> bool:
        """初始化分析器"""
        console.print(Panel("🚀 TradingAgents 自动化分析系统启动", style="bold blue"))
        
        # 连接数据库
        if not self.db_manager.connect():
            return False
        
        # 创建response表
        if not self.db_manager.create_response_table():
            return False
        
        # 初始化交易图
        try:
            # 确保包含所有分析师，特别是新闻分析师和情绪分析师
            selected_analysts = ["market", "social", "news", "fundamentals"]
            
            # 创建配置副本并禁用memory功能
            config = DEFAULT_CONFIG.copy()
            config["memory_enabled"] = False
            
            self.trading_graph = TradingAgentsGraph(
                selected_analysts=selected_analysts,
                config=config,
                debug=False
            )
            logger.info(f"✅ TradingAgentsGraph 初始化成功，包含分析师: {selected_analysts}")
            logger.info(f"🚫 Memory功能已禁用，不会从历史记忆中获取信息")
            console.print(f"[green]✅ 已启用分析师: {', '.join(selected_analysts)}[/green]")
            console.print(f"[yellow]🚫 Memory功能已禁用，每次分析都是独立的[/yellow]")
            return True
        except Exception as e:
            logger.error(f"❌ TradingAgentsGraph 初始化失败: {e}")
            console.print(f"[red]❌ 交易图初始化失败: {e}[/red]")
            return False
    
    def analyze_stock(self, stock_code: str) -> Optional[Dict[str, Any]]:
        """分析单只股票"""
        try:
            console.print(f"\n🔍 开始分析股票: [bold cyan]{stock_code}[/bold cyan]")
            
            # 执行分析
            state, result = self.trading_graph.propagate(stock_code, datetime.date.today().strftime("%Y-%m-%d"))
            
            # 提取关键信息
            if result and isinstance(result, dict):
                # 从state中提取新闻分析和情绪分析结果
                news_analysis = '无新闻分析'
                sentiment_analysis = '无情绪分析'
                
                if state and isinstance(state, dict):
                    # 记录state中的关键字段用于调试
                    logger.debug(f"📊 State字段: {list(state.keys())}")
                    
                    # 提取新闻分析结果
                    news_report = state.get('news_report', '')
                    logger.debug(f"📰 原始新闻报告: {news_report[:200] if news_report else 'None'}...")
                    if news_report and isinstance(news_report, str) and news_report.strip():
                        news_analysis = news_report.strip()
                        logger.info(f"✅ 成功提取新闻分析: {len(news_analysis)} 字符")
                    
                    # 提取情绪分析结果
                    sentiment_report = state.get('sentiment_report', '')
                    logger.debug(f"😊 原始情绪报告: {sentiment_report[:200] if sentiment_report else 'None'}...")
                    if sentiment_report and isinstance(sentiment_report, str) and sentiment_report.strip():
                        sentiment_analysis = sentiment_report.strip()
                        logger.info(f"✅ 成功提取情绪分析: {len(sentiment_analysis)} 字符")
                else:
                    logger.warning(f"⚠️ State为空或格式异常: {type(state)}")
                
                # 解析决策信息
                analysis_result = {
                    'action': result.get('action', '未知'),
                    'target_price': result.get('target_price'),
                    'confidence': result.get('confidence'),
                    'risk_score': result.get('risk_score'),
                    'reasoning': result.get('reasoning', '无详细说明'),
                    'news_analysis': news_analysis,
                    'sentiment_analysis': sentiment_analysis
                }
                
                console.print(f"✅ 股票 {stock_code} 分析完成")
                console.print(f"   动作: [bold]{analysis_result['action']}[/bold]")
                console.print(f"   目标价: {analysis_result['target_price']}")
                console.print(f"   置信度: {analysis_result['confidence']}")
                console.print(f"   风险评分: {analysis_result['risk_score']}")
                
                # 显示新闻分析和情绪分析结果（调试信息）
                if analysis_result['news_analysis'] != '无新闻分析':
                    console.print(f"   [cyan]📰 新闻分析: {analysis_result['news_analysis'][:100]}...[/cyan]")
                else:
                    console.print(f"   [yellow]⚠️ 新闻分析: 未获取到新闻分析结果[/yellow]")
                    
                if analysis_result['sentiment_analysis'] != '无情绪分析':
                    console.print(f"   [cyan]😊 情绪分析: {analysis_result['sentiment_analysis'][:100]}...[/cyan]")
                else:
                    console.print(f"   [yellow]⚠️ 情绪分析: 未获取到情绪分析结果[/yellow]")
                
                return analysis_result
            else:
                logger.warning(f"⚠️ 股票 {stock_code} 分析结果格式异常")
                return None
                
        except Exception as e:
            logger.error(f"❌ 分析股票 {stock_code} 失败: {e}")
            console.print(f"[red]❌ 分析股票 {stock_code} 失败: {e}[/red]")
            return None
    
    def analyze_and_save_stock(self, stock_code: str) -> Dict[str, Any]:
        """分析并保存单只股票的结果"""
        try:
            console.print(f"🔍 开始分析股票: [bold cyan]{stock_code}[/bold cyan]")
            
            # 分析股票
            result = self.analyze_stock(stock_code)
            
            if result:
                # 保存结果
                if self.db_manager.save_analysis_result(stock_code, result):
                    console.print(f"[green]✅ {stock_code} 分析并保存成功[/green]")
                    return {'stock_code': stock_code, 'status': 'success', 'result': result}
                else:
                    console.print(f"[red]❌ {stock_code} 保存失败[/red]")
                    return {'stock_code': stock_code, 'status': 'save_failed', 'result': result}
            else:
                console.print(f"[red]❌ {stock_code} 分析失败[/red]")
                return {'stock_code': stock_code, 'status': 'analysis_failed', 'result': None}
                
        except Exception as e:
            logger.error(f"❌ 处理股票 {stock_code} 时发生错误: {e}")
            console.print(f"[red]❌ 处理股票 {stock_code} 时发生错误: {e}[/red]")
            return {'stock_code': stock_code, 'status': 'error', 'result': None}
    
    async def run_analysis_async(self):
        """运行异步自动化分析"""
        if not self.initialize():
            return
        
        try:
            # 获取今日股票列表
            stock_codes = self.db_manager.get_today_stocks()
            
            if not stock_codes:
                console.print("[yellow]⚠️ 今日没有找到需要分析的股票[/yellow]")
                return
            
            console.print(f"[bold green]📊 获取到 {len(stock_codes)} 只股票，将使用 {self.max_workers} 个并发线程进行分析[/bold green]")
            
            # 显示分析计划
            table = Table(title="📋 分析计划")
            table.add_column("序号", style="cyan")
            table.add_column("股票代码", style="magenta")
            table.add_column("状态", style="green")
            
            for i, code in enumerate(stock_codes, 1):
                table.add_row(str(i), code, "待分析")
            
            console.print(table)
            
            # 使用线程池执行器进行并发分析
            loop = asyncio.get_event_loop()
            
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # 创建任务列表
                tasks = []
                for stock_code in stock_codes:
                    task = loop.run_in_executor(executor, self.analyze_and_save_stock, stock_code)
                    tasks.append(task)
                
                # 使用进度条显示进度
                with Progress() as progress:
                    task_progress = progress.add_task("[green]分析进度...", total=len(stock_codes))
                    
                    # 等待所有任务完成
                    results = []
                    for task in asyncio.as_completed(tasks):
                        result = await task
                        results.append(result)
                        progress.update(task_progress, advance=1)
                        
                        # 实时显示完成的股票
                        status_color = "green" if result['status'] == 'success' else "red"
                        console.print(f"[{status_color}]完成: {result['stock_code']} - {result['status']}[/{status_color}]")
            
            # 统计结果
            successful_count = sum(1 for r in results if r['status'] == 'success')
            failed_count = len(results) - successful_count
            
            # 获取API统计信息
            api_stats = None
            if RATE_LIMITER_AVAILABLE:
                try:
                    api_stats = get_api_statistics()
                    logger.info(f"📊 API调用统计: {api_stats}")
                except Exception as e:
                    logger.warning(f"⚠️ 获取API统计信息失败: {e}")
            
            # 显示最终结果
            console.print(f"\n[bold green]🎉 异步分析完成![/bold green]")
            console.print(f"✅ 成功: {successful_count}")
            console.print(f"❌ 失败: {failed_count}")
            console.print(f"📊 总计: {len(stock_codes)}")
            
            # 显示API统计信息
            if api_stats:
                console.print(f"\n[bold cyan]📊 API调用统计:[/bold cyan]")
                console.print(f"  总调用次数: {api_stats['total_calls']}")
                console.print(f"  当前分钟调用: {api_stats['current_calls_per_minute']}/{api_stats['max_calls_per_minute']}")
                console.print(f"  剩余调用额度: {api_stats['remaining_calls']}")
                console.print(f"  被阻止次数: {api_stats['blocked_calls']}")
                console.print(f"  平均调用频率: {api_stats['calls_per_second']:.2f} 次/秒")
            
            # 显示失败的股票详情
            failed_stocks = [r for r in results if r['status'] != 'success']
            if failed_stocks:
                console.print("\n[yellow]失败的股票:[/yellow]")
                for failed in failed_stocks:
                    console.print(f"  - {failed['stock_code']}: {failed['status']}")
            
        except KeyboardInterrupt:
            console.print("\n[yellow]⚠️ 用户中断分析[/yellow]")
        except Exception as e:
            logger.error(f"❌ 自动化分析过程中发生错误: {e}")
            console.print(f"[red]❌ 分析过程中发生错误: {e}[/red]")
        finally:
            self.db_manager.disconnect()
    
    def run_analysis(self):
        """运行自动化分析（异步版本的同步包装器）"""
        asyncio.run(self.run_analysis_async())

def main():
    """主函数"""
    analyzer = AutoAnalyzer(max_workers=4)  # 并发数量限制为4
    analyzer.run_analysis()

if __name__ == "__main__":
    main()