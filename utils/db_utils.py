import os
import sqlite3

DB_PATH = "students.db"

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Call this once at app startup to create the table if it doesn't exist."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id TEXT PRIMARY KEY,
        name       TEXT NOT NULL,
        class      TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def add_student(student_id: str, name: str, class_name: str) -> bool:
    """
    Insert a new student. 
    Returns True on success, False if the ID already exists.
    """
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO students(student_id, name, class) VALUES (?, ?, ?)",
            (student_id, name, class_name)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return False
    conn.close()
    return True

def get_all_students():
    """Return a list of dicts: [{'student_id':..., 'name':..., 'class':...}, ...]."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT student_id, name, class FROM students ORDER BY student_id")
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_student(student_id: str):
    """Return a dict or None."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT student_id, name, class FROM students WHERE student_id = ?", (student_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None
