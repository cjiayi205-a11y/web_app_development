"""
app.models.record — 算命紀錄 (Record) 資料模型

儲存使用者每次抽籤/算命的結果紀錄，並支援儲存至個人帳號。
"""

from app.models import get_db


class Record:
    """算命紀錄資料模型，對應資料庫 record 資料表。"""

    def __init__(self, id=None, user_id=None, fortune_id=None,
                 question=None, drawn_at=None, is_saved=0):
        self.id = id
        self.user_id = user_id
        self.fortune_id = fortune_id
        self.question = question
        self.drawn_at = drawn_at
        self.is_saved = is_saved

    @staticmethod
    def create(user_id, fortune_id, question=None):
        """建立新的算命紀錄。

        Args:
            user_id (int): 使用者 ID。
            fortune_id (int): 抽中的籤詩 ID。
            question (str, optional): 使用者提出的問題。

        Returns:
            int: 新建立的紀錄 ID。
        """
        db = get_db()
        cursor = db.execute(
            "INSERT INTO record (user_id, fortune_id, question) VALUES (?, ?, ?)",
            (user_id, fortune_id, question)
        )
        db.commit()
        new_id = cursor.lastrowid
        db.close()
        return new_id

    @staticmethod
    def get_all():
        """取得所有算命紀錄。

        Returns:
            list[dict]: 所有紀錄資料。
        """
        db = get_db()
        rows = db.execute(
            "SELECT * FROM record ORDER BY drawn_at DESC"
        ).fetchall()
        db.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(record_id):
        """透過 ID 取得紀錄。

        Args:
            record_id (int): 紀錄 ID。

        Returns:
            dict or None: 紀錄資料，找不到時回傳 None。
        """
        db = get_db()
        row = db.execute(
            "SELECT * FROM record WHERE id = ?", (record_id,)
        ).fetchone()
        db.close()
        return dict(row) if row else None

    @staticmethod
    def get_by_user(user_id, saved_only=False):
        """取得指定使用者的所有算命紀錄（含籤詩詳細資料）。

        Args:
            user_id (int): 使用者 ID。
            saved_only (bool): 是否只取已儲存的紀錄。

        Returns:
            list[dict]: 該使用者的紀錄列表，含籤詩 JOIN 資料。
        """
        db = get_db()
        query = """
            SELECT r.*, f.title, f.poem, f.interpretation, f.fortune_type, f.category
            FROM record r
            JOIN fortune f ON r.fortune_id = f.id
            WHERE r.user_id = ?
        """
        params = [user_id]
        if saved_only:
            query += " AND r.is_saved = 1"
        query += " ORDER BY r.drawn_at DESC"

        rows = db.execute(query, params).fetchall()
        db.close()
        return [dict(row) for row in rows]

    @staticmethod
    def save_record(record_id):
        """將紀錄標記為已儲存。

        Args:
            record_id (int): 紀錄 ID。

        Returns:
            bool: 更新是否成功。
        """
        db = get_db()
        cursor = db.execute(
            "UPDATE record SET is_saved = 1 WHERE id = ?", (record_id,)
        )
        db.commit()
        updated = cursor.rowcount > 0
        db.close()
        return updated

    @staticmethod
    def update(record_id, **kwargs):
        """更新紀錄資料。

        Args:
            record_id (int): 紀錄 ID。
            **kwargs: 要更新的欄位與值。

        Returns:
            bool: 更新是否成功。
        """
        allowed_fields = {'user_id', 'fortune_id', 'question', 'is_saved'}
        fields = {k: v for k, v in kwargs.items() if k in allowed_fields}
        if not fields:
            return False

        set_clause = ", ".join(f"{k} = ?" for k in fields)
        values = list(fields.values()) + [record_id]

        db = get_db()
        db.execute(f"UPDATE record SET {set_clause} WHERE id = ?", values)
        db.commit()
        db.close()
        return True

    @staticmethod
    def delete(record_id):
        """刪除紀錄。

        Args:
            record_id (int): 紀錄 ID。

        Returns:
            bool: 刪除是否成功。
        """
        db = get_db()
        cursor = db.execute("DELETE FROM record WHERE id = ?", (record_id,))
        db.commit()
        deleted = cursor.rowcount > 0
        db.close()
        return deleted
