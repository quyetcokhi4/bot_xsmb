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
        res = requests.post(url, json=payload)
        print(f"Phản hồi từ Telegram: {res.status_code}")
    except Exception as e:
        print(f"Lỗi gửi tin: {e}")

def save_daily_numbers(date_str, btl, x2, x3, de_list):
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"{date_str}|BTL:{btl}|X2:{x2[0]}-{x2[1]}|X3:{x3[0]}-{x3[1]}-{x3[2]}|DE:{','.join(de_list)}\n")

def get_chot_so_content():
    today = datetime.now().strftime("%d/%m/%Y")
    date_key = datetime.now().strftime("%Y-%m-%d")
    
    all_numbers = [f"{i:02d}" for i in range(100)]
    btl = random.choice(all_numbers)
    xien_pool = random.sample(all_numbers, 5)
    xien_2 = (xien_pool[0], xien_pool[1])
    xien_3 = (xien_pool[2], xien_pool[3], xien_pool[4])
    danh_de = sorted(random.sample(all_numbers, 20))
    
    save_daily_numbers(date_key, btl, xien_2, xien_3, danh_de)
    
    msg = f"""🎯 *CHỐT SỐ XSMB HÔM NAY ({today})* 🎯
*Mức vào tiền:* Lô 10d | Xiên 50k | Đề 10k/số

🔥 *Bạch thủ lô (10d):* `{btl}`
⚡ *Xiên 2 (50k):* `{xien_2[0]} - {xien_2[1]}`
⚡ *Xiên 3 (50k):* `{xien_3[0]} - {xien_3[1]} - {xien_3[2]}`

🎲 *Dàn đề 20 số (10k/số):*
`{', '.join(danh_de)}`"""
    return msg

def get_thong_ke_content():
    today = datetime.now().strftime("%d/%m/%Y")
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

print("Bot XSMB đang khởi động...")

# Gửi ngay tin nhắn kiểm tra kết nối ngay khi bot vừa bật lên để bạn thấy kết nối thành công
init_msg = "🤖 *Bot quản lý XSMB đã kết nối thành công!* \nĐang chờ lịch chạy tự động lúc 16:00 và 18:35..."
send_telegram_message(init_msg)

sent_chot_so_today = False
sent_ket_qua_today = False

while True:
    now = datetime.now()
    current_hour = now.hour
    current_minute = now.minute
    
    # 16:00 Chốt số tự động
    if current_hour == 16 and current_minute == 0:
        if not sent_chot_so_today:
            send_telegram_message(get_chot_so_content())
            sent_chot_so_today = True
            time.sleep(60)
            
    # 18:35 Cào kết quả và báo cáo
    elif current_hour == 18 and current_minute == 35:
        if not sent_ket_qua_today:
            send_telegram_message(get_thong_ke_content())
            sent_ket_qua_today = True
            time.sleep(60)
            
    # Reset cờ sang ngày mới lúc 00:00
    elif current_hour == 0 and current_minute == 0:
        sent_ch_so_today = False
        sent_ket_qua_today = False
        time.sleep(60)
        
    time.sleep(30)
