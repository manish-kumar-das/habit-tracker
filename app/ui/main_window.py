"""
Main application window
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QComboBox,
    QMenuBar, QMenu, QStatusBar, QMessageBox, QFileDialog
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction, QFont

from app.ui.complete_habithub_ui import CompleteHabitHubUI
from app.services.habit_service import get_habit_service
from app.services.streak_service import get_streak_service
from app.services.stats_service import get_stats_service


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Habit Tracker")
        self.setMinimumSize(1200, 800)
        
        self.habit_service = get_habit_service()
        self.streak_service = get_streak_service()
        self.stats_service = get_stats_service()
        
        self.setup_ui()
        self.setup_menu()
        self.update_status_bar()
        
    def setup_ui(self):
        """Setup the main UI with constant sidebar"""
        self.setStyleSheet("QMainWindow { background-color: #F9FAFB; }")
    
        # Main container widget
        main_container = QWidget()
        main_layout = QHBoxLayout(main_container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
    
        # Create sidebar (will be constant)
        from app.ui.complete_habithub_ui import Sidebar
        self.sidebar = Sidebar(self)
        main_layout.addWidget(self.sidebar)
    
        # Content area container (this will change)
        self.content_container = QWidget()
        self.content_container.setStyleSheet("background-color: #F8F9FA;")
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
    
        main_layout.addWidget(self.content_container, stretch=1)
    
        # Set as central widget
        self.setCentralWidget(main_container)
    
        # Load dashboard initially
        self.show_dashboard()
        
        # Status bar
        self.statusBar().setStyleSheet("""
            QStatusBar {
                background-color: #FFFFFF;
                border-top: 1px solid #E5E7EB;
                color: #6B7280;
                padding: 6px 12px;
            }
        """)
    
    def setup_menu(self):
        """Setup menu bar"""
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #FFFFFF;
                border-bottom: 1px solid #E5E7EB;
                padding: 6px;
                color: #111827;
            }
            QMenuBar::item {
                padding: 8px 12px;
                background: transparent;
                color: #111827;
                border-radius: 6px;
            }
            QMenuBar::item:selected {
                background-color: #6366F1;
                color: #FFFFFF;
            }
            QMenu {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                padding: 8px;
                color: #111827;
            }
            QMenu::item {
                padding: 10px 24px;
                border-radius: 6px;
                color: #111827;
            }
            QMenu::item:selected {
                background-color: #F3F4F6;
                color: #6366F1;
            }
        """)
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        add_action = QAction("&Add Habit", self)
        add_action.setShortcut("Ctrl+N")
        add_action.triggered.connect(self.show_add_habit_dialog)
        file_menu.addAction(add_action)
        
        file_menu.addSeparator()
        
        export_action = QAction("&Export Data", self)
        export_action.setShortcut("Ctrl+E")
        export_action.triggered.connect(self.export_data)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        trash_action = QAction("&Trash", self)
        trash_action.setShortcut("Ctrl+T")
        trash_action.triggered.connect(self.show_trash)
        file_menu.addAction(trash_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        dashboard_action = QAction("&Dashboard", self)
        dashboard_action.setShortcut("Ctrl+D")
        dashboard_action.triggered.connect(self.show_dashboard)
        view_menu.addAction(dashboard_action)
        
        stats_action = QAction("&Statistics", self)
        stats_action.setShortcut("Ctrl+S")
        stats_action.triggered.connect(self.show_statistics)
        view_menu.addAction(stats_action)
        
        analytics_action = QAction("&Analytics", self)
        analytics_action.setShortcut("Ctrl+Y")
        analytics_action.triggered.connect(self.show_analytics)
        view_menu.addAction(analytics_action)
        
        calendar_action = QAction("&Calendar", self)
        calendar_action.setShortcut("Ctrl+L")
        calendar_action.triggered.connect(self.show_calendar)
        view_menu.addAction(calendar_action)
        
        goals_action = QAction("&Goals", self)
        goals_action.setShortcut("Ctrl+G")
        goals_action.triggered.connect(self.show_goals)
        view_menu.addAction(goals_action)
        
        achievements_action = QAction("A&chievements", self)
        achievements_action.setShortcut("Ctrl+B")
        achievements_action.triggered.connect(self.show_achievements)
        view_menu.addAction(achievements_action)
        
        # Settings menu
        settings_menu = menubar.addMenu("&Settings")
        
        preferences_action = QAction("&Preferences", self)
        preferences_action.setShortcut("Ctrl+,")
        preferences_action.triggered.connect(self.show_settings)
        settings_menu.addAction(preferences_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        shortcuts_action = QAction("&Keyboard Shortcuts", self)
        shortcuts_action.setShortcut("Ctrl+H")
        shortcuts_action.triggered.connect(self.show_keyboard_shortcuts)
        help_menu.addAction(shortcuts_action)
        
        help_menu.addSeparator()
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
     
    def show_dashboard(self):
        """Show dashboard view"""
        # Clear content area
        self.clear_content_area()
    
        # Create and add dashboard
        from app.ui.complete_habithub_ui import DashboardContent
        dashboard = DashboardContent(self)
        self.content_layout.addWidget(dashboard)
    
        # Update sidebar active state
        if hasattr(self, 'sidebar'):
            self.sidebar.update_active_button('dashboard')
    
        self.update_status_bar()

    # def show_today_view(self):
    #     """Show today's habits view"""
    #     self.clear_content_area()
    
    #     from app.ui.today_view import TodayView
    #     today_view = TodayView()
    #     self.content_layout.addWidget(today_view)
    #     today_view.load_habits()
    
    #     if hasattr(self, 'sidebar'):
    #         self.sidebar.update_active_button('today')
    
    #     self.update_status_bar()

    def show_today_view(self):
        """Show today's habits view"""
        self.clear_content_area()
    
        from app.ui.today_content_view import TodayContentView
        today_view = TodayContentView(self)
        self.content_layout.addWidget(today_view)
    
        if hasattr(self, 'sidebar'):
            self.sidebar.update_active_button('today')
    
        self.update_status_bar()

    def show_habits_view(self):
        """Show all habits view"""
        self.clear_content_area()
    
        from app.ui.habits_list_view import HabitsListView
        habits_view = HabitsListView()
        self.content_layout.addWidget(habits_view)
        habits_view.load_habits()
    
        if hasattr(self, 'sidebar'):
            self.sidebar.update_active_button('habits')
    
        self.update_status_bar()

    def clear_content_area(self):
        """Clear all widgets from content area"""
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def show_add_habit_dialog(self):
        """Show add habit dialog"""
        from app.ui.add_habit_dialog import AddHabitDialog
        
        dialog = AddHabitDialog(self)
        if dialog.exec():
            # Reload complete UI
            if hasattr(self, 'complete_ui'):
                self.complete_ui.load_data()
            self.update_status_bar()

    def show_statistics(self):
        """Show statistics view"""
        from app.ui.stats_view import StatsView
        stats_dialog = StatsView(self)
        stats_dialog.show()

    def show_analytics(self):
        """Show analytics in content area"""
        self.clear_content_area()
    
        from app.ui.analytics_content_view import AnalyticsContentView
        analytics_view = AnalyticsContentView(self)
        self.content_layout.addWidget(analytics_view)
    
        if hasattr(self, 'sidebar'):
            self.sidebar.update_active_button('analytics')
    
        self.update_status_bar()

    def show_calendar(self):
        """Show calendar view"""
        from app.ui.calendar_view import CalendarView
        calendar_dialog = CalendarView(self)
        calendar_dialog.show()

    def show_goals(self):
        """Show goals in content area"""
        self.clear_content_area()
    
        from app.ui.goals_content_view import GoalsContentView
        goals_view = GoalsContentView(self)
        self.content_layout.addWidget(goals_view)
    
        if hasattr(self, 'sidebar'):
            self.sidebar.update_active_button('goals')
    
        self.update_status_bar()

    def show_achievements(self):
        """Show achievements & badges"""
        from app.ui.achievements_view import AchievementsView
        achievements_dialog = AchievementsView(self)
        achievements_dialog.show()

    def show_trash(self):
        """Show trash dialog"""
        from app.ui.trash_dialog import TrashDialog
        trash_dialog = TrashDialog(self)
        if trash_dialog.exec():
            if hasattr(self, 'complete_ui'):
                self.complete_ui.load_data()

    # def show_settings(self):
        """Show settings dialog"""
        from app.ui.settings_dialog import SettingsDialog
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec()

    def show_settings(self):
        """Show settings in content area"""
        self.clear_content_area()
    
        from app.ui.settings_content_view import SettingsContentView
        settings_view = SettingsContentView(self)
        self.content_layout.addWidget(settings_view)
    
        if hasattr(self, 'sidebar'):
            self.sidebar.update_active_button('settings')
    
        self.update_status_bar()

    def export_data(self):
        """Export habit data"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Habit Data",
            "",
            "CSV Files (*.csv);;JSON Files (*.json)"
        )
        
        if file_path:
            try:
                import csv
                import json
                
                habits = self.habit_service.get_all_habits()
                
                if file_path.endswith('.csv'):
                    with open(file_path, 'w', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(['Name', 'Category', 'Description', 'Frequency', 'Total Completions'])
                        
                        for habit in habits:
                            completions = len(self.habit_service.get_habit_completions(habit.id))
                            writer.writerow([
                                habit.name,
                                habit.category,
                                habit.description,
                                habit.frequency,
                                completions
                            ])
                
                elif file_path.endswith('.json'):
                    data = []
                    for habit in habits:
                        completions = self.habit_service.get_habit_completions(habit.id)
                        data.append({
                            'name': habit.name,
                            'category': habit.category,
                            'description': habit.description,
                            'frequency': habit.frequency,
                            'completions': completions,
                            'total_completions': len(completions)
                        })
                    
                    with open(file_path, 'w') as f:
                        json.dump(data, f, indent=2)
                
                QMessageBox.information(self, "Success", "Data exported successfully!")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export data: {str(e)}")
    
    def show_keyboard_shortcuts(self):
        """Show keyboard shortcuts help"""
        shortcuts_text = """
        <h2 style='color: #6366F1;'>⌨️ Keyboard Shortcuts</h2>
        
        <h3 style='color: #111827;'>General</h3>
        <table style='color: #111827;'>
            <tr><td><b>Ctrl+N</b></td><td>Add New Habit</td></tr>
            <tr><td><b>Ctrl+Q</b></td><td>Quit Application</td></tr>
        </table>
        
        <h3 style='color: #111827;'>Views</h3>
        <table style='color: #111827;'>
            <tr><td><b>Ctrl+D</b></td><td>Dashboard</td></tr>
            <tr><td><b>Ctrl+S</b></td><td>Statistics</td></tr>
            <tr><td><b>Ctrl+Y</b></td><td>Analytics Dashboard</td></tr>
            <tr><td><b>Ctrl+L</b></td><td>Calendar View</td></tr>
            <tr><td><b>Ctrl+G</b></td><td>Goals</td></tr>
            <tr><td><b>Ctrl+B</b></td><td>Achievements</td></tr>
        </table>
        
        <h3 style='color: #111827;'>Data</h3>
        <table style='color: #111827;'>
            <tr><td><b>Ctrl+E</b></td><td>Export Data</td></tr>
            <tr><td><b>Ctrl+T</b></td><td>Trash / Deleted Habits</td></tr>
        </table>
        
        <h3 style='color: #111827;'>Settings</h3>
        <table style='color: #111827;'>
            <tr><td><b>Ctrl+,</b></td><td>Preferences</td></tr>
            <tr><td><b>Ctrl+H</b></td><td>Show This Help</td></tr>
        </table>
        """
        
        msg = QMessageBox(self)
        msg.setWindowTitle("Keyboard Shortcuts")
        msg.setTextFormat(Qt.RichText)
        msg.setText(shortcuts_text)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #FFFFFF;
            }
            QMessageBox QLabel {
                color: #111827;
            }
            QPushButton {
                background-color: #6366F1;
                color: #FFFFFF;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #4F46E5;
            }
        """)
        msg.exec()
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
        <h2 style='color: #6366F1;'>Habit Tracker</h2>
        <p style='color: #111827;'><b>Version:</b> 1.0.0</p>
        <p style='color: #6B7280;'>
            A modern habit tracking application to help you build 
            better habits and achieve your goals.
        </p>
        <p style='color: #6B7280;'>
            Built with PySide6 and Python.
        </p>
        """
        
        msg = QMessageBox(self)
        msg.setWindowTitle("About Habit Tracker")
        msg.setTextFormat(Qt.RichText)
        msg.setText(about_text)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #FFFFFF;
            }
            QMessageBox QLabel {
                color: #111827;
            }
            QPushButton {
                background-color: #6366F1;
                color: #FFFFFF;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-weight: bold;
                min-width: 80px;
            }
        """)
        msg.exec()
    
    def update_status_bar(self):
        """Update status bar with current stats"""
        habits = self.habit_service.get_all_habits()
        total = len(habits)
        completed_today = sum(1 for h in habits if self.habit_service.is_habit_completed_today(h.id))
        
        self.statusBar().showMessage(
            f"Total Habits: {total} | Completed Today: {completed_today}/{total}"
        )
    
    def apply_theme(self, theme_name):
        """Apply theme to main window"""
        from app.utils.themes import apply_theme, get_dark_colors, get_light_colors
        
        if theme_name == 'light':
            colors = get_light_colors()
            self.setStyleSheet(f"QMainWindow {{ background-color: {colors['bg_primary']}; }}")
        else:
            colors = get_dark_colors()
            self.setStyleSheet(f"QMainWindow {{ background-color: {colors['bg_primary']}; }}")
        
        # Reload dashboard
        if hasattr(self, 'complete_ui'):
            self.complete_ui.load_data()
