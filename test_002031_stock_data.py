#!/usr/bin/env python3
"""
测试002031股票数据获取接口
"""

import sys
sys.path.append('.')

def test_002031_stock_data():
    """测试002031股票数据获取"""
    print("🔍 测试002031股票数据获取接口...")
    print("=" * 60)
    
    stock_code = "002031"
    
    # 测试1: 测试实时数据获取
    print("\n📊 测试1: 实时数据获取")
    print("-" * 40)
    
    try:
        from tradingagents.dataflows.tdx_utils import TongDaXinDataProvider
        
        provider = TongDaXinDataProvider()
        
        if not provider.connect():
            print("❌ Tushare数据接口连接失败")
            return False
            
        print("✅ Tushare数据接口连接成功")
        
        # 获取实时数据
        print(f"\n🔄 获取 {stock_code} 的实时数据...")
        realtime_data = provider.get_real_time_data(stock_code)
        
        if realtime_data:
            print(f"✅ 实时数据获取成功:")
            print(f"   股票代码: {realtime_data.get('code', 'N/A')}")
            print(f"   股票名称: {realtime_data.get('name', 'N/A')}")
            print(f"   当前价格: ¥{realtime_data.get('price', 0):.2f}")
            print(f"   涨跌幅: {realtime_data.get('change_percent', 0):.2f}%")
            print(f"   成交量: {realtime_data.get('volume', 0):,}手")
            print(f"   数据来源: {realtime_data.get('source', 'N/A')}")
        else:
            print(f"❌ 未获取到 {stock_code} 的实时数据")
            
        provider.disconnect()
        
    except Exception as e:
        print(f"❌ 实时数据测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 测试2: 测试历史数据获取
    print("\n📈 测试2: 历史数据获取")
    print("-" * 40)
    
    try:
        from tradingagents.dataflows.interface import get_china_stock_data_tushare
        from datetime import datetime, timedelta
        
        # 获取最近7天的数据
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        print(f"🔄 获取 {stock_code} 从 {start_date} 到 {end_date} 的历史数据...")
        
        historical_data = get_china_stock_data_tushare(stock_code, start_date, end_date)
        
        if historical_data and "❌" not in historical_data:
            print(f"✅ 历史数据获取成功")
            print(f"数据长度: {len(historical_data)} 字符")
            # 显示前200个字符作为预览
            preview = historical_data[:200] + "..." if len(historical_data) > 200 else historical_data
            print(f"数据预览:\n{preview}")
        else:
            print(f"❌ 历史数据获取失败")
            if historical_data:
                print(f"错误信息: {historical_data}")
                
    except Exception as e:
        print(f"❌ 历史数据测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 测试3: 测试股票基本信息获取
    print("\n📋 测试3: 股票基本信息获取")
    print("-" * 40)
    
    try:
        from tradingagents.dataflows.interface import get_china_stock_info_tushare
        
        print(f"🔄 获取 {stock_code} 的基本信息...")
        
        stock_info = get_china_stock_info_tushare(stock_code)
        
        if stock_info and "❌" not in stock_info:
            print(f"✅ 股票基本信息获取成功")
            print(f"信息内容:\n{stock_info}")
        else:
            print(f"❌ 股票基本信息获取失败")
            if stock_info:
                print(f"错误信息: {stock_info}")
                
    except Exception as e:
        print(f"❌ 股票基本信息测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 测试4: 测试统一数据接口
    print("\n🔧 测试4: 统一数据接口")
    print("-" * 40)
    
    try:
        from tradingagents.dataflows.interface import get_china_stock_data_unified
        from datetime import datetime, timedelta
        
        # 获取最近3天的数据
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
        
        print(f"🔄 使用统一接口获取 {stock_code} 从 {start_date} 到 {end_date} 的数据...")
        
        unified_data = get_china_stock_data_unified(stock_code, start_date, end_date)
        
        if unified_data and "❌" not in unified_data:
            print(f"✅ 统一接口数据获取成功")
            print(f"数据长度: {len(unified_data)} 字符")
            # 显示前200个字符作为预览
            preview = unified_data[:200] + "..." if len(unified_data) > 200 else unified_data
            print(f"数据预览:\n{preview}")
        else:
            print(f"❌ 统一接口数据获取失败")
            if unified_data:
                print(f"错误信息: {unified_data}")
                
    except Exception as e:
        print(f"❌ 统一接口测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("🎯 002031股票数据获取接口测试完成")
    print("=" * 60)

if __name__ == "__main__":
    test_002031_stock_data()