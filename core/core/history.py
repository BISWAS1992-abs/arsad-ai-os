import sqlite3

DB_NAME = "memory.db"


def init_history():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            role TEXT,
            message TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_history(user_id, role, message):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO history(user_id, role, message) VALUES (?, ?, ?)",
        (user_id, role, message)
    )

    conn.commit()
    conn.close()


def get_history(user_id, limit=6):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT role, message
        FROM history
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT ?
        """,
        (user_id, limit)
    )

    rows = cursor.fetchall()

    conn.close()

    rows.reverse()

    history = ""

    for role, message in rows:
        history += f"{role}: {message}\n"

    return history
