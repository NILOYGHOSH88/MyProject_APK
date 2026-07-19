import sqlite3

def verify_user(username, password):
    # ডাটাবেস থেকে ইউজার চেক করার কোড
    if username == "testuser" and password == "12345":
        return True
    return False