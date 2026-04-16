# 路由與頁面設計文件

本文件根據 PRD、系統架構與資料庫設計，詳細規劃線上算命系統的 URL 路由、HTTP 方法與對應的模板，以便進行後續的程式碼實作。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁 | GET | `/` | `index.html` | 系統入口、提供開始算命的功能 |
| 註冊頁面 | GET | `/register` | `auth/register.html` | 顯示會員註冊表單 |
| 執行註冊 | POST | `/register` | — | 驗證欄位、建立帳號並重導向至登入頁 |
| 登入頁面 | GET | `/login` | `auth/login.html` | 顯示會員登入表單 |
| 執行登入 | POST | `/login` | — | 驗證帳密，建立 Session，重導向至首頁 |
| 執行登出 | GET | `/logout` | — | 清除 Session，重導向至首頁 |
| 執行抽籤 | POST | `/draw` | — | 接收表單或 AJAX，隨機抽取籤詩，重導向至結果頁 |
| 抽籤結果 | GET | `/result/<int:record_id>` | `result.html` | 顯示特定一筆算命紀錄與籤詩詳細內容 |
| 儲存紀錄 | POST | `/record/<int:record_id>/save` | — | 驗證登入狀態，標記紀錄為已儲存，重導至歷史頁 |
| 歷史紀錄 | GET | `/history` | `history.html` | 顯示登入會員已儲存的所有算命紀錄 |
| 捐款頁面 | GET | `/donate` | `donate.html` | 顯示香油錢捐款表單 |
| 執行捐款 | POST | `/donate` | `donate.html` (成功提示) | 寫入捐獻紀錄，顯示感謝訊息 |

---

## 2. 每個路由的詳細說明

### Auth 模組 (認證相關 - `auth.py`)

#### `GET /register`
- **輸入**: 無
- **處理邏輯**: 渲染註冊表單畫面
- **輸出**: 渲染 `auth/register.html`

#### `POST /register`
- **輸入**: 表單欄位 `username`, `email`, `password`, `confirm_password`
- **處理邏輯**: 
  1. 驗證密碼是否相符，以及帳號、信箱是否已被註冊。
  2. 若無誤，將密碼使用 Bcrypt 雜湊。
  3. 呼叫 `User.create` 建立帳號。
- **輸出**: 成功則重導向至 `/login` 搭配 Flash 成功訊息；失敗則重導回 `/register` 並顯示錯誤訊息。

#### `GET /login`
- **輸入**: 無
- **處理邏輯**: 渲染登入表單畫面
- **輸出**: 渲染 `auth/login.html`

#### `POST /login`
- **輸入**: 表單欄位 `username`, `password`
- **處理邏輯**:
  1. 呼叫 `User.get_by_username` 尋找使用者。
  2. 比對密碼雜湊值。
  3. 成功後將 user_id 寫入 session。
- **輸出**: 成功則重導向 `/`；失敗則重導回 `/login` 並提示錯誤。

#### `GET /logout`
- **輸入**: session
- **處理邏輯**: 清除 session 中的 user_id 資訊。
- **輸出**: 重導向至 `/`。

### Main 模組 (核心功能 - `main.py`)

#### `GET /`
- **輸入**: 無
- **處理邏輯**: 取出網站相關數據（如當前登入者資訊），準備渲染首頁。
- **輸出**: 渲染 `index.html`。

#### `POST /draw`
- **輸入**: 表單中的 `question` (選擇性), `category` (預設為 '抽籤')
- **處理邏輯**:
  1. 呼叫 `Fortune.draw_random(category)` 取得隨機籤詩 ID。
  2. 如果使用者已登入，使用當前 user_id；若未登入，可用特殊匿名 ID（或 Null，依實作決定），呼叫 `Record.create(...)` 建立算命紀錄。
- **輸出**: 重導向至 `/result/<紀錄ID>`。

#### `GET /result/<int:record_id>`
- **輸入**: URL 參數 `record_id`
- **處理邏輯**:
  1. 呼叫 `Record.get_by_id(record_id)` 獲取紀錄，包含 `fortune_id`。
  2. 呼叫 `Fortune.get_by_id(fortune_id)` 獲取籤詩詳細內容。
  3. 檢查目前使用者是否有權限查看（或是否為公開分享狀態）。若無找不到紀錄，返回 404。
- **輸出**: 渲染 `result.html` 帶入關聯資料。

#### `POST /record/<int:record_id>/save`
- **輸入**: URL 參數 `record_id`, 需具備已登入 Session
- **處理邏輯**:
  1. 若未登入，防護阻斷（@login_required）或重導至登入。
  2. 確認該筆紀錄屬於該登入使用者。
  3. 呼叫 `Record.save_record(record_id)` 標示儲存。
- **輸出**: 重導向至 `/history` 並 Flash 提示儲存成功。

#### `GET /history`
- **輸入**: 需具備已登入 Session
- **處理邏輯**:
  1. 取得當前 session 中的 `user_id`。
  2. 呼叫 `Record.get_by_user(user_id, saved_only=True)` 取出歷史算命紀錄。
- **輸出**: 渲染 `history.html` 帶入歷史紀錄列表。

#### `GET /donate`
- **輸入**: 無
- **處理邏輯**: 取得目前捐獻總額 (`Donation.get_total_amount()`) 供顯示。
- **輸出**: 渲染 `donate.html`。

#### `POST /donate`
- **輸入**: 表單欄位 `amount`, `message`
- **處理邏輯**:
  1. 驗證金額是否為正數。
  2. 呼叫 `Donation.create` 建立捐獻紀錄（若有登入則帶入 `user_id`）。
- **輸出**: 重導向至同一頁面 `/donate` 或 `/`，並顯示感謝 Flash 訊息。

---

## 3. Jinja2 模板清單

整個專案將規劃建立以下基礎視圖：

| 模板檔案路徑 | 繼承自 | 說明 |
| --- | --- | --- |
| `templates/base.html` | (無) | 母版：包含 `<html>`, `<head>`, `<nav>`, 底部資訊 與 Flash 訊息顯示區塊。 |
| `templates/index.html` | `base.html` | 首頁：網站介紹、動畫引導與進行算命的輸入框。 |
| `templates/result.html` | `base.html` | 算命結果頁：展現籤詩原文、解籤內容，並提供「儲存」按鈕或分享按鈕。 |
| `templates/history.html` | `base.html` | 歷史紀錄頁：清單式呈現會員過去儲存的抽籤歷程。 |
| `templates/donate.html` | `base.html` | 捐獻頁面：輸入捐獻金額、留言，並提供模擬金流按鈕。 |
| `templates/auth/login.html` | `base.html` | 會員登入表單：提供帳號密碼輸入。 |
| `templates/auth/register.html` | `base.html` | 會員註冊表單：提供建立帳號介面。 |

---

## 4. 路由骨架程式碼

相關路由骨架檔案將建立於 `app/routes/` 目錄中：
- `app/routes/__init__.py` : 路由初始化檔案
- `app/routes/auth.py` : 登入、註冊、登出相關 Blueprint
- `app/routes/main.py` : 包含運勢抽取、結果顯示、紀錄儲存與捐獻相關 Blueprint
