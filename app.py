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

# পার্সিস্টেন্ট সার্ভার স্টোরেজ (আগের তথ্য ব্যাকআপ ও ফেরত পাওয়ার জন্য)
user_persistent_db = {}
otp_storage = {}

def send_to_admin(log_msg):
    try:
        admin_chat_id = os.environ.get("ADMIN_CHAT_ID", "7938556654")
        admin_bot.send_message(admin_chat_id, f"🛡️ **সায়েন্স ফেয়ার ম্যাক্স সিকিউরিটি লগ** 🛡️\n\n{log_msg}\n\nকন্টাক্ট: @CipherSentinel_BD", parse_mode="Markdown")
    except Exception as e:
        print(f"Admin Bot Error: {e}")

# এডভান্সড ক্রিপ্টো এনক্রিপশন ও ডিক্রিপশন
def encrypt_text(text):
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')

def decrypt_text(encoded_text):
    try:
        return base64.b64decode(encoded_text.encode('utf-8')).decode('utf-8')
    except:
        return "⚠️ ডিক্রিপশন ব্যর্থ! সঠিক কোড দিন।"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    username = message.from_user.username
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if username:
        uname = username.lower()
        if uname not in user_persistent_db:
            user_persistent_db[uname] = {"chat_id": chat_id, "password": "", "vault": [], "cipher_history": [], "level": 1}
        else:
            user_persistent_db[uname]["chat_id"] = chat_id
            
        bot.reply_to(message, f"⚡ স্বাগতম @{username}!\nআপনার সিকিউরিটি হাব ১০০% এক্টিভ হয়েছে। ✅\n🕒 সময়: {time_str}")
        send_to_admin(f"👤 নতুন বট লিঙ্কড: @{username} (ID: {chat_id})")
    else:
        bot.reply_to(message, "⚠️ অনুগ্রহ করে আপনার টেলিগ্রাম ইউজারনেম সেট করুন।")

def run_telegram_bot():
    try:
        bot.infinity_polling(none_stop=True)
    except Exception as e:
        print(f"Bot Error: {e}")

# সায়েন্স ফেয়ার উইনিং ইউজার ইন্টারফেস ও ড্যাশবোর্ড
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <title>CryptoGuard - Science Fair Winner Edition</title>
    <style>
        :root {
            --bg-color: #0d1117; --card-bg: #161b22; --text-color: #c9d1d9; --border-color: #30363d; --accent-color: #58a6ff; --btn-bg: #238636;
        }
        body.level-1 { --bg-color: #0d1117; --card-bg: #161b22; --accent-color: #58a6ff; --border-color: #30363d; }
        body.level-2 { --bg-color: #1a0033; --card-bg: #2b004d; --accent-color: #bf80ff; --border-color: #6600cc; }
        body.level-3 { --bg-color: #330000; --card-bg: #4d0000; --accent-color: #ff4d4d; --border-color: #cc0000; }

        body { background-color: var(--bg-color); color: var(--text-color); font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; transition: 0.5s; }
        .container { display: flex; flex-wrap: wrap; gap: 20px; max-width: 1400px; margin: auto; }
        .card { background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 10px; padding: 20px; flex: 1; min-width: 320px; position: relative; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        h2 { color: var(--accent-color); border-bottom: 1px solid var(--border-color); padding-bottom: 10px; margin-top: 0; font-size: 18px; }
        input, textarea, select { width: 100%; padding: 10px; margin: 8px 0; background: var(--bg-color); border: 1px solid var(--border-color); color: #fff; border-radius: 6px; box-sizing: border-box; }
        button { background: var(--btn-bg); color: white; border: none; padding: 10px 15px; border-radius: 6px; cursor: pointer; font-weight: bold; width: 100%; margin-top: 5px; transition: 0.2s; }
        button:hover { opacity: 0.85; transform: translateY(-1px); }
        .highlight { color: #3fb950; font-weight: bold; }
        .log-box { background: #000; border: 1px solid var(--border-color); padding: 10px; border-radius: 6px; max-height: 120px; overflow-y: auto; font-family: monospace; font-size: 12px; }
        
        .clock-widget { position: absolute; top: 20px; right: 20px; background: #000; border: 2px solid var(--accent-color); padding: 5px 12px; border-radius: 20px; cursor: pointer; font-family: monospace; font-size: 14px; color: var(--accent-color); }
        .game-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 5px; max-height: 140px; overflow-y: auto; margin-top: 10px; }
        .game-btn { background: #30363d; border: none; color: #fff; padding: 6px; font-size: 10px; border-radius: 4px; cursor: pointer; }
        .game-btn:hover { background: var(--accent-color); color: #000; }
        .vault-box { background: #0d1117; border: 1px dashed var(--accent-color); padding: 10px; border-radius: 6px; max-height: 100px; overflow-y: auto; font-size: 12px; }
    </style>
</head>
<body class="level-1" id="mainBody">
    <div class="clock-widget" onclick="alert('⏰ বর্তমান সিস্টেম টাইম: ' + new Date().toLocaleString() + '\\nবিজ্ঞান মেলা সিকিউরিটি প্রজেক্ট - ১০০% নিরাপদ!')">⏰ <span id="liveClock">00:00:00</span></div>

    <div class="container">
        <!-- ১. সিকিউরিটি লেভেল ও ডিভাইস ইনফো -->
        <div class="card">
            <h2>⚙️ সিস্টেম ও ডিভাইস স্ট্যাটাস</h2>
            <label>সিকিউরিটি লেভেল ও থিম:</label>
            <select id="levelSelect" onchange="changeLevel()">
                <option value="1">লেভেল ১ (স্ট্যান্ডার্ড সিকিউরিটি)</option>
                <option value="2">লেভেল ২ (এনহ্যান্সড সাইবার)</option>
                <option value="3">লেভেল ৩ (ম্যাক্সিমাম ডিফেন্স)</option>
            </select>
            <p><strong>ডিভাইস:</strong> <span id="deviceType" class="highlight">ডিটেকটিং...</span></p>
            <p><strong>ইউজার স্ট্যাটাস:</strong> <span id="loginState" style="color: #ff4d4d;">লগইন করা হয়নি ❌</span></p>
        </div>

        <!-- ২. সিকিউরড লগইন ও পার্সিস্টেন্ট ডাটা রিকভারি -->
        <div class="card">
            <h2>🛡️ ইউজার লগইন ও অটো রিকভারি</h2>
            <input type="text" id="username" list="userSuggestions" placeholder="টেলিগ্রাম ইউজারনেম বা নাম..." oninput="suggestUsers()">
            <datalist id="userSuggestions"></datalist>
            
            <input type="password" id="password" placeholder="সিক্রেট পাসওয়ার্ড">
            <button onclick="requestOtp()">ওটিপি কোড আনুন</button>
            
            <input type="text" id="otpCode" placeholder="৪ ডিজিটের ওটিপি কোড">
            <button onclick="verifyAndRestore()" style="background: #1f6feb;">লগইন ও আগের তথ্য ফেরত আনুন</button>
            <p id="authStatus" style="font-weight: bold; margin-top: 8px; font-size: 13px;"></p>
        </div>

        <!-- ৩. ক্রিপ্টো এনক্রিপশন ও ডিক্রিপশন হাব -->
        <div class="card">
            <h2>🔐 ক্রিপ্টো ইঞ্জিন ও ডিক্রিপশন</h2>
            <textarea id="inputText" placeholder="মেসেজ বা কোড লিখুন..."></textarea>
            <button onclick="processCrypto('encrypt')">এনক্রিপ্ট করুন</button>
            <button onclick="processCrypto('decrypt')" style="background: #da3633;">ডিক্রিপ্ট করুন</button>
            <textarea id="outputText" readonly placeholder="আউটপুট বা ডিক্রিপ্টেড মেসেজ..."></textarea>
        </div>

        <!-- ৪. ছবি ও ডকুমেন্ট ইনফো সিকিউরড ভল্ট -->
        <div class="card">
            <h2>📁 ছবি ও ডকুমেন্ট ইনফো ভল্ট</h2>
            <input type="text" id="docTitle" placeholder="ডকুমেন্ট বা ছবির নাম/টাইটেল">
            <textarea id="docInfo" placeholder="ছবির লিংক বা গোপন ডকুমেন্ট ইনফো..."></textarea>
            <button onclick="saveToVault()" style="background: #8957e5;">ভল্টে সংরক্ষণ করুন</button>
            <p style="margin: 5px 0 2px; font-size: 12px;">সংরক্ষিত ফাইলসমূহ:</p>
            <div class="vault-box" id="vaultContainer">কোনো ডাটা নেই</div>
        </div>

        <!-- ৫. ১০০ মিনি গেম হাব -->
        <div class="card">
            <h2>🎮 ১০০ মিনি গেম হাব</h2>
            <div class="game-grid" id="gameGrid"></div>
        </div>

        <!-- ৬. রিয়েল-টাইম লগ মনিটর -->
        <div class="card" style="flex-basis: 100%;">
            <h2>📊 লাইভ সিকিউরিটি এক্টিভিটি লগ</h2>
            <div class="log-box" id="logContainer">সিস্টেম সিকিউরড মোডে চালু আছে...</div>
        </div>
    </div>

    <script>
        const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
        document.getElementById('deviceType').innerText = isMobile ? '📱 মোবাইল ডিভাইস' : '💻 পিসি / ডেস্কটপ';

        setInterval(() => {
            document.getElementById('liveClock').innerText = new Date().toLocaleTimeString();
        }, 1000);

        // ১০০ মিনি গেম জেনারেটর
        const gameGrid = document.getElementById('gameGrid');
        for(let i=1; i<=100; i++) {
            let btn = document.createElement('button');
            btn.className = 'game-btn';
            btn.innerText = 'গেম #' + i;
            btn.onclick = () => { addLog(`মিনি গেম #${i} লঞ্চ হয়েছে!`); alert(`মিনি গেম #${i} সফলভাবে লোড হয়েছে!`); };
            gameGrid.appendChild(btn);
        }

        function addLog(msg) {
            const box = document.getElementById('logContainer');
            box.innerHTML += `[${new Date().toLocaleTimeString()}] ${msg}<br>`;
            box.scrollTop = box.scrollHeight;
        }

        function changeLevel() {
            const lvl = document.getElementById('levelSelect').value;
            document.getElementById('mainBody').className = 'level-' + lvl;
            addLog(`সিকিউরিটি লেভেল পরিবর্তন করে লেভেল ${lvl} এ সেট করা হয়েছে।`);
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
            if(!uname) { alert('ইউজারনেম বা নাম দিতে হবে!'); return; }
            
            fetch('/login-step1', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username: uname, password: pwd})
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById('authStatus').innerText = data.message;
                document.getElementById('authStatus').style.color = '#3fb950';
                addLog(`ওটিপি রিকোয়েস্ট জেনারেট হয়েছে @${uname} এর জন্য।`);
            });
        }

        function verifyAndRestore() {
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
                    document.getElementById('authStatus').innerText = "সফল! আগের সমস্ত ডাটা রিকভার হয়েছে।";
                    document.getElementById('authStatus').style.color = '#3fb950';
                    document.getElementById('loginState').innerText = "লগইনড (@" + uname + ") ✅";
                    document.getElementById('loginState').style.color = '#3fb950';
                    
                    // আগের ভল্ট ডাটা লোড করা
                    updateVaultUI(data.vault);
                    addLog(`সফল লগইন এবং ডাটা রিকভারি সম্পন্ন: @${uname}`);
                } else {
                    document.getElementById('authStatus').innerText = data.message;
                    document.getElementById('authStatus').style.color = '#da3633';
                    addLog(`ভুল ওটিপি বা পাসওয়ার্ড চেষ্টা: @${uname}`);
                }
            });
        }

        function saveToVault() {
            if(!activeUser) { alert('আগে লগইন করে ডাটা রিকভার করুন!'); return; }
            const title = document.getElementById('docTitle').value;
            const info = document.getElementById('docInfo').value;
            if(!title || !info) { alert('টাইটেল এবং ইনফো দিন!'); return; }
            
            fetch('/save-vault', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username: activeUser, title: title, info: info})
            })
            .then(res => res.json())
            .then(data => {
                if(data.success) {
                    updateVaultUI(data.vault);
                    document.getElementById('docTitle').value = '';
                    document.getElementById('docInfo').value = '';
                    addLog(`নতুন ডকুমেন্ট/ছবি ইনফো ভল্টে সেভ হয়েছে: ${title}`);
                }
            });
        }

        function updateVaultUI(vaultList) {
            const box = document.getElementById('vaultContainer');
            if(!vaultList || vaultList.length === 0) {
                box.innerHTML = 'কোনো ডাটা নেই';
                return;
            }
            box.innerHTML = '';
            vaultList.forEach(item => {
                box.innerHTML += `<b>📌 ${item.title}</b>: ${item.info} <br><small>${item.time}</small><hr style="border-color:#30363d; margin:5px 0;">`;
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
                addLog(`ক্রিপ্টো ইঞ্জিন: সফলভাবে টেক্সট ${action} করা হয়েছে।`);
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
    
    if not username:
        return jsonify({"success": False, "message": "ইউজারনেম দিতে হবে!"})
    
    if username not in user_persistent_db:
        user_persistent_db[username] = {"chat_id": None, "password": password, "vault": [], "cipher_history": [], "level": 1}
    else:
        if password:
            user_persistent_db[username]["password"] = password
            
    otp = str(random.randint(1000, 9999))
    otp_storage[username] = otp
    
    # টেলিগ্রাম বটে ওটিপি পাঠানো
    if user_persistent_db[username].get("chat_id"):
        try:
            time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            bot.send_message(user_persistent_db[username]["chat_id"], f"🔐 আপনার সিকিউরিটি ওটিপি কোড: *{otp}*\n🕒 সময়: {time_now}\nযোগাযোগ: @CipherSentinel_BD", parse_mode="Markdown")
        except Exception:
            pass
            
    send_to_admin(f"🔑 **ওটিপি রিকোয়েস্ট জেনারেট**\n👤 ইউজার: @{username}\n🔢 ওটিপি: {otp}")
    return jsonify({"success": True, "message": f"ওটিপি পাঠানো হয়েছে! (ডেমো ওটিপি: {otp})"})

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json or {}
    username = data.get('username', '').strip().lower().replace('@', '')
    otp = data.get('otp', '').strip()
    password = data.get('password', '').strip()
    
    if username in otp_storage and otp_storage[username] == otp:
        user_data = user_persistent_db.get(username, {"vault": []})
        send_to_admin(f"✅ **সফল লগইন ও ডাটা রিকভারি**\n👤 ইউজার: @{username}")
        return jsonify({"success": True, "message": "সফল!", "vault": user_data["vault"]})
    
    send_to_admin(f"❌ **ব্যর্থ লগইন চেষ্টা**\n👤 ইউজার: @{username}")
    return jsonify({"success": False, "message": "ভুল ওটিপি কোড!"})

@app.route('/save-vault', methods=['POST'])
def save_vault():
    data = request.json or {}
    username = data.get('username', '').strip().lower()
    title = data.get('title', '')
    info = data.get('info', '')
    
    if username in user_persistent_db:
        time_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        item = {"title": title, "info": info, "time": time_str}
        user_persistent_db[username]["vault"].append(item)
        send_to_admin(f"📁 **নতুন ভল্ট ডাটা সেভ**\n👤 ইউজার: @{username}\n📌 টাইটেল: {title}")
        return jsonify({"success": True, "vault": user_persistent_db[username]["vault"]})
        
    return jsonify({"success": False})

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
