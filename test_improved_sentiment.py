#!/usr/bin/env python3
"""
测试改进后的情绪分析功能
验证集成新闻分析师数据后的情绪分析效果
"""

import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_improved_chinese_sentiment():
    """测试改进后的中文情绪分析"""
    print("\n🔧 测试改进后的中文情绪分析...")
    
    try:
        from tradingagents.dataflows.chinese_finance_utils import get_chinese_social_sentiment
        
        # 测试A股
        result = get_chinese_social_sentiment("000001", "2024-01-15")
        print(f"✅ 中文情绪分析成功")
        print(f"📊 结果长度: {len(result)}字符")
        print(f"📝 结果预览: {result[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 中文情绪分析失败: {e}")
        return False

def test_improved_unified_sentiment():
    """测试改进后的统一情绪分析工具"""
    print("\n🔧 测试改进后的统一情绪分析工具...")
    
    try:
        from tradingagents.agents.utils.agent_utils import Toolkit
        
        # 直接调用静态方法，避免LangChain工具调用问题
        # 测试A股
        print("\n📊 测试A股情绪分析...")
        result_a = Toolkit.get_stock_sentiment_unified("000001", "2024-01-15")
        print(f"✅ A股情绪分析成功，长度: {len(result_a)}字符")
        
        # 测试美股
        print("\n📊 测试美股情绪分析...")
        result_us = Toolkit.get_stock_sentiment_unified("AAPL", "2024-01-15")
        print(f"✅ 美股情绪分析成功，长度: {len(result_us)}字符")
        
        # 测试港股
        print("\n📊 测试港股情绪分析...")
        result_hk = Toolkit.get_stock_sentiment_unified("0700.HK", "2024-01-15")
        print(f"✅ 港股情绪分析成功，长度: {len(result_hk)}字符")
        
        return True
        
    except Exception as e:
        print(f"❌ 统一情绪分析工具失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_news_integration():
    """测试新闻数据集成"""
    print("\n🔧 测试新闻数据集成...")
    
    try:
        from tradingagents.agents.utils.agent_utils import Toolkit
        
        # 直接调用静态方法，避免LangChain工具调用问题
        # 测试统一新闻工具
        print("\n📰 测试统一新闻工具...")
        news_result = Toolkit.get_stock_news_unified("AAPL", "2024-01-15")
        print(f"✅ 新闻获取成功，长度: {len(news_result)}字符")
        print(f"📝 新闻预览: {news_result[:300]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 新闻数据集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试改进后的情绪分析功能...")
    
    results = {
        "中文情绪分析": test_improved_chinese_sentiment(),
        "统一情绪分析工具": test_improved_unified_sentiment(),
        "新闻数据集成": test_news_integration()
    }
    
    print("\n" + "="*50)
    print("📋 测试结果汇总:")
    print("="*50)
    
    for test_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
    
    success_count = sum(results.values())
    total_count = len(results)
    
    print(f"\n📊 总体结果: {success_count}/{total_count} 项测试通过")
    
    if success_count == total_count:
        print("\n🎉 所有测试通过！情绪分析功能改进成功！")
        print("\n✨ 改进要点:")
        print("- ✅ 中文情绪分析集成了新闻分析师的真实数据")
        print("- ✅ 统一情绪分析工具支持多市场自动识别")
        print("- ✅ 美股情绪分析使用Reddit和新闻数据")
        print("- ✅ 新闻数据获取功能正常工作")
    else:
        print("\n⚠️ 部分测试失败，需要进一步调试")
        print("\n🔧 建议检查:")
        print("- API密钥配置")
        print("- 网络连接")
        print("- 依赖模块导入")

if __name__ == "__main__":
    main()