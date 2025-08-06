#!/usr/bin/env python3
"""
API频率限制管理器
实现全局API调用计数器和精确的分钟级频率监控
"""

import time
import threading
from collections import deque
from datetime import datetime, timedelta
from typing import Dict, Optional

from tradingagents.utils.logging_manager import get_logger
logger = get_logger('agents')


class GlobalRateLimiter:
    """全局API频率限制器"""
    
    def __init__(self, max_calls_per_minute: int = 950, safety_margin: int = 50):
        """
        初始化全局频率限制器
        
        Args:
            max_calls_per_minute: 每分钟最大调用次数（默认950，为Tushare 1000次/分钟留出安全边距）
            safety_margin: 安全边距，当接近限制时提前降速
        """
        self.max_calls_per_minute = max_calls_per_minute
        self.safety_margin = safety_margin
        self.warning_threshold = max_calls_per_minute - safety_margin
        
        # 使用deque存储调用时间戳，自动维护1分钟窗口
        self.call_timestamps = deque()
        self.lock = threading.Lock()
        
        # 动态调整的等待时间
        self.base_wait_time = 0.5  # 基础等待时间（秒）
        self.current_wait_time = self.base_wait_time
        
        # 统计信息
        self.total_calls = 0
        self.blocked_calls = 0
        self.last_reset_time = time.time()
        
        logger.info(f"📊 全局API频率限制器初始化完成")
        logger.info(f"   最大调用频率: {max_calls_per_minute}/分钟")
        logger.info(f"   警告阈值: {self.warning_threshold}/分钟")
        logger.info(f"   基础等待时间: {self.base_wait_time}秒")
    
    def _cleanup_old_timestamps(self):
        """清理超过1分钟的时间戳"""
        current_time = time.time()
        cutoff_time = current_time - 60  # 1分钟前
        
        while self.call_timestamps and self.call_timestamps[0] < cutoff_time:
            self.call_timestamps.popleft()
    
    def get_current_call_count(self) -> int:
        """获取当前1分钟内的调用次数"""
        with self.lock:
            self._cleanup_old_timestamps()
            return len(self.call_timestamps)
    
    def get_remaining_calls(self) -> int:
        """获取当前分钟内剩余可调用次数"""
        current_count = self.get_current_call_count()
        return max(0, self.max_calls_per_minute - current_count)
    
    def calculate_dynamic_wait_time(self, current_count: int = None) -> float:
        """根据当前调用频率动态计算等待时间"""
        if current_count is None:
            current_count = self.get_current_call_count()
        
        if current_count >= self.max_calls_per_minute:
            # 已达到限制，等待到下一分钟
            oldest_timestamp = self.call_timestamps[0] if self.call_timestamps else time.time()
            wait_time = 61 - (time.time() - oldest_timestamp)  # 等待到最老调用过期+1秒
            return max(wait_time, 1.0)
        
        elif current_count >= self.warning_threshold:
            # 接近限制，大幅增加等待时间
            progress = (current_count - self.warning_threshold) / self.safety_margin
            wait_time = self.base_wait_time * (1 + progress * 10)  # 最多增加10倍
            return min(wait_time, 30.0)  # 最大等待30秒
        
        elif current_count >= self.warning_threshold * 0.7:
            # 中等负载，适度增加等待时间
            progress = (current_count - self.warning_threshold * 0.7) / (self.warning_threshold * 0.3)
            wait_time = self.base_wait_time * (1 + progress * 2)  # 最多增加2倍
            return wait_time
        
        else:
            # 低负载，使用基础等待时间
            return self.base_wait_time
    
    def wait_for_api_call(self, api_name: str = "unknown") -> bool:
        """
        等待API调用许可
        
        Args:
            api_name: API名称，用于日志记录
            
        Returns:
            bool: True表示可以调用，False表示被阻止
        """
        # 初始化变量
        need_long_wait = False
        long_wait_time = 0
        wait_time = self.base_wait_time
        
        # 第一步：检查当前状态
        with self.lock:
            current_time = time.time()
            self._cleanup_old_timestamps()
            
            current_count = len(self.call_timestamps)
            remaining_calls = self.max_calls_per_minute - current_count
            
            # 记录调用统计
            self.total_calls += 1
            
            # 检查是否需要长时间等待
            need_long_wait = current_count >= self.max_calls_per_minute
            if need_long_wait:
                self.blocked_calls += 1
                oldest_timestamp = self.call_timestamps[0] if self.call_timestamps else current_time
                long_wait_time = 61 - (current_time - oldest_timestamp)
                
                logger.warning(f"🚫 API调用频率已达限制 ({current_count}/{self.max_calls_per_minute})")
                logger.warning(f"   API: {api_name}")
                logger.warning(f"   等待时间: {long_wait_time:.1f}秒")
        
        # 第二步：如果需要长时间等待，释放锁后等待
        if need_long_wait:
            time.sleep(max(long_wait_time, 1.0))
        
        # 第三步：重新获取锁，记录调用并计算短等待
        with self.lock:
            current_time = time.time()
            self._cleanup_old_timestamps()
            current_count = len(self.call_timestamps)
            remaining_calls = self.max_calls_per_minute - current_count
            
            # 动态计算等待时间（传入current_count避免重复获取锁）
            wait_time = self.calculate_dynamic_wait_time(current_count)
            
            # 记录调用
            self.call_timestamps.append(current_time)
            
            # 日志记录
            if current_count >= self.warning_threshold:
                logger.warning(f"⚠️ API调用频率接近限制 ({current_count}/{self.max_calls_per_minute})")
                logger.warning(f"   API: {api_name}")
                logger.warning(f"   剩余调用: {remaining_calls}")
                logger.warning(f"   动态等待: {wait_time:.1f}秒")
            elif current_count % 100 == 0:  # 每100次调用记录一次
                logger.info(f"📊 API调用统计: {current_count}/{self.max_calls_per_minute} (剩余: {remaining_calls})")
        
        # 第四步：应用等待时间（在锁外进行）
        if wait_time > self.base_wait_time:
            time.sleep(wait_time)
        else:
            time.sleep(self.base_wait_time)
        
        return True
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        with self.lock:
            self._cleanup_old_timestamps()
            current_time = time.time()
            uptime = current_time - self.last_reset_time
            current_count = len(self.call_timestamps)
            remaining_calls = max(0, self.max_calls_per_minute - current_count)
            
            return {
                'current_calls_per_minute': current_count,
                'max_calls_per_minute': self.max_calls_per_minute,
                'remaining_calls': remaining_calls,
                'total_calls': self.total_calls,
                'blocked_calls': self.blocked_calls,
                'current_wait_time': self.current_wait_time,
                'uptime_seconds': uptime,
                'calls_per_second': self.total_calls / uptime if uptime > 0 else 0
            }
    
    def reset_statistics(self):
        """重置统计信息"""
        with self.lock:
            self.total_calls = 0
            self.blocked_calls = 0
            self.last_reset_time = time.time()
            logger.info("📊 API频率限制器统计信息已重置")


# 全局实例
_global_rate_limiter: Optional[GlobalRateLimiter] = None
_limiter_lock = threading.Lock()


def get_global_rate_limiter() -> GlobalRateLimiter:
    """获取全局频率限制器实例"""
    global _global_rate_limiter
    
    if _global_rate_limiter is None:
        with _limiter_lock:
            if _global_rate_limiter is None:
                _global_rate_limiter = GlobalRateLimiter()
    
    return _global_rate_limiter


def wait_for_tushare_api(api_name: str = "tushare") -> bool:
    """Tushare API调用前的频率控制"""
    limiter = get_global_rate_limiter()
    return limiter.wait_for_api_call(api_name)


def get_api_statistics() -> Dict:
    """获取API调用统计信息"""
    limiter = get_global_rate_limiter()
    return limiter.get_statistics()


def reset_api_statistics():
    """重置API调用统计信息"""
    limiter = get_global_rate_limiter()
    limiter.reset_statistics()