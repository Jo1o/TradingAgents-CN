#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试股票数据获取接口
验证 start_auto_analysis.py 中使用的股票数据获取接口是否正常
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
import time

def test_china_stock_data_interface():
    """测试中国股票数据获取接口"""
    print("🔍 测试中国股票数据获取接口...")
    
    # 测试股票代码
    test_stocks = ['603150', '002031']
    
    # 设置日期范围
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    print(f"📅 测试日期范围: {start_date} 到 {end_date}")
    
    for stock_code in test_stocks:
        print(f"\n📊 测试股票: {stock_code}")
        
        try:
            # 测试统一接口
            print("  🔧 测试统一数据接口...")
            from tradingagents.dataflows.interface import get_china_stock_data_unified
            
            result = get_china_stock_data_unified(stock_code, start_date, end_date)
            
            if result and "❌" not in result and "错误" not in result:
                print(f"  ✅ 统一接口测试成功")
                print(f"  📄 返回数据长度: {len(result)} 字符")
                print(f"  📝 数据预览: {result[:200]}...")
            else:
                print(f"  ❌ 统一接口测试失败")
                print(f"  📄 返回结果: {result[:500] if result else 'None'}")
                
        except Exception as e:
            print(f"  ❌ 统一接口异常: {e}")
            import traceback
            print(f"  📋 详细错误: {traceback.format_exc()}")
        
        # 添加延迟避免API限制
        time.sleep(2)
        
        try:
            # 测试 Tushare 接口
            print("  🔧 测试 Tushare 接口...")
            from tradingagents.dataflows.interface import get_china_stock_data_tushare
            
            result = get_china_stock_data_tushare(stock_code, start_date, end_date)
            
            if result and "❌" not in result and "错误" not in result:
                print(f"  ✅ Tushare 接口测试成功")
                print(f"  📄 返回数据长度: {len(result)} 字符")
            else:
                print(f"  ❌ Tushare 接口测试失败")
                print(f"  📄 返回结果: {result[:500] if result else 'None'}")
                
        except Exception as e:
            print(f"  ❌ Tushare 接口异常: {e}")
            import traceback
            print(f"  📋 详细错误: {traceback.format_exc()}")
        
        # 添加延迟避免API限制
        time.sleep(2)

def test_data_source_manager():
    """测试数据源管理器"""
    print("\n🔍 测试数据源管理器...")
    
    try:
        from tradingagents.dataflows.data_source_manager import get_data_source_manager
        
        manager = get_data_source_manager()
        print(f"  📊 当前数据源: {manager.get_current_source().value}")
        print(f"  📋 可用数据源: {[source.value for source in manager._check_available_sources()]}")
        
        # 测试获取股票数据
        test_code = '603150'
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        print(f"  🔧 测试获取 {test_code} 数据...")
        result = manager.get_stock_data(test_code, start_date, end_date)
        
        if result and "❌" not in result and "错误" not in result:
            print(f"  ✅ 数据源管理器测试成功")
            print(f"  📄 返回数据长度: {len(result)} 字符")
        else:
            print(f"  ❌ 数据源管理器测试失败")
            print(f"  📄 返回结果: {result[:500] if result else 'None'}")
            
    except Exception as e:
        print(f"  ❌ 数据源管理器异常: {e}")
        import traceback
        print(f"  📋 详细错误: {traceback.format_exc()}")

def test_toolkit_interface():
    """测试工具包接口"""
    print("\n🔍 测试工具包接口...")
    
    try:
        from tradingagents.agents.utils.agent_utils import Toolkit
        from tradingagents.default_config import DEFAULT_CONFIG
        
        config = DEFAULT_CONFIG.copy()
        config["online_tools"] = True
        toolkit = Toolkit(config)
        
        # 测试 get_china_stock_data 工具
        test_code = '002031'
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        print(f"  🔧 测试工具包 get_china_stock_data...")
        result = toolkit.get_china_stock_data(test_code, start_date, end_date)
        
        if result and "❌" not in result and "错误" not in result:
            print(f"  ✅ 工具包接口测试成功")
            print(f"  📄 返回数据长度: {len(result)} 字符")
        else:
            print(f"  ❌ 工具包接口测试失败")
            print(f"  📄 返回结果: {result[:500] if result else 'None'}")
            
    except Exception as e:
        print(f"  ❌ 工具包接口异常: {e}")
        import traceback
        print(f"  📋 详细错误: {traceback.format_exc()}")

def main():
    """主函数"""
    print("🚀 开始测试股票数据获取接口...")
    print("=" * 60)
    
    # 测试各个接口
    test_china_stock_data_interface()
    test_data_source_manager()
    test_toolkit_interface()
    
    print("\n" + "=" * 60)
    print("🎯 测试完成！")
    print("\n📋 总结:")
    print("- 如果所有接口都显示 ✅，说明股票数据获取接口正常")
    print("- 如果出现 ❌，请检查相应的错误信息")
    print("- 常见问题: Tushare API 频率限制、网络连接问题、配置错误")

if __name__ == "__main__":
    main()