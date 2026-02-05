"""
Habit log model
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class HabitLog:
    """Habit log data model"""
    id: Optional[int]
    habit_id: int
    completed_date: str
    created_at: str
    
    @staticmethod
    def from_db_row(row) -> 'HabitLog':
        """Create HabitLog instance from database row"""
        return HabitLog(
            id=row['id'],
            habit_id=row['habit_id'],
            completed_date=row['completed_date'],
            created_at=row['created_at']
        )
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'habit_id': self.habit_id,
            'completed_date': self.completed_date,
            'created_at': self.created_at
        }
