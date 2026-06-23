import sqlite3
conn = sqlite3.connect('database/university.db')
conn.executescript("""
CREATE TABLE IF NOT EXISTS users (
    user_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT NOT NULL UNIQUE,
    email         TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role          TEXT NOT NULL CHECK(role IN ('Student', 'Faculty', 'Admin')),
    department    TEXT NOT NULL,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")
conn.commit()

tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print("Tables in DB:", [t[0] for t in tables])
conn.close()
print("Done!")
