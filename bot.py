import os
import time
import random
from datetime import datetime
import requests

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

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
        print(f"Lỗi: {e}")

def main_job():
    today = datetime.now().strftime("%d/%m/%Y")
    all_numbers = [f"{i:02d}" for i in range(100)]
    btl = random.choice(all_numbers)
    xien_pool = random.sample(all_numbers, 5)
    xien_2 = (xien_pool[0], xien_pool[1])
    xien_3 = (xien_pool[2], xien_pool[3], xien_pool[4])
    danh_de = sorted(random.sample(all_numbers, 20))
    
    msg = f"""🎯 *CHỐT SỐ XSMB HÔM NAY ({today})* 🎯

🔥 *Bạch thủ lô:* `{btl}`
⚡ *Xiên 2:* `{xien_2[0]} - {xien_2[1]}`
⚡ *Xiên 3:* `{xien_3[0]} - {xien_3[1]} - {xien_3[2]}`

🎲 *Dàn đề (20 số):*
`{', '.join(danh_de)}`"""

    send_telegram_message(msg)

print("Bot XSMB đang chạy ngầm...")
while True:
    now = datetime.now()
    if now.hour == 16 and now.minute == 30:
        main_job()
        time.sleep(60)
    time.sleep(30)
