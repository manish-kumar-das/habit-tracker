"""
Database schema definitions - FIXED
"""

def create_habits_table(cursor):
    """Create habits table"""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            category TEXT DEFAULT 'General',
            frequency TEXT DEFAULT 'daily',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Add category column if it doesn't exist
    try:
        cursor.execute('ALTER TABLE habits ADD COLUMN category TEXT DEFAULT "General"')
    except:
        pass
    
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_habits_category ON habits(category)')


def create_habit_logs_table(cursor):
    """Create habit completion logs table - FIXED"""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            completed_date TEXT NOT NULL,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (habit_id) REFERENCES habits (id) ON DELETE CASCADE,
            UNIQUE(habit_id, completed_date)
        )
    ''')
    
    # Add notes column if it doesn't exist
    try:
        cursor.execute('ALTER TABLE habit_logs ADD COLUMN notes TEXT')
    except:
        pass
    
    # Add created_at if it doesn't exist
    try:
        cursor.execute('ALTER TABLE habit_logs ADD COLUMN created_at TEXT DEFAULT CURRENT_TIMESTAMP')
    except:
        pass
    
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_habit_logs_date ON habit_logs(completed_date)')


def create_deleted_habits_table(cursor):
    """Create deleted habits table"""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS deleted_habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_habit_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            category TEXT,
            frequency TEXT,
            created_at TEXT,
            deleted_at TEXT DEFAULT CURRENT_TIMESTAMP,
            completion_count INTEGER DEFAULT 0
        )
    ''')


def create_settings_table(cursor):
    """Create settings table"""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    ''')
    
    default_settings = [
        ('theme', 'dark'),
        ('notifications_enabled', 'true'),
        ('notification_time', '09:00'),
        ('show_completed', 'true'),
        ('compact_mode', 'false')
    ]
    
    for key, value in default_settings:
        cursor.execute('INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)', (key, value))


def create_goals_table(cursor):
    """Create goals table"""
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


def create_achievements_table(cursor):
    """Create achievements table"""
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


def create_tables(cursor):
    """Create all database tables"""
    create_habits_table(cursor)
    create_habit_logs_table(cursor)
    create_deleted_habits_table(cursor)
    create_settings_table(cursor)
    create_goals_table(cursor)
    create_achievements_table(cursor)
