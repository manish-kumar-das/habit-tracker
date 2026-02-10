"""
Test desktop notifications
"""

from app.services.notification_service import get_notification_service
from app.services.settings_service import get_settings_service

print("=" * 60)
print("TESTING DESKTOP NOTIFICATIONS")
print("=" * 60)

# Enable notifications
settings = get_settings_service()
settings.set_notifications_enabled(True)

print("\n1. Testing basic notification...")
notif = get_notification_service()
notif.send_notification(
    "Test Notification",
    "This is a test notification from Habit Tracker!"
)
print("✅ Basic notification sent")

print("\n2. Testing habit completed notification...")
notif.send_habit_completed("Morning Exercise")
print("✅ Habit completed notification sent")

print("\n3. Testing streak milestone notification...")
notif.send_streak_milestone("Reading", 7)
print("✅ Streak milestone notification sent")

print("\n4. Testing daily reminder...")
notif.send_daily_reminder()
print("✅ Daily reminder sent")

print("\n" + "=" * 60)
print("CHECK YOUR DESKTOP FOR NOTIFICATIONS!")
print("=" * 60)
print("\nIf you didn't see notifications:")
print("1. Make sure libnotify-bin is installed")
print("2. Check your system notification settings")
print("3. Try: notify-send 'Test' 'Hello World'")
