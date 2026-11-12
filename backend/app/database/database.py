
import sqlite3
from pathlib import Path
from datetime import datetime, timezone



# DATABASE CONFIGURATION


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Database directory outside backend
DATABASE_DIR = PROJECT_ROOT / "database"

DATABASE_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATABASE_DIR / "documents.db"


# DATABASE CONNECTION

def get_connection():

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    return conn



# INITIALIZE DATABASE


def init_db():

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                title TEXT NOT NULL,

                file_type TEXT NOT NULL,

                file_path TEXT,

                status TEXT NOT NULL DEFAULT 'uploaded',

                created_at TEXT NOT NULL
            )
        """)

        conn.commit()

    finally:
        conn.close()



# INSERT DOCUMENT


def insert_document(
    title: str,
    file_type: str,
    file_path: str = None
):

    conn = get_connection()

    try:
        cursor = conn.cursor()

        created_at = datetime.now(timezone.utc).isoformat()

        cursor.execute("""
            INSERT INTO documents
            (title, file_type, file_path, status, created_at)

            VALUES (?, ?, ?, 'uploaded', ?)
        """, (
            title,
            file_type,
            file_path,
            created_at
        ))

        conn.commit()

        document_id = cursor.lastrowid

        return {
            "id": document_id,
            "title": title,
            "file_type": file_type,
            "file_path": file_path,
            "status": "uploaded",
            "created_at": created_at
        }

    finally:
        conn.close()



# GET ALL DOCUMENTS


def get_all_documents():

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, title, file_type, file_path, status, created_at
            FROM documents
            ORDER BY id DESC
        """)

        rows = cursor.fetchall()

        return [dict(row) for row in rows]

    finally:
        conn.close()



# GET DOCUMENT BY ID


def get_document_by_id(document_id: int):

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM documents
            WHERE id = ?
        """, (document_id,))

        row = cursor.fetchone()

        return dict(row) if row else None

    finally:
        conn.close()



# UPDATE DOCUMENT STATUS


def update_document_status(
    document_id: int,
    status: str
):

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE documents
            SET status = ?
            WHERE id = ?
        """, (status, document_id))

        conn.commit()

        return cursor.rowcount > 0

    finally:
        conn.close()
