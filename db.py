import sqlite3, os

DB_PATH = "data/storage.db"

def get_conn():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            storage_limit INTEGER DEFAULT 5368709120,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            original_name TEXT NOT NULL,
            file_type TEXT NOT NULL,
            file_size INTEGER NOT NULL,
            mime_type TEXT DEFAULT '',
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_starred INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)
    conn.commit(); conn.close()

def _row(conn, q, p=()):
    r = conn.execute(q, p).fetchone()
    return dict(r) if r else None

def _rows(conn, q, p=()):
    return [dict(r) for r in conn.execute(q, p).fetchall()]

def get_user_by_username(username):
    c = get_conn(); u = _row(c, "SELECT * FROM users WHERE username=?", (username,)); c.close(); return u

def get_user_by_email(email):
    c = get_conn(); u = _row(c, "SELECT * FROM users WHERE email=?", (email,)); c.close(); return u

def create_user(username, email, pw_hash):
    c = get_conn()
    try:
        c.execute("INSERT INTO users (username,email,password_hash) VALUES (?,?,?)", (username, email, pw_hash))
        c.commit(); return True
    except sqlite3.IntegrityError: return False
    finally: c.close()

def update_password(user_id, new_hash):
    c = get_conn(); c.execute("UPDATE users SET password_hash=? WHERE id=?", (new_hash, user_id)); c.commit(); c.close()

def save_file(user_id, filename, original_name, file_type, file_size, mime_type):
    c = get_conn()
    c.execute("INSERT INTO files (user_id,filename,original_name,file_type,file_size,mime_type) VALUES (?,?,?,?,?,?)",
              (user_id, filename, original_name, file_type, file_size, mime_type))
    c.commit(); c.close()

def get_files(user_id, search="", ftype="All"):
    c = get_conn()
    q = "SELECT * FROM files WHERE user_id=?"
    p = [user_id]
    if search: q += " AND original_name LIKE ?"; p.append(f"%{search}%")
    if ftype != "All": q += " AND file_type=?"; p.append(ftype)
    q += " ORDER BY upload_date DESC"
    rows = _rows(c, q, p); c.close(); return rows

def delete_file(file_id, user_id):
    c = get_conn()
    r = _row(c, "SELECT filename FROM files WHERE id=? AND user_id=?", (file_id, user_id))
    if r: c.execute("DELETE FROM files WHERE id=? AND user_id=?", (file_id, user_id)); c.commit()
    c.close(); return r["filename"] if r else None

def toggle_star(file_id, user_id):
    c = get_conn()
    c.execute("UPDATE files SET is_starred=1-is_starred WHERE id=? AND user_id=?", (file_id, user_id))
    c.commit(); c.close()

def get_stats(user_id):
    c = get_conn()
    breakdown = _rows(c, "SELECT file_type, COUNT(*) cnt, COALESCE(SUM(file_size),0) sz FROM files WHERE user_id=? GROUP BY file_type", (user_id,))
    total_files = c.execute("SELECT COUNT(*) FROM files WHERE user_id=?", (user_id,)).fetchone()[0]
    total_size  = c.execute("SELECT COALESCE(SUM(file_size),0) FROM files WHERE user_id=?", (user_id,)).fetchone()[0]
    limit       = c.execute("SELECT storage_limit FROM users WHERE id=?", (user_id,)).fetchone()[0]
    recent      = _rows(c, "SELECT * FROM files WHERE user_id=? ORDER BY upload_date DESC LIMIT 6", (user_id,))
    c.close()
    return {"total_files": total_files, "total_size": total_size, "limit": limit,
            "breakdown": {r["file_type"]: {"count": r["cnt"], "size": r["sz"]} for r in breakdown},
            "recent": recent}
