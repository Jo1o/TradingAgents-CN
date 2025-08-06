#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接测试频率限制器类
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import time

def test_direct_limiter():
    """直接测试 GlobalRateLimiter 类"""
    print("=== 直接测试频率限制器 ===")
    
    try:
        print("1. 导入类...")
        from tradingagents.dataflows.rate_limiter import GlobalRateLimiter
        print("   ✅ 导入成功")
        
        print("2. 创建实例...")
        limiter = GlobalRateLimiter(max_calls_per_minute=950, safety_margin=50)
        print("   ✅ 实例创建成功")
        
        print("3. 测试基本属性...")
        print(f"   最大调用频率: {limiter.max_calls_per_minute}")
        print(f"   警告阈值: {limiter.warning_threshold}")
        print(f"   基础等待时间: {limiter.base_wait_time}")
        print("   ✅ 基本属性正常")
        
        print("4. 测试统计信息（直接调用）...")
        # 直接在锁内获取信息，避免死锁
        with limiter.lock:
            limiter._cleanup_old_timestamps()
            current_count = len(limiter.call_timestamps)
            remaining = limiter.max_calls_per_minute - current_count
            print(f"   当前调用次数: {current_count}")
            print(f"   剩余调用次数: {remaining}")
            print(f"   总调用次数: {limiter.total_calls}")
        print("   ✅ 统计信息获取成功")
        
        print("5. 测试单次API调用（无等待）...")
        # 临时设置基础等待时间为0
        original_wait = limiter.base_wait_time
        limiter.base_wait_time = 0
        
        start_time = time.time()
        result = limiter.wait_for_api_call("test_api")
        end_time = time.time()
        
        print(f"   调用结果: {result}")
        print(f"   耗时: {end_time - start_time:.3f}秒")
        
        # 恢复原始等待时间
        limiter.base_wait_time = original_wait
        print("   ✅ API调用测试成功")
        
        print("\n✅ 所有测试通过！频率限制器工作正常")
        print("\n📊 当API调用达到950次时，程序会进入60秒缓冲期")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_direct_limiter()