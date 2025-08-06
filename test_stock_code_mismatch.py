#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试股票代码数据不匹配问题
验证Tushare API返回的数据是否与请求的股票代码匹配
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()

from tradingagents.dataflows.tushare_adapter import TushareDataAdapter
from tradingagents.utils.logging_manager import get_logger

logger = get_logger("test_mismatch")

def test_stock_code_mismatch():
    """测试股票代码数据不匹配问题"""
    print("🔍 测试股票代码数据不匹配问题")
    print("=" * 50)
    
    # 初始化Tushare适配器
    adapter = TushareDataAdapter()
    
    # 测试股票代码列表
    test_codes = ['002031', '000519', '000949']
    
    for stock_code in test_codes:
        print(f"\n📊 测试股票代码: {stock_code}")
        print("-" * 30)
        
        try:
            # 获取股票数据
            data = adapter.get_stock_data(stock_code, start_date='2025-07-01', end_date='2025-08-06')
            
            if data is not None and not data.empty:
                # 检查返回数据中的股票代码（标准化后可能是code字段）
                unique_codes = []
                if 'ts_code' in data.columns:
                    unique_codes = data['ts_code'].unique()
                elif 'code' in data.columns:
                    unique_codes = data['code'].unique()
                elif '股票代码' in data.columns:
                    unique_codes = data['股票代码'].unique()
                
                print(f"✅ 请求股票代码: {stock_code}")
                print(f"📈 返回数据条数: {len(data)}")
                print(f"🔍 数据列名: {list(data.columns)}")
                print(f"🔍 返回数据中的股票代码: {list(unique_codes)}")
                
                # 检查是否匹配
                expected_codes = [f"{stock_code}.SZ", f"{stock_code}.SS", stock_code]
                actual_codes = list(unique_codes)
                
                is_match = any(code in actual_codes for code in expected_codes)
                
                if is_match:
                    print(f"✅ 数据匹配: 请求 {stock_code}，返回 {actual_codes}")
                else:
                    print(f"❌ 数据不匹配: 请求 {stock_code}，返回 {actual_codes}")
                    print(f"⚠️ 这是一个严重的数据错误！")
                
                # 显示数据样本
                if len(data) > 0:
                    latest_data = data.iloc[0]
                    print(f"📅 最新数据日期: {latest_data.get('trade_date', 'N/A')}")
                    print(f"💰 最新收盘价: {latest_data.get('close', 'N/A')}")
                    
            else:
                print(f"❌ 未获取到 {stock_code} 的数据")
                
        except Exception as e:
            print(f"❌ 测试 {stock_code} 时发生错误: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("🎯 测试完成")

def test_stock_info_mismatch():
    """测试股票基本信息不匹配问题"""
    print("\n🔍 测试股票基本信息数据不匹配问题")
    print("=" * 50)
    
    # 初始化Tushare适配器
    adapter = TushareDataAdapter()
    
    # 测试股票代码列表
    test_codes = ['002031', '000519', '000949']
    
    for stock_code in test_codes:
        print(f"\n📊 测试股票基本信息: {stock_code}")
        print("-" * 30)
        
        try:
            # 获取股票基本信息
            info = adapter.get_stock_info(stock_code)
            
            if info:
                print(f"✅ 请求股票代码: {stock_code}")
                print(f"📋 返回信息: {info}")
                
                # 检查信息中是否包含正确的股票代码
                if stock_code in info:
                    print(f"✅ 信息匹配: 包含请求的股票代码 {stock_code}")
                else:
                    print(f"⚠️ 信息可能不匹配: 未明确包含股票代码 {stock_code}")
                    
            else:
                print(f"❌ 未获取到 {stock_code} 的基本信息")
                
        except Exception as e:
            print(f"❌ 测试 {stock_code} 基本信息时发生错误: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("🎯 基本信息测试完成")

if __name__ == "__main__":
    test_stock_code_mismatch()
    test_stock_info_mismatch()