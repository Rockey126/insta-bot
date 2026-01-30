from flask import Flask, request
import telebot
import requests
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
    return "Forbidden", 403

@bot.message_handler(func=lambda message: True)
def handle_view_request(message):
    try:
        # Use absolute path to find the license file on Vercel
        lic_path = os.path.join(os.getcwd(), 'LICENSE.json')
        if not os.path.exists(lic_path):
             bot.reply_to(message, "❌ Error: LICENSE.json not found in root.")
             return

        with open(lic_path, 'r') as f:
            lic = json.load(f)
        
        # Security check: Make sure this is YOUR Telegram ID
        if str(message.from_user.id) != str(lic.get("owner_id")):
            bot.reply_to(message, f"❌ Unauthorized ID: {message.from_user.id}")
            return

        # Basic input check
        msg_parts = message.text.split()
        if not msg_parts[0].startswith("http"):
            bot.reply_to(message, "Please send a valid Instagram URL.")
            return

        # Single request only to avoid Vercel 10s timeout
        url = "https://indianbestsmm.com/insta.php"
        headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 10)",
            'Cookie': "PHPSESSID=644c9fa32cb89d43c74c37d97c2d7f16"
        }
        
        payload = {'user_link': msg_parts[0]}
        # Set a short timeout for the SMM request itself
        response = requests.post(url, data=payload, headers=headers, timeout=5)
        
        bot.reply_to(message, f"✅ Request sent! Status: {response.status_code}")

    except Exception as e:
        # This will send the exact error to your Telegram instead of crashing
        bot.reply_to(message, f"⚠️ Script Error: {str(e)}")

if name == "__main__":
    app.run()
