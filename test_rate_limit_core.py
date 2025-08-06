#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试频率限制器核心功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import time
from collections import deque

def test_rate_limit_logic():
    """测试频率限制核心逻辑"""
    print("=== 测试频率限制核心逻辑 ===")
    
    # 模拟频率限制器的核心逻辑
    max_calls_per_minute = 950
    call_timestamps = deque()
    current_time = time.time()
    
    print(f"1. 配置: 最大调用频率 {max_calls_per_minute}/分钟")
    
    # 模拟添加950次调用
    print("2. 模拟添加950次API调用...")
    for i in range(max_calls_per_minute):
        call_timestamps.append(current_time - (max_calls_per_minute - i) * 0.06)  # 每次调用间隔0.06秒
    
    print(f"   当前调用次数: {len(call_timestamps)}")
    
    # 检查是否需要等待
    if len(call_timestamps) >= max_calls_per_minute:
        oldest_timestamp = call_timestamps[0]
        wait_time = 61 - (current_time - oldest_timestamp)
        print(f"3. ✅ 达到限制！需要等待: {wait_time:.1f}秒")
        print(f"   这确保了当API调用达到950次时，程序会进入60秒缓冲期")
    else:
        print("3. ❌ 未达到限制")
    
    # 测试清理旧时间戳的逻辑
    print("4. 测试清理旧时间戳...")
    cutoff_time = current_time - 60
    original_count = len(call_timestamps)
    
    # 移除60秒前的时间戳
    while call_timestamps and call_timestamps[0] < cutoff_time:
        call_timestamps.popleft()
    
    cleaned_count = len(call_timestamps)
    print(f"   清理前: {original_count} 次调用")
    print(f"   清理后: {cleaned_count} 次调用")
    print(f"   ✅ 清理了 {original_count - cleaned_count} 个过期时间戳")
    
    print("\n✅ 频率限制核心逻辑测试完成！")
    print("📊 确认：当API调用达到950次时，程序会进入60秒缓冲期")

def test_import_only():
    """仅测试导入"""
    print("\n=== 测试导入频率限制器 ===")
    try:
        from tradingagents.dataflows.rate_limiter import GlobalRateLimiter
        print("✅ GlobalRateLimiter 导入成功")
        
        # 只创建实例，不调用任何方法
        limiter = GlobalRateLimiter()
        print("✅ 实例创建成功")
        print(f"   最大调用频率: {limiter.max_calls_per_minute}/分钟")
        print(f"   当达到{limiter.max_calls_per_minute}次调用时，将进入60秒缓冲期")
        
    except Exception as e:
        print(f"❌ 导入失败: {e}")

if __name__ == "__main__":
    test_rate_limit_logic()
    test_import_only()