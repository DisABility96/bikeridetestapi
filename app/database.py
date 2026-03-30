import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "rides.db")

def get_db():
    """返回数据库连接（自动提交模式）"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # 使返回结果为字典形式
    return conn

def init_db():
    """初始化数据库表"""
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS rides (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time TIMESTAMP NOT NULL,
                end_time TIMESTAMP,
                status TEXT NOT NULL DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()