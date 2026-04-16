"""
app.models — 資料庫模型套件初始化

提供資料庫連線管理與建表初始化功能。
"""

import sqlite3
import os

# 資料庫檔案路徑（放在 instance/ 資料夾內）
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'database.db')
SCHEMA_PATH = os.path.join(BASE_DIR, 'database', 'schema.sql')


def get_db():
    """取得 SQLite 資料庫連線。

    回傳的連線啟用外鍵約束，並使用 sqlite3.Row 作為 row_factory，
    讓查詢結果可以像字典一樣透過欄位名稱存取。
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """根據 database/schema.sql 初始化資料庫。

    如果 instance/ 資料夾不存在會自動建立。
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db()
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.close()
