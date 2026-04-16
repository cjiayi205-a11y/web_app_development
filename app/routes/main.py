from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.fortune import Fortune
from app.models.record import Record
from app.models.donation import Donation

# 建立名為 main 的 Blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    """
    首頁：顯示系統導覽與開始算命按鈕。
    GET /
    渲染模板: index.html
    """
    pass

@main_bp.route('/draw', methods=['POST'])
def execute_draw():
    """
    執行抽籤請求。
    POST /draw
    呼叫 Fortune.draw_random 取出籤詩，建立一筆未儲存的算命紀錄。
    成功後 redirect 至 /result/<record_id> 頁面。
    """
    pass

@main_bp.route('/result/<int:record_id>', methods=['GET'])
def parse_result(record_id):
    """
    顯示特定的算命/抽籤結果詳情。
    GET /result/<record_id>
    根據 record_id 查詢對應的紀錄與籤詩內容。
    渲染模板: result.html
    """
    pass

@main_bp.route('/record/<int:record_id>/save', methods=['POST'])
def save_record(record_id):
    """
    儲存算命紀錄並綁定到目前登入的使用者。
    POST /record/<record_id>/save
    將該紀錄標示為已儲存 (is_saved = 1)。
    儲存成功後 redirect 至 /history 頁面。
    """
    pass

@main_bp.route('/history', methods=['GET'])
def user_history():
    """
    顯示目前登入會員的算命紀錄列表。
    GET /history
    查詢當前 session 會員的已儲存紀錄。
    渲染模板: history.html
    """
    pass

@main_bp.route('/donate', methods=['GET'])
def render_donate():
    """
    顯示香油錢捐獻表單。
    GET /donate
    統計系統總捐獻金額。
    渲染模板: donate.html
    """
    pass

@main_bp.route('/donate', methods=['POST'])
def process_donate():
    """
    處理香油錢捐獻請求。
    POST /donate
    接收捐獻金額並寫入資料庫（支援登入與匿名）。
    成功後 redirect 回原頁面並 flash 感謝訊息。
    """
    pass
