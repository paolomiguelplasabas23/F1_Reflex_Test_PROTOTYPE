from database import DB

def login(username: str):
    """Return a player dict if the username exists, otherwise None."""
    if not username:
        return None
    return DB.find_player(username)

def register(fullname: str, username: str):
    """Create a new player. Returns (success: bool, message: str)."""
    if not fullname or not username:
        return False, "Fill in all fields."

    pid = DB.create_player(fullname, username)
    if pid is None:
        return False, "Username already exists."

    return True, "Account created."