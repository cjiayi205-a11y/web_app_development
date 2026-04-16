"""
app.models.donation — 香油錢捐獻 (Donation) 資料模型

管理使用者的線上香油錢捐獻紀錄，支援匿名與具名捐獻。
"""

from app.models import get_db


class Donation:
    """香油錢捐獻資料模型，對應資料庫 donation 資料表。"""

    def __init__(self, id=None, user_id=None, amount=None,
                 message=None, donated_at=None):
        self.id = id
        self.user_id = user_id
        self.amount = amount
        self.message = message
        self.donated_at = donated_at

    @staticmethod
    def create(amount, user_id=None, message=None):
        """建立新的捐獻紀錄。

        Args:
            amount (float): 捐獻金額。
            user_id (int, optional): 會員 ID，匿名捐獻時為 None。
            message (str, optional): 祈願留言。

        Returns:
            int: 新建立的捐獻紀錄 ID。
        """
        db = get_db()
        cursor = db.execute(
            "INSERT INTO donation (user_id, amount, message) VALUES (?, ?, ?)",
            (user_id, amount, message)
        )
        db.commit()
        new_id = cursor.lastrowid
        db.close()
        return new_id

    @staticmethod
    def get_all():
        """取得所有捐獻紀錄。

        Returns:
            list[dict]: 所有捐獻紀錄。
        """
        db = get_db()
        rows = db.execute(
            "SELECT * FROM donation ORDER BY donated_at DESC"
        ).fetchall()
        db.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(donation_id):
        """透過 ID 取得捐獻紀錄。

        Args:
            donation_id (int): 捐獻紀錄 ID。

        Returns:
            dict or None: 捐獻紀錄資料，找不到時回傳 None。
        """
        db = get_db()
        row = db.execute(
            "SELECT * FROM donation WHERE id = ?", (donation_id,)
        ).fetchone()
        db.close()
        return dict(row) if row else None

    @staticmethod
    def get_by_user(user_id):
        """取得指定使用者的捐獻紀錄。

        Args:
            user_id (int): 使用者 ID。

        Returns:
            list[dict]: 該使用者的捐獻紀錄列表。
        """
        db = get_db()
        rows = db.execute(
            "SELECT * FROM donation WHERE user_id = ? ORDER BY donated_at DESC",
            (user_id,)
        ).fetchall()
        db.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_total_amount():
        """取得全系統的捐獻總金額。

        Returns:
            float: 總捐獻金額。
        """
        db = get_db()
        row = db.execute(
            "SELECT COALESCE(SUM(amount), 0) as total FROM donation"
        ).fetchone()
        db.close()
        return row['total']

    @staticmethod
    def update(donation_id, **kwargs):
        """更新捐獻紀錄。

        Args:
            donation_id (int): 捐獻紀錄 ID。
            **kwargs: 要更新的欄位與值。

        Returns:
            bool: 更新是否成功。
        """
        allowed_fields = {'user_id', 'amount', 'message'}
        fields = {k: v for k, v in kwargs.items() if k in allowed_fields}
        if not fields:
            return False

        set_clause = ", ".join(f"{k} = ?" for k in fields)
        values = list(fields.values()) + [donation_id]

        db = get_db()
        db.execute(f"UPDATE donation SET {set_clause} WHERE id = ?", values)
        db.commit()
        db.close()
        return True

    @staticmethod
    def delete(donation_id):
        """刪除捐獻紀錄。

        Args:
            donation_id (int): 捐獻紀錄 ID。

        Returns:
            bool: 刪除是否成功。
        """
        db = get_db()
        cursor = db.execute(
            "DELETE FROM donation WHERE id = ?", (donation_id,)
        )
        db.commit()
        deleted = cursor.rowcount > 0
        db.close()
        return deleted
