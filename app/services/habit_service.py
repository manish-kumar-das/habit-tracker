"""
Habit service - handles all habit-related operations
"""

from typing import List, Optional
from app.db.database import get_db
from app.models.habit import Habit
from app.utils.dates import get_today
from app.utils.constants import FREQUENCY_DAILY


class HabitService:
    """Service for managing habits"""
    
    def __init__(self):
        self.db = get_db()
    
    def create_habit(self, name: str, description: str = "", frequency: str = FREQUENCY_DAILY) -> Habit:
        """Create a new habit"""
        query = """
            INSERT INTO habits (name, description, frequency, created_at, is_active)
            VALUES (?, ?, ?, ?, 1)
        """
        habit_id = self.db.insert(query, (name, description, frequency, get_today()))
        
        return Habit(
            id=habit_id,
            name=name,
            description=description,
            frequency=frequency,
            created_at=get_today(),
            is_active=True
        )
    
    def get_all_habits(self, active_only: bool = True) -> List[Habit]:
        """Get all habits"""
        if active_only:
            query = "SELECT * FROM habits WHERE is_active = 1 ORDER BY created_at DESC"
        else:
            query = "SELECT * FROM habits ORDER BY created_at DESC"
        
        rows = self.db.fetchall(query)
        return [Habit.from_db_row(row) for row in rows]
    
    def get_habit_by_id(self, habit_id: int) -> Optional[Habit]:
        """Get a specific habit by ID"""
        query = "SELECT * FROM habits WHERE id = ?"
        row = self.db.fetchone(query, (habit_id,))
        
        if row:
            return Habit.from_db_row(row)
        return None
    
    def update_habit(self, habit_id: int, name: str = None, description: str = None, 
                    frequency: str = None) -> bool:
        """Update habit details"""
        habit = self.get_habit_by_id(habit_id)
        if not habit:
            return False
        
        # Build dynamic update query
        updates = []
        params = []
        
        if name is not None:
            updates.append("name = ?")
            params.append(name)
        if description is not None:
            updates.append("description = ?")
            params.append(description)
        if frequency is not None:
            updates.append("frequency = ?")
            params.append(frequency)
        
        if not updates:
            return True  # Nothing to update
        
        params.append(habit_id)
        query = f"UPDATE habits SET {', '.join(updates)} WHERE id = ?"
        
        self.db.execute(query, tuple(params))
        return True
    
    def delete_habit(self, habit_id: int) -> bool:
        """Soft delete a habit (mark as inactive)"""
        query = "UPDATE habits SET is_active = 0 WHERE id = ?"
        self.db.execute(query, (habit_id,))
        return True
    
    def hard_delete_habit(self, habit_id: int) -> bool:
        """Permanently delete a habit and all its logs"""
        # Foreign key constraint will cascade delete logs
        query = "DELETE FROM habits WHERE id = ?"
        self.db.execute(query, (habit_id,))
        return True
    
    def mark_habit_complete(self, habit_id: int, date: str = None) -> bool:
        """Mark a habit as complete for a specific date"""
        if date is None:
            date = get_today()
        
        # Check if already completed
        check_query = "SELECT id FROM habit_logs WHERE habit_id = ? AND completed_date = ?"
        existing = self.db.fetchone(check_query, (habit_id, date))
        
        if existing:
            return False  # Already completed
        
        # Insert completion log
        query = """
            INSERT INTO habit_logs (habit_id, completed_date, created_at)
            VALUES (?, ?, ?)
        """
        self.db.execute(query, (habit_id, date, get_today()))
        return True
    
    def unmark_habit_complete(self, habit_id: int, date: str = None) -> bool:
        """Remove completion for a specific date"""
        if date is None:
            date = get_today()
        
        query = "DELETE FROM habit_logs WHERE habit_id = ? AND completed_date = ?"
        self.db.execute(query, (habit_id, date))
        return True
    
    def is_habit_completed_today(self, habit_id: int) -> bool:
        """Check if habit is completed for today"""
        query = "SELECT id FROM habit_logs WHERE habit_id = ? AND completed_date = ?"
        result = self.db.fetchone(query, (habit_id, get_today()))
        return result is not None
    
    def get_habit_completions(self, habit_id: int, limit: int = None) -> List[str]:
        """Get list of completion dates for a habit"""
        if limit:
            query = """
                SELECT completed_date FROM habit_logs 
                WHERE habit_id = ? 
                ORDER BY completed_date DESC 
                LIMIT ?
            """
            rows = self.db.fetchall(query, (habit_id, limit))
        else:
            query = """
                SELECT completed_date FROM habit_logs 
                WHERE habit_id = ? 
                ORDER BY completed_date DESC
            """
            rows = self.db.fetchall(query, (habit_id,))
        
        return [row['completed_date'] for row in rows]


# Global service instance
_habit_service_instance = None


def get_habit_service() -> HabitService:
    """Get global habit service instance"""
    global _habit_service_instance
    if _habit_service_instance is None:
        _habit_service_instance = HabitService()
    return _habit_service_instance
