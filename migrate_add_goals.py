"""
Migration: Add goals table
"""

import sqlite3
import os

DB_PATH = os.path.join("data", "habits.db")

def migrate():
    """Add goals table to existing database"""
    print("🔄 Starting migration: Add goals table...")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Create goals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER,
                goal_type TEXT NOT NULL,
                target_value INTEGER NOT NULL,
                current_value INTEGER DEFAULT 0,
                description TEXT NOT NULL,
                start_date TEXT NOT NULL,
                deadline TEXT,
                is_completed INTEGER DEFAULT 0,
                completed_date TEXT,
                category TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (habit_id) REFERENCES habits (id) ON DELETE CASCADE
            )
        ''')
        
        conn.commit()
        print("✅ Goals table created successfully!")
        
        conn.close()
        print("✅ Migration completed!")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        raise

if __name__ == "__main__":
    migrate()
