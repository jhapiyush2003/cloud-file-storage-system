import sqlite3
from pathlib import Path
from typing import List, Optional

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DB_PATH = DATA_DIR / "storage.db"


def get_connection() -> sqlite3.Connection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            original_name TEXT NOT NULL,
            storage_path TEXT NOT NULL,
            mime_type TEXT NOT NULL,
            size INTEGER NOT NULL,
            description TEXT,
            uploaded_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )
    conn.commit()
    conn.close()


def create_user(username: str, password_hash: str, full_name: Optional[str] = None) -> bool:
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO users (username, password_hash, full_name) VALUES (?, ?, ?)",
            (username, password_hash, full_name),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_user(username: str) -> Optional[sqlite3.Row]:
    conn = get_connection()
    cursor = conn.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user


def get_user_by_id(user_id: int) -> Optional[sqlite3.Row]:
    conn = get_connection()
    cursor = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user


def add_file_record(
    user_id: int,
    original_name: str,
    storage_path: str,
    mime_type: str,
    size: int,
    description: Optional[str] = None,
) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO files (user_id, original_name, storage_path, mime_type, size, description) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, original_name, storage_path, mime_type, size, description),
    )
    conn.commit()
    file_id = cursor.lastrowid
    conn.close()
    return file_id


def get_user_files(user_id: int) -> List[sqlite3.Row]:
    conn = get_connection()
    cursor = conn.execute(
        "SELECT * FROM files WHERE user_id = ? ORDER BY uploaded_at DESC", (user_id,)
    )
    result = cursor.fetchall()
    conn.close()
    return result


def search_user_files(user_id: int, search_term: str) -> List[sqlite3.Row]:
    query = f"%{search_term.strip().lower()}%"
    conn = get_connection()
    cursor = conn.execute(
        "SELECT * FROM files WHERE user_id = ? AND (LOWER(original_name) LIKE ? OR LOWER(description) LIKE ?) ORDER BY uploaded_at DESC",
        (user_id, query, query),
    )
    result = cursor.fetchall()
    conn.close()
    return result


def get_file_by_id(file_id: int, user_id: int) -> Optional[sqlite3.Row]:
    conn = get_connection()
    cursor = conn.execute(
        "SELECT * FROM files WHERE id = ? AND user_id = ?", (file_id, user_id)
    )
    file_row = cursor.fetchone()
    conn.close()
    return file_row


def delete_file_record(file_id: int, user_id: int) -> bool:
    conn = get_connection()
    cursor = conn.execute(
        "DELETE FROM files WHERE id = ? AND user_id = ?", (file_id, user_id)
    )
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted


def get_user_stats(user_id: int) -> dict:
    conn = get_connection()
    cursor = conn.execute(
        "SELECT COUNT(*) AS total_files, COALESCE(SUM(size), 0) AS total_bytes FROM files WHERE user_id = ?",
        (user_id,),
    )
    row = cursor.fetchone()
    conn.close()
    return {
        "total_files": row["total_files"],
        "total_bytes": row["total_bytes"],
    }
