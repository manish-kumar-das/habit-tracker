"""
Stats service - generates statistics and analytics
"""

from typing import Dict, List
from datetime import datetime, timedelta
from app.services.habit_service import get_habit_service
from app.utils.dates import parse_date, get_today


class StatsService:
    """Service for generating habit statistics"""
    
    def __init__(self):
        self.habit_service = get_habit_service()
    
    def get_completion_rate(self, habit_id: int, days: int = 30) -> float:
        """
        Calculate completion rate for last N days.
        Returns percentage (0-100).
        """
        habit = self.habit_service.get_habit_by_id(habit_id)
        if not habit:
            return 0.0
        
        created_date = parse_date(habit.created_at)
        today = parse_date(get_today())
        
        # Calculate actual days to consider
        days_since_creation = (today - created_date).days + 1
        days_to_check = min(days, days_since_creation)
        
        if days_to_check <= 0:
            return 0.0
        
        # Get completions
        completions = self.habit_service.get_habit_completions(habit_id)
        completion_dates = set(completions)
        
        # Count completions in the period
        completed_count = 0
        for i in range(days_to_check):
            check_date = today - timedelta(days=i)
            if check_date >= created_date:
                if check_date.strftime("%Y-%m-%d") in completion_dates:
                    completed_count += 1
        
        return (completed_count / days_to_check) * 100
    
    def get_total_completions(self, habit_id: int) -> int:
        """Get total number of completions for a habit"""
        completions = self.habit_service.get_habit_completions(habit_id)
        return len(completions)
    
    def get_habit_stats(self, habit_id: int) -> Dict:
        """Get comprehensive statistics for a habit"""
        habit = self.habit_service.get_habit_by_id(habit_id)
        if not habit:
            return {}
        
        from app.services.streak_service import get_streak_service
        streak_service = get_streak_service()
        
        streak_info = streak_service.get_streak_info(habit_id)
        
        return {
            'habit_id': habit_id,
            'habit_name': habit.name,
            'current_streak': streak_info['current_streak'],
            'longest_streak': streak_info['longest_streak'],
            'total_completions': streak_info['total_completions'],
            'completion_rate_7d': round(self.get_completion_rate(habit_id, 7), 1),
            'completion_rate_30d': round(self.get_completion_rate(habit_id, 30), 1),
            'created_at': habit.created_at,
            'is_completed_today': self.habit_service.is_habit_completed_today(habit_id)
        }
    
    def get_all_habits_stats(self) -> List[Dict]:
        """Get statistics for all active habits"""
        habits = self.habit_service.get_all_habits()
        return [self.get_habit_stats(habit.id) for habit in habits]
    
    def get_weekly_completion_count(self, habit_id: int) -> Dict[str, int]:
        """Get completion count for each day of the current week"""
        today = parse_date(get_today())
        week_start = today - timedelta(days=today.weekday())  # Monday
        
        completions = self.habit_service.get_habit_completions(habit_id)
        completion_dates = set(completions)
        
        weekly_data = {}
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        for i, day_name in enumerate(days):
            check_date = week_start + timedelta(days=i)
            if check_date <= today:
                completed = 1 if check_date.strftime("%Y-%m-%d") in completion_dates else 0
                weekly_data[day_name] = completed
        
        return weekly_data


# Global service instance
_stats_service_instance = None


def get_stats_service() -> StatsService:
    """Get global stats service instance"""
    global _stats_service_instance
    if _stats_service_instance is None:
        _stats_service_instance = StatsService()
    return _stats_service_instance
