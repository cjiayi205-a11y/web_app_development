from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.user import User

# 建立名為 auth 的 Blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET'])
def render_register():
    """
    顯示會員註冊表單頁面。
    GET /register
    渲染模板: auth/register.html
    """
    pass

@auth_bp.route('/register', methods=['POST'])
def process_register():
    """
    處理會員註冊請求。
    POST /register
    接收表單資料，驗證並建立 User 紀錄。
    成功則 redirect 至 /login；失敗則重新渲染註冊表單並顯示錯誤。
    """
    pass

@auth_bp.route('/login', methods=['GET'])
def render_login():
    """
    顯示會員登入表單頁面。
    GET /login
    渲染模板: auth/login.html
    """
    pass

@auth_bp.route('/login', methods=['POST'])
def process_login():
    """
    處理會員登入請求。
    POST /login
    接收表單資料，驗證帳密。
    成功則將 user_id 寫入 session 並 redirect 至 / ；失敗則重新渲染登入表單並顯示錯誤。
    """
    pass

@auth_bp.route('/logout', methods=['GET'])
def process_logout():
    """
    處理會員登出請求。
    GET /logout
    清除 session 中的 user 資訊。
    完成後 redirect 至 / 。
    """
    pass
