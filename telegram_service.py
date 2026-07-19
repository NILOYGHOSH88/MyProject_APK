def send_to_telegram(text):
    # আপনার নতুন টোকেন এখানে বসান
    token = "8047864259:AAHEokK5sjq1jJFuIq_e94sPIeTM2OlsqSs" 
    # আপনার ইউজার আইডি এখানে বসান
    chat_id = "7938556654" 
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    
    try:
        import requests
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Error: {e}")