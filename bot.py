import os
import time
import random
from datetime import datetime
import requests

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# File lưu lịch sử chơi và tổng kết tháng
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

def save_daily_numbers(date_str, btl, x2, x3, de_list):
    """Lưu số đã đánh trong ngày để tối dò kết quả"""
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"{date_str}|BTL:{btl}|X2:{x2[0]}-{x2[1]}|X3:{x3[0]}-{x3[1]}-{x3[2]}|DE:{','.join(de_list)}\n")

def main_chot_so():
    today = datetime.now().strftime("%d/%m/%Y")
    date_key = datetime.now().strftime("%Y-%m-%d")
    
    all_numbers = [f"{i:02d}" for i in range(100)]
    btl = random.choice(all_numbers)
    xien_pool = random.sample(all_numbers, 5)
    xien_2 = (xien_pool[0], xien_pool[1])
    xien_3 = (xien_pool[2], xien_pool[3], xien_pool[4])
    danh_de = sorted(random.sample(all_numbers, 20))
    
    # Lưu lại để tối đối chiếu
    save_daily_numbers(date_key, btl, xien_2, xien_3, danh_de)
    
    msg = f"""🎯 *CHỐT SỐ XSMB HÔM NAY ({today})* 🎯
*Mức vào tiền:* Lô 10d | Xiên 50k | Đề 10k/số

🔥 *Bạch thủ lô (10d):* `{btl}`
⚡ *Xiên 2 (50k):* `{xien_2[0]} - {xien_2[1]}`
⚡ *Xiên 3 (50k):* `{xien_3[0]} - {xien_3[1]} - {xien_3[2]}`

🎲 *Dàn đề 20 số (10k/số):*
`{', '.join(danh_de)}`"""

    send_telegram_message(msg)

def main_thong_ke_ket_qua():
    """Hàm chạy lúc 18h35 để cào kết quả, đối chiếu và báo cáo"""
    today = datetime.now().strftime("%d/%m/%Y")
    
    try:
        # Logic cào kết quả XSMB
        res = requests.get("https://wapi.ketqua.net/api/v1/lotto-result/mb")
        data = res.json()
    except Exception as e:
        print(f"Lỗi lấy kết quả: {e}")

    # Mẫu báo cáo tự động gửi về sau khi có kết quả
    baocao = f"""📊 *BÁO CÁO KẾT QUẢ XSMB ({today})* 📊

🎰 *Kết quả quay thưởng:*
- Đề về: `[Đang cập nhật từ hệ thống]`
- Lô về: `[Đang cập nhật]`

💰 *Tổng kết hôm nay:*
- Tiền xác bỏ ra: 450k (200k đề + 230k lô + xiên)
- Tiền thu về: `...`k
👉 *Lãi / Lỗ ngày:* `...`k

📈 *THỐNG KÊ LŨY KẾ CẢ THÁNG:*
- Tổng số ngày đánh: ... ngày
- Tổng lãi/lỗ cả tháng: `...`k
"""
    send_telegram_message(baocao)

print("Bot quản lý XSMB & Thống kê đang chạy ngầm 24/7...")

sent_chot_so_today = False
sent_ket_qua_today = False

while True:
    now = datetime.now()
    current_hour = now.hour
    current_minute = now.minute
    
    # 16:00 Chốt số
    if current_hour == 16 and current_minute == 0:
        if not sent_chot_so_today:
            main_chot_so()
            sent_chot_so_today = True
            time.sleep(60)
            
    # 18:35 Cào kết quả và báo cáo
    elif current_hour == 18 and current_minute == 35:
        if not sent_ket_qua_today:
            main_thong_ke_ket_qua()
            sent_ket_qua_today = True
            time.sleep(60)
            
    # Reset cờ sang ngày mới khi qua 00:00 đêm
    elif current_hour == 0 and current_minute == 0:
        sent_chot_so_today = False
        sent_ket_qua_today = False
        time.sleep(60)
        
    time.sleep(20)
