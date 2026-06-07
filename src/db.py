
import sqlite3
import os
 
DB_PATH = "data/storage.db"
 
def get_conn():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn
 
def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.executescript("""
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
    conn.commit()
    conn.close()
 
def get_user_by_username(username):
    conn = get_conn()
    row = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
    conn.close()
    return dict(row) if row else None
 
def get_user_by_email(email):
    conn = get_conn()
    row = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
    conn.close()
    return dict(row) if row else None
 
def create_user(username, email, password_hash):
    conn = get_conn()
    try:
        conn.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?,?,?)",
            (username, email, password_hash)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
 
def update_user_password(user_id, new_hash):
    conn = get_conn()
    conn.execute("UPDATE users SET password_hash=? WHERE id=?", (new_hash, user_id))
    conn.commit()
    conn.close()
 
def save_file_record(user_id, filename, original_name, file_type, file_size, mime_type):
    conn = get_conn()
    conn.execute(
        """INSERT INTO files (user_id, filename, original_name, file_type, file_size, mime_type)
           VALUES (?,?,?,?,?,?)""",
        (user_id, filename, original_name, file_type, file_size, mime_type)
    )
    conn.commit()
    conn.close()
 
def get_user_files(user_id, search="", file_type_filter="All"):
    conn = get_conn()
    query = "SELECT * FROM files WHERE user_id=?"
    params = [user_id]
    if search:
        query += " AND original_name LIKE ?"
        params.append(f"%{search}%")
    if file_type_filter != "All":
        query += " AND file_type=?"
        params.append(file_type_filter)
    query += " ORDER BY upload_date DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]
 
def delete_file_record(file_id, user_id):
    conn = get_conn()
    row = conn.execute("SELECT filename FROM files WHERE id=? AND user_id=?", (file_id, user_id)).fetchone()
    if row:
        conn.execute("DELETE FROM files WHERE id=? AND user_id=?", (file_id, user_id))
        conn.commit()
    conn.close()
    return row["filename"] if row else None
 
def toggle_star(file_id, user_id):
    conn = get_conn()
    conn.execute(
        "UPDATE files SET is_starred = 1 - is_starred WHERE id=? AND user_id=?",
        (file_id, user_id)
    )
    conn.commit()
    conn.close()
 
def get_user_stats(user_id):
    conn = get_conn()
    rows = conn.execute("SELECT file_type, COUNT(*) as cnt, SUM(file_size) as total FROM files WHERE user_id=? GROUP BY file_type", (user_id,)).fetchall()
    total_files = conn.execute("SELECT COUNT(*) FROM files WHERE user_id=?", (user_id,)).fetchone()[0]
    total_size = conn.execute("SELECT COALESCE(SUM(file_size),0) FROM files WHERE user_id=?", (user_id,)).fetchone()[0]
    storage_limit = conn.execute("SELECT storage_limit FROM users WHERE id=?", (user_id,)).fetchone()[0]
    conn.close()
    type_breakdown = {r["file_type"]: {"count": r["cnt"], "size": r["total"] or 0} for r in rows}
    return {
        "total_files": total_files,
        "total_size": total_size,
        "storage_limit": storage_limit,
        "type_breakdown": type_breakdown,
    }
 
def get_recent_files(user_id, limit=5):
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM files WHERE user_id=? ORDER BY upload_date DESC LIMIT ?",
        (user_id, limit)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
