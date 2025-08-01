-- 升级response表，添加新闻分析师和情绪分析师字段
-- 执行前请备份数据库

USE coredata;

-- 检查字段是否已存在，如果不存在则添加
SET @sql = '';

-- 添加news_analysis字段
SELECT COUNT(*) INTO @col_exists 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = 'coredata' 
  AND TABLE_NAME = 'response' 
  AND COLUMN_NAME = 'news_analysis';

SET @sql = IF(@col_exists = 0, 
    'ALTER TABLE response ADD COLUMN news_analysis TEXT DEFAULT NULL COMMENT "新闻分析师结果" AFTER reasoning;',
    'SELECT "news_analysis字段已存在" as message;');

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 添加sentiment_analysis字段
SELECT COUNT(*) INTO @col_exists 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = 'coredata' 
  AND TABLE_NAME = 'response' 
  AND COLUMN_NAME = 'sentiment_analysis';

SET @sql = IF(@col_exists = 0, 
    'ALTER TABLE response ADD COLUMN sentiment_analysis TEXT DEFAULT NULL COMMENT "情绪分析师结果" AFTER news_analysis;',
    'SELECT "sentiment_analysis字段已存在" as message;');

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 显示更新后的表结构
DESC response;

-- 显示升级完成信息
SELECT 'response表升级完成，已添加新闻分析师和情绪分析师字段' as upgrade_status;