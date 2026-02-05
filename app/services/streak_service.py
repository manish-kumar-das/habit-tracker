"""
Streak service - handles streak calculations
"""

from datetime import datetime, timedelta
from typing import Dict
from app.services.habit_service import get_habit_service
from app.utils.dates import parse_date, get_today, get_yesterday


class StreakService:
    """Service for calculating habit streaks"""
    
    def __init__(self):
        self.habit_service = get_habit_service()
    
    def calculate_current_streak(self, habit_id: int) -> int:
        """
        Calculate current streak for a habit.
        Streak continues if completed today OR yesterday (grace period).
        """
        completions = self.habit_service.get_habit_completions(habit_id)
        
        if not completions:
            return 0
        
        # Sort dates in descending order (most recent first)
        completion_dates = sorted([parse_date(d) for d in completions], reverse=True)
        today = parse_date(get_today())
        
        # Check if completed today or yesterday
        most_recent = completion_dates[0]
        yesterday = today - timedelta(days=1)
        
        if most_recent < yesterday:
            return 0  # Streak broken
        
        # Count consecutive days
        streak = 0
        expected_date = today
        
        for completion_date in completion_dates:
            # Allow today or yesterday as starting point
            if streak == 0:
                if completion_date == today or completion_date == yesterday:
                    streak = 1
                    expected_date = completion_date - timedelta(days=1)
                else:
                    break
            else:
                if completion_date == expected_date:
                    streak += 1
                    expected_date -= timedelta(days=1)
                elif completion_date < expected_date:
                    # Gap found, streak ends
                    break
        
        return streak
    
    def calculate_longest_streak(self, habit_id: int) -> int:
        """Calculate the longest streak ever achieved for a habit"""
        completions = self.habit_service.get_habit_completions(habit_id)
        
        if not completions:
            return 0
        
        # Sort dates in ascending order
        completion_dates = sorted([parse_date(d) for d in completions])
        
        longest_streak = 1
        current_streak = 1
        
        for i in range(1, len(completion_dates)):
            previous_date = completion_dates[i - 1]
            current_date = completion_dates[i]
            
            # Check if consecutive days
            if (current_date - previous_date).days == 1:
                current_streak += 1
                longest_streak = max(longest_streak, current_streak)
            else:
                current_streak = 1
        
        return longest_streak
    
    def get_streak_info(self, habit_id: int) -> Dict[str, int]:
        """Get comprehensive streak information"""
        return {
            'current_streak': self.calculate_current_streak(habit_id),
            'longest_streak': self.calculate_longest_streak(habit_id),
            'total_completions': len(self.habit_service.get_habit_completions(habit_id))
        }
    
    def is_streak_at_risk(self, habit_id: int) -> bool:
        """Check if streak is at risk (not completed today)"""
        return not self.habit_service.is_habit_completed_today(habit_id)


# Global service instance
_streak_service_instance = None


def get_streak_service() -> StreakService:
    """Get global streak service instance"""
    global _streak_service_instance
    if _streak_service_instance is None:
        _streak_service_instance = StreakService()
    return _streak_service_instance
