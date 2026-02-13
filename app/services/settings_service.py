"""
Service for managing application settings
"""

from app.db.database import get_db_connection
from app.utils.constants import THEME_DARK, THEME_LIGHT


class SettingsService:
    """Service for settings operations"""
    
    def __init__(self):
        self._ensure_defaults()
    
    def _ensure_defaults(self):
        """Ensure default settings exist"""
        defaults = {
            'theme': THEME_DARK,
            'notifications_enabled': 'true',
            'notification_time': '09:00',
            'show_completed': 'true',
            'compact_mode': 'false'
        }
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        for key, value in defaults.items():
            cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
            if cursor.fetchone() is None:
                cursor.execute('INSERT INTO settings (key, value) VALUES (?, ?)', (key, value))
        
        conn.commit()
        conn.close()
    
    def get_setting(self, key, default=None):
        """Get a setting value"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
        row = cursor.fetchone()
        
        conn.close()
        
        return row['value'] if row else default
    
    def set_setting(self, key, value):
        """Set a setting value"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO settings (key, value)
            VALUES (?, ?)
        ''', (key, str(value)))
        
        conn.commit()
        conn.close()
    
    def get_theme(self):
        """Get current theme"""
        return self.get_setting('theme', THEME_DARK)
    
    def set_theme(self, theme):
        """Set theme"""
        if theme in [THEME_DARK, THEME_LIGHT]:
            self.set_setting('theme', theme)
    
    def is_notifications_enabled(self):
        """Check if notifications are enabled"""
        value = self.get_setting('notifications_enabled', 'true')
        return value.lower() == 'true'
    
    def set_notifications_enabled(self, enabled):
        """Enable/disable notifications"""
        self.set_setting('notifications_enabled', 'true' if enabled else 'false')
    
    def get_notification_time(self):
        """Get notification time"""
        return self.get_setting('notification_time', '09:00')
    
    def set_notification_time(self, time_str):
        """Set notification time (HH:MM format)"""
        self.set_setting('notification_time', time_str)
    
    def get_show_completed(self):
        """Check if completed habits should be shown"""
        value = self.get_setting('show_completed', 'true')
        return value.lower() == 'true'
    
    def set_show_completed(self, show):
        """Set whether to show completed habits"""
        self.set_setting('show_completed', 'true' if show else 'false')
    
    def get_compact_mode(self):
        """Check if compact mode is enabled"""
        value = self.get_setting('compact_mode', 'false')
        return value.lower() == 'true'
    
    def set_compact_mode(self, compact):
        """Enable/disable compact mode"""
        self.set_setting('compact_mode', 'true' if compact else 'false')


# Global service instance
_settings_service_instance = None


def get_settings_service() -> SettingsService:
    """Get global settings service instance"""
    global _settings_service_instance
    if _settings_service_instance is None:
        _settings_service_instance = SettingsService()
    return _settings_service_instance
