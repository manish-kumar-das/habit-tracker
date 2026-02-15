"""
Database connection and initialization
"""

import sqlite3
import os
from app.db.schema import create_tables

DB_PATH = os.path.join("data", "habits.db")


def get_db_connection():
    """Get database connection with row factory"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Initialize database with schema"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create all tables
    create_tables(cursor)
    
    conn.commit()
    conn.close()
    
    print("✅ Database initialized successfully!")


def get_db():
    """Legacy function for compatibility"""
    return get_db_connection()
