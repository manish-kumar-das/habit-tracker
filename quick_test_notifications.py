#!/usr/bin/env python3
"""Quick notification test"""
from app.services.notification_service import get_notification_service
from app.services.settings_service import get_settings_service

# Enable notifications
settings = get_settings_service()
settings.set_notifications_enabled(True)

# Get service
notif = get_notification_service()

print("Sending 3 test notifications...")
print("1. Basic notification...")
notif.send_notification("Test 1", "Basic notification works!")

print("2. Habit completed...")
notif.send_habit_completed("Morning Exercise")

print("3. Daily reminder...")
notif.send_daily_reminder()

print("\nDone! Check your desktop for 3 notifications.")
