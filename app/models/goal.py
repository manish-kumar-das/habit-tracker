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
            id=row["id"],
            habit_id=row["habit_id"],
            goal_type=row["goal_type"],
            target_value=row["target_value"],
            current_value=row["current_value"],
            description=row["description"],
            start_date=row["start_date"],
            deadline=row["deadline"],
            is_completed=bool(row["is_completed"]),
            completed_date=row["completed_date"],
            category=row["category"] if "category" in row.keys() else None,
        )

        """Goal model class"""
    
    def __init__(self, id=None, habit_id=None, goal_type=None, target_value=0, 
                 current_value=0, is_completed=False, created_at=None, completed_at=None):
        self.id = id
        self.habit_id = habit_id
        self.goal_type = goal_type
        self.target_value = target_value
        self.current_value = current_value
        self.is_completed = is_completed
        self.created_at = created_at
        self.completed_at = completed_at
    
    def __repr__(self):
        return f"Goal(id={self.id}, habit_id={self.habit_id}, type={self.goal_type}, target={self.target_value}, current={self.current_value}, completed={self.is_completed})"

    def get_progress_percentage(self) -> int:
        """Get progress as percentage"""
        if self.target_value == 0:
            return 0
        return min(int((self.current_value / self.target_value) * 100), 100)

    def is_achieved(self) -> bool:
        """Check if goal is achieved"""
        return self.current_value >= self.target_value
