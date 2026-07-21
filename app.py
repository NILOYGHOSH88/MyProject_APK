import os
import random
from flask import Flask, render_template, request, jsonify
from telegram_service import start_telegram_bots_background, send_admin_alert, send_otp_to_user

app = Flask(__name__)

# অ্যাপ চালুর সাথেই টেলিগ্রাম বট ব্যাকগ্রাউন্ডে রান করিয়ে দেওয়া
start_telegram_bots_background()

# সাময়িকভাবে ওটিপি কোড সেভ রাখার ডিকশনারি
temp_otp_storage = {}

@app.route('/')
def home():
    return render_template('dashboard.html')

# ওটিপি রিকোয়েস্ট পাঠানোর রাউট
@app.route('/send-otp', methods=['POST'])
def send_otp():
    data = request.json
    username = data.get('username')
    
    if not username:
        return jsonify({"success": False, "message": "ইউজারনেম দিন!"})
    
    # ৪ ডিজিটের র‍্যান্ডম ওটিপি জেনারেট করা
    otp_code = str(random.randint(1000, 9999))
    temp_otp_storage[username.replace('@', '').lower()] = otp_code
    
    # টেলিগ্রাম বটের মাধ্যমে ওটিপি পাঠানো
    sent = send_otp_to_user(username, otp_code)
    
    if sent:
        send_admin_alert(f"⚠️ ইউজারের কাছে ওটিপি পাঠানো হয়েছে: <b>{username}</b>")
        return jsonify({"success": True, "message": "টেলিগ্রামে ওটিপি পাঠানো হয়েছে!"})
    else:
        return jsonify({"success": False, "message": "ইউজারকে খুঁজে পাওয়া যায়নি! প্রথমে বটে গিয়ে /start দিন।"})

# ওটিপি ভেরিফাই করার রাউট
@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json
    username = data.get('username', '').replace('@', '').lower()
    user_entered_otp = data.get('otp')
    
    if temp_otp_storage.get(username) == user_entered_otp:
        send_admin_alert(f"✅ সফলভাবে লগইন করেছে: <b>{username}</b>")
        return jsonify({"success": True, "message": "লগইন সফল!"})
    else:
        return jsonify({"success": False, "message": "ভুল ওটিপি কোড!"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
