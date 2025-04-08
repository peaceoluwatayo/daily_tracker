# database.py

# Temporary in-memory "user store"
users = {}

def add_user(username, password):
    if username in users:
        return False  # User already exists
    users[username] = password
    return True

def authenticate_user(username, password):
    return users.get(username) == password
