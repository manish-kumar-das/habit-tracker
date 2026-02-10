"""
Debug scheduler - see what's happening
"""

import sys
from datetime import datetime
from PySide6.QtWidgets import QApplication
from app.services.settings_service import get_settings_service
from app.services.scheduler_service import get_scheduler_service
from app.services.notification_service import get_notification_service

app = QApplication(sys.argv)

print("=" * 70)
print("SCHEDULER DEBUG")
print("=" * 70)

# Check settings
settings = get_settings_service()
print(f"\n📋 Settings:")
print(f"   Notifications enabled: {settings.is_notifications_enabled()}")
print(f"   Notification time: {settings.get_notification_time()}")

# Test notification service directly
print(f"\n🧪 Testing notification service...")
notif = get_notification_service()

print(f"   Sending test notification...")
notif.send_notification("Test", "Direct notification test")

print(f"\n   Sending daily reminder...")
notif.send_daily_reminder()

print(f"\n✅ If you saw 2 notifications, the service works!")
print(f"❌ If not, check libnotify-bin is installed")

# Now test scheduler
print(f"\n🚀 Starting scheduler for 30 seconds...")
scheduler = get_scheduler_service()

from PySide6.QtCore import QTimer
exit_timer = QTimer()
exit_timer.timeout.connect(app.quit)
exit_timer.start(30000)

sys.exit(app.exec())
