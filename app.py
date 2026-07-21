import os
import threading
import random
import telebot
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# টেলিগ্রাম বটের টোকেন
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8868227957:AAFULZPQT0RMUGWXnQfhLItkMSYFEgkLstg")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

user_db = {}
otp_storage = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    username = message.from_user.username
    if username:
        user_db[username.lower()] = {"chat_id": chat_id, "cipher_text": "", "level": 1}
        bot.reply_to(message, f"⚡ স্বাগতম @{username}!\nআপনার টেলিগ্রাম একাউন্ট সফলভাবে লিঙ্ক হয়েছে। ✅\n\nযেলাযোগাযোগ: @CipherSentinel_BD")
    else:
        bot.reply_to(message, "⚠️ আপনার টেলিগ্রাম ইউজারনেম নেই।\nযোগাযোগ: @CipherSentinel_BD")

def run_telegram_bot():
    try:
        bot.infinity_polling(none_stop=True)
    except Exception as e:
        print(f"Telegram Bot Error: {e}")

# ড্যাশবোর্ড ও ডেভেলপার ইনফোসহ ডিজাইনড হোম পেজ
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <title>CryptoGuard & Developer Dashboard</title>
    <style>
        body { background-color: #0d1117; color: #c9d1d9; font-family: Arial, sans-serif; margin: 0; padding: 20px; }
        .container { display: flex; flex-wrap: wrap; gap: 20px; max-width: 1200px; margin: auto; }
        .card { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 20px; flex: 1; min-width: 300px; }
        h2 { color: #58a6ff; border-bottom: 1px solid #30363d; padding-bottom: 10px; }
        p { line-height: 1.6; }
        .highlight { color: #3fb950; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <!-- মূল সার্ভার ও বট স্ট্যাটাস সাইড -->
        <div class="card">
            <h2>🚀 সার্ভার ও বট স্ট্যাটাস</h2>
            <p>স্ট্যাটাস: <span class="highlight">অ্যাক্টিভ এবং রানিং (Online) ✅</span></p>
            <p>টেলিগ্রাম কন্টাক্ট: <a href="https://t.me/CipherSentinel_BD" target="_blank" style="color: #58a6ff;">@CipherSentinel_BD</a></p>
            <p>ইউজার আইডি: <code>7938556654</code></p>
            <p>নাম: Cipher Sentinel</p>
        </div>

        <!-- ডেভেলপার ড্যাশবোর্ড ও বার্থডে ব্লপার সাইড -->
        <div class="card">
            <h2>💻 ডেভেলপার ড্যাশবোর্ড & ব্লপার ইনফো</h2>
            <p><strong>ডেভেলপার:</strong> Cipher Sentinel Team</p>
            <p><strong>সিস্টেম লেভেল:</strong> সিকিউরড হাব v2.0</p>
            <hr style="border: 0; border-top: 1px solid #30363d; margin: 15px 0;">
            <p style="color: #f85149;"><strong>🎂 বার্থডে ব্লপার নোট (Birthday Blooper):</strong></p>
            <p>কোড করতে গিয়ে জন্মদিনের কেক কাটার সময় সার্ভার ক্রাশ করানোর মজার স্মৃতি এবং ডেপ্লয়মেন্টের সময়কার কিছু ভুলের (Bloopers) সমন্বিত ড্যাশবোর্ড এটি!</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/login-step1', methods=['POST'])
def login_step1():
    data = request.json or {}
    username = data.get('username', '').strip().lower().replace('@', '')
    if not username:
        return jsonify({"success": False, "message": "ইউজারনেম দিতে হবে!"})
    
    otp = str(random.randint(1000, 9999))
    otp_storage[username] = otp
    
    if username in user_db and user_db[username].get("chat_id"):
        try:
            bot.send_message(user_db[username]["chat_id"], f"🔐 আপনার সিকিউরিটি ওটিপি কোড: *{otp}*\n\nযোগাযোগ: @CipherSentinel_BD", parse_mode="Markdown")
        except Exception:
            pass
            
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
