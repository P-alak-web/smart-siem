import sqlite3

DB_NAME = "smart_siem.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Create logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_id TEXT,
            ip_address TEXT,
            username TEXT,
            action TEXT,
            timestamp TEXT,
            risk_score INTEGER,
            is_noise BOOLEAN,
            reason TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_log_to_db(log_data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO logs (agent_id, ip_address, username, action, timestamp, risk_score, is_noise, reason)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        log_data["agent_id"],
        log_data["ip_address"],
        log_data["username"],
        log_data["action"],
        log_data["timestamp"],
        log_data["risk_score"],
        log_data["is_noise"],
        log_data["reason"]
    ))
    conn.commit()
    conn.close()

def get_all_logs_from_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # To return results as dictionaries
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]