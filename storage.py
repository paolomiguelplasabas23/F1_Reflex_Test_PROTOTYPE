import json

# USERS_FILE = "users.json"
SCORES_FILE = "scores.json"

def load_scores():
    try:
        with open(SCORES_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_scores(scores):
    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f, indent = 2)

def add_score(reaction_ms):
    scores = load_scores()
    scores.append({"reaction_ms": reaction_ms})
    save_scores(scores)

def delete_score(index):
    scores = load_scores()
    if 0 <= index < len(scores):
        scores.pop(index)
        save_scores(scores)
        return True
    return False
# NOT FINAL CRUD YET
# # -------------- USERS CRUD ------------------
# def create_user(fullname, username, password):
#     users = load_users()
#     for u in users:
#         if u["username"] == username:
#             return False
#     users.append({"fullname": fullname, "username": username, "password": password})
#     save_users(users)
#     return True

# def read_user(username):
#     for u in load_users():
#         if u["username"] == username:
#             return u
#         return None

# def update_user(username, new_fullname=None, new_password=None):
#     users = load_users()
#     filtered = []
#     for u in users:
#         if u ["username"] != username:
#             filtered.append(u) 
 