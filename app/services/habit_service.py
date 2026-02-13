"""
Service layer for habit-related operations
"""

from datetime import datetime
from app.db.database import get_db_connection
from app.models.habit import Habit


class HabitService:
    """Service for habit CRUD operations"""
    
    def __init__(self):
        pass
    
    def create_habit(self, name, description="", frequency="daily", category="General"):
        """Create a new habit"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO habits (name, description, frequency, category)
            VALUES (?, ?, ?, ?)
        ''', (name, description, frequency, category))
        
        habit_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return habit_id
    
    def get_all_habits(self, category=None):
        """Get all habits, optionally filtered by category"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if category:
            cursor.execute('SELECT * FROM habits WHERE category = ? ORDER BY created_at DESC', (category,))
        else:
            cursor.execute('SELECT * FROM habits ORDER BY created_at DESC')
        
        rows = cursor.fetchall()
        conn.close()
        
        return [Habit.from_db_row(row) for row in rows]
    
    def get_habit_by_id(self, habit_id):
        """Get a specific habit by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM habits WHERE id = ?', (habit_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        return Habit.from_db_row(row) if row else None
    
    def update_habit(self, habit_id, name=None, description=None, frequency=None, category=None):
        """Update a habit"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
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
        if category is not None:
            updates.append("category = ?")
            params.append(category)
        
        if updates:
            params.append(habit_id)
            query = f"UPDATE habits SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, params)
            conn.commit()
        
        conn.close()
    
    def hard_delete_habit(self, habit_id, save_to_trash=True):
        """Delete a habit (optionally save to trash first)"""
        if save_to_trash:
            # Get habit details
            habit = self.get_habit_by_id(habit_id)
            if habit:
                # Count completions
                completions = self.get_habit_completions(habit_id)
                completion_count = len(completions)
                
                # Save to deleted_habits
                conn = get_db_connection()
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO deleted_habits 
                    (original_habit_id, name, description, category, frequency, created_at, completion_count)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (habit.id, habit.name, habit.description, habit.category, 
                      habit.frequency, habit.created_at, completion_count))
                
                conn.commit()
                conn.close()
        
        # Delete the habit
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM habits WHERE id = ?', (habit_id,))
        
        conn.commit()
        conn.close()
    
    def mark_habit_complete(self, habit_id, date=None, notes=""):
        """Mark a habit as complete for a specific date"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO habit_logs (habit_id, completed_date, notes)
                VALUES (?, ?, ?)
            ''', (habit_id, date, notes))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.close()
            return False
    
    def unmark_habit_complete(self, habit_id, date=None):
        """Remove completion for a specific date"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM habit_logs 
            WHERE habit_id = ? AND completed_date = ?
        ''', (habit_id, date))
        
        conn.commit()
        conn.close()
    
    def is_habit_completed_today(self, habit_id):
        """Check if habit is completed today"""
        today = datetime.now().strftime("%Y-%m-%d")
        return self.is_habit_completed_on_date(habit_id, today)
    
    def is_habit_completed_on_date(self, habit_id, date_str):
        """Check if habit was completed on specific date"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) FROM habit_logs 
            WHERE habit_id = ? AND completed_date = ?
        ''', (habit_id, date_str))
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count > 0
    
    def get_habit_completions(self, habit_id):
        """Get all completion dates for a habit"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT completed_date FROM habit_logs 
            WHERE habit_id = ? 
            ORDER BY completed_date DESC
        ''', (habit_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [row['completed_date'] for row in rows]
    
    def get_completion_notes(self, habit_id, date=None):
        """Get notes for a specific completion"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT notes FROM habit_logs 
            WHERE habit_id = ? AND completed_date = ?
        ''', (habit_id, date))
        
        row = cursor.fetchone()
        conn.close()
        
        return row['notes'] if row and row['notes'] else ""
    
    def get_deleted_habits(self, limit=10):
        """Get deleted habits from trash"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM deleted_habits 
            ORDER BY deleted_at DESC 
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return rows
    
    def restore_habit(self, deleted_habit_id):
        """Restore a habit from trash"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get deleted habit
        cursor.execute('SELECT * FROM deleted_habits WHERE id = ?', (deleted_habit_id,))
        deleted = cursor.fetchone()
        
        if deleted:
            # Recreate habit
            cursor.execute('''
                INSERT INTO habits (name, description, category, frequency, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (deleted['name'], deleted['description'], deleted['category'],
                  deleted['frequency'], deleted['created_at']))
            
            # Remove from trash
            cursor.execute('DELETE FROM deleted_habits WHERE id = ?', (deleted_habit_id,))
            
            conn.commit()
        
        conn.close()
    
    def empty_trash(self):
        """Permanently delete all habits in trash"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM deleted_habits')
        
        conn.commit()
        conn.close()
    
    def get_categories_with_counts(self):
        """Get all categories with habit counts"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT category, COUNT(*) as count 
            FROM habits 
            GROUP BY category 
            ORDER BY count DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        return {row['category']: row['count'] for row in rows}


# Global service instance
_habit_service_instance = None


def get_habit_service() -> HabitService:
    """Get global habit service instance"""
    global _habit_service_instance
    if _habit_service_instance is None:
        _habit_service_instance = HabitService()
    return _habit_service_instance
