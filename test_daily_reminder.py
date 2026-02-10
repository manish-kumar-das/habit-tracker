#!/usr/bin/env python3
"""Test daily reminder specifically"""

from app.services.notification_service import get_notification_service
from app.services.settings_service import get_settings_service
from app.services.habit_service import get_habit_service

print("=" * 70)
print("DAILY REMINDER TEST")
print("=" * 70)

# Enable notifications
settings = get_settings_service()
settings.set_notifications_enabled(True)

print(f"\n✅ Notifications enabled: {settings.is_notifications_enabled()}")

# Check habits
habit_service = get_habit_service()
habits = habit_service.get_all_habits()
print(f"📋 You have {len(habits)} total habits")

incomplete = [h for h in habits if not habit_service.is_habit_completed_today(h.id)]
print(f"⏳ You have {len(incomplete)} incomplete habits today")

if incomplete:
    print(f"\nIncomplete habits:")
    for h in incomplete:
        print(f"  - {h.name}")

# Test notification
print(f"\n🔔 Sending daily reminder notification...")
notif = get_notification_service()
result = notif.send_daily_reminder()

if result:
    print(f"✅ Daily reminder sent successfully!")
else:
    print(f"❌ Daily reminder failed to send")

print("=" * 70)
