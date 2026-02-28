import psycopg2
import psycopg2.extras
from app.config import Config


def get_connection():
    """Open and return a new Postgres connection (autocommit on)."""
    conn = psycopg2.connect(
        host=Config.POSTGRES_HOST,
        port=Config.POSTGRES_PORT,
        dbname=Config.POSTGRES_DB,
        user=Config.POSTGRES_USER,
        password=Config.POSTGRES_PASSWORD,
    )
    conn.autocommit = True
    return conn


def init_db():
    """Create the notes table if it doesn't exist."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id         SERIAL PRIMARY KEY,
                    content    TEXT        NOT NULL,
                    author     VARCHAR(80) NOT NULL DEFAULT 'Anonymous',
                    created_at TIMESTAMP   NOT NULL DEFAULT NOW()
                );
            """)


def ping():
    """Return True if Postgres is reachable."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
    return True


def get_all_notes():
    """Return all notes ordered by newest first."""
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                "SELECT id, content, author, created_at::text FROM notes ORDER BY created_at DESC"
            )
            return [dict(row) for row in cur.fetchall()]


def insert_note(content: str, author: str) -> dict:
    """Insert a note and return its id + created_at."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO notes (content, author) VALUES (%s, %s) RETURNING id, created_at::text",
                (content, author),
            )
            row = cur.fetchone()
    return {"id": row[0], "created_at": row[1]}


def delete_note(note_id: int) -> bool:
    """Delete a note by id. Returns True if a row was deleted."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM notes WHERE id = %s RETURNING id", (note_id,))
            return cur.fetchone() is not None


def count_notes() -> int:
    """Return the total number of notes."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM notes")
            return cur.fetchone()[0]
