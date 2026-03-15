"""
Database connection and initialization
"""
import logging
import sqlite3
import os
import time

logger = logging.getLogger(__name__)

from app.db.schema import create_tables


def _get_db_path() -> str:
    """
    Return a persistent, writable path for the SQLite database.

    - When running from source (development): uses  <project-root>/data/habits.db
      (same behaviour as before – CWD is assumed to be the project root).
    - When running as a PyInstaller frozen executable: uses
      ~/.local/share/Growthly/habits.db so data survives between runs and the
      executable never tries to write inside the read-only bundle.
    """
    if getattr(__import__("sys"), "frozen", False):
        # Frozen / packaged executable
        data_dir = os.path.join(
            os.path.expanduser("~"), ".local", "share", "Growthly"
        )
    else:
        # Development – keep data next to the project root
        project_root = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        data_dir = os.path.join(project_root, "data")

    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "habits.db")


DB_PATH = _get_db_path()


def get_db_connection(retries: int = 3):
    """Get a database connection with row factory and retry logic."""
    for attempt in range(retries):
        try:
            conn = sqlite3.connect(DB_PATH, timeout=10.0)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys = ON")
            return conn
        except sqlite3.OperationalError as e:
            if "locked" in str(e) and attempt < retries - 1:
                logger.warning(
                    "Database locked, retrying… (attempt %d/%d)", attempt + 1, retries
                )
                time.sleep(0.5)
            else:
                raise

    raise sqlite3.OperationalError("Database is locked after multiple retries")


def init_db():
    """Initialize database with schema."""
    conn = get_db_connection()
    cursor = conn.cursor()
    create_tables(cursor)
    conn.commit()
    conn.close()
    logger.info("✅ Database initialized successfully at: %s", DB_PATH)


def get_db():
    """Legacy alias kept for compatibility."""
    return get_db_connection()