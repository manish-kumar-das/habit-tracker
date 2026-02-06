"""
Application-wide constants
"""

# Database
DB_NAME = "habits.db"
DB_PATH = "data/habits.db"

# Date formats
DATE_FORMAT = "%Y-%m-%d"
DISPLAY_DATE_FORMAT = "%B %d, %Y"

# Habit frequencies
FREQUENCY_DAILY = "daily"
FREQUENCY_WEEKLY = "weekly"

# Habit categories
CATEGORIES = [
    ("General", "📌"),
    ("Health", "💪"),
    ("Fitness", "🏃"),
    ("Learning", "📚"),
    ("Work", "💼"),
    ("Finance", "💰"),
    ("Social", "👥"),
    ("Mindfulness", "🧘"),
    ("Creativity", "🎨"),
    ("Home", "��"),
]

CATEGORY_COLORS = {
    "General": "#9AA0A6",
    "Health": "#6FCF97",
    "Fitness": "#F2994A",
    "Learning": "#7C83FD",
    "Work": "#4FD1C5",
    "Finance": "#FFB74D",
    "Social": "#E57373",
    "Mindfulness": "#BA68C8",
    "Creativity": "#FF8A80",
    "Home": "#4DB6AC",
}

# UI Constants
WINDOW_TITLE = "Habit Tracker"
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 600

# Theme
THEME_DARK = "dark"
THEME_LIGHT = "light"

# Colors (for future use)
COLOR_SUCCESS = "#6FCF97"
COLOR_WARNING = "#F2C94C"
COLOR_DANGER = "#EF5350"
COLOR_PRIMARY = "#4FD1C5"
