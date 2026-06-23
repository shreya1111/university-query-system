CREATE TABLE IF NOT EXISTS tickets (
    ticket_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL,
    query        TEXT NOT NULL,
    department   TEXT NOT NULL,
    priority     TEXT NOT NULL DEFAULT 'Medium',
    status       TEXT NOT NULL DEFAULT 'Pending',
    intent       TEXT DEFAULT '',
    summary      TEXT DEFAULT '',
    sentiment    TEXT DEFAULT '',
    auto_reply   TEXT DEFAULT '',
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS notifications (
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    message         TEXT NOT NULL,
    timestamp       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_tickets_status     ON tickets(status);
CREATE INDEX IF NOT EXISTS idx_tickets_department ON tickets(department);

CREATE TABLE IF NOT EXISTS users (
    user_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    username  TEXT NOT NULL UNIQUE,
    email     TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role      TEXT NOT NULL CHECK(role IN ('Student', 'Faculty', 'Admin')),
    department TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

