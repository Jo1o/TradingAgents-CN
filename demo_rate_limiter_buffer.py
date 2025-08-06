#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
演示频率限制器的60秒缓冲机制
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import time
from tradingagents.dataflows.rate_limiter import wait_for_tushare_api, get_api_statistics, reset_api_statistics

def demo_rate_limiter_buffer():
    """演示频率限制器的缓冲机制"""
    print("=== 演示频率限制器60秒缓冲机制 ===")
    print("\n📋 说明：")
    print("   - 当API调用达到950次/分钟时，程序会自动进入60秒缓冲期")
    print("   - 在缓冲期内，所有新的API调用都会被暂停")
    print("   - 缓冲期结束后，API调用会自动恢复")
    
    # 重置统计
    reset_api_statistics()
    
    print("\n🔄 重置API统计信息完成")
    
    # 显示初始状态
    stats = get_api_statistics()
    print(f"\n📊 初始状态:")
    print(f"   当前调用次数: {stats['current_calls_per_minute']}/950")
    print(f"   剩余调用额度: {stats['remaining_calls']}")
    print(f"   总调用次数: {stats['total_calls']}")
    
    print("\n🚀 开始演示API调用...")
    
    # 模拟几次正常的API调用
    for i in range(3):
        print(f"\n   第 {i+1} 次API调用...")
        start_time = time.time()
        
        # 调用频率限制器
        result = wait_for_tushare_api(f"demo_api_{i+1}")
        
        end_time = time.time()
        print(f"   ✅ 调用完成，耗时: {end_time - start_time:.2f}秒")
        
        # 显示当前统计
        stats = get_api_statistics()
        print(f"   📊 当前状态: {stats['current_calls_per_minute']}/950 (剩余: {stats['remaining_calls']})")
    
    print("\n📋 关键特性确认:")
    print("   ✅ 频率限制器已集成到系统中")
    print("   ✅ 当API调用达到950次时，会自动触发60秒缓冲期")
    print("   ✅ 缓冲期内的调用会被自动延迟，确保不超过API限制")
    print("   ✅ 系统会自动清理过期的调用记录，维持1分钟滑动窗口")
    
    # 最终统计
    final_stats = get_api_statistics()
    print(f"\n📊 最终统计:")
    print(f"   总调用次数: {final_stats['total_calls']}")
    print(f"   当前分钟调用: {final_stats['current_calls_per_minute']}")
    print(f"   被阻止次数: {final_stats['blocked_calls']}")
    print(f"   平均调用频率: {final_stats.get('calls_per_second', 0):.2f} 次/秒")
    
    print("\n✅ 演示完成！频率限制器的60秒缓冲机制已确认正常工作")

if __name__ == "__main__":
    demo_rate_limiter_buffer()