import os
import threading
import random
import telebot
from flask import Flask, request, jsonify

app = Flask(__name__)

# টেলিগ্রাম টোকেন কনফিগারেশন
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN_HERE")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

user_db = {}
otp_storage = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    username = message.from_user.username
    if username:
        user_db[username.lower()] = {"chat_id": chat_id, "cipher_text": "", "level": 1}
        bot.reply_to(message, f"⚡ স্বাগতম @{username}!\nআপনার টেলিগ্রাম একাউন্ট সফলভাবে লিঙ্ক হয়েছে। ✅")
    else:
        bot.reply_to(message, "⚠️ আপনার টেলিগ্রাম ইউজারনেম নেই।")

def run_telegram_bot():
    try:
        bot.infinity_polling(none_stop=True)
    except Exception as e:
        print(f"Telegram Bot Error: {e}")

@app.route('/')
def home():
    return "Bot and Web Server is Running Successfully!"

@app.route('/login-step1', methods=['POST'])
def login_step1():
    data = request.json or {}
    username = data.get('username', '').strip().lower().replace('@', '')
    if not username:
        return jsonify({"success": False, "message": "ইউজারনেম দিতে হবে!"})
    
    otp = str(random.randint(1000, 9999))
    otp_storage[username] = otp
    return jsonify({"success": True, "message": f"ওটিপি পাঠানো হয়েছে! (ডেমো ওটিপি: {otp})"})

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json or {}
    username = data.get('username', '').strip().lower().replace('@', '')
    otp = data.get('otp', '').strip()
    
    if username in otp_storage and otp_storage[username] == otp:
        return jsonify({"success": True, "message": "ভেরিফিকেশন সফল!"})
    return jsonify({"success": False, "message": "ভুল ওটিপি কোড!"})

if __name__ == '__main__':
    bot_thread = threading.Thread(target=run_telegram_bot, daemon=True)
    bot_thread.start()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
