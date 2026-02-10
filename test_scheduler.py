"""
Test scheduler and daily reminders
"""

import sys
from datetime import datetime
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from app.services.settings_service import get_settings_service
from app.services.scheduler_service import get_scheduler_service

print("=" * 70)
print("SCHEDULER TEST - Daily Reminder")
print("=" * 70)

# Create Qt application (required for QTimer)
app = QApplication(sys.argv)

# Enable notifications
settings = get_settings_service()
settings.set_notifications_enabled(True)

# Get current time
now = datetime.now()
current_time = f"{now.hour:02d}:{now.minute:02d}"

print(f"\n⏰ Current time: {current_time}")
print(f"📋 Current settings:")
print(f"   - Notifications enabled: {settings.is_notifications_enabled()}")
print(f"   - Notification time: {settings.get_notification_time()}")

# Calculate test time (1 minute from now)
test_minute = (now.minute + 1) % 60
test_hour = now.hour if (now.minute + 1) < 60 else (now.hour + 1) % 24
test_time = f"{test_hour:02d}:{test_minute:02d}"

print(f"\n�� To test, set notification time to: {test_time}")
print(f"   (This is 1 minute from now)")

# Optionally set it automatically
response = input("\nSet notification time automatically to 1 minute from now? (y/n): ")
if response.lower() == 'y':
    settings.set_notification_time(test_time)
    print(f"✅ Notification time set to: {test_time}")

# Start scheduler
print("\n🚀 Starting scheduler...")
scheduler = get_scheduler_service()

print("\n⏳ Waiting for reminder (press Ctrl+C to stop)...")
print("📺 Watch for desktop notifications and console output...\n")

# Create a timer to check status every 5 seconds
def print_status():
    now = datetime.now()
    current_time = f"{now.hour:02d}:{now.minute:02d}"
    target_time = settings.get_notification_time()
    print(f"⏰ Current: {current_time} | Target: {target_time} | Waiting...")

status_timer = QTimer()
status_timer.timeout.connect(print_status)
status_timer.start(5000)

# Auto-exit after 5 minutes
exit_timer = QTimer()
exit_timer.timeout.connect(lambda: (print("\n⏱️ Test timeout (5 minutes)"), app.quit()))
exit_timer.start(300000)

try:
    sys.exit(app.exec())
except KeyboardInterrupt:
    print("\n\n👋 Test stopped by user")
    scheduler.stop()
