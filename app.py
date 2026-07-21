import os
import random
from flask import Flask, render_template, request, jsonify
from telegram_service import start_telegram_bots_background, send_admin_alert, send_otp_to_user

app = Flask(__name__)

# ব্যাকগ্রাউন্ডে টেলিগ্রাম বট চালু করা
start_telegram_bots_background()

# সাময়িকভাবে ইউজার ডাটা এবং ওটিপি সংরক্ষণের ডিকশনারি
temp_storage = {}

@app.route('/')
def home():
    return render_template('dashboard.html')

# ধাপ ১: ইউজারনেম ও পাসওয়ার্ড চেক এবং ওটিপি পাঠানো
@app.route('/login-step1', methods=['POST'])
def login_step1():
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    
    if not username or not password:
        return jsonify({"success": False, "message": "ইউজারনেম এবং পাসওয়ার্ড উভয়ই দিতে হবে!"})
    
    # এখানে আপনার পছন্দমতো পাসওয়ার্ড ভ্যালিডেশন দিতে পারেন (বর্তমানে ডেমো হিসেবে যেকোনো পাসওয়ার্ড গ্রহণ করবে)
    clean_username = username.replace('@', '').lower()
    
    # ৪ ডিজিটের ওটিপি জেনারেট
    otp_code = str(random.randint(1000, 9999))
    temp_storage[clean_username] = {
        "otp": otp_code,
        "password": password
    }
    
    # টেলিগ্রামে ওটিপি পাঠানো
    sent = send_otp_to_user(username, otp_code)
    
    if sent:
        send_admin_alert(f"🔐 লগইন প্রচেষ্টা (ধাপ ১): <b>{username}</b>")
        return jsonify({"success": True, "message": "পাসওয়ার্ড সঠিক! টেলিগ্রামে ওটিপি পাঠানো হয়েছে।"})
    else:
        return jsonify({"success": False, "message": "টেলিগ্রাম ইউজার পাওয়া যায়নি! প্রথমে বটে গিয়ে /start দিন।"})

# ধাপ ২: ওটিপি ভেরিফিকেশন
@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json
    username = data.get('username', '').replace('@', '').lower()
    user_entered_otp = data.get('otp', '').strip()
    
    user_data = temp_storage.get(username)
    
    if user_data and user_data["otp"] == user_entered_otp:
        send_admin_alert(f"✅ সফলভাবে লগইন ও ভেরিফাই করেছে: <b>{username}</b>")
        return jsonify({"success": True, "message": "ওটিপি ভেরিফিকেশন সফল! ড্যাশবোর্ডে প্রবেশ করছেন..."})
    else:
        return jsonify({"success": False, "message": "ভুল ওটিপি কোড!"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
