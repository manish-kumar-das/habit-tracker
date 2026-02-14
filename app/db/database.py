"""
Database connection and operations
"""

import sqlite3
import os
from typing import List, Tuple, Optional, Any
from app.utils.constants import DB_PATH
from app.db.schema import get_all_schema_queries


class Database:
    """Database manager class"""
    
    def __init__(self, db_path: str = DB_PATH):
        """Initialize database connection"""
        self.db_path = db_path
        self._ensure_data_directory()
        self._initialize_database()
    
    def _ensure_data_directory(self):
        """Ensure data directory exists"""
        data_dir = os.path.dirname(self.db_path)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def _initialize_database(self):
        """Create tables if they don't exist"""
        queries = get_all_schema_queries()
        for query in queries:
            self.execute(query)
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Access columns by name
        conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign keys
        return conn
    
    def execute(self, query: str, params: Tuple = ()) -> sqlite3.Cursor:
        """Execute a query and commit"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor
        finally:
            conn.close()
    
    def fetchall(self, query: str, params: Tuple = ()) -> List[sqlite3.Row]:
        """Execute query and fetch all results"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            conn.close()
    
    def fetchone(self, query: str, params: Tuple = ()) -> Optional[sqlite3.Row]:
        """Execute query and fetch one result"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()
        finally:
            conn.close()
    
    def insert(self, query: str, params: Tuple = ()) -> int:
        """Insert and return last row id"""
        cursor = self.execute(query, params)
        return cursor.lastrowid


# Global database instance
_db_instance = None


def get_db() -> Database:
    """Get global database instance (singleton pattern)"""
    global _db_instance
    if _db_instance is None:
        _db_instance = Database()
    return _db_instance
