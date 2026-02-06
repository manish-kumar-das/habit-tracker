"""
Habit service with categories, notes, and undo delete support
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
    
    def create_habit(self, name: str, description: str = "", category: str = "General", 
                    frequency: str = FREQUENCY_DAILY) -> Habit:
        """Create a new habit"""
        query = """
            INSERT INTO habits (name, description, category, frequency, created_at, is_active)
            VALUES (?, ?, ?, ?, ?, 1)
        """
        habit_id = self.db.insert(query, (name, description, category, frequency, get_today()))
        
        return Habit(
            id=habit_id,
            name=name,
            description=description,
            category=category,
            frequency=frequency,
            created_at=get_today(),
            is_active=True
        )
    
    def get_all_habits(self, active_only: bool = True, category: str = None) -> List[Habit]:
        """Get all habits, optionally filtered by category"""
        if category:
            if active_only:
                query = "SELECT * FROM habits WHERE is_active = 1 AND category = ? ORDER BY created_at DESC"
                rows = self.db.fetchall(query, (category,))
            else:
                query = "SELECT * FROM habits WHERE category = ? ORDER BY created_at DESC"
                rows = self.db.fetchall(query, (category,))
        else:
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
                    category: str = None, frequency: str = None) -> bool:
        """Update habit details"""
        habit = self.get_habit_by_id(habit_id)
        if not habit:
            return False
        
        updates = []
        params = []
        
        if name is not None:
            updates.append("name = ?")
            params.append(name)
        if description is not None:
            updates.append("description = ?")
            params.append(description)
        if category is not None:
            updates.append("category = ?")
            params.append(category)
        if frequency is not None:
            updates.append("frequency = ?")
            params.append(frequency)
        
        if not updates:
            return True
        
        params.append(habit_id)
        query = f"UPDATE habits SET {', '.join(updates)} WHERE id = ?"
        
        self.db.execute(query, tuple(params))
        return True
    
    def delete_habit(self, habit_id: int) -> bool:
        """Soft delete a habit (mark as inactive)"""
        query = "UPDATE habits SET is_active = 0 WHERE id = ?"
        self.db.execute(query, (habit_id,))
        return True
    
    def hard_delete_habit(self, habit_id: int, save_to_trash: bool = True) -> bool:
        """Permanently delete a habit, optionally saving to trash for undo"""
        if save_to_trash:
            # Save to deleted_habits table
            habit = self.get_habit_by_id(habit_id)
            if habit:
                completion_count = len(self.get_habit_completions(habit_id))
                
                trash_query = """
                    INSERT INTO deleted_habits 
                    (original_habit_id, name, description, category, frequency, created_at, deleted_at, completion_count)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """
                self.db.execute(trash_query, (
                    habit_id, habit.name, habit.description, habit.category,
                    habit.frequency, habit.created_at, get_today(), completion_count
                ))
        
        # Delete the habit (cascades to logs)
        query = "DELETE FROM habits WHERE id = ?"
        self.db.execute(query, (habit_id,))
        return True
    
    def get_deleted_habits(self, limit: int = 10) -> List[dict]:
        """Get recently deleted habits"""
        query = """
            SELECT * FROM deleted_habits 
            ORDER BY deleted_at DESC 
            LIMIT ?
        """
        rows = self.db.fetchall(query, (limit,))
        return [dict(row) for row in rows]
    
    def restore_habit(self, deleted_habit_id: int) -> Optional[Habit]:
        """Restore a deleted habit"""
        # Get deleted habit info
        query = "SELECT * FROM deleted_habits WHERE id = ?"
        row = self.db.fetchone(query, (deleted_habit_id,))
        
        if not row:
            return None
        
        # Recreate the habit
        habit = self.create_habit(
            name=row['name'],
            description=row['description'] or "",
            category=row['category'] or "General",
            frequency=row['frequency']
        )
        
        # Remove from trash
        delete_query = "DELETE FROM deleted_habits WHERE id = ?"
        self.db.execute(delete_query, (deleted_habit_id,))
        
        return habit
    
    def mark_habit_complete(self, habit_id: int, date: str = None, notes: str = "") -> bool:
        """Mark a habit as complete for a specific date with optional notes"""
        if date is None:
            date = get_today()
        
        # Check if already completed
        check_query = "SELECT id FROM habit_logs WHERE habit_id = ? AND completed_date = ?"
        existing = self.db.fetchone(check_query, (habit_id, date))
        
        if existing:
            # Update notes if provided
            if notes:
                update_query = "UPDATE habit_logs SET notes = ? WHERE habit_id = ? AND completed_date = ?"
                self.db.execute(update_query, (notes, habit_id, date))
            return False
        
        # Insert completion log
        query = """
            INSERT INTO habit_logs (habit_id, completed_date, notes, created_at)
            VALUES (?, ?, ?, ?)
        """
        self.db.execute(query, (habit_id, date, notes, get_today()))
        return True
    
    def unmark_habit_complete(self, habit_id: int, date: str = None) -> bool:
        """Remove completion for a specific date"""
        if date is None:
            date = get_today()
        
        query = "DELETE FROM habit_logs WHERE habit_id = ? AND completed_date = ?"
        self.db.execute(query, (habit_id, date))
        return True
    
    def get_completion_notes(self, habit_id: int, date: str = None) -> Optional[str]:
        """Get notes for a specific completion"""
        if date is None:
            date = get_today()
        
        query = "SELECT notes FROM habit_logs WHERE habit_id = ? AND completed_date = ?"
        row = self.db.fetchone(query, (habit_id, date))
        
        if row and row['notes']:
            return row['notes']
        return None
    
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
    
    def get_categories_with_counts(self) -> List[tuple]:
        """Get all categories with habit counts"""
        query = """
            SELECT category, COUNT(*) as count 
            FROM habits 
            WHERE is_active = 1 
            GROUP BY category 
            ORDER BY count DESC
        """
        rows = self.db.fetchall(query)
        return [(row['category'], row['count']) for row in rows]


# Global service instance
_habit_service_instance = None


def get_habit_service() -> HabitService:
    """Get global habit service instance"""
    global _habit_service_instance
    if _habit_service_instance is None:
        _habit_service_instance = HabitService()
    return _habit_service_instance
