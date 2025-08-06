#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def check_002031_data():
    """检查数据库中002031的数据"""
    try:
        conn = pymysql.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DATABASE'),
            charset='utf8mb4'
        )
        
        cursor = conn.cursor()
        
        # 查询002031的所有数据
        print("🔍 查询002031的所有历史数据...")
        cursor.execute("SELECT * FROM rising_stocks WHERE code = '002031' ORDER BY record_date DESC LIMIT 10")
        results = cursor.fetchall()
        
        if results:
            print(f"✅ 找到 {len(results)} 条002031的数据:")
            for row in results:
                print(f"  - {row}")
        else:
            print("❌ 数据库中没有找到002031的数据")
        
        # 查询今日所有股票
        print("\n🔍 查询今日所有股票...")
        cursor.execute("SELECT code, record_date FROM rising_stocks WHERE record_date = CURDATE()")
        today_results = cursor.fetchall()
        
        if today_results:
            print(f"✅ 今日共有 {len(today_results)} 只股票:")
            for row in today_results:
                print(f"  - {row[0]} ({row[1]})")
        else:
            print("❌ 今日没有股票数据")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ 数据库查询失败: {e}")

if __name__ == "__main__":
    check_002031_data()