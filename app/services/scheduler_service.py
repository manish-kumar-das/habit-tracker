"""
Scheduler service for daily reminders - COMPLETELY FIXED
"""

from PySide6.QtCore import QTimer
from datetime import datetime
from app.services.notification_service import get_notification_service
from app.services.settings_service import get_settings_service


class SchedulerService:
    """Service for scheduling daily tasks"""
    
    def __init__(self):
        self.notification_service = get_notification_service()
        self.settings_service = get_settings_service()
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_daily_reminder)
        self.last_notification_minute = None
        
        # Check every 30 seconds
        self.timer.start(30000)
    
    def check_daily_reminder(self):
        """Check if it's time to send daily reminder"""
        if not self.settings_service.is_notifications_enabled():
            return
        
        now = datetime.now()
        current_minute_key = f"{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}"
        
        # Only send once per minute
        if self.last_notification_minute == current_minute_key:
            return
        
        # Get notification time from settings
        time_str = self.settings_service.get_notification_time()
        hour, minute = map(int, time_str.split(':'))
        
        # Check if current time matches
        if now.hour == hour and now.minute == minute:
            self.notification_service.send_daily_reminder()
            self.last_notification_minute = current_minute_key
    
    def stop(self):
        """Stop the scheduler"""
        self.timer.stop()


# Global service instance
_scheduler_service_instance = None


def get_scheduler_service() -> SchedulerService:
    """Get global scheduler service instance"""
    global _scheduler_service_instance
    if _scheduler_service_instance is None:
        _scheduler_service_instance = SchedulerService()
    return _scheduler_service_instance
