"""
Notification service - FIXED daily reminder
"""

import sys
import subprocess
from app.services.settings_service import get_settings_service


class NotificationService:
    """Service for desktop notifications"""
    
    def __init__(self):
        self.settings_service = get_settings_service()
    
    def send_notification(self, title, message):
        """Send a desktop notification"""
        if not self.settings_service.is_notifications_enabled():
            print(f"❌ Notifications disabled in settings")
            return False
        
        try:
            if sys.platform == 'linux':
                result = subprocess.run([
                    'notify-send',
                    '--app-name=Habit Tracker',
                    '--icon=dialog-information',
                    title,
                    message
                ], check=False, capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"✅ Notification sent: {title}")
                    return True
                else:
                    print(f"❌ notify-send failed: {result.stderr}")
                    return False
                    
            elif sys.platform == 'darwin':
                subprocess.run([
                    'osascript', '-e',
                    f'display notification "{message}" with title "{title}"'
                ], check=False, capture_output=True)
                return True
                
            elif sys.platform == 'win32':
                try:
                    from win10toast import ToastNotifier
                    toaster = ToastNotifier()
                    toaster.show_toast(title, message, duration=5, threaded=True)
                    return True
                except:
                    return False
                    
        except Exception as e:
            print(f"❌ Notification error: {e}")
            return False
    
    def send_daily_reminder(self):
        """Send daily reminder for incomplete habits"""
        print(f"\n🔔 send_daily_reminder() called")
        
        if not self.settings_service.is_notifications_enabled():
            print(f"❌ Notifications disabled")
            return False
        
        # Import here to avoid circular dependency
        from app.services.habit_service import get_habit_service
        habit_service = get_habit_service()
        
        habits = habit_service.get_all_habits()
        print(f"📋 Total habits: {len(habits)}")
        
        incomplete = [h for h in habits if not habit_service.is_habit_completed_today(h.id)]
        print(f"⏳ Incomplete habits: {len(incomplete)}")
        
        count = len(incomplete)
        
        if count == 0:
            title = "Great Job! 🎉"
            message = "All habits completed today!"
        else:
            title = "Habit Reminder 📋"
            message = f"You have {count} incomplete habit{'s' if count > 1 else ''} today!"
        
        print(f"📢 Sending: {title} - {message}")
        return self.send_notification(title, message)
    
    def send_habit_completed(self, habit_name):
        """Send notification when habit is completed"""
        if not self.settings_service.is_notifications_enabled():
            return False
        
        title = "Habit Completed! ✅"
        message = f"Great job on '{habit_name}'!"
        return self.send_notification(title, message)
    
    def send_streak_milestone(self, habit_name, streak):
        """Send notification for streak milestones"""
        if not self.settings_service.is_notifications_enabled():
            return False
        
        if streak in [7, 14, 30, 60, 90, 100, 365]:
            title = "Streak Milestone! 🔥"
            message = f"{streak} day streak on '{habit_name}'!"
            return self.send_notification(title, message)
        
        return False


# Global service instance
_notification_service_instance = None


def get_notification_service() -> NotificationService:
    """Get global notification service instance"""
    global _notification_service_instance
    if _notification_service_instance is None:
        _notification_service_instance = NotificationService()
    return _notification_service_instance
