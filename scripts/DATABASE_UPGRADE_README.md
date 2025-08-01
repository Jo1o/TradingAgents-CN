# 数据库升级指南

## 概述

本升级将为MySQL数据库的`response`表添加两个新字段：
- `news_analysis`: 存储新闻分析师的分析结果
- `sentiment_analysis`: 存储情绪分析师的分析结果

## 升级方法

### 方法一：使用自动升级脚本（推荐）

#### Windows用户
```powershell
# 在PowerShell中执行
.\scripts\upgrade_database.ps1
```

#### Linux/macOS用户
```bash
# 在终端中执行
chmod +x scripts/upgrade_database.sh
./scripts/upgrade_database.sh
```

### 方法二：手动执行SQL脚本

1. 连接到MySQL数据库
2. 执行以下SQL文件：
   ```sql
   source scripts/upgrade_response_table.sql;
   ```

### 方法三：直接执行SQL命令

```sql
-- 连接到coredata数据库
USE coredata;

-- 添加新闻分析师字段
ALTER TABLE response 
ADD COLUMN news_analysis TEXT DEFAULT NULL COMMENT '新闻分析师结果' 
AFTER reasoning;

-- 添加情绪分析师字段
ALTER TABLE response 
ADD COLUMN sentiment_analysis TEXT DEFAULT NULL COMMENT '情绪分析师结果' 
AFTER news_analysis;

-- 查看更新后的表结构
DESC response;
```

## 升级后的表结构

升级完成后，`response`表将包含以下字段：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | INT AUTO_INCREMENT | 主键 |
| stock_code | VARCHAR(20) | 股票代码 |
| action | VARCHAR(50) | 投资动作 |
| target_price | DECIMAL(10,2) | 目标价格 |
| confidence | DECIMAL(3,2) | 置信度 |
| risk_score | DECIMAL(3,2) | 风险评分 |
| reasoning | TEXT | 分析推理 |
| **news_analysis** | **TEXT** | **新闻分析师结果** |
| **sentiment_analysis** | **TEXT** | **情绪分析师结果** |
| analysis_date | DATE | 分析日期 |
| created_at | TIMESTAMP | 创建时间 |

## 验证升级

升级完成后，可以通过以下SQL命令验证：

```sql
USE coredata;
DESC response;
```

应该能看到新增的`news_analysis`和`sentiment_analysis`字段。

## 注意事项

1. **备份数据**：升级前请备份数据库
2. **权限要求**：需要对数据库有ALTER权限
3. **兼容性**：此升级向后兼容，不会影响现有数据
4. **自动填充**：升级后运行分析时，新字段将自动填充相应的分析结果

## 故障排除

### 常见错误

1. **字段已存在错误**
   - 如果字段已存在，升级脚本会自动跳过
   - 可以安全地重复执行升级脚本

2. **权限不足错误**
   ```
   ERROR 1142 (42000): ALTER command denied
   ```
   - 解决方案：使用具有ALTER权限的用户执行升级

3. **表不存在错误**
   ```
   ERROR 1146 (42S02): Table 'coredata.response' doesn't exist
   ```
   - 解决方案：先运行一次自动分析，系统会自动创建表

## 联系支持

如果在升级过程中遇到问题，请：
1. 检查MySQL错误日志
2. 确认数据库连接配置
3. 验证用户权限
4. 查看项目文档或提交Issue