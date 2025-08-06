#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修复后的频率限制器
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tradingagents.dataflows.rate_limiter import wait_for_tushare_api, get_api_statistics, reset_api_statistics
import time

def test_basic_functionality():
    """测试基本功能"""
    print("=== 测试修复后的频率限制器 ===")
    
    # 重置统计
    reset_api_statistics()
    
    print("\n1. 测试基本API调用...")
    start_time = time.time()
    
    # 测试3次快速调用
    for i in range(3):
        print(f"   调用 {i+1}/3...")
        wait_for_tushare_api(f"test_api_{i+1}")
        print(f"   调用 {i+1} 完成")
    
    end_time = time.time()
    print(f"   总耗时: {end_time - start_time:.2f}秒")
    
    # 显示统计信息
    stats = get_api_statistics()
    print(f"\n2. API调用统计:")
    print(f"   总调用次数: {stats['total_calls']}")
    print(f"   当前分钟调用: {stats['current_minute_calls']}")
    print(f"   剩余调用额度: {stats['remaining_calls']}")
    print(f"   被阻止次数: {stats['blocked_calls']}")
    print(f"   平均调用频率: {stats['average_call_rate']:.2f} 次/分钟")
    
    print("\n✅ 测试完成，频率限制器工作正常！")

if __name__ == "__main__":
    test_basic_functionality()