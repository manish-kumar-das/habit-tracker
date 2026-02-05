"""
Final integration test - verify everything works
"""

import os
from app.services.habit_service import get_habit_service
from app.services.streak_service import get_streak_service
from app.services.stats_service import get_stats_service

print("=" * 70)
print("FINAL INTEGRATION TEST")
print("=" * 70)

# Test 1: Database exists
print("\n[TEST 1] Checking database...")
db_path = "data/habits.db"
if os.path.exists(db_path):
    print(f"✅ Database found at: {db_path}")
else:
    print(f"❌ Database not found!")

# Test 2: Services working
print("\n[TEST 2] Testing services...")
habit_service = get_habit_service()
streak_service = get_streak_service()
stats_service = get_stats_service()
print("✅ All services initialized successfully")

# Test 3: Get habits
print("\n[TEST 3] Checking habits...")
habits = habit_service.get_all_habits()
print(f"✅ Found {len(habits)} habit(s)")
for i, habit in enumerate(habits, 1):
    streak_info = streak_service.get_streak_info(habit.id)
    status = "✓" if habit_service.is_habit_completed_today(habit.id) else "✗"
    print(f"   {i}. {status} {habit.name} - {streak_info['current_streak']} day streak")

# Test 4: Statistics
print("\n[TEST 4] Testing statistics...")
if habits:
    stats = stats_service.get_habit_stats(habits[0].id)
    print(f"✅ Statistics generated for '{habits[0].name}'")
    print(f"   - Current Streak: {stats['current_streak']} days")
    print(f"   - Total Completions: {stats['total_completions']}")
    print(f"   - 7-day Rate: {stats['completion_rate_7d']}%")
else:
    print("⚠️  No habits to generate statistics for")

# Test 5: File structure
print("\n[TEST 5] Verifying file structure...")
required_files = [
    "main.py",
    "requirements.txt",
    "README.md",
    "LICENSE",
    ".gitignore",
    "app/ui/main_window.py",
    "app/ui/today_view.py",
    "app/ui/add_habit_dialog.py",
    "app/services/habit_service.py",
    "app/services/streak_service.py",
    "app/services/stats_service.py",
    "app/db/database.py",
    "app/models/habit.py",
    "app/assets/styles/theme.qss",
    "docs/roadmap.md"
]

missing_files = []
for file in required_files:
    if not os.path.exists(file):
        missing_files.append(file)

if missing_files:
    print(f"❌ Missing {len(missing_files)} file(s):")
    for f in missing_files:
        print(f"   - {f}")
else:
    print(f"✅ All {len(required_files)} required files present")

print("\n" + "=" * 70)
print("✨ FINAL TEST COMPLETE!")
print("=" * 70)

if not missing_files:
    print("\n🎉 Your Habit Tracker is ready to ship!")
    print("📦 Next step: Push to GitHub")
else:
    print("\n⚠️  Please create the missing files before proceeding")
