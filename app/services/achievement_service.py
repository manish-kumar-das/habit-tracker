"""
Service for managing achievements - SIMPLIFIED
"""

from datetime import datetime
from app.db.database import get_db_connection
from app.models.achievement import Achievement, ACHIEVEMENT_DEFINITIONS


class AchievementService:
    """Service for achievement operations"""
    
    def __init__(self):
        self.initialize_achievements()
    
    def initialize_achievements(self):
        """Initialize achievement definitions in database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        for achievement_def in ACHIEVEMENT_DEFINITIONS:
            cursor.execute('''
                INSERT OR IGNORE INTO achievements 
                (id, name, description, icon, category, requirement, rarity)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                achievement_def['id'],
                achievement_def['name'],
                achievement_def['description'],
                achievement_def['icon'],
                achievement_def['category'],
                achievement_def['requirement'],
                achievement_def['rarity']
            ))
        
        conn.commit()
        conn.close()
    
    def get_all_achievements(self):
        """Get all achievements"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM achievements 
            ORDER BY 
                CASE rarity
                    WHEN 'legendary' THEN 1
                    WHEN 'epic' THEN 2
                    WHEN 'rare' THEN 3
                    ELSE 4
                END,
                is_unlocked DESC,
                requirement ASC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        return [Achievement.from_db_row(row) for row in rows]
    
    def unlock_achievement(self, achievement_id):
        """Unlock an achievement"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT is_unlocked FROM achievements WHERE id = ?', (achievement_id,))
        row = cursor.fetchone()
        
        if row and not row['is_unlocked']:
            unlocked_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute('''
                UPDATE achievements 
                SET is_unlocked = 1, unlocked_date = ?
                WHERE id = ?
            ''', (unlocked_date, achievement_id))
            
            conn.commit()
            conn.close()
            return True
        
        conn.close()
        return False
    
    def check_and_unlock_achievements(self):
        """Check all conditions and unlock achievements"""
        from app.services.habit_service import get_habit_service
        from app.services.streak_service import get_streak_service
        
        habit_service = get_habit_service()
        streak_service = get_streak_service()
        
        newly_unlocked = []
        habits = habit_service.get_all_habits()
        
        # Check streak achievements
        max_streak = 0
        for habit in habits:
            streak_info = streak_service.get_streak_info(habit.id)
            current_streak = streak_info['current_streak']
            max_streak = max(max_streak, current_streak)
        
        if max_streak >= 7 and self.unlock_achievement('streak_7'):
            newly_unlocked.append('Week Warrior')
        if max_streak >= 30 and self.unlock_achievement('streak_30'):
            newly_unlocked.append('Monthly Master')
        if max_streak >= 100 and self.unlock_achievement('streak_100'):
            newly_unlocked.append('Century Champion')
        if max_streak >= 365 and self.unlock_achievement('streak_365'):
            newly_unlocked.append('Year Legend')
        
        # Check completion achievements
        max_completions = 0
        for habit in habits:
            completions = habit_service.get_habit_completions(habit.id)
            max_completions = max(max_completions, len(completions))
        
        if max_completions >= 10 and self.unlock_achievement('complete_10'):
            newly_unlocked.append('Getting Started')
        if max_completions >= 50 and self.unlock_achievement('complete_50'):
            newly_unlocked.append('Habit Builder')
        if max_completions >= 100 and self.unlock_achievement('complete_100'):
            newly_unlocked.append('Century Club')
        if max_completions >= 500 and self.unlock_achievement('complete_500'):
            newly_unlocked.append('Master of Habits')
        
        # Check habit creator
        if len(habits) >= 5 and self.unlock_achievement('habit_creator'):
            newly_unlocked.append('Habit Creator')
        
        return newly_unlocked
    
    def get_achievement_stats(self):
        """Get achievement statistics"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM achievements WHERE is_unlocked = 1')
        unlocked_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM achievements')
        total_count = cursor.fetchone()[0]
        
        conn.close()
        
        percentage = int((unlocked_count / total_count) * 100) if total_count > 0 else 0
        
        return {
            'unlocked': unlocked_count,
            'total': total_count,
            'percentage': percentage
        }


# Global service instance
_achievement_service_instance = None


def get_achievement_service() -> AchievementService:
    """Get global achievement service instance"""
    global _achievement_service_instance
    if _achievement_service_instance is None:
        _achievement_service_instance = AchievementService()
    return _achievement_service_instance
