import os
import random
from flask import Flask, render_template, request, jsonify
from telegram_service import start_telegram_bots_background, send_admin_alert, send_otp_to_user

app = Flask(__name__)

# ব্যাকগ্রাউন্ডে টেলিগ্রাম বট চালু করা
start_telegram_bots_background()

# ইউজার ডেটা স্থায়ীভাবে বা সেশনে সেভ রাখার জন্য ডিকশনারি
user_database = {}
temp_storage = {}

@app.route('/')
def home():
    return render_template('dashboard.html')

# টেলিগ্রাম ইউজারনেম দিয়ে লগইন (ধাপ ১)
@app.route('/login-step1', methods=['POST'])
def login_step1():
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    
    if not username or not password:
        return jsonify({"success": False, "message": "ইউজারনেম এবং পাসওয়ার্ড উভয়ই দিতে হবে!"})
    
    clean_username = username.replace('@', '').lower()
    
    if clean_username in user_database:
        if user_database[clean_username]["password"] != password:
            return jsonify({"success": False, "message": "ভুল পাসওয়ার্ড! সঠিক পাসওয়ার্ড দিন।"})
    else:
        user_database[clean_username] = {
            "password": password,
            "saved_text": "",
            "cipher_text": "",
            "level": 1
        }
    
    otp_code = str(random.randint(1000, 9999))
    temp_storage[clean_username] = otp_code
    
    sent = send_otp_to_user(username, otp_code)
    
    if sent:
        send_admin_alert(f"🔐 টেলিগ্রাম লগইন প্রচেষ্টা: <b>{username}</b>")
        return jsonify({"success": True, "message": "পাসওয়ার্ড সঠিক! টেলিগ্রামে ওটিপি পাঠানো হয়েছে।"})
    else:
        return jsonify({"success": False, "message": "টেলিগ্রাম ইউজার পাওয়া যায়নি! প্রথমে বটে গিয়ে /start দিন বা অল্টারনেটিভ লগইন ব্যবহার করুন।"})

# অল্টারনেটিভ লগইন (ফোন নম্বর, নাম ও পাসওয়ার্ড দিয়ে সরাসরি প্রবেশ)
@app.route('/alternative-login', methods=['POST'])
def alternative_login():
    data = request.json
    phone = data.get('phone', '').strip()
    name = data.get('name', '').strip()
    password = data.get('password', '').strip()
    email = data.get('email', '').strip() # অপশনাল
    
    if not phone or not name or not password:
        return jsonify({"success": False, "message": "ফোন, নাম এবং পাসওয়ার্ড অবশ্যই দিতে হবে!"})
    
    identifier = phone.lower()
    
    if identifier in user_database:
        if user_database[identifier]["password"] != password:
            return jsonify({"success": False, "message": "ভুল পাসওয়ার্ড! সঠিক পাসওয়ার্ড দিন।"})
    else:
        user_database[identifier] = {
            "password": password,
            "name": name,
            "email": email,
            "saved_text": "",
            "cipher_text": "",
            "level": 1
        }
    
    send_admin_alert(f"📱 অল্টারনেটিভ লগইন (ফোন): <b>{phone}</b> | নাম: <b>{name}</b>")
    
    user_info = user_database[identifier]
    return jsonify({
        "success": True, 
        "message": "লগইন সফল! ড্যাশবোর্ড লোড হচ্ছে...",
        "data": user_info
    })

# ওটিপি ভেরিফিকেশন (টেলিগ্রাম ইউজারদের জন্য)
@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json
    username = data.get('username', '').replace('@', '').lower()
    user_entered_otp = data.get('otp', '').strip()
    
    correct_otp = temp_storage.get(username)
    
    if correct_otp and correct_otp == user_entered_otp:
        send_admin_alert(f"✅ সফলভাবে টেলিগ্রাম ওটিপি ভেরিফাই করেছে: <b>{username}</b>")
        user_info = user_database.get(username, {})
        return jsonify({
            "success": True, 
            "message": "ওটিপি ভেরিফিকেশন সফল! ডেটা লোড হচ্ছে...",
            "data": user_info
        })
    else:
        return jsonify({"success": False, "message": "ভুল ওটিপি কোড!"})

# ইউজার ডেটা সেভ ও সিন্স করার এন্ডপয়েন্ট
@app.route('/save-user-data', methods=['POST'])
def save_user_data():
    data = request.json
    identifier = data.get('identifier', '').strip().lower()
    
    if identifier in user_database:
        user_database[identifier]["saved_text"] = data.get('saved_text', '')
        user_database[identifier]["cipher_text"] = data.get('cipher_text', '')
        user_database[identifier]["level"] = data.get('level', 1)
        return jsonify({"success": True})
    
    return jsonify({"success": False})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
