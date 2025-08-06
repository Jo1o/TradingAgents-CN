#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单诊断脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import time

def test_basic_import():
    """测试基本导入"""
    print("=== 诊断测试 ===")
    
    try:
        print("1. 测试导入...")
        from tradingagents.dataflows.rate_limiter import GlobalRateLimiter
        print("   ✅ GlobalRateLimiter 导入成功")
        
        print("2. 测试实例化...")
        limiter = GlobalRateLimiter()
        print("   ✅ GlobalRateLimiter 实例化成功")
        
        print("3. 测试基本方法...")
        stats = limiter.get_statistics()
        print(f"   ✅ 获取统计信息成功: {stats}")
        
        print("4. 测试简单调用（无等待）...")
        # 临时设置基础等待时间为0
        original_wait = limiter.base_wait_time
        limiter.base_wait_time = 0
        
        start_time = time.time()
        result = limiter.wait_for_api_call("test")
        end_time = time.time()
        
        print(f"   ✅ API调用完成，结果: {result}，耗时: {end_time - start_time:.3f}秒")
        
        # 恢复原始等待时间
        limiter.base_wait_time = original_wait
        
        print("\n✅ 所有测试通过！")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_basic_import()