import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_path: str = "f1_reflex.db"):
        self.db_path = db_path

    # ==========================================================
    # CONNECTION
    # ==========================================================
    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    # ==========================================================
    # CREATE TABLES
    # ==========================================================
    def create_table(self) -> None:
        with self.connect() as conn:

            conn.execute("""
                CREATE TABLE IF NOT EXISTS player (
                    player_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                    fullname    VARCHAR(50) NOT NULL,
                    username    VARCHAR(50) NOT NULL UNIQUE
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS game_sessions (
                    session_id    INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_id     INTEGER NOT NULL,
                    session_date  DATE,
                    session_time  TIME,
                    result        VARCHAR(50)
                                  CHECK(result IN ('Valid', 'Jump Start')),
                    FOREIGN KEY (player_id) REFERENCES player(player_id)
                        ON DELETE CASCADE
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS reaction_time (
                    reaction_id    INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id     INTEGER NOT NULL,
                    player_id      INTEGER NOT NULL,
                    reaction_time  DECIMAL(11,2),
                    rating         VARCHAR(50),
                    FOREIGN KEY (session_id) REFERENCES game_sessions(session_id)
                        ON DELETE CASCADE,
                    FOREIGN KEY (player_id)  REFERENCES player(player_id)
                        ON DELETE CASCADE
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS leaderboard (
                    leaderboard_id  INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_id       INTEGER NOT NULL,
                    rank            INTEGER,
                    date_achieved   DATE,
                    FOREIGN KEY (player_id) REFERENCES player(player_id)
                        ON DELETE CASCADE
                )
            """)

    # ==========================================================
    # PLAYER CRUD
    # ==========================================================
    def create_player(self, fullname: str, username: str):
        try:
            with self.connect() as conn:
                cursor = conn.execute(
                    "INSERT INTO player (fullname, username) VALUES (?, ?)",
                    (fullname, username),
                )
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

    def login_player(self, username: str):
        with self.connect() as conn:
            row = conn.execute(
                "SELECT * FROM player WHERE username = ?",
                (username,),
            ).fetchone()
        return dict(row) if row else None

    def find_player(self, username: str):
        with self.connect() as conn:
            row = conn.execute(
                "SELECT * FROM player WHERE username = ?", (username,)
            ).fetchone()
        return dict(row) if row else None

    def update_player(self, player_id: int, fullname: str = None, password: str = None):
        fields, values = [], []
        if fullname:
            fields.append("fullname = ?")
            values.append(fullname)
        if password:
            fields.append("password = ?")
            values.append(password)
        if not fields:
            return False
        values.append(player_id)
        with self.connect() as conn:
            conn.execute(
                f"UPDATE player SET {', '.join(fields)} WHERE player_id = ?",
                values,
            )
        return True

    def delete_player(self, player_id: int):
        with self.connect() as conn:
            conn.execute("DELETE FROM player WHERE player_id = ?", (player_id,))

    # ==========================================================
    # GAME SESSIONS
    # ==========================================================
    def create_session(self, player_id: int, result: str):
        now = datetime.now()
        with self.connect() as conn:
            cursor = conn.execute(
                """INSERT INTO game_sessions
                   (player_id, session_date, session_time, result)
                   VALUES (?, ?, ?, ?)""",
                (player_id,
                 now.date().isoformat(),
                 now.time().strftime("%H:%M:%S"),
                 result),
            )
            return cursor.lastrowid

    def get_sessions(self, player_id: int):
        with self.connect() as conn:
            rows = conn.execute(
                "SELECT * FROM game_sessions WHERE player_id = ? ORDER BY session_id DESC",
                (player_id,),
            ).fetchall()
        return [dict(r) for r in rows]

    # ==========================================================
    # REACTION TIME
    # ==========================================================
    def save_reaction(self, session_id: int, player_id: int,
                      reaction_ms: float, rating: str):
        with self.connect() as conn:
            cursor = conn.execute(
                """INSERT INTO reaction_time
                   (session_id, player_id, reaction_time, rating)
                   VALUES (?, ?, ?, ?)""",
                (session_id, player_id, reaction_ms, rating),
            )
            return cursor.lastrowid

    def get_reactions(self, player_id: int):
        with self.connect() as conn:
            rows = conn.execute(
                "SELECT * FROM reaction_time WHERE player_id = ? ORDER BY reaction_id DESC",
                (player_id,),
            ).fetchall()
        return [dict(r) for r in rows]

    # ==========================================================
    # LEADERBOARD
    # ==========================================================
    def refresh_leaderboard(self):
        with self.connect() as conn:
            conn.execute("DELETE FROM leaderboard")

            rows = conn.execute("""
                SELECT r.player_id,
                       MIN(r.reaction_time) AS best_time,
                       DATE('now') AS today
                FROM reaction_time r
                JOIN game_sessions gs ON gs.session_id = r.session_id
                WHERE gs.result = 'Valid'
                GROUP BY r.player_id
                ORDER BY best_time ASC
                LIMIT 10
            """).fetchall()

            for i, row in enumerate(rows):
                conn.execute(
                    """INSERT INTO leaderboard
                       (player_id, rank, date_achieved)
                       VALUES (?, ?, ?)""",
                    (row["player_id"], i + 1, row["today"]),
                )

    def get_leaderboard(self):
        with self.connect() as conn:
            rows = conn.execute("""
                SELECT l.rank,
                       p.fullname,
                       MIN(r.reaction_time) AS best_time,
                       l.date_achieved
                FROM leaderboard l
                JOIN player p             ON p.player_id = l.player_id
                LEFT JOIN reaction_time r ON r.player_id = p.player_id
                GROUP BY l.leaderboard_id
                ORDER BY l.rank ASC
            """).fetchall()
        return [dict(r) for r in rows]

    # ==========================================================
    # RATING HELPER
    # ==========================================================
    @staticmethod
    def rate_reaction(ms: int) -> str:
        if ms < 150: return "F1 Racer"
        if ms < 200: return "F2 Racer"
        if ms < 250: return "F3 Racer"
        if ms < 350: return "Karting Racer"
        return "Normal Driver"

    