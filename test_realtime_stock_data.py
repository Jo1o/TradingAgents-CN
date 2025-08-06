#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试获取603150和002031的实时股票数据
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
import time

def test_realtime_stock_data():
    """测试获取实时股票数据"""
    print("🚀 开始测试实时股票数据获取...")
    print("=" * 60)
    
    # 测试股票代码
    test_stocks = ['603150', '002031']
    
    # 获取今日日期
    today = datetime.now().strftime('%Y-%m-%d')
    
    print(f"📅 测试日期: {today}")
    print(f"📊 测试股票: {', '.join(test_stocks)}")
    print()
    
    for i, stock_code in enumerate(test_stocks, 1):
        print(f"\n{'='*20} 测试股票 {i}: {stock_code} {'='*20}")
        
        try:
            # 使用统一接口获取实时数据
            print(f"🔍 正在获取 {stock_code} 的实时数据...")
            
            from tradingagents.dataflows.interface import get_china_stock_data_unified
            
            # 获取最近3天的数据（包含实时数据）
            from datetime import timedelta
            start_date = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
            
            result = get_china_stock_data_unified(stock_code, start_date, today)
            
            if result and "❌" not in result and "错误" not in result:
                print(f"✅ {stock_code} 数据获取成功！")
                print(f"📄 数据长度: {len(result)} 字符")
                print("\n📊 数据内容预览:")
                print("-" * 50)
                # 显示前800字符的数据内容
                preview = result[:800]
                print(preview)
                if len(result) > 800:
                    print("\n... (数据已截断，显示前800字符) ...")
                print("-" * 50)
                
                # 尝试提取关键信息
                lines = result.split('\n')
                for line in lines[:20]:  # 查看前20行
                    if '当前价格' in line or '股票名称' in line or '涨跌幅' in line or '成交量' in line:
                        print(f"🔍 关键信息: {line.strip()}")
                        
            else:
                print(f"❌ {stock_code} 数据获取失败")
                print(f"📄 返回结果: {result[:300] if result else 'None'}...")
                
        except Exception as e:
            print(f"❌ {stock_code} 获取异常: {e}")
            import traceback
            print(f"📋 详细错误:\n{traceback.format_exc()}")
        
        # 添加延迟避免API限制
        if i < len(test_stocks):
            print(f"\n⏳ 等待2秒后继续下一个股票...")
            time.sleep(2)

def test_alternative_methods():
    """测试其他获取方法"""
    print("\n\n🔧 测试其他数据获取方法...")
    print("=" * 60)
    
    test_code = '603150'  # 以603150为例
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 方法1: 直接使用Tushare接口
    try:
        print(f"\n📡 方法1: 使用Tushare接口获取 {test_code}...")
        from tradingagents.dataflows.interface import get_china_stock_data_tushare
        
        result = get_china_stock_data_tushare(test_code, today, today)
        
        if result and "❌" not in result:
            print(f"✅ Tushare接口成功")
            print(f"📄 数据长度: {len(result)} 字符")
            # 显示前300字符
            print(f"📊 数据预览: {result[:300]}...")
        else:
            print(f"❌ Tushare接口失败: {result[:200] if result else 'None'}")
            
    except Exception as e:
        print(f"❌ Tushare接口异常: {e}")
    
    time.sleep(2)
    
    # 方法2: 使用工具包接口
    try:
        print(f"\n🛠️ 方法2: 使用工具包接口获取 {test_code}...")
        from tradingagents.agents.utils.agent_utils import Toolkit
        from tradingagents.default_config import DEFAULT_CONFIG
        
        config = DEFAULT_CONFIG.copy()
        config["online_tools"] = True
        toolkit = Toolkit(config)
        
        result = toolkit.get_china_stock_data(test_code, today, today)
        
        if result and "❌" not in result:
            print(f"✅ 工具包接口成功")
            print(f"📄 数据长度: {len(result)} 字符")
            # 显示前300字符
            print(f"📊 数据预览: {result[:300]}...")
        else:
            print(f"❌ 工具包接口失败: {result[:200] if result else 'None'}")
            
    except Exception as e:
        print(f"❌ 工具包接口异常: {e}")

def main():
    """主函数"""
    print("🎯 实时股票数据测试程序")
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 测试主要功能
    test_realtime_stock_data()
    
    # 测试其他方法
    test_alternative_methods()
    
    print("\n" + "=" * 60)
    print("🎉 测试完成！")
    print("\n📋 说明:")
    print("- ✅ 表示数据获取成功")
    print("- ❌ 表示数据获取失败")
    print("- 实时数据包含当前价格、涨跌幅、成交量等信息")
    print("- 如果是非交易时间，显示的是最近交易日的收盘数据")

if __name__ == "__main__":
    main()