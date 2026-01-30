from flask import Flask, request
import telebot
import requests
import json
import os

app = Flask(__name__)
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
        # Better path finding for Vercel
        path = os.path.join(os.getcwd(), 'LICENSE.json')
        with open(path, 'r') as f:
            lic = json.load(f)
        
        if str(message.from_user.id) != str(lic.get("owner_id")):
            bot.reply_to(message, "❌ Unauthorized User.")
            return

        msg = message.text.split()
        if not msg[0].startswith("http"):
            bot.reply_to(message, "Send: [URL] [Count]")
            return

        # Vercel Fix: No loops, just one request to prevent Timeout
        url = "https://indianbestsmm.com/insta.php"
        headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 10)",
            'Cookie': "PHPSESSID=644c9fa32cb89d43c74c37d97c2d7f16"
        }
        
        resp = requests.post(url, data={'user_link': msg[0]}, headers=headers, timeout=5)
        bot.reply_to(message, f"✅ Request Sent! Response: {resp.status_code}")

    except Exception as e:
        bot.reply_to(message, f"⚠️ Error: {str(e)}")

if name == "__main__":
    app.run()
