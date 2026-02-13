"""
Service for managing goals
"""

from datetime import datetime
from app.db.database import get_db_connection
from app.models.goal import Goal
from app.services.habit_service import get_habit_service
from app.services.streak_service import get_streak_service


class GoalService:
    """Service for goal operations"""
    
    def __init__(self):
        self.habit_service = get_habit_service()
        self.streak_service = get_streak_service()
    
    def create_goal(self, habit_id, goal_type, target_value, description, 
                    deadline=None, category=None):
        """Create a new goal"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        start_date = datetime.now().strftime("%Y-%m-%d")
        
        cursor.execute('''
            INSERT INTO goals (habit_id, goal_type, target_value, description,
                             start_date, deadline, category)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (habit_id, goal_type, target_value, description, 
              start_date, deadline, category))
        
        goal_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Calculate initial progress
        self.update_goal_progress(goal_id)
        
        return goal_id
    
    def get_all_goals(self, include_completed=True):
        """Get all goals"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if include_completed:
            cursor.execute('SELECT * FROM goals ORDER BY is_completed ASC, created_at DESC')
        else:
            cursor.execute('SELECT * FROM goals WHERE is_completed = 0 ORDER BY created_at DESC')
        
        rows = cursor.fetchall()
        conn.close()
        
        return [Goal.from_db_row(row) for row in rows]
    
    def get_goals_by_habit(self, habit_id):
        """Get goals for specific habit"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM goals 
            WHERE habit_id = ? 
            ORDER BY is_completed ASC, created_at DESC
        ''', (habit_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [Goal.from_db_row(row) for row in rows]
    
    def get_goal_by_id(self, goal_id):
        """Get goal by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM goals WHERE id = ?', (goal_id,))
        row = cursor.fetchone()
        conn.close()
        
        return Goal.from_db_row(row) if row else None
    
    def update_goal_progress(self, goal_id):
        """Update goal progress based on current data"""
        goal = self.get_goal_by_id(goal_id)
        if not goal:
            return
        
        current_value = 0
        
        if goal.goal_type == 'streak':
            # Get current streak
            if goal.habit_id:
                streak_info = self.streak_service.get_streak_info(goal.habit_id)
                current_value = streak_info['current_streak']
        
        elif goal.goal_type == 'total':
            # Get total completions
            if goal.habit_id:
                completions = self.habit_service.get_habit_completions(goal.habit_id)
                current_value = len(completions)
        
        elif goal.goal_type == 'consistency':
            # Get completion rate for last 30 days
            if goal.habit_id:
                from app.services.stats_service import get_stats_service
                stats = get_stats_service().get_habit_stats(goal.habit_id)
                current_value = stats['completion_rate_30d']
        
        # Check if completed
        is_completed = current_value >= goal.target_value
        completed_date = datetime.now().strftime("%Y-%m-%d") if is_completed and not goal.is_completed else goal.completed_date
        
        # Update database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE goals 
            SET current_value = ?, is_completed = ?, completed_date = ?
            WHERE id = ?
        ''', (current_value, 1 if is_completed else 0, completed_date, goal_id))
        
        conn.commit()
        conn.close()
        
        return is_completed and not goal.is_completed  # Return True if newly completed
    
    def update_all_goals_progress(self):
        """Update progress for all active goals"""
        goals = self.get_all_goals(include_completed=False)
        newly_completed = []
        
        for goal in goals:
            if self.update_goal_progress(goal.id):
                newly_completed.append(goal)
        
        return newly_completed
    
    def delete_goal(self, goal_id):
        """Delete a goal"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM goals WHERE id = ?', (goal_id,))
        
        conn.commit()
        conn.close()
    
    def get_active_goals_count(self):
        """Get count of active goals"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM goals WHERE is_completed = 0')
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
    
    def get_completed_goals_count(self):
        """Get count of completed goals"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM goals WHERE is_completed = 1')
        count = cursor.fetchone()[0]
        
        conn.close()
        return count


# Global service instance
_goal_service_instance = None


def get_goal_service() -> GoalService:
    """Get global goal service instance"""
    global _goal_service_instance
    if _goal_service_instance is None:
        _goal_service_instance = GoalService()
    return _goal_service_instance
