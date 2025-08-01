# TradingAgents 自动化分析指南

## 概述

自动化分析功能允许您从MySQL数据库自动读取股票代码，并使用TradingAgents的多智能体系统进行批量分析。分析结果会自动保存到数据库中，便于后续查询和统计。

## 功能特性

- 🔄 **自动化流程**: 从数据库读取 → 智能体分析 → 结果保存
- 📊 **批量处理**: 支持同时分析多只股票（可配置最大数量）
- 🛡️ **资源保护**: 内置限流机制，防止API过度调用
- 💾 **结果存储**: 分析结果自动保存到MySQL数据库
- 📈 **进度跟踪**: 实时显示分析进度和状态
- ⚡ **错误处理**: 完善的异常处理和重试机制

## 数据库配置

### 1. 环境变量设置

在项目根目录的 `.env` 文件中添加MySQL配置：

```bash
# MySQL数据库配置
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=coredata
```

### 2. 数据库表结构

#### rising_stocks 表（输入表）

```sql
CREATE TABLE IF NOT EXISTS rising_stocks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(20) NOT NULL COMMENT '股票代码',
    record_date DATE NOT NULL COMMENT '记录日期',
    INDEX idx_code (code),
    INDEX idx_record_date (record_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### response 表（输出表，自动创建）

```sql
CREATE TABLE IF NOT EXISTS response (
    id INT AUTO_INCREMENT PRIMARY KEY,
    stock_code VARCHAR(20) NOT NULL COMMENT '股票代码',
    action VARCHAR(50) DEFAULT NULL COMMENT '投资动作',
    target_price DECIMAL(10,2) DEFAULT NULL COMMENT '目标价格',
    confidence DECIMAL(3,2) DEFAULT NULL COMMENT '置信度',
    risk_score DECIMAL(3,2) DEFAULT NULL COMMENT '风险评分',
    reasoning TEXT DEFAULT NULL COMMENT '分析推理',
    news_analysis TEXT DEFAULT NULL COMMENT '新闻分析师结果',
    sentiment_analysis TEXT DEFAULT NULL COMMENT '情绪分析师结果',
    analysis_date DATE NOT NULL COMMENT '分析日期',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_stock_code (stock_code),
    INDEX idx_analysis_date (analysis_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 3. 示例数据

```sql
-- 插入今日需要分析的股票
INSERT INTO rising_stocks (code, record_date) VALUES 
('000001', CURDATE()),  -- 平安银行
('600036', CURDATE()),  -- 招商银行
('000002', CURDATE()),  -- 万科A
('600519', CURDATE()),  -- 贵州茅台
('000858', CURDATE());  -- 五粮液
```

## 使用方法

### 方法1: CLI命令行

```bash
# 基本用法
python -m cli.main auto-analysis

# 指定最大分析股票数量
python -m cli.main auto-analysis --max 3

# 试运行模式（暂未实现）
python -m cli.main auto-analysis --dry-run

# 查看帮助
python -m cli.main auto-analysis --help
```

### 方法2: Python脚本

```python
from cli.auto_analysis import AutoAnalyzer

# 创建分析器
analyzer = AutoAnalyzer(max_stocks=5)

# 运行分析
analyzer.run_analysis()
```

### 方法3: 运行演示

```bash
# 运行完整演示，包含配置检查和使用指南
python examples/auto_analysis_demo.py
```

## 分析流程

1. **数据库连接**: 连接到MySQL数据库
2. **表检查**: 检查并创建必要的数据表
3. **股票获取**: 从 `rising_stocks` 表读取今日股票代码
4. **数量限制**: 根据 `max_stocks` 参数限制分析数量
5. **逐一分析**: 使用TradingAgents多智能体系统分析每只股票
6. **结果保存**: 将分析结果保存到 `response` 表
7. **进度报告**: 显示分析完成情况和统计信息

## 分析结果字段说明

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| stock_code | VARCHAR(20) | 股票代码 | "000001" |
| action | VARCHAR(50) | 投资建议 | "买入", "持有", "卖出" |
| target_price | DECIMAL(10,2) | 目标价格 | 12.50 |
| confidence | DECIMAL(3,2) | 置信度 | 0.85 (85%) |
| risk_score | DECIMAL(3,2) | 风险评分 | 0.3 (30%) |
| reasoning | TEXT | 分析推理 | 详细的分析说明 |
| analysis_date | DATE | 分析日期 | 2025-01-18 |
| created_at | TIMESTAMP | 创建时间 | 2025-01-18 14:30:25 |

## 查询分析结果

### 查看今日所有分析结果

```sql
SELECT 
    stock_code,
    action,
    target_price,
    confidence,
    risk_score,
    LEFT(reasoning, 100) as reasoning_preview,
    created_at
FROM response 
WHERE analysis_date = CURDATE()
ORDER BY created_at DESC;
```

### 查看特定股票的历史分析

```sql
SELECT 
    analysis_date,
    action,
    target_price,
    confidence,
    risk_score,
    created_at
FROM response 
WHERE stock_code = '000001'
ORDER BY analysis_date DESC
LIMIT 10;
```

### 统计分析结果

```sql
-- 今日分析统计
SELECT 
    action,
    COUNT(*) as count,
    AVG(confidence) as avg_confidence,
    AVG(risk_score) as avg_risk_score
FROM response 
WHERE analysis_date = CURDATE()
GROUP BY action;
```

## 配置参数

### AutoAnalyzer 参数

- `max_stocks` (int): 最大分析股票数量，默认5
- 更多参数可在类初始化时配置

### CLI 参数

- `--max, -m`: 最大分析股票数量
- `--dry-run, -d`: 试运行模式（暂未实现）

## 注意事项

### 1. API调用限制

- 每次分析会消耗LLM API调用次数
- 建议合理设置 `max_stocks` 参数
- 系统内置3秒间隔，避免API限流

### 2. 数据库权限

- 确保MySQL用户有创建表的权限
- 确保有读写 `rising_stocks` 和 `response` 表的权限

### 3. 网络连接

- 需要稳定的网络连接访问数据源API
- 需要访问配置的LLM服务（如阿里百炼、OpenAI等）

### 4. 日期匹配

- 系统只分析 `record_date` 为当前日期的股票
- 确保 `rising_stocks` 表中有当日数据

## 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查MySQL服务是否启动
   - 验证连接参数是否正确
   - 确认网络连接正常

2. **没有找到股票数据**
   - 检查 `rising_stocks` 表是否存在
   - 确认表中有当日日期的数据
   - 验证日期格式是否正确

3. **分析失败**
   - 检查LLM API配置是否正确
   - 确认API密钥是否有效
   - 查看日志文件获取详细错误信息

4. **依赖缺失**
   ```bash
   # 安装MySQL依赖
   pip install pymysql
   
   # 或安装所有依赖
   pip install -r requirements.txt
   ```

### 日志查看

系统日志保存在项目的日志目录中，可以通过以下方式查看：

```bash
# 查看最新日志
tail -f logs/tradingagents.log

# 搜索特定错误
grep "ERROR" logs/tradingagents.log
```

## 扩展功能

### 自定义分析逻辑

可以通过继承 `AutoAnalyzer` 类来实现自定义分析逻辑：

```python
from cli.auto_analysis import AutoAnalyzer

class CustomAutoAnalyzer(AutoAnalyzer):
    def analyze_stock(self, stock_code: str):
        # 自定义分析逻辑
        result = super().analyze_stock(stock_code)
        
        # 添加自定义处理
        if result:
            result['custom_field'] = 'custom_value'
        
        return result
```

### 定时任务

可以结合cron或其他定时任务工具实现定时分析：

```bash
# 每天上午9点执行自动化分析
0 9 * * * cd /path/to/TradingAgents-CN && python -m cli.main auto-analysis --max 10
```

## 相关文档

- [TradingAgents 快速开始](../overview/quick-start.md)
- [配置管理指南](../configuration/config-guide.md)
- [数据库设置指南](../DATABASE_SETUP_GUIDE.md)
- [API配置指南](../configuration/llm-config.md)