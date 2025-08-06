#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取603150和002031的当前实时数据
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
import time

def get_current_stock_data():
    """获取当前股票数据"""
    print("🚀 获取603150和002031的当前实时数据")
    print("=" * 60)
    
    # 测试股票代码
    test_stocks = ['603150', '002031']
    
    # 获取今日日期
    today = datetime.now().strftime('%Y-%m-%d')
    
    print(f"📅 查询日期: {today}")
    print(f"⏰ 查询时间: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    for stock_code in test_stocks:
        print(f"\n📊 股票代码: {stock_code}")
        print("-" * 40)
        
        try:
            from tradingagents.dataflows.interface import get_china_stock_data_unified
            
            # 只获取今日数据
            result = get_china_stock_data_unified(stock_code, today, today)
            
            if result and "❌" not in result and "错误" not in result:
                print("✅ 数据获取成功")
                
                # 提取关键信息
                lines = result.split('\n')
                for line in lines:
                    line = line.strip()
                    if any(keyword in line for keyword in ['股票名称', '当前价格', '涨跌幅', '成交量', '数据来源']):
                        print(f"  {line}")
                
                # 查找历史数据概览
                print("\n📈 数据概览:")
                for line in lines:
                    line = line.strip()
                    if any(keyword in line for keyword in ['数据期间', '数据条数', '期间最高', '期间最低']):
                        print(f"  {line}")
                        
            else:
                print("❌ 数据获取失败")
                print(f"返回结果: {result[:200] if result else 'None'}...")
                
        except Exception as e:
            print(f"❌ 获取异常: {e}")
        
        # 添加延迟
        if stock_code != test_stocks[-1]:
            time.sleep(1)
    
    print("\n" + "=" * 60)
    print("📋 说明:")
    print("- 以上数据为实时或最新交易日数据")
    print("- 如果是交易时间，显示实时价格")
    print("- 如果是非交易时间，显示最近交易日收盘价")

if __name__ == "__main__":
    get_current_stock_data()