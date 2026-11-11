import sqlite3
import os
from datetime import datetime

# Database file will be created at backend/documents.db
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "documents.db")

def get_connection() -> sqlite3.Connection:
    """
    Creates and returns a connection to the SQLite database.
    Row factory set so results come back as dict-like objects.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # lets you access columns by name e.g. row["title"]
    return conn

def init_db() -> None:
    """
    Creates the documents table if it doesn't already exist.
    Call this once when the app starts up.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT    NOT NULL,
            file_type   TEXT    NOT NULL,
            file_path   TEXT,
            status      TEXT    NOT NULL DEFAULT 'uploaded',
            created_at  TEXT    NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def insert_document(title: str, file_type: str, file_path: str = None) -> dict:
    """
    Inserts a new document record and returns the created row.

    Args:
        title: Document title.
        file_type: One of pdf, docx, txt.
        file_path: Path to the stored file (optional for now).

    Returns:
        Dict with the new document's data including its generated id.
    """
    conn = get_connection()
    cursor = conn.cursor()

    created_at = datetime.utcnow().isoformat()

    cursor.execute("""
        INSERT INTO documents (title, file_type, file_path, status, created_at)
        VALUES (?, ?, ?, 'uploaded', ?)
    """, (title, file_type, file_path, created_at))

    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return {
        "id": new_id,
        "title": title,
        "file_type": file_type,
        "file_path": file_path,
        "status": "uploaded",
        "created_at": created_at
    }

def get_all_documents() -> list[dict]:
    """
    Returns all document records from the database.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM documents ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

def get_document_by_id(document_id: int) -> dict | None:
    """
    Returns a single document by ID, or None if not found.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM documents WHERE id = ?", (document_id,))
    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None

def update_document_status(document_id: int, status: str) -> None:
    """
    Updates the processing status of a document.
    Useful for marking a document as 'processed' or 'failed'.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE documents SET status = ? WHERE id = ?
    """, (status, document_id))

    conn.commit()
    conn.close()