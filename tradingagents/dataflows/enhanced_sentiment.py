#!/usr/bin/env python3
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
