"""
Achievement model for tracking unlocked badges
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Achievement:
    """Represents an achievement/badge"""
    id: str
    name: str
    description: str
    icon: str
    category: str
    requirement: int
    is_unlocked: bool
    unlocked_date: Optional[str]
    rarity: str
    
    @classmethod
    def from_db_row(cls, row):
        """Create Achievement from database row"""
        return cls(
            id=row['id'],
            name=row['name'],
            description=row['description'],
            icon=row['icon'],
            category=row['category'],
            requirement=row['requirement'],
            is_unlocked=bool(row['is_unlocked']),
            unlocked_date=row['unlocked_date'],
            rarity=row['rarity']
        )


# Achievement definitions
ACHIEVEMENT_DEFINITIONS = [
    # Streak Achievements
    {
        'id': 'streak_7',
        'name': 'Week Warrior',
        'description': 'Maintain a 7-day streak on any habit',
        'icon': '🔥',
        'category': 'streak',
        'requirement': 7,
        'rarity': 'common'
    },
    {
        'id': 'streak_30',
        'name': 'Monthly Master',
        'description': 'Maintain a 30-day streak on any habit',
        'icon': '🌟',
        'category': 'streak',
        'requirement': 30,
        'rarity': 'rare'
    },
    {
        'id': 'streak_100',
        'name': 'Century Champion',
        'description': 'Maintain a 100-day streak on any habit',
        'icon': '💯',
        'category': 'streak',
        'requirement': 100,
        'rarity': 'epic'
    },
    {
        'id': 'streak_365',
        'name': 'Year Legend',
        'description': 'Maintain a 365-day streak on any habit',
        'icon': '👑',
        'category': 'streak',
        'requirement': 365,
        'rarity': 'legendary'
    },
    
    # Completion Achievements
    {
        'id': 'complete_10',
        'name': 'Getting Started',
        'description': 'Complete any habit 10 times',
        'icon': '✅',
        'category': 'completion',
        'requirement': 10,
        'rarity': 'common'
    },
    {
        'id': 'complete_50',
        'name': 'Habit Builder',
        'description': 'Complete any habit 50 times',
        'icon': '🎯',
        'category': 'completion',
        'requirement': 50,
        'rarity': 'rare'
    },
    {
        'id': 'complete_100',
        'name': 'Century Club',
        'description': 'Complete any habit 100 times',
        'icon': '💪',
        'category': 'completion',
        'requirement': 100,
        'rarity': 'epic'
    },
    {
        'id': 'complete_500',
        'name': 'Master of Habits',
        'description': 'Complete any habit 500 times',
        'icon': '🏆',
        'category': 'completion',
        'requirement': 500,
        'rarity': 'legendary'
    },
    
    # Consistency Achievements
    {
        'id': 'perfect_week',
        'name': 'Perfect Week',
        'description': 'Complete all habits for 7 days straight',
        'icon': '⭐',
        'category': 'consistency',
        'requirement': 7,
        'rarity': 'rare'
    },
    {
        'id': 'perfect_month',
        'name': 'Perfect Month',
        'description': 'Complete all habits for 30 days straight',
        'icon': '🌙',
        'category': 'consistency',
        'requirement': 30,
        'rarity': 'epic'
    },
    
    # Special Achievements
    {
        'id': 'early_bird',
        'name': 'Early Bird',
        'description': 'Complete a habit before 6 AM',
        'icon': '🌅',
        'category': 'special',
        'requirement': 1,
        'rarity': 'rare'
    },
    {
        'id': 'night_owl',
        'name': 'Night Owl',
        'description': 'Complete a habit after 10 PM',
        'icon': '🦉',
        'category': 'special',
        'requirement': 1,
        'rarity': 'rare'
    },
    {
        'id': 'habit_creator',
        'name': 'Habit Creator',
        'description': 'Create 5 different habits',
        'icon': '📝',
        'category': 'special',
        'requirement': 5,
        'rarity': 'common'
    },
    {
        'id': 'goal_setter',
        'name': 'Goal Setter',
        'description': 'Create your first goal',
        'icon': '🎯',
        'category': 'special',
        'requirement': 1,
        'rarity': 'common'
    },
    {
        'id': 'goal_achiever',
        'name': 'Goal Achiever',
        'description': 'Complete your first goal',
        'icon': '🏅',
        'category': 'special',
        'requirement': 1,
        'rarity': 'rare'
    },
]
