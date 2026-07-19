def encrypt(text):
    # আপনার আসল এনক্রিপশন লজিক এখানে হবে
    return text[::-1] + "_ENCRYPTED"

def decrypt(text):
    return text.replace("_ENCRYPTED", "")[::-1]