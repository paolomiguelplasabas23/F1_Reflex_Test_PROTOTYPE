from database import DB


def rate_reaction(ms: int) -> str:
    """Convert a reaction time in milliseconds to a rating tier."""
    if ms < 150: return "F1 Racer"
    if ms < 200: return "F2 Racer"
    if ms < 250: return "F3 Racer"
    if ms < 350: return "Karting Racer"
    return "Normal Driver, Slow"


def save_jump_start(player_id: int):
    """Record a jump-start session."""
    DB.create_session(player_id, "Jump Start")


def save_valid_reaction(player_id: int, reaction_ms: int) -> str:
    """Record a valid reaction, then rebuild the leaderboard."""
    rating = rate_reaction(reaction_ms)
    session_id = DB.create_session(player_id, "Valid")
    DB.save_reaction(session_id, player_id, reaction_ms, rating)
    DB.refresh_leaderboard()
    return rating