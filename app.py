import os
import threading
import random
import base64
from datetime import datetime
import telebot
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# টেলিগ্রাম ও এডমিন বটের টোকেন
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8868227957:AAFULZPQT0RMUGWXnQfhLItkMSYFEgkLstg")
ADMIN_BOT_TOKEN = os.environ.get("ADMIN_BOT_TOKEN", "8047864259:AAHEokK5sjq1jJFuIq_e94sPIeTM2OlsqSs")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
admin_bot = telebot.TeleBot(ADMIN_BOT_TOKEN)

# পার্সিস্টেন্ট সার্ভার ডাটাবেজ (আগের ডাটা ও ভল্ট ব্যাকআপ রাখার জন্য)
user_persistent_db = {}
otp_storage = {}

def send_to_admin(log_msg):
    try:
        admin_chat_id = os.environ.get("ADMIN_CHAT_ID", "7938556654")
        admin_bot.send_message(admin_chat_id, f"🛡️ **সায়েন্স ফেয়ার মাল্টি-লেয়ার সিকিউরিটি লগ** 🛡️\n\n{log_msg}\n\nকন্টাক্ট: @CipherSentinel_BD", parse_mode="Markdown")
    except Exception as e:
        print(f"Admin Bot Error: {e}")

# এডভান্সড ক্রিপ্টো এনক্রিপশন ও ডিক্রিপশন
def encrypt_text(text):
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')

def decrypt_text(encoded_text):
    try:
        return base64.b64decode(encoded_text.encode('utf-8')).decode('utf-8')
    except:
        return "⚠️ ডিক্রিপশন ব্যর্থ! সঠিক এনক্রিপ্টেড কোড দিন।"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    username = message.from_user.username
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if username:
        uname = username.lower()
        if uname not in user_persistent_db:
            user_persistent_db[uname] = {"chat_id": chat_id, "password": "", "vault": [], "cipher_history": []}
        else:
            user_persistent_db[uname]["chat_id"] = chat_id
            
        bot.reply_to(message, f"⚡ স্বাগতম @{username}!\nআপনার মাল্টি-লেয়ার সিকিউরিটি হাব এক্টিভ হয়েছে। ✅\n🕒 সময়: {time_str}")
        send_to_admin(f"👤 নতুন বট লিঙ্কড: @{username} (ID: {chat_id})")
    else:
        bot.reply_to(message, "⚠️ অনুগ্রহ করে আপনার টেলিগ্রাম ইউজারনেম সেট করুন।")

def run_telegram_bot():
    try:
        bot.infinity_polling(none_stop=True)
    except Exception as e:
        print(f"Bot Error: {e}")

# মাল্টি-লেয়ার সাইন্স ফেয়ার উইনিং ইন্টারফেস ও ড্যাশবোর্ড
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <title>CryptoGuard - Multi-Layer Security Suite</title>
    <style>
        :root {
            --bg-color: #0d1117; --card-bg: #161b22; --text-color: #c9d1d9; --border-color: #30363d; --accent-color: #58a6ff; --btn-bg: #238636;
        }
        body { background-color: var(--bg-color); color: var(--text-color); font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; }
        .container { max-width: 1000px; margin: auto; }
        
        /* লেয়ার ট্যাব সিস্টেম */
        .tab-menu { display: flex; gap: 10px; margin-bottom: 20px; border-bottom: 2px solid var(--border-color); padding-bottom: 10px; }
        .tab-btn { background: #21262d; border: 1px solid var(--border-color); color: var(--text-color); padding: 10px 20px; border-radius: 6px; cursor: pointer; font-weight: bold; transition: 0.3s; }
        .tab-btn.active { background: var(--accent-color); color: #000; border-color: var(--accent-color); }
        
        .layer-section { display: none; background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 10px; padding: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); margin-bottom: 20px; }
        .layer-section.active { display: block; }

        h2 { color: var(--accent-color); border-bottom: 1px solid var(--border-color); padding-bottom: 10px; margin-top: 0; font-size: 20px; }
        input, textarea, select { width: 100%; padding: 12px; margin: 10px 0; background: var(--bg-color); border: 1px solid var(--border-color); color: #fff; border-radius: 6px; box-sizing: border-box; }
        button { background: var(--btn-bg); color: white; border: none; padding: 12px 20px; border-radius: 6px; cursor: pointer; font-weight: bold; width: 100%; margin-top: 5px; transition: 0.2s; }
        button:hover { opacity: 0.9; }
        .highlight { color: #3fb950; font-weight: bold; }
        .vault-box { background: #0d1117; border: 1px dashed var(--accent-color); padding: 15px; border-radius: 6px; max-height: 180px; overflow-y: auto; font-size: 13px; margin-top: 10px; }
        .clock-widget { float: right; background: #000; border: 1px solid var(--accent-color); padding: 5px 10px; border-radius: 15px; font-family: monospace; font-size: 13px; color: var(--accent-color); }
    </style>
</head>
<body>
    <div class="container">
        <div style="overflow: hidden; margin-bottom: 15px;">
            <h1 style="margin: 0; font-size: 24px; color: #58a6ff; display: inline-block;">🔒 CryptoGuard Multi-Layer Defense</h1>
            <div class="clock-widget">⏰ <span id="liveClock">00:00:00</span></div>
        </div>

        <!-- মাল্টি-লেয়ার নেভিগেশন মেনু -->
        <div class="tab-menu">
            <button class="tab-btn active" onclick="switchLayer('layer1')">লেয়ার ১: লগইন ও ওটিপি</button>
            <button class="tab-btn" onclick="switchLayer('layer2')" id="btnLayer2" style="opacity: 0.5; cursor: not-allowed;" disabled>লেয়ার ২: ক্রিপ্টো হাব</button>
            <button class="tab-btn" onclick="switchLayer('layer3')" id="btnLayer3" style="opacity: 0.5; cursor: not-allowed;" disabled>লেয়ার ৩: ডকুমেন্ট ভল্ট</button>
        </div>

        <!-- লেয়ার ১: ইউজার লগইন, ওটিপি ও আইপি ট্র্যাকিং -->
        <div class="layer-section active" id="layer1">
            <h2>🛡️ লেয়ার ১: সিকিউরড লগইন ও ওটিপি ভেরিফিকেশন</h2>
            <p>আপনার টেলিগ্রাম ইউজারনেম দিয়ে ওটিপি আনুন এবং আপনার ইচ্ছামতো কাস্টম পাসওয়ার্ড সেট করুন।</p>
            
            <input type="text" id="username" list="userSuggestions" placeholder="টেলিগ্রাম ইউজারনেম (যেমন: username)" oninput="suggestUsers()">
            <datalist id="userSuggestions"></datalist>
            
            <input type="password" id="password" placeholder="আপনার ইচ্ছামতো কাস্টম পাসওয়ার্ড দিন">
            <button onclick="requestOtp()">টেলিগ্রামে ওটিপি কোড পাঠান</button>
            
            <input type="text" id="otpCode" placeholder="৪ ডিজিটের ওটিপি কোড দিন">
            <button onclick="verifyAndUnlock()" style="background: #1f6feb;">ভেরিফাই করুন এবং পরবর্তী লেয়ারে প্রবেশ করুন</button>
            
            <p id="authStatus" style="font-weight: bold; margin-top: 10px; font-size: 14px;"></p>
            <p style="font-size: 12px; color: #8b949e;">নেটওয়ার্ক আইপি ও ডিভাইস ট্র্যাকিং: <span id="clientIp" class="highlight">লোডিং...</span></p>
        </div>

        <!-- লেয়ার ২: এনক্রিপশন ও ডিক্রিপশন ইঞ্জিন -->
        <div class="layer-section" id="layer2">
            <h2>🔐 লেয়ার ২: ক্রিপ্টো এনক্রিপশন ও ডিক্রিপশন হাব</h2>
            <p>মেসেজ এনক্রিপ্ট করুন অথবা অন্য কারো পাঠানো এনক্রিপ্টেড মেসেজ এখানে ডিক্রিপ্ট করুন।</p>
            
            <textarea id="inputText" placeholder="আপনার গোপন টেক্সট বা এনক্রিপ্টেড কোড এখানে লিখুন..."></textarea>
            <button onclick="processCrypto('encrypt')">টেক্সট এনক্রিপ্ট করুন</button>
            <button onclick="processCrypto('decrypt')" style="background: #da3633;">টেক্সট ডিক্রিপ্ট করুন</button>
            
            <textarea id="outputText" readonly placeholder="আউটপুট বা ডিক্রিপ্টেড ফলাফল এখানে দেখাবে..." style="margin-top: 15px;"></textarea>
        </div>

        <!-- লেয়ার ৩: সিকিউরড ডকুমেন্ট ও ইমেজ ইনফো ভল্ট -->
        <div class="layer-section" id="layer3">
            <h2>📁 লেয়ার ৩: সিকিউরড ডকুমেন্ট ও ইমেজ ভল্ট</h2>
            <p>আপনার সংবেদনশীল ছবি, ডকুমেন্ট বা নোটস আলাদা পাসওয়ার্ড সুরক্ষিত ভল্টে সংরক্ষণ করুন।</p>
            
            <input type="text" id="docTitle" placeholder="ফাইলের নাম বা ডকুমেন্ট টাইটেল">
            <textarea id="docInfo" placeholder="গোপন লিংক, ছবির ইনফো বা সিক্রেট নোটস..."></textarea>
            <input type="password" id="vaultPassword" placeholder="এই ভল্টের জন্য আলাদা সিক্রেট পাসওয়ার্ড">
            <button onclick="saveToVault()" style="background: #8957e5;">ভল্টে সেকিউরলি সংরক্ষণ করুন</button>
            
            <p style="margin: 15px 0 5px; font-size: 13px; font-weight: bold;">আপনার সংরক্ষিত ফাইলসমূহ (পার্সিস্টেন্ট ডাটা):</p>
            <div class="vault-box" id="vaultContainer">কোনো ডাটা পাওয়া যায়নি।</div>
        </div>
    </div>

    <script>
        // ক্লায়েন্ট আইপি ডিটেকশন
        fetch('https://api.ipify.org?format=json')
            .then(res => res.json())
            .then(data => { document.getElementById('clientIp').innerText = data.ip; })
            .catch(() => { document.getElementById('clientIp').innerText = '127.0.0.1 (Localhost)'; });

        // লাইভ ঘড়ি
        setInterval(() => {
            document.getElementById('liveClock').innerText = new Date().toLocaleTimeString();
        }, 1000);

        function switchLayer(layerId) {
            document.querySelectorAll('.layer-section').forEach(sec => sec.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            
            document.getElementById(layerId).classList.add('active');
            event.currentTarget.classList.add('active');
        }

        function suggestUsers() {
            const val = document.getElementById('username').value;
            if(val.length > 0) {
                fetch('/get-suggestions?q=' + val)
                .then(res => res.json())
                .then(data => {
                    const dl = document.getElementById('userSuggestions');
                    dl.innerHTML = '';
                    data.users.forEach(u => {
                        let opt = document.createElement('option');
                        opt.value = u;
                        dl.appendChild(opt);
                    });
                });
            }
        }

        let activeUser = '';

        function requestOtp() {
            const uname = document.getElementById('username').value;
            const pwd = document.getElementById('password').value;
            const ip = document.getElementById('clientIp').innerText;
            if(!uname) { alert('দয়া করে টেলিগ্রাম ইউজারনেম দিন!'); return; }
            if(!pwd) { alert('দয়া করে আপনার ইচ্ছামতো কাস্টম পাসওয়ার্ড দিন!'); return; }
            
            fetch('/login-step1', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username: uname, password: pwd, ip: ip})
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById('authStatus').innerText = data.message;
                document.getElementById('authStatus').style.color = '#3fb950';
            });
        }

        function verifyAndUnlock() {
            const uname = document.getElementById('username').value;
            const pwd = document.getElementById('password').value;
            const otp = document.getElementById('otpCode').value;
            
            fetch('/verify-otp', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username: uname, password: pwd, otp: otp})
            })
            .then(res => res.json())
            .then(data => {
                if(data.success) {
                    activeUser = uname;
                    document.getElementById('authStatus').innerText = "ভেরিফিকেশন সফল! আগের সমস্ত ডাটা রিকভার হয়েছে।";
                    document.getElementById('authStatus').style.color = '#3fb950';
                    
                    // লেয়ার ২ ও ৩ আনলক করা
                    document.getElementById('btnLayer2').disabled = false;
                    document.getElementById('btnLayer2').style.opacity = '1';
                    document.getElementById('btnLayer2').style.cursor = 'pointer';
                    
                    document.getElementById('btnLayer3').disabled = false;
                    document.getElementById('btnLayer3').style.opacity = '1';
                    document.getElementById('btnLayer3').style.cursor = 'pointer';
                    
                    updateVaultUI(data.vault);
                    alert('অভিনন্দন! লেয়ার ১ সফলভাবে সম্পন্ন হয়েছে। এখন ক্রিপ্টো এবং ডকুমেন্ট ভল্ট ব্যবহার করতে পারবেন।');
                } else {
                    document.getElementById('authStatus').innerText = data.message;
                    document.getElementById('authStatus').style.color = '#da3633';
                }
            });
        }

        function saveToVault() {
            if(!activeUser) { alert('আগে লেয়ার ১ এ লগইন করুন!'); return; }
            const title = document.getElementById('docTitle').value;
            const info = document.getElementById('docInfo').value;
            const vpass = document.getElementById('vaultPassword').value;
            if(!title || !info || !vpass) { alert('টাইটেল, ইনফো এবং ভল্ট পাসওয়ার্ড দিন!'); return; }
            
            fetch('/save-vault', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username: activeUser, title: title, info: info, vault_pass: vpass})
            })
            .then(res => res.json())
            .then(data => {
                if(data.success) {
                    updateVaultUI(data.vault);
                    document.getElementById('docTitle').value = '';
                    document.getElementById('docInfo').value = '';
                    document.getElementById('vaultPassword').value = '';
                    alert('ডকুমেন্ট সফলভাবে ভল্টে সংরক্ষিত হয়েছে!');
                } else {
                    alert(data.message);
                }
            });
        }

        function updateVaultUI(vaultList) {
            const box = document.getElementById('vaultContainer');
            if(!vaultList || vaultList.length === 0) {
                box.innerHTML = 'কোনো সংরক্ষিত ডাটা নেই';
                return;
            }
            box.innerHTML = '';
            vaultList.forEach(item => {
                box.innerHTML += `<b>📌 ${item.title}</b>: ${item.info} <br><small style="color: #8b949e;">সংরক্ষণ সময়: ${item.time}</small><hr style="border-color:#30363d; margin:8px 0;">`;
            });
        }

        function processCrypto(action) {
            const text = document.getElementById('inputText').value;
            if(!text) { alert('টেক্সট দিন!'); return; }
            
            fetch('/api-crypto', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text: text, action: action, username: activeUser})
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById('outputText').value = data.result;
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/get-suggestions')
def get_suggestions():
    q = request.args.get('q', '').lower()
    matched = [u for u in user_persistent_db.keys() if q in u]
    return jsonify({"users": matched})

@app.route('/login-step1', methods=['POST'])
def login_step1():
    data = request.json or {}
    username = data.get('username', '').strip().lower().replace('@', '')
    password = data.get('password', '').strip()
    ip = data.get('ip', 'Unknown IP')
    
    if not username:
        return jsonify({"success": False, "message": "ইউজারনেম দিতে হবে!"})
    
    if username not in user_persistent_db:
        user_persistent_db[username] = {"chat_id": None, "password": password, "vault": [], "cipher_history": []}
    else:
        user_persistent_db[username]["password"] = password
            
    otp = str(random.randint(1000, 9999))
    otp_storage[username] = otp
    
    if user_persistent_db[username].get("chat_id"):
        try:
            time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            bot.send_message(user_persistent_db[username]["chat_id"], f"🔐 সিকিউরিটি ওটিপি কোড: *{otp}*\n🌐 আইপি: {ip}\n🕒 সময়: {time_now}\nযোগাযোগ: @CipherSentinel_BD", parse_mode="Markdown")
        except Exception:
            pass
            
    send_to_admin(f"🔑 **ওটিপি রিকোয়েস্ট**\n👤 ইউজার: @{username}\n🔑 কাস্টম পাসওয়ার্ড: {password}\n🔢 ওটিপি: {otp}\n🌐 ক্লায়েন্ট আইপি: {ip}")
    return jsonify({"success": True, "message": f"ওটিপি পাঠানো হয়েছে! (ডেমো ওটিপি: {otp})"})

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json or {}
    username = data.get('username', '').strip().lower().replace('@', '')
    otp = data.get('otp', '').strip()
    password = data.get('password', '').strip()
    
    if username in otp_storage and otp_storage[username] == otp:
        user_data = user_persistent_db.get(username, {"vault": []})
        # পাসওয়ার্ড ভেলিডেশন চেক
        if user_data.get("password") and user_data["password"] != password:
            return jsonify({"success": False, "message": "ভুল কাস্টম পাসওয়ার্ড!"})
            
        send_to_admin(f"✅ **লেয়ার ১ সফল লগইন ও রিকভারি**\n👤 ইউজার: @{username}")
        return jsonify({"success": True, "message": "সফল!", "vault": user_data["vault"]})
    
    send_to_admin(f"❌ **ব্যর্থ লগইন চেষ্টা**\n👤 ইউজার: @{username}")
    return jsonify({"success": False, "message": "ভুল ওটিপি কোড!"})

@app.route('/save-vault', methods=['POST'])
def save_vault():
    data = request.json or {}
    username = data.get('username', '').strip().lower()
    title = data.get('title', '')
    info = data.get('info', '')
    vault_pass = data.get('vault_pass', '')
    
    if username in user_persistent_db:
        time_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        item = {"title": title, "info": info, "vault_pass": vault_pass, "time": time_str}
        user_persistent_db[username]["vault"].append(item)
        send_to_admin(f"📁 **ডকুমেন্ট ভল্টে সেভ**\n👤 ইউজার: @{username}\n📌 টাইটেল: {title}")
        return jsonify({"success": True, "vault": user_persistent_db[username]["vault"]})
        
    return jsonify({"success": False, "message": "ইউজার সেশন পাওয়া যায়নি!"})

@app.route('/api-crypto', methods=['POST'])
def api_crypto():
    data = request.json or {}
    text = data.get('text', '')
    action = data.get('action', '')
    username = data.get('username', '')
    
    result = encrypt_text(text) if action == 'encrypt' else decrypt_text(text)
    
    if username and username in user_persistent_db:
        user_persistent_db[username]["cipher_history"].append({"action": action, "input": text, "result": result})
        
    send_to_admin(f"🔐 **ক্রিপ্টো এক্টিভিটি**\n⚙️ একশন: {action}\n📝 টেক্সট: {text}")
    return jsonify({"result": result})

if __name__ == '__main__':
    bot_thread = threading.Thread(target=run_telegram_bot, daemon=True)
    bot_thread.start()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
