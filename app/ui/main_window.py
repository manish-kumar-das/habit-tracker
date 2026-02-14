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
        
        # Start scheduler
        from app.services.scheduler_service import get_scheduler_service
        self.scheduler = get_scheduler_service()
    
    def setup_ui(self):
        """Setup the main UI"""
        # Set window background
        self.setStyleSheet("QMainWindow { background-color: #F9FAFB; }")
        
        # Central widget - DASHBOARD
        self.complete_ui = CompleteHabitHubUI(self)
        self.setCentralWidget(self.complete_ui)
        # self.setCentralWidget(self.dashboard)
        
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
        self.dashboard = ModernDashboard()
        self.setCentralWidget(self.dashboard)
        self.update_status_bar()
    
    def show_add_habit_dialog(self):
        """Show add habit dialog"""
        from app.ui.add_habit_dialog import AddHabitDialog
        
        dialog = AddHabitDialog(self)
        if dialog.exec():
            self.dashboard.load_dashboard()
            self.update_status_bar()
    
    def show_statistics(self):
        """Show statistics view"""
        from app.ui.statistics_view import StatisticsView
        stats_dialog = StatisticsView(self)
        stats_dialog.show()
    
    def show_analytics(self):
        """Show analytics dashboard"""
        from app.ui.analytics_view import AnalyticsView
        analytics_dialog = AnalyticsView(self)
        analytics_dialog.show()
    
    def show_calendar(self):
        """Show calendar view"""
        from app.ui.calendar_view import CalendarView
        calendar_dialog = CalendarView(self)
        calendar_dialog.show()
    
    def show_goals(self):
        """Show goals & milestones"""
        from app.ui.goals_view import GoalsView
        goals_dialog = GoalsView(self)
        goals_dialog.show()
    
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
            self.dashboard.load_dashboard()
    
    def show_settings(self):
        """Show settings dialog"""
        from app.ui.settings_dialog import SettingsDialog
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec()
    
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
        self.dashboard.load_dashboard()
