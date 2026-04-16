"""
app.models.fortune — 籤詩庫 (Fortune) 資料模型

管理系統中所有可供抽取的籤詩資料（靜態資料表）。
"""

import random
from app.models import get_db


class Fortune:
    """籤詩庫資料模型，對應資料庫 fortune 資料表。"""

    def __init__(self, id=None, title=None, poem=None,
                 interpretation=None, fortune_type=None, category=None):
        self.id = id
        self.title = title
        self.poem = poem
        self.interpretation = interpretation
        self.fortune_type = fortune_type
        self.category = category

    @staticmethod
    def create(title, poem, interpretation, fortune_type, category='抽籤'):
        """新增籤詩。

        Args:
            title (str): 籤詩名稱。
            poem (str): 籤詩詩文。
            interpretation (str): 解籤說明。
            fortune_type (str): 吉凶分類。
            category (str): 算命類別，預設為「抽籤」。

        Returns:
            int: 新建立的籤詩 ID。
        """
        db = get_db()
        cursor = db.execute(
            "INSERT INTO fortune (title, poem, interpretation, fortune_type, category) "
            "VALUES (?, ?, ?, ?, ?)",
            (title, poem, interpretation, fortune_type, category)
        )
        db.commit()
        new_id = cursor.lastrowid
        db.close()
        return new_id

    @staticmethod
    def get_all():
        """取得所有籤詩。

        Returns:
            list[dict]: 所有籤詩資料。
        """
        db = get_db()
        rows = db.execute("SELECT * FROM fortune ORDER BY id").fetchall()
        db.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(fortune_id):
        """透過 ID 取得籤詩。

        Args:
            fortune_id (int): 籤詩 ID。

        Returns:
            dict or None: 籤詩資料，找不到時回傳 None。
        """
        db = get_db()
        row = db.execute(
            "SELECT * FROM fortune WHERE id = ?", (fortune_id,)
        ).fetchone()
        db.close()
        return dict(row) if row else None

    @staticmethod
    def get_by_category(category):
        """透過類別取得籤詩。

        Args:
            category (str): 算命類別（抽籤/擲筊/塔羅）。

        Returns:
            list[dict]: 該類別的所有籤詩。
        """
        db = get_db()
        rows = db.execute(
            "SELECT * FROM fortune WHERE category = ? ORDER BY id",
            (category,)
        ).fetchall()
        db.close()
        return [dict(row) for row in rows]

    @staticmethod
    def draw_random(category='抽籤'):
        """隨機抽取一支籤。

        Args:
            category (str): 算命類別，預設為「抽籤」。

        Returns:
            dict or None: 隨機抽中的籤詩資料，無資料時回傳 None。
        """
        fortunes = Fortune.get_by_category(category)
        if not fortunes:
            return None
        return random.choice(fortunes)

    @staticmethod
    def update(fortune_id, **kwargs):
        """更新籤詩資料。

        Args:
            fortune_id (int): 籤詩 ID。
            **kwargs: 要更新的欄位與值。

        Returns:
            bool: 更新是否成功。
        """
        allowed_fields = {'title', 'poem', 'interpretation', 'fortune_type', 'category'}
        fields = {k: v for k, v in kwargs.items() if k in allowed_fields}
        if not fields:
            return False

        set_clause = ", ".join(f"{k} = ?" for k in fields)
        values = list(fields.values()) + [fortune_id]

        db = get_db()
        db.execute(f"UPDATE fortune SET {set_clause} WHERE id = ?", values)
        db.commit()
        db.close()
        return True

    @staticmethod
    def delete(fortune_id):
        """刪除籤詩。

        Args:
            fortune_id (int): 籤詩 ID。

        Returns:
            bool: 刪除是否成功。
        """
        db = get_db()
        cursor = db.execute("DELETE FROM fortune WHERE id = ?", (fortune_id,))
        db.commit()
        deleted = cursor.rowcount > 0
        db.close()
        return deleted
