"""
Settings service for app configuration
"""

from app.db.database import get_db
from app.utils.constants import THEME_DARK


class SettingsService:
    """Service for managing app settings"""
    
    def __init__(self):
        self.db = get_db()
        self._ensure_defaults()
    
    def _ensure_defaults(self):
        """Ensure default settings exist"""
        defaults = {
            'theme': THEME_DARK,
            'notifications_enabled': 'true',
            'notification_time': '09:00',
            'show_completed': 'true',
            'compact_mode': 'false',
        }
        
        for key, value in defaults.items():
            existing = self.get_setting(key)
            if existing is None:
                self.set_setting(key, value)
    
    def get_setting(self, key: str, default: str = None) -> str:
        """Get a setting value"""
        query = "SELECT value FROM settings WHERE key = ?"
        row = self.db.fetchone(query, (key,))
        
        if row:
            return row['value']
        return default
    
    def set_setting(self, key: str, value: str):
        """Set a setting value"""
        query = """
            INSERT OR REPLACE INTO settings (key, value)
            VALUES (?, ?)
        """
        self.db.execute(query, (key, value))
    
    def get_theme(self) -> str:
        """Get current theme"""
        return self.get_setting('theme', THEME_DARK)
    
    def set_theme(self, theme: str):
        """Set theme"""
        self.set_setting('theme', theme)
    
    def is_notifications_enabled(self) -> bool:
        """Check if notifications are enabled"""
        return self.get_setting('notifications_enabled', 'true') == 'true'
    
    def set_notifications_enabled(self, enabled: bool):
        """Enable/disable notifications"""
        self.set_setting('notifications_enabled', 'true' if enabled else 'false')
    
    def get_notification_time(self) -> str:
        """Get notification time (HH:MM format)"""
        return self.get_setting('notification_time', '09:00')
    
    def set_notification_time(self, time: str):
        """Set notification time"""
        self.set_setting('notification_time', time)


# Global service instance
_settings_service_instance = None


def get_settings_service() -> SettingsService:
    """Get global settings service instance"""
    global _settings_service_instance
    if _settings_service_instance is None:
        _settings_service_instance = SettingsService()
    return _settings_service_instance
