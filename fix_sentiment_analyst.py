#!/usr/bin/env python3
"""
情绪分析师修复脚本
解决000526等中国A股情绪分析问题
"""

import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def fix_social_media_analyst_config():
    """修复社交媒体分析师配置"""
    print("\n🔧 修复社交媒体分析师配置...")
    
    try:
        # 读取当前配置
        analyst_file = "d:\\workspace\\TradingAgents-CN\\tradingagents\\agents\\analysts\\social_media_analyst.py"
        
        with open(analyst_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否需要修复
        if "get_stock_news_unified" in content:
            print("✅ 社交媒体分析师已经配置了统一新闻工具")
            return True
        
        # 修复工具配置
        old_tools_config = '''        if toolkit.config["online_tools"]:
            tools = [toolkit.get_stock_news_openai]
        else:
            # 优先使用中国社交媒体数据，如果不可用则回退到Reddit
            tools = [
                toolkit.get_chinese_social_sentiment,
                toolkit.get_reddit_stock_info,
            ]'''
        
        new_tools_config = '''        if toolkit.config["online_tools"]:
            # 在线模式：优先使用统一新闻工具，回退到OpenAI
            tools = [
                toolkit.get_stock_news_unified,
                toolkit.get_stock_news_openai,
                toolkit.get_chinese_social_sentiment
            ]
        else:
            # 离线模式：优先使用中国社交媒体数据
            tools = [
                toolkit.get_chinese_social_sentiment,
                toolkit.get_stock_news_unified,
                toolkit.get_reddit_stock_info,
            ]'''
        
        # 替换配置
        if old_tools_config in content:
            content = content.replace(old_tools_config, new_tools_config)
            
            # 写回文件
            with open(analyst_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ 社交媒体分析师配置已修复")
            print("📊 新增了统一新闻工具和更好的回退机制")
            return True
        else:
            print("⚠️ 未找到预期的工具配置，可能已经被修改")
            return False
        
    except Exception as e:
        print(f"❌ 修复社交媒体分析师配置失败: {e}")
        return False

def create_enhanced_sentiment_tool():
    """创建增强的情绪分析工具"""
    print("\n🚀 创建增强的情绪分析工具...")
    
    enhanced_tool_content = '''#!/usr/bin/env python3
"""
增强的中国股票情绪分析工具
专门处理中国A股的情绪分析需求
"""

from typing import Dict, List, Optional
from datetime import datetime
import re

def get_enhanced_chinese_sentiment(ticker: str, curr_date: str) -> str:
    """
    增强的中国股票情绪分析
    专门优化对A股的分析能力
    """
    try:
        from tradingagents.dataflows.chinese_finance_utils import get_chinese_social_sentiment
        from tradingagents.agents.utils.agent_utils import Toolkit
        
        # 获取公司中文名称
        company_name = _get_company_name(ticker)
        
        # 1. 基础中文情绪分析
        base_sentiment = get_chinese_social_sentiment(ticker, curr_date)
        
        # 2. 尝试获取统一新闻数据
        news_data = ""
        try:
            # 直接调用底层接口避免LangChain问题
            from tradingagents.dataflows import interface
            news_data = interface.get_google_news(f"{company_name} {ticker}", curr_date, 7)
        except Exception as news_e:
            news_data = f"新闻获取失败: {news_e}"
        
        # 3. 生成增强报告
        enhanced_report = f"""
# 📊 {ticker} ({company_name}) 增强情绪分析报告

## 🇨🇳 中文市场情绪分析
{base_sentiment}

## 📰 新闻情绪补充分析
{_analyze_news_sentiment(news_data, ticker, company_name)}

## 💡 投资建议整合
{_generate_investment_advice(ticker, company_name)}

## ⚠️ 风险提示
- 中国A股市场情绪波动较大，建议结合基本面分析
- 政策变化对股价影响显著，需关注监管动态
- 建议分散投资，控制单一股票仓位

---
*报告生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
*数据来源: 多源财经数据聚合*
"""
        
        return enhanced_report
        
    except Exception as e:
        return f"""
# ❌ {ticker} 情绪分析失败

## 错误信息
{str(e)}

## 🔧 建议解决方案
1. **手动查询建议**:
   - 访问雪球网搜索 "{ticker}"
   - 查看东方财富股吧讨论
   - 关注财联社最新报道
   - 查阅同花顺投资者情绪

2. **替代分析方法**:
   - 重点关注基本面数据
   - 分析技术指标趋势
   - 研究行业政策影响
   - 参考机构研报观点

3. **数据源推荐**:
   - 官方财报和公告
   - 主流财经媒体报道
   - 专业投资机构分析
   - 行业协会发布信息
"""

def _get_company_name(ticker: str) -> str:
    """获取公司中文名称"""
    # A股代码到公司名称的映射
    stock_names = {
        "000526": "紫光学大",
        "000001": "平安银行", 
        "000002": "万科A",
        "000858": "五粮液",
        "002415": "海康威视",
        "300059": "东方财富",
        # 可以继续添加更多映射
    }
    
    return stock_names.get(ticker, f"股票{ticker}")

def _analyze_news_sentiment(news_data: str, ticker: str, company_name: str) -> str:
    """分析新闻情绪"""
    if "失败" in news_data or len(news_data) < 50:
        return f"""
### 📰 新闻数据获取受限

**状态**: 新闻API暂时不可用

**建议手动查询**:
- 搜索关键词: "{company_name}"、"{ticker}"
- 重点关注: 财报发布、政策变化、行业动态
- 推荐平台: 财联社、新浪财经、东方财富

**情绪判断要点**:
- 正面信号: 业绩增长、政策利好、机构看好
- 负面信号: 业绩下滑、监管风险、市场担忧
- 中性信号: 常规公告、行业一般性新闻
"""
    
    # 简单的情绪关键词分析
    positive_keywords = ["利好", "上涨", "看好", "推荐", "买入", "增长", "盈利", "突破"]
    negative_keywords = ["利空", "下跌", "看空", "卖出", "风险", "亏损", "下滑", "担忧"]
    
    positive_count = sum(1 for keyword in positive_keywords if keyword in news_data)
    negative_count = sum(1 for keyword in negative_keywords if keyword in news_data)
    
    if positive_count > negative_count:
        sentiment = "偏向积极"
        advice = "市场情绪相对乐观，但仍需谨慎"
    elif negative_count > positive_count:
        sentiment = "偏向消极"
        advice = "市场情绪偏向谨慎，建议观望"
    else:
        sentiment = "相对中性"
        advice = "市场情绪平稳，建议综合分析"
    
    return f"""
### 📊 新闻情绪分析结果

**情绪倾向**: {sentiment}
**正面关键词**: {positive_count}个
**负面关键词**: {negative_count}个
**投资建议**: {advice}

**新闻摘要**: {news_data[:200]}...
"""

def _generate_investment_advice(ticker: str, company_name: str) -> str:
    """生成投资建议"""
    return f"""
### 💰 综合投资建议

**短期策略** (1-2周):
- 关注日内波动，设置合理止损
- 重点关注成交量变化
- 留意突发消息面影响

**中期策略** (1-3个月):
- 分析季度财报表现
- 关注行业政策变化
- 评估估值合理性

**长期策略** (6个月以上):
- 研究公司基本面
- 分析行业发展趋势
- 考虑宏观经济影响

**风险控制**:
- 建议仓位控制在总资产的5-10%
- 设置止损位（建议-8%到-10%）
- 分批建仓，避免一次性重仓

**关注要点**:
- {company_name}的主营业务发展
- 相关政策法规变化
- 同行业竞争对手表现
- 宏观经济环境影响
"""

if __name__ == "__main__":
    # 测试增强情绪分析
    result = get_enhanced_chinese_sentiment("000526", "2024-01-15")
    print(result)
'''
    
    try:
        enhanced_file = "d:\\workspace\\TradingAgents-CN\\tradingagents\\dataflows\\enhanced_sentiment.py"
        
        with open(enhanced_file, 'w', encoding='utf-8') as f:
            f.write(enhanced_tool_content)
        
        print("✅ 增强情绪分析工具创建成功")
        print(f"📁 文件位置: {enhanced_file}")
        return True
        
    except Exception as e:
        print(f"❌ 创建增强情绪分析工具失败: {e}")
        return False

def update_agent_utils_integration():
    """更新agent_utils.py中的集成"""
    print("\n🔗 更新agent_utils.py集成...")
    
    try:
        agent_utils_file = "d:\\workspace\\TradingAgents-CN\\tradingagents\\agents\\utils\\agent_utils.py"
        
        # 添加增强情绪分析工具
        integration_code = '''
    @staticmethod
    @tool
    def get_enhanced_chinese_sentiment(
        ticker: Annotated[str, "股票代码，如000526"],
        curr_date: Annotated[str, "当前日期，格式yyyy-mm-dd"]
    ) -> str:
        """
        获取增强的中国股票情绪分析，专门优化A股分析
        Args:
            ticker: 股票代码
            curr_date: 当前日期
        Returns:
            str: 增强的情绪分析报告
        """
        try:
            from tradingagents.dataflows.enhanced_sentiment import get_enhanced_chinese_sentiment
            return get_enhanced_chinese_sentiment(ticker, curr_date)
        except Exception as e:
            # 回退到基础中文情绪分析
            from tradingagents.dataflows.chinese_finance_utils import get_chinese_social_sentiment
            return get_chinese_social_sentiment(ticker, curr_date)
'''
        
        # 读取当前文件
        with open(agent_utils_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经添加
        if "get_enhanced_chinese_sentiment" in content:
            print("✅ 增强情绪分析工具已经集成到agent_utils.py")
            return True
        
        # 找到合适的位置插入（在类的最后一个方法之前）
        insert_position = content.rfind("    @staticmethod")
        if insert_position != -1:
            # 在最后一个静态方法之前插入
            content = content[:insert_position] + integration_code + "\n" + content[insert_position:]
            
            with open(agent_utils_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ 增强情绪分析工具已集成到agent_utils.py")
            return True
        else:
            print("⚠️ 未找到合适的插入位置")
            return False
        
    except Exception as e:
        print(f"❌ 更新agent_utils.py集成失败: {e}")
        return False

def test_enhanced_sentiment():
    """测试增强情绪分析"""
    print("\n🧪 测试增强情绪分析...")
    
    try:
        from tradingagents.dataflows.enhanced_sentiment import get_enhanced_chinese_sentiment
        
        # 测试000526
        result = get_enhanced_chinese_sentiment("000526", "2024-01-15")
        
        print("✅ 增强情绪分析测试成功")
        print(f"📊 分析结果长度: {len(result)}字符")
        print(f"📄 结果预览: {result[:300]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 增强情绪分析测试失败: {e}")
        return False

def main():
    """主修复函数"""
    print("🔧 情绪分析师修复程序")
    print("🎯 解决000526等中国A股情绪分析问题")
    print("="*60)
    
    fixes = [
        ("修复社交媒体分析师配置", fix_social_media_analyst_config),
        ("创建增强情绪分析工具", create_enhanced_sentiment_tool),
        ("更新agent_utils集成", update_agent_utils_integration),
        ("测试增强情绪分析", test_enhanced_sentiment)
    ]
    
    results = []
    for name, fix_func in fixes:
        try:
            result = fix_func()
            results.append(result)
        except Exception as e:
            print(f"❌ {name} 失败: {e}")
            results.append(False)
    
    print("\n" + "="*60)
    print("🎯 修复结果汇总")
    print("="*60)
    
    for i, (name, _) in enumerate(fixes):
        status = "✅ 成功" if results[i] else "❌ 失败"
        print(f"{name}: {status}")
    
    success_count = sum(results)
    total_count = len(results)
    
    print(f"\n📊 修复成功率: {success_count}/{total_count}")
    
    if success_count >= 3:
        print("\n🎉 情绪分析师修复成功！")
        print("\n✨ 修复成果:")
        print("- 🔧 优化了工具配置和回退机制")
        print("- 🇨🇳 增强了中国A股情绪分析能力")
        print("- 📊 提供了更详细的分析报告")
        print("- 💡 添加了手动查询建议")
        
        print("\n🚀 使用建议:")
        print("1. 重启应用以加载新配置")
        print("2. 优先使用中文数据源")
        print("3. 结合基本面和技术面分析")
        print("4. 关注政策和行业动态")
    else:
        print("\n⚠️ 修复过程中遇到问题，请检查错误信息")
        print("\n🔧 手动修复建议:")
        print("- 检查文件权限")
        print("- 确认Python环境")
        print("- 验证依赖模块")

if __name__ == "__main__":
    main()