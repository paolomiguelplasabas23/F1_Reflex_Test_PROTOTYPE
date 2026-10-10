from database import DB

def get_top_10():
    """Return the top-10 leaderboard rows."""
    return DB.get_leaderboard()