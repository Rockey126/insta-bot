from flask import Flask, request
import telebot
import requests
import json
import os

app = Flask(__name__)
# Use your verified Bot Token
bot = telebot.TeleBot("8558560055:AAE3_3XmN4VK-iwrwD8BLeL8i-1_LHF9_mM")

@app.route('/api/bot', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "OK", 200
    return "Forbidden", 403

@bot.message_handler(func=lambda message: True)
def handle_view_request(message):
    try:
        # 1. FIX PATH: Find LICENSE.json in the root folder
        base_path = os.path.dirname(os.path.abspath(__file__))
        lic_path = os.path.join(base_path, '..', 'LICENSE.json')
        
        with open(lic_path, 'r') as f:
            lic = json.load(f)
        
        # 2. OWNER CHECK: Ensure the IDs match exactly
        if str(message.from_user.id) != str(lic.get("owner_id")):
            bot.reply_to(message, f"❌ Unauthorized. Your ID: {message.from_user.id}")
            return

        # 3. INPUT CHECK
        msg_text = message.text.split()
        if not msg_text[0].startswith("http"):
            bot.reply_to(message, "Send a valid Instagram URL.")
            return

        # 4. SEND SINGLE REQUEST: Prevents 10s Vercel Timeout
        url = "https://indianbestsmm.com/insta.php"
        headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 10)",
            'Cookie': "PHPSESSID=644c9fa32cb89d43c74c37d97c2d7f16"
        }
        
        bot.send_message(message.chat.id, "🚀 Processing one request...")
        response = requests.post(url, data={'user_link': msg_text[0]}, headers=headers, timeout=5)
        
        bot.reply_to(message, f"✅ Done! Server responded with: {response.status_code}")

    except Exception as e:
        # This will tell you the EXACT error in Telegram
        bot.reply_to(message, f"⚠️ Error: {str(e)}")

if name == "__main__":
    app.run()
