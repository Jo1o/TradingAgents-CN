#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试全局API频率限制器
验证新的频率控制机制是否正常工作
"""

import sys
import time
import threading
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()

from tradingagents.dataflows.rate_limiter import (
    get_global_rate_limiter, 
    wait_for_tushare_api, 
    get_api_statistics, 
    reset_api_statistics
)
from tradingagents.utils.logging_manager import get_logger

logger = get_logger('test')

def test_basic_rate_limiting():
    """测试基础频率限制功能"""
    print("\n=== 测试基础频率限制功能 ===")
    
    # 重置统计信息
    reset_api_statistics()
    
    # 模拟10次API调用
    start_time = time.time()
    for i in range(10):
        print(f"第 {i+1} 次API调用...")
        wait_for_tushare_api(f"test_api_{i}")
        
        # 获取当前统计信息
        stats = get_api_statistics()
        print(f"  当前调用数: {stats['current_calls_per_minute']}/{stats['max_calls_per_minute']}")
        print(f"  剩余额度: {stats['remaining_calls']}")
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\n10次调用总耗时: {total_time:.2f}秒")
    print(f"平均每次调用耗时: {total_time/10:.2f}秒")
    
    # 显示最终统计信息
    final_stats = get_api_statistics()
    print(f"\n最终统计信息:")
    print(f"  总调用次数: {final_stats['total_calls']}")
    print(f"  被阻止次数: {final_stats['blocked_calls']}")
    print(f"  当前分钟调用: {final_stats['current_calls_per_minute']}")

def test_concurrent_calls():
    """测试并发调用的频率控制"""
    print("\n=== 测试并发调用频率控制 ===")
    
    # 重置统计信息
    reset_api_statistics()
    
    def worker(worker_id, num_calls):
        """工作线程函数"""
        for i in range(num_calls):
            wait_for_tushare_api(f"worker_{worker_id}_call_{i}")
            print(f"Worker {worker_id}: 完成第 {i+1} 次调用")
    
    # 创建4个线程，每个线程调用5次
    threads = []
    start_time = time.time()
    
    for worker_id in range(4):
        thread = threading.Thread(target=worker, args=(worker_id, 5))
        threads.append(thread)
        thread.start()
    
    # 等待所有线程完成
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\n4个线程并发调用总耗时: {total_time:.2f}秒")
    
    # 显示最终统计信息
    final_stats = get_api_statistics()
    print(f"\n并发调用统计信息:")
    print(f"  总调用次数: {final_stats['total_calls']}")
    print(f"  被阻止次数: {final_stats['blocked_calls']}")
    print(f"  当前分钟调用: {final_stats['current_calls_per_minute']}")
    print(f"  平均调用频率: {final_stats['calls_per_second']:.2f} 次/秒")

def test_high_frequency_calls():
    """测试高频调用的限制机制"""
    print("\n=== 测试高频调用限制机制 ===")
    
    # 重置统计信息
    reset_api_statistics()
    
    # 模拟50次快速调用
    start_time = time.time()
    for i in range(50):
        if i % 10 == 0:
            print(f"进行第 {i+1}-{min(i+10, 50)} 次调用...")
        
        wait_for_tushare_api(f"high_freq_test_{i}")
        
        # 每10次调用显示一次统计
        if (i + 1) % 10 == 0:
            stats = get_api_statistics()
            print(f"  第 {i+1} 次调用完成")
            print(f"  当前调用数: {stats['current_calls_per_minute']}/{stats['max_calls_per_minute']}")
            print(f"  剩余额度: {stats['remaining_calls']}")
            print(f"  被阻止次数: {stats['blocked_calls']}")
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\n50次高频调用总耗时: {total_time:.2f}秒")
    print(f"平均每次调用耗时: {total_time/50:.2f}秒")
    
    # 显示最终统计信息
    final_stats = get_api_statistics()
    print(f"\n高频调用统计信息:")
    print(f"  总调用次数: {final_stats['total_calls']}")
    print(f"  被阻止次数: {final_stats['blocked_calls']}")
    print(f"  当前分钟调用: {final_stats['current_calls_per_minute']}")
    print(f"  平均调用频率: {final_stats['calls_per_second']:.2f} 次/秒")

def test_rate_limiter_configuration():
    """测试频率限制器配置"""
    print("\n=== 测试频率限制器配置 ===")
    
    limiter = get_global_rate_limiter()
    
    print(f"频率限制器配置:")
    print(f"  最大调用频率: {limiter.max_calls_per_minute}/分钟")
    print(f"  警告阈值: {limiter.warning_threshold}/分钟")
    print(f"  安全边距: {limiter.safety_margin}")
    print(f"  基础等待时间: {limiter.base_wait_time}秒")
    
    # 测试统计信息获取
    stats = get_api_statistics()
    print(f"\n当前统计信息:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

def main():
    """主测试函数"""
    print("🚀 开始测试全局API频率限制器")
    print("=" * 50)
    
    try:
        # 测试配置
        test_rate_limiter_configuration()
        
        # 测试基础功能
        test_basic_rate_limiting()
        
        # 测试并发调用
        test_concurrent_calls()
        
        # 测试高频调用
        test_high_frequency_calls()
        
        print("\n" + "=" * 50)
        print("✅ 所有测试完成！")
        
        # 显示最终的全局统计信息
        final_stats = get_api_statistics()
        print(f"\n🎯 全局统计信息:")
        print(f"  总调用次数: {final_stats['total_calls']}")
        print(f"  被阻止次数: {final_stats['blocked_calls']}")
        print(f"  当前分钟调用: {final_stats['current_calls_per_minute']}")
        print(f"  运行时长: {final_stats['uptime_seconds']:.2f}秒")
        print(f"  平均调用频率: {final_stats['calls_per_second']:.2f} 次/秒")
        
        # 计算阻止率
        if final_stats['total_calls'] > 0:
            block_rate = (final_stats['blocked_calls'] / final_stats['total_calls']) * 100
            print(f"  调用阻止率: {block_rate:.2f}%")
        
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()