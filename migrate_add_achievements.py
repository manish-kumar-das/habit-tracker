"""
Migration: Add achievements table
"""

import sqlite3
import os

DB_PATH = os.path.join("data", "habits.db")

def migrate():
    """Add achievements table"""
    print("🔄 Starting migration: Add achievements table...")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS achievements (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                icon TEXT NOT NULL,
                category TEXT NOT NULL,
                requirement INTEGER NOT NULL,
                is_unlocked INTEGER DEFAULT 0,
                unlocked_date TEXT,
                rarity TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        print("✅ Achievements table created!")
        
        conn.close()
        print("✅ Migration completed!")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        raise

if __name__ == "__main__":
    migrate()
