from flask import Flask, request
import telebot
import requests
import time
import json
import os

app = Flask(__name__)
# Your Bot Token
bot = telebot.TeleBot("8558560055:AAE3_3XmN4VK-iwrwD8BLeL8i-1_LHF9_mM")

@app.route('/api/bot', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "OK", 200
    else:
        return "Invalid Content-Type", 403

@bot.message_handler(func=lambda message: True)
def handle_view_request(message):
    # 1. LOAD & CHECK LICENSE
    try:
        # Vercel looks for files in the root directory relative to the function
        license_path = os.path.join(os.getcwd(), 'LICENSE.json')
        with open(license_path, 'r') as f:
            license_data = json.load(f)
        
        if str(message.from_user.id) != str(license_data.get("owner_id")):
            bot.reply_to(message, "❌ Unauthorized: You do not own this license.")
            return
    except Exception as e:
        bot.reply_to(message, f"⚠️ License Error: {str(e)}")
        return

    # 2. PROCESS INPUT
    msg_parts = message.text.split()
    if not msg_parts[0].startswith("http"):
        bot.reply_to(message, "Please send: [URL] [Count]\nExample: https://instagr.am/p/xyz 3")
        return

    insta_url = msg_parts[0]
    # Limit count to 3 because Vercel will timeout after 10 seconds
    count = min(int(msg_parts[1]), 3) if len(msg_parts) > 1 else 1

    url = "https://indianbestsmm.com/insta.php"
    payload = {'user_link': insta_url}
    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        'origin': "https://indianbestsmm.com",
        'referer': "https://indianbestsmm.com/insta.php",
        'Cookie': "PHPSESSID=644c9fa32cb89d43c74c37d97c2d7f16"
    }

    bot.reply_to(message, f"🚀 Processing {count} runs...")

    for i in range(count):
        try:
            requests.post(url, data=payload, headers=headers, timeout=5)
            bot.send_message(message.chat.id, f"✅ Run {i+1} complete.")
        except Exception:
            bot.send_message(message.chat.id, f"❌ Run {i+1} failed.")
        time.sleep(1)

    bot.send_message(message.chat.id, "🏁 Task finished.")

if name == "__main__":
    app.run()
