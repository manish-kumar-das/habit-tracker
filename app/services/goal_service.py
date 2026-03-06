"""
Goal Service - Handles all goal-related operations - FULLY FIXED
"""

from app.db.database import get_db_connection
from app.models.goal import Goal
from datetime import datetime


class GoalService:
    """Service for managing goals"""

    def __init__(self):
        self._ensure_goals_table()

    def _ensure_goals_table(self):
        """Ensure goals table exists with correct schema"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS goals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_id INTEGER NOT NULL,
                    goal_type TEXT NOT NULL,
                    target_value INTEGER NOT NULL,
                    current_value INTEGER DEFAULT 0,
                    is_completed INTEGER DEFAULT 0,
                    created_at TEXT NOT NULL,
                    completed_at TEXT,
                    FOREIGN KEY (habit_id) REFERENCES habits (id) ON DELETE CASCADE
                )
            """)

            conn.commit()
            conn.close()
            print("✅ Goals table ensured")
        except Exception as e:
            print(f"❌ Error ensuring goals table: {e}")

    def create_goal(self, habit_id, goal_type, target_value):
        """Create a new goal"""
        try:
            if not habit_id:
                return None
            if not goal_type:
                return None
            if not target_value or target_value <= 0:
                return None

            conn = get_db_connection()
            cursor = conn.cursor()

            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(
                """
                INSERT INTO goals (habit_id, goal_type, target_value, current_value, is_completed, created_at)
                VALUES (?, ?, ?, 0, 0, ?)
            """,
                (habit_id, goal_type, target_value, created_at),
            )

            goal_id = cursor.lastrowid

            conn.commit()
            conn.close()

            return goal_id

        except Exception as e:
            print(f"Error creating goal: {e}")
            import traceback

            traceback.print_exc()
            return None

    def get_all_goals(self, include_completed=False):
        """Get all goals - FIXED"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            if include_completed:
                cursor.execute("SELECT * FROM goals ORDER BY created_at DESC")
            else:
                cursor.execute(
                    "SELECT * FROM goals WHERE is_completed = 0 ORDER BY created_at DESC"
                )

            rows = cursor.fetchall()
            conn.close()

            goals = []
            for row in rows:
                goal = Goal(
                    id=row["id"],
                    habit_id=row["habit_id"],
                    goal_type=row["goal_type"],
                    target_value=row["target_value"],
                    current_value=row["current_value"],
                    is_completed=bool(row["is_completed"]),
                    created_at=row["created_at"],
                    completed_at=row["completed_at"] if row["completed_at"] else None,
                )
                goals.append(goal)

            return goals
        except Exception as e:
            print(f"Error getting goals: {e}")
            import traceback

            traceback.print_exc()
            return []

    def get_goal_by_id(self, goal_id):
        """Get a specific goal by ID - FIXED"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM goals WHERE id = ?", (goal_id,))
            row = cursor.fetchone()

            conn.close()

            if row:
                return Goal(
                    id=row["id"],
                    habit_id=row["habit_id"],
                    goal_type=row["goal_type"],
                    target_value=row["target_value"],
                    current_value=row["current_value"],
                    is_completed=bool(row["is_completed"]),
                    created_at=row["created_at"],
                    completed_at=row["completed_at"] if row["completed_at"] else None,
                )

            return None
        except Exception as e:
            print(f"Error getting goal by id: {e}")
            return None

    def get_goals_by_habit(self, habit_id, include_completed=False):
        """Get all goals for a specific habit - FIXED"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            if include_completed:
                cursor.execute(
                    "SELECT * FROM goals WHERE habit_id = ? ORDER BY created_at DESC",
                    (habit_id,),
                )
            else:
                cursor.execute(
                    "SELECT * FROM goals WHERE habit_id = ? AND is_completed = 0 ORDER BY created_at DESC",
                    (habit_id,),
                )

            rows = cursor.fetchall()
            conn.close()

            goals = []
            for row in rows:
                goal = Goal(
                    id=row["id"],
                    habit_id=row["habit_id"],
                    goal_type=row["goal_type"],
                    target_value=row["target_value"],
                    current_value=row["current_value"],
                    is_completed=bool(row["is_completed"]),
                    created_at=row["created_at"],
                    completed_at=row["completed_at"] if row["completed_at"] else None,
                )
                goals.append(goal)

            return goals
        except Exception as e:
            print(f"Error getting goals by habit: {e}")
            return []

    def update_goal_progress(self, goal_id, current_value):
        """Update goal progress"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE goals 
                SET current_value = ? 
                WHERE id = ?
            """,
                (current_value, goal_id),
            )

            conn.commit()
            conn.close()

            return True
        except Exception as e:
            print(f"Error updating goal progress: {e}")
            return False

    def complete_goal(self, goal_id):
        """Mark a goal as completed"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(
                """
                UPDATE goals 
                SET is_completed = 1, completed_at = ? 
                WHERE id = ?
            """,
                (completed_at, goal_id),
            )

            conn.commit()
            conn.close()

            return True
        except Exception as e:
            print(f"Error completing goal: {e}")
            return False

    def delete_goal(self, goal_id):
        """Delete a goal"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM goals WHERE id = ?", (goal_id,))

            conn.commit()
            conn.close()

            return True
        except Exception as e:
            print(f"Error deleting goal: {e}")
            return False

    def check_and_update_goals(self, habit_id):
        """Check and update all active goals for a habit"""
        try:
            from app.services.streak_service import get_streak_service
            from app.services.habit_service import get_habit_service
            from app.services.notification_service import get_notification_service

            goals = self.get_goals_by_habit(habit_id, include_completed=False)
            streak_service = get_streak_service()
            habit_service = get_habit_service()

            for goal in goals:
                if "streak" in goal.goal_type.lower():
                    streak_info = streak_service.get_streak_info(habit_id)
                    current_value = streak_info.get("current_streak", 0)
                elif "completions" in goal.goal_type.lower():
                    completions = habit_service.get_habit_completions(habit_id)
                    current_value = len(completions)
                else:
                    current_value = goal.current_value

                self.update_goal_progress(goal.id, current_value)

                if current_value >= goal.target_value:
                    if self.complete_goal(goal.id):
                        get_notification_service().send_goal_completed(
                            goal.goal_type, goal.target_value
                        )
        except Exception as e:
            print(f"Error checking and updating goals: {e}")


# Singleton instance
_goal_service_instance = None


def get_goal_service():
    """Get the goal service singleton instance"""
    global _goal_service_instance
    if _goal_service_instance is None:
        _goal_service_instance = GoalService()
    return _goal_service_instance
