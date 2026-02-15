"""
Goal model for tracking habit goals
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Goal:
    """Represents a habit goal"""
    id: int
    habit_id: Optional[int]
    goal_type: str
    target_value: int
    current_value: int
    description: str
    start_date: str
    deadline: Optional[str]
    is_completed: bool
    completed_date: Optional[str]
    category: Optional[str]
    
    @classmethod
    def from_db_row(cls, row):
        """Create Goal from database row"""
        return cls(
            id=row['id'],
            habit_id=row['habit_id'],
            goal_type=row['goal_type'],
            target_value=row['target_value'],
            current_value=row['current_value'],
            description=row['description'],
            start_date=row['start_date'],
            deadline=row['deadline'],
            is_completed=bool(row['is_completed']),
            completed_date=row['completed_date'],
            category=row['category'] if 'category' in row.keys() else None
        )
    
    def get_progress_percentage(self) -> int:
        """Get progress as percentage"""
        if self.target_value == 0:
            return 0
        return min(int((self.current_value / self.target_value) * 100), 100)
    
    def is_achieved(self) -> bool:
        """Check if goal is achieved"""
        return self.current_value >= self.target_value
