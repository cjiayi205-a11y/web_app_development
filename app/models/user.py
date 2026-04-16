"""
app.models.user — 會員 (User) 資料模型

處理會員的註冊、登入驗證與基本 CRUD 操作。
密碼以 Bcrypt 雜湊後儲存，確保安全性。
"""

from app.models import get_db


class User:
    """會員資料模型，對應資料庫 user 資料表。"""

    def __init__(self, id=None, username=None, email=None,
                 password_hash=None, created_at=None):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at

    @staticmethod
    def create(username, email, password_hash):
        """建立新會員。

        Args:
            username (str): 使用者帳號。
            email (str): 電子信箱。
            password_hash (str): 經 Bcrypt 雜湊後的密碼。

        Returns:
            int: 新建立的會員 ID。
        """
        db = get_db()
        cursor = db.execute(
            "INSERT INTO user (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, password_hash)
        )
        db.commit()
        new_id = cursor.lastrowid
        db.close()
        return new_id

    @staticmethod
    def get_all():
        """取得所有會員。

        Returns:
            list[dict]: 所有會員資料。
        """
        db = get_db()
        rows = db.execute("SELECT * FROM user ORDER BY created_at DESC").fetchall()
        db.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(user_id):
        """透過 ID 取得會員。

        Args:
            user_id (int): 會員 ID。

        Returns:
            dict or None: 會員資料，找不到時回傳 None。
        """
        db = get_db()
        row = db.execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        db.close()
        return dict(row) if row else None

    @staticmethod
    def get_by_username(username):
        """透過帳號取得會員（登入驗證用）。

        Args:
            username (str): 使用者帳號。

        Returns:
            dict or None: 會員資料，找不到時回傳 None。
        """
        db = get_db()
        row = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()
        db.close()
        return dict(row) if row else None

    @staticmethod
    def get_by_email(email):
        """透過電子信箱取得會員。

        Args:
            email (str): 電子信箱。

        Returns:
            dict or None: 會員資料，找不到時回傳 None。
        """
        db = get_db()
        row = db.execute(
            "SELECT * FROM user WHERE email = ?", (email,)
        ).fetchone()
        db.close()
        return dict(row) if row else None

    @staticmethod
    def update(user_id, **kwargs):
        """更新會員資料。

        Args:
            user_id (int): 會員 ID。
            **kwargs: 要更新的欄位與值（支援 username, email, password_hash）。

        Returns:
            bool: 更新是否成功。
        """
        allowed_fields = {'username', 'email', 'password_hash'}
        fields = {k: v for k, v in kwargs.items() if k in allowed_fields}
        if not fields:
            return False

        set_clause = ", ".join(f"{k} = ?" for k in fields)
        values = list(fields.values()) + [user_id]

        db = get_db()
        db.execute(f"UPDATE user SET {set_clause} WHERE id = ?", values)
        db.commit()
        db.close()
        return True

    @staticmethod
    def delete(user_id):
        """刪除會員。

        Args:
            user_id (int): 會員 ID。

        Returns:
            bool: 刪除是否成功。
        """
        db = get_db()
        cursor = db.execute("DELETE FROM user WHERE id = ?", (user_id,))
        db.commit()
        deleted = cursor.rowcount > 0
        db.close()
        return deleted
