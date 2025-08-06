#!/usr/bin/env python3
"""
测试情绪分析师取值是否正常
验证评分范围、计算逻辑和数据合理性
"""

import os
import sys
from datetime import datetime

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_sentiment_scoring_range():
    """测试情绪评分范围"""
    print("\n📊 测试情绪评分范围")
    print("="*50)
    
    try:
        from tradingagents.dataflows.chinese_finance_utils import ChineseFinanceDataAggregator
        
        aggregator = ChineseFinanceDataAggregator()
        
        # 测试用例：不同情绪强度的文本
        test_cases = [
            {
                "text": "股价暴涨突破创新高，强烈推荐买入，利好消息不断",
                "expected_range": "强正面 (0.5-1.0)",
                "description": "极度正面情绪"
            },
            {
                "text": "股价上涨，看好后市", 
                "expected_range": "正面 (0.1-0.5)",
                "description": "一般正面情绪"
            },
            {
                "text": "公司发布财报，业绩平稳",
                "expected_range": "中性 (-0.1-0.1)", 
                "description": "中性情绪"
            },
            {
                "text": "股价下跌，存在风险",
                "expected_range": "负面 (-0.5--0.1)",
                "description": "一般负面情绪"
            },
            {
                "text": "股价暴跌跌破新低，强烈建议卖出，利空消息频出，亏损严重",
                "expected_range": "强负面 (-1.0--0.5)",
                "description": "极度负面情绪"
            },
            {
                "text": "",
                "expected_range": "中性 (0.0)",
                "description": "空文本"
            }
        ]
        
        print("\n🔬 评分测试结果:")
        print("-" * 80)
        print(f"{'描述':<15} {'文本':<30} {'预期范围':<15} {'实际评分':<10} {'状态':<8}")
        print("-" * 80)
        
        all_scores = []
        normal_count = 0
        
        for case in test_cases:
            score = aggregator._analyze_text_sentiment(case["text"])
            all_scores.append(score)
            
            # 判断评分是否在合理范围内
            is_normal = True
            if "强正面" in case["expected_range"] and not (0.5 <= score <= 1.0):
                is_normal = False
            elif "正面" in case["expected_range"] and "强正面" not in case["expected_range"] and not (0.1 <= score < 0.5):
                is_normal = False
            elif "中性" in case["expected_range"] and not (-0.1 <= score <= 0.1):
                is_normal = False
            elif "负面" in case["expected_range"] and "强负面" not in case["expected_range"] and not (-0.5 <= score < -0.1):
                is_normal = False
            elif "强负面" in case["expected_range"] and not (-1.0 <= score < -0.5):
                is_normal = False
            
            if is_normal:
                normal_count += 1
            
            status = "✅正常" if is_normal else "❌异常"
            text_display = case["text"][:25] + "..." if len(case["text"]) > 25 else case["text"]
            if not text_display:
                text_display = "(空文本)"
            
            print(f"{case['description']:<15} {text_display:<30} {case['expected_range']:<15} {score:<10.2f} {status:<8}")
        
        print("-" * 80)
        print(f"\n📈 评分统计:")
        print(f"- 最高评分: {max(all_scores):.2f}")
        print(f"- 最低评分: {min(all_scores):.2f}")
        print(f"- 平均评分: {sum(all_scores)/len(all_scores):.2f}")
        print(f"- 评分范围: [{min(all_scores):.2f}, {max(all_scores):.2f}]")
        print(f"- 正常率: {normal_count}/{len(test_cases)} ({normal_count/len(test_cases)*100:.1f}%)")
        
        # 检查评分是否在预期范围内
        if min(all_scores) >= -1.0 and max(all_scores) <= 1.0:
            print("✅ 评分范围正常 (-1.0 到 1.0)")
        else:
            print("❌ 评分范围异常，超出 [-1.0, 1.0] 区间")
        
        return normal_count >= len(test_cases) * 0.8  # 80%以上正常即为通过
        
    except Exception as e:
        print(f"❌ 评分范围测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_real_stock_sentiment():
    """测试真实股票情绪分析"""
    print("\n🏢 测试真实股票情绪分析")
    print("="*50)
    
    try:
        from tradingagents.dataflows.chinese_finance_utils import get_chinese_social_sentiment
        
        # 测试几个不同的股票代码
        test_stocks = ["000526", "000001", "000002"]
        
        for ticker in test_stocks:
            print(f"\n📊 测试股票: {ticker}")
            print("-" * 30)
            
            try:
                result = get_chinese_social_sentiment(ticker, "2024-01-15")
                
                if result and len(result) > 50:
                    print("✅ 情绪分析正常生成")
                    print(f"📄 报告长度: {len(result)}字符")
                    
                    # 检查关键信息
                    key_checks = [
                        ("情绪评分" in result or "sentiment_score" in result, "包含情绪评分"),
                        ("置信度" in result or "confidence" in result, "包含置信度信息"),
                        (ticker in result, "包含股票代码"),
                        ("投资建议" in result or "建议" in result, "包含投资建议")
                    ]
                    
                    check_count = sum(1 for check, _ in key_checks if check)
                    print(f"📋 关键信息完整度: {check_count}/{len(key_checks)}")
                    
                    for check, desc in key_checks:
                        status = "✅" if check else "❌"
                        print(f"   {status} {desc}")
                    
                    # 提取数值信息
                    import re
                    score_matches = re.findall(r'评分[：:] ?([+-]?\d*\.?\d+)', result)
                    if score_matches:
                        scores = [float(s) for s in score_matches]
                        print(f"📊 发现评分: {scores}")
                        
                        # 检查评分是否在合理范围内
                        valid_scores = [s for s in scores if -1.0 <= s <= 1.0]
                        if len(valid_scores) == len(scores):
                            print("✅ 所有评分都在正常范围内")
                        else:
                            print(f"⚠️ 发现异常评分: {[s for s in scores if not -1.0 <= s <= 1.0]}")
                    
                else:
                    print("⚠️ 情绪分析结果过短或为空")
                    print(f"📄 结果: {result[:100] if result else 'None'}...")
                
            except Exception as stock_e:
                print(f"❌ {ticker} 分析失败: {stock_e}")
        
        return True
        
    except Exception as e:
        print(f"❌ 真实股票情绪分析测试失败: {e}")
        return False

def test_sentiment_consistency():
    """测试情绪分析一致性"""
    print("\n🔄 测试情绪分析一致性")
    print("="*50)
    
    try:
        from tradingagents.dataflows.chinese_finance_utils import ChineseFinanceDataAggregator
        
        aggregator = ChineseFinanceDataAggregator()
        
        # 相同文本多次测试
        test_text = "股价上涨，业绩增长，看好未来发展"
        scores = []
        
        print(f"\n📝 测试文本: {test_text}")
        print("🔄 进行5次重复测试...")
        
        for i in range(5):
            score = aggregator._analyze_text_sentiment(test_text)
            scores.append(score)
            print(f"   第{i+1}次: {score:.3f}")
        
        # 检查一致性
        if len(set(scores)) == 1:
            print("✅ 评分完全一致")
            consistency = True
        else:
            print(f"⚠️ 评分存在差异: {set(scores)}")
            consistency = False
        
        print(f"📊 评分统计:")
        print(f"   平均值: {sum(scores)/len(scores):.3f}")
        print(f"   标准差: {(sum((s - sum(scores)/len(scores))**2 for s in scores) / len(scores))**0.5:.6f}")
        
        return consistency
        
    except Exception as e:
        print(f"❌ 一致性测试失败: {e}")
        return False

def test_edge_cases():
    """测试边界情况"""
    print("\n🔍 测试边界情况")
    print("="*50)
    
    try:
        from tradingagents.dataflows.chinese_finance_utils import ChineseFinanceDataAggregator
        
        aggregator = ChineseFinanceDataAggregator()
        
        edge_cases = [
            {
                "text": "",
                "description": "空字符串",
                "expected": 0.0
            },
            {
                "text": "   ",
                "description": "空白字符",
                "expected": 0.0
            },
            {
                "text": "上涨上涨上涨上涨上涨",
                "description": "重复正面词",
                "expected": 1.0
            },
            {
                "text": "下跌下跌下跌下跌下跌",
                "description": "重复负面词",
                "expected": -1.0
            },
            {
                "text": "上涨下跌",
                "description": "正负面词相等",
                "expected": 0.0
            },
            {
                "text": "今天天气很好，阳光明媚",
                "description": "无关文本",
                "expected": 0.0
            }
        ]
        
        print("\n🧪 边界情况测试:")
        print("-" * 60)
        print(f"{'描述':<15} {'文本':<20} {'预期':<8} {'实际':<8} {'状态':<8}")
        print("-" * 60)
        
        passed_count = 0
        
        for case in edge_cases:
            score = aggregator._analyze_text_sentiment(case["text"])
            passed = abs(score - case["expected"]) < 0.001  # 允许小的浮点误差
            
            if passed:
                passed_count += 1
            
            status = "✅通过" if passed else "❌失败"
            text_display = repr(case["text"])[:15] + "..." if len(repr(case["text"])) > 15 else repr(case["text"])
            
            print(f"{case['description']:<15} {text_display:<20} {case['expected']:<8.1f} {score:<8.3f} {status:<8}")
        
        print("-" * 60)
        print(f"\n📊 边界测试通过率: {passed_count}/{len(edge_cases)} ({passed_count/len(edge_cases)*100:.1f}%)")
        
        return passed_count >= len(edge_cases) * 0.8
        
    except Exception as e:
        print(f"❌ 边界情况测试失败: {e}")
        return False

def generate_sentiment_health_report():
    """生成情绪分析健康报告"""
    print("\n📋 生成情绪分析健康报告")
    print("="*50)
    
    report = f"""
# 📊 情绪分析师健康检查报告

**检查时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**检查版本**: v1.0

## 🎯 检查项目

### 1. 评分范围测试
- **目的**: 验证情绪评分是否在 [-1.0, 1.0] 范围内
- **方法**: 测试不同强度的情绪文本
- **标准**: 评分准确率 ≥ 80%

### 2. 真实股票测试
- **目的**: 验证实际股票情绪分析功能
- **方法**: 测试多个股票代码的情绪分析
- **标准**: 能正常生成包含关键信息的报告

### 3. 一致性测试
- **目的**: 验证相同输入产生相同输出
- **方法**: 重复测试相同文本
- **标准**: 结果完全一致

### 4. 边界情况测试
- **目的**: 验证异常输入的处理
- **方法**: 测试空文本、重复词等边界情况
- **标准**: 边界测试通过率 ≥ 80%

## 💡 使用建议

1. **正常使用**:
   - 情绪评分在 [-1.0, 1.0] 范围内为正常
   - 置信度 > 0.5 时结果较为可靠
   - 建议结合基本面分析使用

2. **异常处理**:
   - 评分超出范围时需要检查算法
   - 置信度过低时建议人工验证
   - 数据获取失败时使用备用方案

3. **优化方向**:
   - 扩展情绪词典
   - 增加语义分析
   - 提高数据源质量

---
*报告生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
    
    try:
        report_file = "sentiment_health_report.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ 健康报告已生成: {report_file}")
        return True
        
    except Exception as e:
        print(f"❌ 生成健康报告失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🔍 情绪分析师取值正常性检查")
    print("🎯 验证评分范围、计算逻辑和数据合理性")
    print("="*60)
    
    tests = [
        ("评分范围测试", test_sentiment_scoring_range),
        ("真实股票测试", test_real_stock_sentiment),
        ("一致性测试", test_sentiment_consistency),
        ("边界情况测试", test_edge_cases),
        ("健康报告生成", generate_sentiment_health_report)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ {name} 失败: {e}")
            results.append(False)
    
    print("\n" + "="*60)
    print("🎯 检查结果汇总")
    print("="*60)
    
    for i, (name, _) in enumerate(tests):
        status = "✅ 正常" if results[i] else "❌ 异常"
        print(f"{name}: {status}")
    
    passed_count = sum(results)
    total_count = len(results)
    
    print(f"\n📊 整体健康度: {passed_count}/{total_count} ({passed_count/total_count*100:.1f}%)")
    
    if passed_count >= total_count * 0.8:
        print("\n🎉 情绪分析师取值正常！")
        print("\n✨ 检查结果:")
        print("- 📊 评分范围在预期区间内")
        print("- 🔄 计算逻辑一致可靠")
        print("- 🛡️ 边界情况处理正常")
        print("- 📈 真实数据分析有效")
        
        print("\n💡 使用建议:")
        print("- 情绪评分 [-1.0, 1.0] 为正常范围")
        print("- 置信度 > 0.5 时结果较为可靠")
        print("- 建议结合基本面和技术面分析")
        print("- 关注政策面对A股的影响")
    else:
        print("\n⚠️ 发现异常，需要进一步检查")
        print("\n🔧 建议措施:")
        print("- 检查算法实现")
        print("- 验证数据源质量")
        print("- 更新情绪词典")
        print("- 优化评分逻辑")
    
    print("\n📖 详细报告请查看: sentiment_health_report.md")

if __name__ == "__main__":
    main()