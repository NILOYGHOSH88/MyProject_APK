import os
import threading
import random
import telebot
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# টেলিগ্রাম টোকেন কনফিগারেশন (আপনার বটের টোকেন এখানে দিন)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN_HERE")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# ডেটা সংরক্ষণ ডিকশনারি
user_db = {}
otp_storage = {}

# টেলিগ্রাম বট লজিক ও ওটিপি হ্যান্ডলিং
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    username = message.from_user.username
    if username:
        user_db[username.lower()] = {"chat_id": chat_id, "cipher_text": "", "level": 1}
        bot.reply_to(message, f"⚡ স্বাগতম @{username}!\nআপনার টেলিগ্রাম একাউন্ট সিকিউরড হ্যাকার হাবের সাথে সফলভাবে লিঙ্ক হয়েছে। ✅")
    else:
        bot.reply_to(message, "⚠️ আপনার টেলিগ্রাম ইউজারনেম নেই। দয়া করে ইউজারনেম সেট করুন।")

def run_telegram_bot():
    try:
        bot.infinity_polling(none_stop=True)
    except Exception as e:
        print(f"Telegram Bot Error: {e}")

# ফ্লাস্ক রাউটসমূহ
@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/login-step1', methods=['POST'])
def login_step1():
    data = request.json or {}
    username = data.get('username', '').strip().lower().replace('@', '')
    
    if not username:
        return jsonify({"success": False, "message": "ইউজারনেম দিতে হবে!"})
    
    otp = str(random.randint(1000, 9999))
    otp_storage[username] = otp
    
    # টেলিগ্রামে ওটিপি পাঠানো চেষ্টা
    chat_id = None
    if username in user_db:
        chat_id = user_db[username].get("chat_id")
    
    if chat_id:
        try:
            bot.send_message(chat_id, f"🔐 আপনার সিকিউরিটি ওটিপি কোড: *{otp}*", parse_mode="Markdown")
        except Exception:
            pass
            
    return jsonify({"success": True, "message": f"ওটিপি পাঠানো হয়েছে! (ডেমো ওটিপি: {otp})"})

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json or {}
    username = data.get('username', '').strip().lower().replace('@', '')
    otp = data.get('otp', '').strip()
    
    if username in otp_storage and otp_storage[username] == otp:
        if username not in user_db:
            user_db[username] = {"chat_id": None, "cipher_text": "", "level": 1}
        return jsonify({"success": True, "message": "ভেরিফিকেশন সফল!", "data": user_db[username]})
    
    return jsonify({"success": False, "message": "ভুল ওটিপি কোড!"})

@app.route('/alternative-login', methods=['POST'])
def alternative_login():
    data = request.json or {}
    phone = data.get('phone', '').strip().lower()
    if not phone:
        return jsonify({"success": False, "message": "সঠিক তথ্য দিন!"})
    
    if phone not in user_db:
        user_db[phone] = {"chat_id": None, "cipher_text": "", "level": 1}
        
    return jsonify({"success": True, "message": "লগইন সফল!", "data": user_db[phone]})

@app.route('/save-user-data', methods=['POST'])
def save_user_data():
    data = request.json or {}
    identifier = data.get('identifier', '').strip().lower()
    cipher_text = data.get('cipher_text', '')
    level = data.get('level', 1)
    
    if identifier:
        if identifier not in user_db:
            user_db[identifier] = {"chat_id": None}
        user_db[identifier]["cipher_text"] = cipher_text
        user_db[identifier]["level"] = level
        return jsonify({"success": True})
        
    return jsonify({"success": False})

@app.route('/notify-activity', methods=['POST'])
def notify_activity():
    data = request.json or {}
    identifier = data.get('identifier', '')
    action = data.get('action', '')
    
    if identifier in user_db and user_db[identifier].get("chat_id"):
        chat_id = user_db[identifier]["chat_id"]
        try:
            bot.send_message(chat_id, f"🔔 এক্টিভিটি নোটিফিকেশন: আপনার একাউন্টে সফলভাবে [{action}] সম্পন্ন হয়েছে।")
        except Exception:
            pass
            
    return jsonify({"success": True})

if __name__ == '__main__':
    # ব্যাকগ্রাউন্ডে টেলিগ্রাম বট রান করার জন্য থ্রেডিং
    bot_thread = threading.Thread(target=run_telegram_bot, daemon=True)
    bot_thread.start()
    
    # রেন্ডার সার্ভার পোর্টের জন্য কনফিগারেশন
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
