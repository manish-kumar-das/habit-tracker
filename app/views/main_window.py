"""
Main application window
"""

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QFileDialog,
)
from app.services.habit_service import get_habit_service
from app.services.streak_service import get_streak_service
from app.services.stats_service import get_stats_service
from app.services.scheduler_service import get_scheduler_service
from app.themes import get_theme_manager


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Habit Tracker")
        self.setMinimumSize(1200, 800)

        self.habit_service = get_habit_service()
        self.streak_service = get_streak_service()
        self.stats_service = get_stats_service()
        self.scheduler = get_scheduler_service()
        self.theme_manager = get_theme_manager()
        self.theme_manager.load_preference()

        self.setup_ui()
        self.update_status_bar()

    def setup_ui(self):
        """Setup the main UI with constant sidebar"""
        colors = self.theme_manager.get_theme()
        self.setStyleSheet(f"QMainWindow {{ background-color: {colors.BG_PRIMARY}; }}")

        # Main container widget
        main_container = QWidget()
        main_layout = QHBoxLayout(main_container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create sidebar (will be constant)
        from app.views.sidebar import Sidebar

        self.sidebar = Sidebar(self)
        main_layout.addWidget(self.sidebar)

        # Content area container (this will change)
        self.content_container = QWidget()
        colors = self.theme_manager.get_theme()
        self.content_container.setStyleSheet(f"background-color: {colors.BG_PRIMARY};")
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)

        main_layout.addWidget(self.content_container, stretch=1)

        # Set as central widget
        self.setCentralWidget(main_container)

        # Load dashboard initially
        self.show_dashboard()

    def show_dashboard(self):
        """Show dashboard view"""
        self.clear_content_area()

        from app.views.dashboard_content_view import DashboardContentView

        dashboard = DashboardContentView(self)
        self.content_layout.addWidget(dashboard)

        if hasattr(self, "sidebar"):
            self.sidebar.update_active_button("dashboard")

        self.update_status_bar()

    # def show_today_view(self):
    #     """Show today's habits view"""
    #     self.clear_content_area()

    #     from app.views.today_content_view import TodayContentView
    #     today_view = TodayContentView(self)
    #     self.content_layout.addWidget(today_view)

    #     if hasattr(self, 'sidebar'):
    #         self.sidebar.update_active_button('today')

    #     self.update_status_bar()

    # def show_habits_view(self):
    #     """Show all habits view"""
    #     self.clear_content_area()

    #     from app.views.habits_list_view import HabitsListView
    #     habits_view = HabitsListView()
    #     self.content_layout.addWidget(habits_view)
    #     habits_view.load_habits()

    #     if hasattr(self, 'sidebar'):
    #         self.sidebar.update_active_button('habits')

    #     self.update_status_bar()

    def clear_content_area(self):
        """Clear all widgets from content area"""
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def show_add_habit_dialog(self):
        """Show add habit dialog and refresh current view if successful"""
        from app.views.add_habit_dialog import AddHabitDialog

        dialog = AddHabitDialog(self)
        result = dialog.exec()

        if result:
            # Refresh current content view if it has a load method
            if hasattr(self, "content_layout") and self.content_layout.count() > 0:
                item = self.content_layout.itemAt(0)
                if item and item.widget():
                    widget = item.widget()
                    # Try various load methods common in our views
                    for method in ["load_dashboard", "load_data", "load_habits"]:
                        if hasattr(widget, method):
                            getattr(widget, method)()
                            break

            # Reload complete UI (if it exists)
            if hasattr(self, "complete_ui"):
                self.complete_ui.load_data()
            self.update_status_bar()

        return result

    def show_analytics(self):
        """Show analytics in content area"""
        self.clear_content_area()

        from app.views.analytics_content_view import AnalyticsContentView

        analytics_view = AnalyticsContentView(self)
        self.content_layout.addWidget(analytics_view)

        if hasattr(self, "sidebar"):
            self.sidebar.update_active_button("analytics")

        self.update_status_bar()

    def show_goals(self):
        """Show goals in content area"""
        self.clear_content_area()

        from app.views.goals_content_view import GoalsContentView

        goals_view = GoalsContentView(self)
        self.content_layout.addWidget(goals_view)

        if hasattr(self, "sidebar"):
            self.sidebar.update_active_button("goals")

        self.update_status_bar()

    def show_trash(self):
        """Show trash dialog"""
        from app.views.trash_view import TrashDialog

        trash_dialog = TrashDialog(self)
        if trash_dialog.exec():
            if hasattr(self, "complete_ui"):
                self.complete_ui.load_data()

    def show_settings(self):
        """Show settings in content area"""
        self.clear_content_area()

        from app.views.settings_content_view import SettingsContentView

        settings_view = SettingsContentView(self)
        self.content_layout.addWidget(settings_view)

        if hasattr(self, "sidebar"):
            self.sidebar.update_active_button("settings")

        self.update_status_bar()

    def show_profile(self):
        """Show profile in content area"""
        self.clear_content_area()

        from app.views.profile_content_view import ProfileContentView

        profile_view = ProfileContentView(self)
        self.content_layout.addWidget(profile_view)

        # Don't highlight any sidebar button for profile
        if hasattr(self, "sidebar"):
            # Keep current active button as is
            pass

        self.update_status_bar()

    def export_data(self):
        """Export habit data"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Habit Data", "", "CSV Files (*.csv);;JSON Files (*.json)"
        )

        if file_path:
            try:
                import csv
                import json

                habits = self.habit_service.get_all_habits()

                if file_path.endswith(".csv"):
                    with open(file_path, "w", newline="") as f:
                        writer = csv.writer(f)
                        writer.writerow(
                            [
                                "Name",
                                "Category",
                                "Description",
                                "Frequency",
                                "Total Completions",
                            ]
                        )

                        for habit in habits:
                            completions = len(
                                self.habit_service.get_habit_completions(habit.id)
                            )
                            writer.writerow(
                                [
                                    habit.name,
                                    habit.category,
                                    habit.description,
                                    habit.frequency,
                                    completions,
                                ]
                            )

                elif file_path.endswith(".json"):
                    data = []
                    for habit in habits:
                        completions = self.habit_service.get_habit_completions(habit.id)
                        data.append(
                            {
                                "name": habit.name,
                                "category": habit.category,
                                "description": habit.description,
                                "frequency": habit.frequency,
                                "completions": completions,
                                "total_completions": len(completions),
                            }
                        )

                    with open(file_path, "w") as f:
                        json.dump(data, f, indent=2)

                QMessageBox.information(self, "Success", "Data exported successfully!")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export data: {str(e)}")

    def update_status_bar(self):
        """Update status bar with current stats"""
        _ = self.habit_service.get_all_habits()
        # Stats logic can be expanded here if needed

    def apply_theme(self):
        """Apply theme to main window"""
        colors = self.theme_manager.get_theme()
        self.setStyleSheet(f"QMainWindow {{ background-color: {colors.BG_PRIMARY}; }}")
        if hasattr(self, 'content_container'):
            self.content_container.setStyleSheet(f"background-color: {colors.BG_PRIMARY};")

    def apply_theme_to_all(self):
        """Update all views with the current theme"""
        self.apply_theme()
        
        if hasattr(self, 'sidebar') and hasattr(self.sidebar, 'apply_theme'):
            self.sidebar.apply_theme()
            
        if hasattr(self, 'content_layout') and self.content_layout.count() > 0:
            item = self.content_layout.itemAt(0)
            if item and item.widget():
                widget = item.widget()
                if hasattr(widget, 'apply_theme'):
                    widget.apply_theme()
