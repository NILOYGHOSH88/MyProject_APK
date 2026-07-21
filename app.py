import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# আপনার টেলিগ্রাম বটের টোকেন এবং আপনার টেলিগ্রাম চ্যাট আইডি এখানে বসান
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
ADMIN_CHAT_ID = "YOUR_ADMIN_CHAT_ID_HERE"

# পাবলিক ইউজারদের ডাটা সাময়িকভাবে মনে রাখার জন্য ডিকশনারি
user_database = {}


def send_telegram_alert(message):
  try:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": ADMIN_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
    }
    requests.post(url, json=payload, timeout=5)
  except Exception as e:
    print("Telegram Alert Error:", e)


@app.route('/login-step1', methods=['POST'])
def login_step1():
  data = request.get_json()
  username = data.get('username')
  # এখানে আপনার টেলিগ্রাম ওটিপি পাঠানোর লজিক থাকবে
  return jsonify(
      {'success': True, 'message': 'ওটিপি কোড সফলভাবে পাঠানো হয়েছে!'}
  )


@app.route('/verify-otp', methods=['POST'])
def verify_otp():
  data = request.get_json()
  username = data.get('username', '').lower()
  user_data = user_database.get(
      username, {'cipher_text': '', 'saved_text': '', 'level': 1}
  )
  return jsonify({'success': True, 'data': user_data})


@app.route('/alternative-login', methods=['POST'])
def alternative_login():
  data = request.get_json()
  phone = data.get('phone', '').lower()
  user_data = user_database.get(
      phone, {'cipher_text': '', 'saved_text': '', 'level': 1}
  )
  return jsonify({'success': True, 'data': user_data})


@app.route('/save-user-data', methods=['POST'])
def save_user_data():
  data = request.get_json()
  identifier = data.get('identifier')
  if identifier:
    user_database[identifier] = {
        'cipher_text': data.get('cipher_text', ''),
        'level': data.get('level', 1),
    }
  return jsonify({'success': True})


@app.route('/notify-activity', methods=['POST'])
def notify_activity():
  data = request.get_json()
  identifier = data.get('identifier', 'Public User')
  action = data.get('action', 'Unknown')
  text_content = data.get('text', '')

  alert_msg = (
      f"🚨 *নতুন হ্যাকার অ্যাক্টিভিটি!*\n\n👤 *ইউজার:* `{identifier}`\n⚡"
      f" *অ্যাকশন:* `{action}`\n📝 *টেক্সট/কোড:* `{text_content[:100]}`"
  )
  send_telegram_alert(alert_msg)

  return jsonify({'success': True})


if __name__ == '__main__':
  app.run(debug=True)
