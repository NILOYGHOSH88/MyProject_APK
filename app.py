import os
import random
from flask import Flask, render_template, request, jsonify
from telegram_service import start_telegram_bots_background, send_admin_alert, send_otp_to_user

app = Flask(__name__)

# ব্যাকগ্রাউন্ডে টেলিগ্রাম বট চালু করা
start_telegram_bots_background()

# ইউজার ডাটা স্থায়ীভাবে বা সেশনে সেভ রাখার জন্য ডিকশনারি
user_database = {}
temp_storage = {}

@app.route('/')
def home():
    return render_template('dashboard.html')

# ধাপ ১: ইউজারনেম ও পাসওয়ার্ড চেক এবং ওটিপি পাঠানো (আগের ডেটা চেক করা)
@app.route('/login-step1', methods=['POST'])
def login_step1():
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    
    if not username or not password:
        return jsonify({"success": False, "message": "ইউজারনেম এবং পাসওয়ার্ড উভয়ই দিতে হবে!"})
    
    clean_username = username.replace('@', '').lower()
    
    # ইউজার যদি আগে থেকে রেজিস্টার্ড থাকে, পাসওয়ার্ড মিলিয়ে দেখা
    if clean_username in user_database:
        if user_database[clean_username]["password"] != password:
            return jsonify({"success": False, "message": "ভুল পাসওয়ার্ড! সঠিক পাসওয়ার্ড দিন।"})
    else:
        # নতুন ইউজার হলে রেজিস্টার করে নেওয়া
        user_database[clean_username] = {
            "password": password,
            "saved_text": "",
            "cipher_text": "",
            "level": 1
        }
    
    # ৪ ডিজিটের ওটিপি জেনারেট
    otp_code = str(random.randint(1000, 9999))
    temp_storage[clean_username] = otp_code
    
    # টেলিগ্রামে ওটিপি পাঠানো
    sent = send_otp_to_user(username, otp_code)
    
    if sent:
        send_admin_alert(f"🔐 লগইন প্রচেষ্টা (ধাপ ১): <b>{username}</b>")
        return jsonify({"success": True, "message": "পাসওয়ার্ড সঠিক! টেলিগ্রামে ওটিপি পাঠানো হয়েছে।", "is_returning": clean_username in user_database})
    else:
        return jsonify({"success": False, "message": "টেলিগ্রাম ইউজার পাওয়া যায়নি! প্রথমে বটে গিয়ে /start দিন।"})

# ধাপ ২: ওটিপি ভেরিফিকেশন এবং আগের ডেটা ফিরিয়ে দেওয়া
@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json
    username = data.get('username', '').replace('@', '').lower()
    user_entered_otp = data.get('otp', '').strip()
    
    correct_otp = temp_storage.get(username)
    
    if correct_otp and correct_otp == user_entered_otp:
        send_admin_alert(f"✅ সফলভাবে লগইন ও ভেরিফাই করেছে: <b>{username}</b>")
        user_info = user_database.get(username, {})
        return jsonify({
            "success": True, 
            "message": "ওটিপি ভেরিফিকেশন সফল! আগের ডেটা লোড হচ্ছে...",
            "data": user_info
        })
    else:
        return jsonify({"success": False, "message": "ভুল ওটিপি কোড!"})

# ইউজার ডেটা সেভ করার এন্ডপয়েন্ট
@app.route('/save-user-data', methods=['POST'])
def save_user_data():
    data = request.json
    username = data.get('username', '').replace('@', '').lower()
    
    if username in user_database:
        user_database[username]["saved_text"] = data.get('saved_text', '')
        user_database[username]["cipher_text"] = data.get('cipher_text', '')
        user_database[username]["level"] = data.get('level', 1)
        return jsonify({"success": True, "message": "ডেটা সফলভাবে সেভ হয়েছে!"})
    
    return jsonify({"success": False, "message": "ইউজার পাওয়া যায়নি!"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
