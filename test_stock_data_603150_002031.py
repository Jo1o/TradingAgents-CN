#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试获取603150和002031股票数据的脚本
"""

import sys
import os
from datetime import datetime, timedelta
import time

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from tradingagents.dataflows.data_source_manager import DataSourceManager, get_china_stock_data_unified, get_china_stock_info_unified
    from tradingagents.dataflows.interface import get_china_stock_data_tushare, get_china_stock_data_akshare
except ImportError as e:
    print(f"❌ 导入数据管理模块失败: {e}")
    sys.exit(1)

def test_data_source_manager():
    """测试DataSourceManager基本功能"""
    print("\n=== 测试DataSourceManager初始化 ===")
    try:
        dsm = DataSourceManager()
        print("✅ DataSourceManager初始化成功")
        print(f"当前数据源: {dsm.current_source.value}")
        print(f"可用数据源: {[s.value for s in dsm.available_sources]}")
        return dsm
    except Exception as e:
        print(f"❌ DataSourceManager初始化失败: {e}")
        return None
    
def test_stock_basic_info(dsm, stock_codes):
    """测试获取股票基本信息"""
    print("\n=== 测试获取股票基本信息 ===")
    for code in stock_codes:
        try:
            print(f"\n📊 获取 {code} 基本信息...")
            
            # 使用统一接口
            info = get_china_stock_info_unified(code)
            
            if info:
                print(f"✅ {code} 基本信息获取成功:")
                if isinstance(info, dict):
                    for key, value in info.items():
                        print(f"   {key}: {value}")
                else:
                    print(f"   {info}")
            else:
                print(f"❌ {code} 基本信息获取失败")
                
        except Exception as e:
            print(f"❌ 获取 {code} 基本信息时出错: {e}")

def test_stock_historical_data(dsm, stock_codes):
    """测试获取股票历史数据"""
    print("\n=== 测试获取股票历史数据 ===")
    
    # 设置日期范围（最近30天）
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    for code in stock_codes:
        try:
            print(f"\n📈 获取 {code} 历史数据 ({start_date} 到 {end_date})...")
            
            # 使用统一接口
            data = get_china_stock_data_unified(code, start_date, end_date)
            
            if data:
                print(f"✅ {code} 历史数据获取成功")
                # 显示前200个字符
                preview = str(data)[:200]
                print(f"   数据预览: {preview}...")
            else:
                print(f"❌ {code} 历史数据获取失败")
                
        except Exception as e:
            print(f"❌ 获取 {code} 历史数据时出错: {e}")
            
        # 添加延迟以避免API频率限制
        print("   等待2秒以避免API频率限制...")
        time.sleep(2)

def test_individual_providers(stock_codes):
    """测试单独的数据提供商"""
    print("\n=== 测试单独的数据提供商 ===")
    
    # 设置日期范围
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    for code in stock_codes:
        print(f"\n🔍 测试 {code} 的不同数据源:")
        
        # 测试Tushare
        try:
            print(f"   📊 Tushare数据源...")
            tushare_data = get_china_stock_data_tushare(code, start_date, end_date)
            if tushare_data:
                print(f"   ✅ Tushare获取成功，数据长度: {len(str(tushare_data))}")
                print(f"   预览: {str(tushare_data)[:100]}...")
            else:
                print(f"   ❌ Tushare获取失败")
        except Exception as e:
            print(f"   ❌ Tushare获取失败: {e}")
        
        # 添加延迟
        time.sleep(2)
        
        # 测试AKShare
        try:
            print(f"   📊 AKShare数据源...")
            akshare_data = get_china_stock_data_akshare(code, start_date, end_date)
            if akshare_data:
                print(f"   ✅ AKShare获取成功，数据长度: {len(str(akshare_data))}")
                print(f"   预览: {str(akshare_data)[:100]}...")
            else:
                print(f"   ❌ AKShare获取失败")
        except Exception as e:
            print(f"   ❌ AKShare获取失败: {e}")
            
        # 添加延迟
        time.sleep(2)

def main():
    """主函数"""
    print("🚀 开始测试股票数据获取功能")
    print("目标股票: 603150 (万朗磁塑), 002031 (巨轮智能)")
    
    stock_codes = ['603150', '002031']
    
    # 1. 测试DataSourceManager初始化
    dsm = test_data_source_manager()
    if not dsm:
        print("❌ DataSourceManager初始化失败，无法继续测试")
        return
    
    # 2. 测试获取股票基本信息
    test_stock_basic_info(dsm, stock_codes)
    
    # 3. 测试获取股票历史数据
    test_stock_historical_data(dsm, stock_codes)
    
    # 4. 测试单独的数据提供商
    test_individual_providers(stock_codes)
    
    print("\n🎉 测试完成！")

if __name__ == "__main__":
    print("🚀 TradingAgents 股票数据获取测试")
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 主要测试
    main()
    
    print("\n🎉 所有测试完成！")