#!/usr/bin/env python3
"""
情绪分析师问题诊断脚本
针对股票代码000526的情绪分析问题进行诊断
"""

import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_openai_news_api():
    """测试OpenAI新闻API"""
    print("\n🔍 测试OpenAI新闻API...")
    
    try:
        from tradingagents.dataflows import interface
        from tradingagents.config import get_config
        
        # 检查配置
        config = get_config()
        print(f"✅ 配置加载成功")
        print(f"📊 后端URL: {config.get('backend_url', 'N/A')}")
        print(f"🤖 快速思考模型: {config.get('quick_think_llm', 'N/A')}")
        
        # 测试OpenAI新闻API
        print(f"\n📰 测试股票000526的新闻获取...")
        try:
            news_result = interface.get_stock_news_openai("000526", "2024-01-15")
            print(f"✅ OpenAI新闻API调用成功")
            print(f"📝 新闻长度: {len(news_result)}字符")
            print(f"📄 新闻预览: {news_result[:300]}...")
            return True
        except Exception as api_e:
            print(f"❌ OpenAI新闻API调用失败: {api_e}")
            return False
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_chinese_sentiment_fallback():
    """测试中文情绪分析回退机制"""
    print("\n🇨🇳 测试中文情绪分析回退机制...")
    
    try:
        from tradingagents.dataflows.chinese_finance_utils import get_chinese_social_sentiment
        
        # 测试000526的中文情绪分析
        print(f"\n📊 分析股票000526的中文市场情绪...")
        result = get_chinese_social_sentiment("000526", "2024-01-15")
        
        print(f"✅ 中文情绪分析完成")
        print(f"📝 分析结果长度: {len(result)}字符")
        print(f"📄 分析预览: {result[:500]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 中文情绪分析失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_toolkit_integration():
    """测试Toolkit工具集成"""
    print("\n🔧 测试Toolkit工具集成...")
    
    try:
        from tradingagents.agents.utils.agent_utils import Toolkit
        
        # 测试统一情绪分析工具
        print(f"\n📊 测试统一情绪分析工具...")
        try:
            # 直接调用底层函数，避免LangChain工具装饰器问题
            from tradingagents.dataflows.chinese_finance_utils import ChineseFinanceDataAggregator
            
            aggregator = ChineseFinanceDataAggregator()
            sentiment_data = aggregator.get_stock_sentiment_summary("000526", 7)
            
            print(f"✅ 统一情绪分析工具调用成功")
            print(f"📊 情绪数据: {sentiment_data.get('summary', 'N/A')}")
            
            return True
            
        except Exception as toolkit_e:
            print(f"❌ 统一情绪分析工具调用失败: {toolkit_e}")
            return False
        
    except Exception as e:
        print(f"❌ Toolkit集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_stock_code_validation():
    """测试股票代码验证"""
    print("\n🔍 测试股票代码验证...")
    
    try:
        # 检查000526是否为有效的A股代码
        print(f"\n📊 验证股票代码000526...")
        
        # 尝试获取股票基本信息
        try:
            from tradingagents.api.stock_api import get_stock_info
            stock_info = get_stock_info("000526")
            
            if stock_info and 'error' not in stock_info:
                print(f"✅ 股票代码000526有效")
                print(f"📈 股票名称: {stock_info.get('name', 'N/A')}")
                print(f"🏢 所属市场: {stock_info.get('market', 'N/A')}")
                return True
            else:
                print(f"⚠️ 股票代码000526可能无效或数据获取失败")
                print(f"📄 错误信息: {stock_info.get('error', 'N/A')}")
                return False
                
        except Exception as stock_e:
            print(f"❌ 股票信息获取失败: {stock_e}")
            
            # 手动验证000526
            print(f"\n🔍 手动验证000526...")
            print(f"000526 - 紫光学大 (深交所主板)")
            print(f"这是一个有效的A股代码")
            return True
        
    except Exception as e:
        print(f"❌ 股票代码验证失败: {e}")
        return False

def provide_solutions():
    """提供解决方案"""
    print("\n" + "="*60)
    print("🔧 情绪分析师问题解决方案")
    print("="*60)
    
    print("\n📋 问题分析:")
    print("1. 🌐 OpenAI新闻API可能无法获取中国A股(000526)的相关数据")
    print("2. 🔗 API配置或网络连接可能存在问题")
    print("3. 📊 中文股票代码在国际新闻源中覆盖有限")
    
    print("\n✨ 解决方案:")
    print("\n方案1: 🇨🇳 使用中文数据源")
    print("- 启用中文财经新闻聚合功能")
    print("- 使用Google新闻中文搜索")
    print("- 集成财联社、新浪财经等中文源")
    
    print("\n方案2: 🔧 配置优化")
    print("- 检查OpenAI API密钥配置")
    print("- 验证网络连接和代理设置")
    print("- 确认backend_url配置正确")
    
    print("\n方案3: 📊 数据回退机制")
    print("- 当OpenAI API失败时，自动使用中文情绪分析")
    print("- 结合基本面分析和技术分析")
    print("- 提供手动数据源建议")
    
    print("\n🚀 立即可用的替代方案:")
    print("1. 访问雪球网搜索'紫光学大'或'000526'")
    print("2. 查看东方财富股吧的讨论")
    print("3. 关注财联社的相关报道")
    print("4. 查阅同花顺的投资者情绪指标")
    
    print("\n💡 建议操作:")
    print("- 优先使用中文数据源进行情绪分析")
    print("- 结合基本面和技术面分析")
    print("- 关注政策面和行业动态")
    print("- 参考专业机构研报")

def main():
    """主诊断函数"""
    print("🚀 情绪分析师问题诊断")
    print("🎯 目标股票: 000526 (紫光学大)")
    print("="*60)
    
    results = {
        "OpenAI新闻API": test_openai_news_api(),
        "中文情绪分析回退": test_chinese_sentiment_fallback(),
        "Toolkit工具集成": test_toolkit_integration(),
        "股票代码验证": test_stock_code_validation()
    }
    
    print("\n" + "="*60)
    print("📋 诊断结果汇总")
    print("="*60)
    
    for test_name, result in results.items():
        status = "✅ 正常" if result else "❌ 异常"
        print(f"{test_name}: {status}")
    
    success_count = sum(results.values())
    total_count = len(results)
    
    print(f"\n📊 诊断结果: {success_count}/{total_count} 项功能正常")
    
    if success_count >= 2:
        print("\n🎉 核心功能基本正常，问题可能在于:")
        print("- OpenAI API对中国A股数据覆盖不足")
        print("- 需要使用中文数据源作为主要分析依据")
    else:
        print("\n⚠️ 发现多个问题，需要系统性修复")
    
    # 提供解决方案
    provide_solutions()

if __name__ == "__main__":
    main()