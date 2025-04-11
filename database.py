import uuid

# Simulated in-memory database
users_db = {}

def add_user(username, password, email):
    if username in users_db:
        return False, None

    token = str(uuid.uuid4())
    users_db[username] = {
        "username": username, 
        "password": password,
        "email": email,
        "verified": False,
        "token": token
    }
    return True, token

def authenticate_user(username, password):
    user = users_db.get(username)
    if not user:
        return "invalid"
    if user["password"] != password:
        return "invalid"
    if not user["verified"]:
        return "unverified"
    return "success"

def verify_user_token(token):
    for user in users_db.values():
        if user["token"] == token:
            user["verified"] = True
            return True
    return False

