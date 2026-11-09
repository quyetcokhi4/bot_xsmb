import os
import time
import random
from datetime import datetime
import requests

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

HISTORY_FILE = "history_log.txt"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Lỗi gửi tin: {e}")

def get_today_saved_numbers(date_key):
    """Kiểm tra xem hôm nay đã lưu số chưa, nếu có rồi thì đọc ra dùng lại"""
    if not os.path.exists(HISTORY_FILE):
        return None
    
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            parts = line.strip().split("|")
            if parts[0] == date_key:
                # Format lưu: date|btl|x2_1-x2_2|x3_1-x3_2-x3_3|de_list
                btl = parts[1].replace("BTL:", "")
                x2 = parts[2].replace("X2:", "").split("-")
                x3 = parts[3].replace("X3:", "").split("-")
                de_list = parts[4].replace("DE:", "").split(",")
                return btl, x2, x3, de_list
    return None

def save_daily_numbers(date_str, btl, x2, x3, de_list):
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"{date_str}|BTL:{btl}|X2:{x2[0]}-{x2[1]}|X3:{x3[0]}-{x3[1]}-{x3[2]}|DE:{','.join(de_list)}\n")

def get_chot_so_content():
    today = datetime.now().strftime("%d/%m/%Y")
    date_key = datetime.now().strftime("%Y-%m-%d")
    
    # Kiểm tra xem hôm nay đã chốt số chưa
    saved_data = get_today_saved_numbers(date_key)
    
    if saved_data:
        # Nếu có rồi thì dùng lại đúng bộ số đó cho cả ngày
        btl, x2, x3, danh_de = saved_data
    else:
        # Nếu chưa có thì mới random tạo mới và lưu lại
        all_numbers = [f"{i:02d}" for i in range(100)]
        btl = random.choice(all_numbers)
        xien_pool = random.sample(all_numbers, 5)
        x2 = (xien_pool[0], xien_pool[1])
        x3 = (xien_pool[2], xien_pool[3], xien_pool[4])
        danh_de = sorted(random.sample(all_numbers, 20))
        
        save_daily_numbers(date_key, btl, x2, x3, danh_de)
    
    msg = f"""🎯 *CHỐT SỐ XSMB HÔM NAY ({today})* 🎯
*Mức vào tiền:* Lô 10d | Xiên 50k | Đề 10k/số

🔥 *Bạch thủ lô (10d):* `{btl}`
⚡ *Xiên 2 (50k):* `{x2[0]} - {x2[1]}`
⚡ *Xiên 3 (50k):* `{x3[0]} - {x3[1]} - {x3[2]}`

🎲 *Dàn đề 20 số (10k/số):*
`{', '.join(danh_de)}`"""
    return msg

def get_thong_ke_content():
    today = datetime.now().strftime("%d/%m/%Y")
    try:
        res = requests.get("https://wapi.ketqua.net/api/v1/lotto-result/mb")
        data = res.json()
    except Exception as e:
        print(f"Lỗi lấy kết quả: {e}")

    baocao = f"""📊 *BÁO CÁO KẾT QUẢ XSMB ({today})* 📊

🎰 *Kết quả quay thưởng:*
- Đề về: `[Đang cập nhật]`
- Lô về: `[Đang cập nhật]`

💰 *Tổng kết hôm nay:*
- Tiền xác bỏ ra: 450k (200k đề + 230k lô + xiên)
- Tiền thu về: `...`k
👉 *Lãi / Lỗ ngày:* `...`k

📈 *THỐNG KÊ LŨY KẾ CẢ THÁNG:*
- Tổng lãi/lỗ cả tháng: `...`k
"""
    return baocao

def check_telegram_updates(last_update_id):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates?offset={last_update_id + 1}&timeout=5"
    try:
        res = requests.get(url, timeout=10)
        data = res.json()
        if data.get("ok") and data.get("result"):
            for update in data["result"]:
                last_update_id = update["update_id"]
                message = update.get("message", {})
                text = message.get("text", "").strip().lower()
                
                if text in ["/start", "/chotso"]:
                    msg = get_chot_so_content()
                    send_telegram_message(msg)
                elif text == "/result":
                    baocao = get_thong_ke_content()
                    send_telegram_message(baocao)
    except Exception as e:
        print(f"Lỗi đọc tin nhắn Telegram: {e}")
    return last_update_id

print("Bot XSMB đã sẵn sàng cố định số trong ngày...")
send_telegram_message("🤖 *Bot đã sẵn sàng!* Số chốt sẽ được cố định duy nhất 1 bộ cho cả ngày.")

last_update_id = 0
sent_chot_so_today = False
sent_ket_qua_today = False

while True:
    now = datetime.now()
    current_hour = now.hour
    current_minute = now.minute
    
    last_update_id = check_telegram_updates(last_update_id)
    
    # 16:00 Chốt số tự động gửi
    if current_hour == 16 and current_minute == 0:
        if not sent_chot_so_today:
            send_telegram_message(get_chot_so_content())
            sent_chot_so_today = True
            time.sleep(60)
            
    # 18:35 Báo cáo kết quả
    elif current_hour == 18 and current_minute == 35:
        if not sent_ket_qua_today:
            send_telegram_message(get_thong_ke_content())
            sent_ket_qua_today = True
            time.sleep(60)
            
    elif current_hour == 0 and current_minute == 0:
        sent_chot_so_today = False
        sent_ket_qua_today = False
        time.sleep(60)
        
    time.sleep(3)
