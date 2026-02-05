"""
Database schema definitions
"""

CREATE_HABITS_TABLE = """
CREATE TABLE IF NOT EXISTS habits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    frequency TEXT NOT NULL DEFAULT 'daily',
    created_at TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1
)
"""

CREATE_HABIT_LOGS_TABLE = """
CREATE TABLE IF NOT EXISTS habit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    habit_id INTEGER NOT NULL,
    completed_date TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (habit_id) REFERENCES habits (id) ON DELETE CASCADE,
    UNIQUE(habit_id, completed_date)
)
"""

CREATE_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_habit_logs_habit_id ON habit_logs(habit_id)",
    "CREATE INDEX IF NOT EXISTS idx_habit_logs_date ON habit_logs(completed_date)",
    "CREATE INDEX IF NOT EXISTS idx_habits_active ON habits(is_active)"
]


def get_all_schema_queries():
    """Get all schema creation queries"""
    queries = [
        CREATE_HABITS_TABLE,
        CREATE_HABIT_LOGS_TABLE
    ]
    queries.extend(CREATE_INDEXES)
    return queries
