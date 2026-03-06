"""
Notification service - FIXED daily reminder
"""

import sys
import subprocess
from app.db.database import get_db_connection
from app.services.settings_service import get_settings_service


class NotificationService:
    """Service for desktop notifications"""

    def __init__(self):
        self.settings_service = get_settings_service()

    def send_notification(self, title, message):
        """Send a desktop notification"""
        if not self.settings_service.is_notifications_enabled():
            print("❌ Notifications disabled in settings")
            return False

        try:
            if sys.platform == "linux":
                result = subprocess.run(
                    [
                        "notify-send",
                        "--app-name=Habit Tracker",
                        "--icon=dialog-information",
                        title,
                        message,
                    ],
                    check=False,
                    capture_output=True,
                    text=True,
                )

                if result.returncode == 0:
                    print(f"✅ Notification sent: {title}")
                    return True
                else:
                    print(f"❌ notify-send failed: {result.stderr}")
                    return False

            elif sys.platform == "darwin":
                subprocess.run(
                    [
                        "osascript",
                        "-e",
                        f'display notification "{message}" with title "{title}"',
                    ],
                    check=False,
                    capture_output=True,
                )
                return True

            elif sys.platform == "win32":
                try:
                    from win10toast import ToastNotifier

                    toaster = ToastNotifier()
                    toaster.show_toast(title, message, duration=5, threaded=True)
                    return True
                except Exception:
                    return False

        except Exception as e:
            print(f"❌ Notification error: {e}")
            return False
        finally:
            # Always save to database for in-app display, even if desktop fails
            self.save_to_db(title, message)

    def save_to_db(self, title, message, type="reminder"):
        """Save notification to database"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            from datetime import datetime
            now = datetime.now().isoformat()
            cursor.execute(
                "INSERT INTO notifications (title, message, type, created_at) VALUES (?, ?, ?, ?)",
                (title, message, type, now),
            )
            conn.commit()
            conn.close()
            print(f"📦 Saved notification to DB: {title}")
        except Exception as e:
            print(f"❌ Error saving notification: {e}")

    def get_all_notifications(self, limit=50):
        """Get all notifications from database"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM notifications ORDER BY created_at DESC LIMIT ?", (limit,)
            )
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"❌ Error fetching notifications: {e}")
            return []

    def get_unread_count(self):
        """Get count of unread notifications"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM notifications WHERE is_read = 0"
            )
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except Exception as e:
            print(f"❌ Error getting unread count: {e}")
            return 0

    def mark_all_as_read(self):
        """Mark all notifications as read"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE notifications SET is_read = 1 WHERE is_read = 0")
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ Error marking notifications as read: {e}")
            return False

    def mark_as_read(self, notif_id):
        """Mark a single notification as read"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE notifications SET is_read = 1 WHERE id = ?", (notif_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ Error marking notification as read: {e}")
            return False

    def send_daily_reminder(self):
        """Send daily reminder for incomplete habits"""
        print("\n🔔 send_daily_reminder() called")

        if not self.settings_service.is_notifications_enabled():
            print("❌ Notifications disabled")
            return False

        # Import here to avoid circular dependency
        from app.services.habit_service import get_habit_service

        habit_service = get_habit_service()

        habits = habit_service.get_all_habits()
        print(f"📋 Total habits: {len(habits)}")

        incomplete = [
            h for h in habits if not habit_service.is_habit_completed_today(h.id)
        ]
        print(f"⏳ Incomplete habits: {len(incomplete)}")

        count = len(incomplete)

        # Goals check
        from app.services.goal_service import get_goal_service
        goal_service = get_goal_service()
        active_goals = goal_service.get_all_goals(include_completed=False)
        goal_count = len(active_goals)
        print(f"🎯 Active goals: {goal_count}")

        if count == 0:
            if goal_count == 0:
                title = "Perfect Day! 🌟"
                message = "All habits and goals completed!"
            else:
                title = "Habits Done! ✅"
                message = f"Habits are done, but you have {goal_count} active goal{'s' if goal_count > 1 else ''} in progress!"
        else:
            title = "Daily Reminder 📋"
            notif_msg = f"You have {count} incomplete habit{'s' if count > 1 else ''} today."
            if goal_count > 0:
                notif_msg += f" Plus {goal_count} goal{'s' if goal_count > 1 else ''} in progress!"
            message = notif_msg

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

        title = "Streak Milestone! 🔥"
        message = f"{streak} day streak on '{habit_name}'!"
        return self.send_notification(title, message)

    def send_goal_completed(self, goal_type, target):
        """Send notification when a goal is achieved"""
        if not self.settings_service.is_notifications_enabled():
            return False

        title = "Goal Achieved! 🏆"
        goal_name = goal_type.replace("_", " ").title()
        message = f"Congratulations! You've reached your {target} {goal_name} target!"
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
