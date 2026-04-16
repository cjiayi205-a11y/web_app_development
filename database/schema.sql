-- ============================================
-- 線上算命系統 — SQLite 資料庫建表腳本
-- ============================================

-- 啟用外鍵約束（SQLite 預設不啟用）
PRAGMA foreign_keys = ON;

-- -------------------------------------------
-- 1. USER — 會員資料表
-- -------------------------------------------
CREATE TABLE IF NOT EXISTS user (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    username       TEXT    NOT NULL UNIQUE,
    email          TEXT    NOT NULL UNIQUE,
    password_hash  TEXT    NOT NULL,
    created_at     TEXT    NOT NULL DEFAULT (datetime('now'))
);

-- -------------------------------------------
-- 2. FORTUNE — 籤詩庫
-- -------------------------------------------
CREATE TABLE IF NOT EXISTS fortune (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    title           TEXT    NOT NULL,
    poem            TEXT    NOT NULL,
    interpretation  TEXT    NOT NULL,
    fortune_type    TEXT    NOT NULL,
    category        TEXT    NOT NULL DEFAULT '抽籤'
);

-- -------------------------------------------
-- 3. RECORD — 算命紀錄
-- -------------------------------------------
CREATE TABLE IF NOT EXISTS record (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    fortune_id  INTEGER NOT NULL,
    question    TEXT,
    drawn_at    TEXT    NOT NULL DEFAULT (datetime('now')),
    is_saved    INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id)    REFERENCES user(id)    ON DELETE CASCADE,
    FOREIGN KEY (fortune_id) REFERENCES fortune(id) ON DELETE CASCADE
);

-- -------------------------------------------
-- 4. DONATION — 香油錢捐獻紀錄
-- -------------------------------------------
CREATE TABLE IF NOT EXISTS donation (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER,
    amount      REAL    NOT NULL,
    message     TEXT,
    donated_at  TEXT    NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE SET NULL
);

-- -------------------------------------------
-- 5. 初始籤詩種子資料
-- -------------------------------------------
INSERT INTO fortune (title, poem, interpretation, fortune_type, category) VALUES
('第一籤 — 開天闢地', '日出東方照大千，雲開霧散見青天。若問前途何所往，一路光明在眼前。', '大吉之籤。目前困境即將突破，前方道路一片光明，放手去做必有好結果。', '大吉', '抽籤'),
('第二籤 — 姜公釣魚', '良辰吉日自然來，莫把心機強安排。等待時機方成事，雲開月出自徘徊。', '中吉之籤。時機尚未成熟，不宜操之過急，耐心等待自會水到渠成。', '中吉', '抽籤'),
('第三籤 — 董永賣身', '金鱗此去入深潭，一片誠心感動天。雖然眼前多險阻，貴人相助渡難關。', '中吉之籤。目前雖有困難，但只要誠心誠意，必有貴人出現協助。', '中吉', '抽籤'),
('第四籤 — 孟母三遷', '居安思危莫遲疑，環境改變運自移。三思而後再行動，前路自然步步宜。', '小吉之籤。需要改變目前的狀態才能轉運，審慎評估後果斷行動。', '小吉', '抽籤'),
('第五籤 — 劉備借荊州', '借力使力順風行，眼前機會莫推辭。善用資源成大事，但記有借終須還。', '中吉之籤。善用身邊的資源與人脈，但別忘了感恩回報。', '中吉', '抽籤'),
('第六籤 — 蘇武牧羊', '風霜雨雪苦中行，堅持到底見光明。莫因眼前多磨難，守得雲開月自明。', '小吉之籤。目前正處於考驗期，只要堅持不放棄，最終必將苦盡甘來。', '小吉', '抽籤'),
('第七籤 — 呂洞賓戲牡丹', '花開富貴在今朝，莫待無花空折枝。眼前良機切莫失，猶豫不決悔難追。', '大吉之籤。機會就在眼前，要果斷把握，切勿猶豫錯失良機。', '大吉', '抽籤'),
('第八籤 — 李白醉月', '月落星沉夢未醒，迷濛之中路難行。暫且收心靜待時，撥雲見日自分明。', '凶之籤。目前思緒混亂、方向不明，建議暫時停下腳步，靜心思考後再行動。', '凶', '抽籤'),
('第九籤 — 孔明借東風', '萬事俱備欠東風，靜候良機一點通。巧用智慧成大計，天時地利與人同。', '大吉之籤。準備工作已經充分，只差一個契機，耐心等待即可大功告成。', '大吉', '抽籤'),
('第十籤 — 關公過五關', '披荊斬棘勇向前，重重難關一一穿。忠心不改終有報，凱旋歸來在眼前。', '中吉之籤。路途雖然艱辛，但只要保持信念與勇氣，定能一一克服困難。', '中吉', '抽籤');
