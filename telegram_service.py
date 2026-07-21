import threading
from telebot import TeleBot

# ১. অ্যাডমিন বট (নোটিফিকেশনের জন্য)
ADMIN_BOT_TOKEN = "8047864259:AAHEokK5sjq1jJFuIq_e94sPIeTM2OlsqSs"
admin_bot = TeleBot(ADMIN_BOT_TOKEN)
ADMIN_CHAT_ID = "7938556654"

# ২. পাবলিক ওটিপি বট (ইউজারদের কোড পাঠানোর জন্য)
OTP_BOT_TOKEN = "8868227957:AAFULZPQT0RMUGWXnQfhLItkMSYFEgkLstg"
otp_bot = TeleBot(OTP_BOT_TOKEN)

# ইউজারদের চ্যাট আইডি সেভ করার মেমোরি ডিকশনারি
user_otp_sessions = {}

# অ্যাডমিন অ্যালার্ট পাঠানোর ফাংশন
def send_admin_alert(message):
    try:
        admin_bot.send_message(ADMIN_CHAT_ID, message, parse_mode="HTML")
    except Exception as e:
        print(f"Admin Bot Error: {e}")

# ওটিপি বটের /start কমান্ড হ্যান্ডলার
@otp_bot.message_handler(commands=['start'])
def handle_otp_start(message):
    chat_id = message.chat.id
    username = message.from_user.username
    
    if username:
        user_otp_sessions[username.lower()] = chat_id
        otp_bot.send_message(chat_id, "✅ সিকিউরিটি ওটিপি সিস্টেমে সফলভাবে কানেক্ট হয়েছেন! এখন ওয়েবসাইট থেকে ওটিপি পেতে পারেন।")
    else:
        otp_bot.send_message(chat_id, "⚠️ আপনার টেলিগ্রাম অ্যাকাউন্টে কোনো ইউজারনেম (Username) সেট করা নেই। দয়া করে ইউজারনেম সেট করুন।")

# ইউজারকে ওটিপি পাঠানোর ফাংশন
def send_otp_to_user(username, otp_code):
    clean_username = username.replace('@', '').lower()
    chat_id = user_otp_sessions.get(clean_username)
    
    if chat_id:
        try:
            otp_bot.send_message(chat_id, f"🔐 আপনার লগইন ওটিপি কোড হলো: *{otp_code}*", parse_mode="Markdown")
            return True
        except Exception as e:
            print(f"OTP Bot Send Error: {e}")
    return False

# ব্যাকগ্রাউন্ডে ওটিপি বট পোলিং চালু রাখার থ্রেড
def run_otp_bot():
    try:
        print("🤖 ওটিপি বট ব্যাকগ্রাউন্ডে চালু হচ্ছে...")
        otp_bot.infinity_polling(none_stop=True)
    except Exception as e:
        print(f"OTP Bot Polling Error: {e}")

def start_telegram_bots_background():
    bot_thread = threading.Thread(target=run_otp_bot, daemon=True)
    bot_thread.start()
