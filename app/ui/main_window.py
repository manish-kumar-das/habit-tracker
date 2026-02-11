"""
Main application window - Dark Mode Design with all Tier 1 & 2 features
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QMessageBox, QStatusBar, QLineEdit, QComboBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction, QFont, QShortcut, QKeySequence
from app.ui.today_view import TodayView
from app.ui.add_habit_dialog import AddHabitDialog
from app.ui.stats_view import StatsView
from app.ui.export_dialog import ExportDialog
from app.ui.trash_dialog import TrashDialog
from app.utils.constants import WINDOW_TITLE, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT
from app.ui.settings_dialog import SettingsDialog
from app.services.settings_service import get_settings_service
from app.utils.themes import apply_theme, get_dark_colors, get_light_colors


class MainWindow(QMainWindow):
    """Main application window - Dark theme with all features"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_menu()
        self.setup_statusbar()
        self.setup_shortcuts()
    
    def setup_ui(self):
        """Setup the main UI"""
        self.setWindowTitle(WINDOW_TITLE)
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0F1115;
            }
        """)
        
        # Create central widget
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #0F1115;")
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(24)
        
        # Header section
        header_layout = QHBoxLayout()
        header_layout.setSpacing(16)
        
        # App icon/emoji
        icon_label = QLabel("✨")
        icon_label.setFont(QFont("Inter", 32))
        icon_label.setStyleSheet("background: transparent;")
        header_layout.addWidget(icon_label)
        
        # Title and subtitle
        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)
        
        title = QLabel("Today's Habits")
        title.setFont(QFont("Inter", 28, QFont.Bold))
        title.setStyleSheet("color: #E4E6EB; background: transparent;")
        title_layout.addWidget(title)
        
        from app.utils.dates import get_today
        from datetime import datetime
        today_str = datetime.strptime(get_today(), "%Y-%m-%d").strftime("%A, %B %d")
        subtitle = QLabel(today_str)
        subtitle.setFont(QFont("Inter", 14))
        subtitle.setStyleSheet("color: #9AA0A6; background: transparent;")
        title_layout.addWidget(subtitle)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Search and Sort toolbar
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setSpacing(12)
        
        # Search bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search habits...")
        self.search_input.setFont(QFont("Inter", 13))
        self.search_input.setFixedHeight(44)
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 10px 16px;
                border: 2px solid #2A2D35;
                border-radius: 10px;
                background-color: #1C1F26;
                color: #E4E6EB;
                selection-background-color: #4FD1C5;
            }
            QLineEdit:focus {
                border: 2px solid #4FD1C5;
                background-color: #20232B;
            }
        """)
        self.search_input.textChanged.connect(self.on_search_changed)
        toolbar_layout.addWidget(self.search_input, stretch=1)
        
        # Sort dropdown
        sort_label = QLabel("Sort:")
        sort_label.setFont(QFont("Inter", 13))
        sort_label.setStyleSheet("color: #9AA0A6; background: transparent;")
        toolbar_layout.addWidget(sort_label)
        
        self.sort_combo = QComboBox()
        self.sort_combo.addItem("📅 Recent", "date_desc")
        self.sort_combo.addItem("🔤 A → Z", "name_asc")
        self.sort_combo.addItem("🔤 Z → A", "name_desc")
        self.sort_combo.addItem("🔥 Highest Streak", "streak_desc")
        self.sort_combo.addItem("📊 Most Complete", "completion_desc")
        self.sort_combo.setFont(QFont("Inter", 12))
        self.sort_combo.setFixedHeight(44)
        self.sort_combo.setFixedWidth(180)
        self.sort_combo.setCursor(Qt.PointingHandCursor)
        self.sort_combo.setStyleSheet("""
            QComboBox {
                padding: 10px 16px;
                border: 2px solid #2A2D35;
                border-radius: 10px;
                background-color: #1C1F26;
                color: #E4E6EB;
            }
            QComboBox:hover {
                border: 2px solid #4FD1C5;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 12px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #9AA0A6;
                margin-right: 8px;
            }
            QComboBox QAbstractItemView {
                background-color: #1C1F26;
                border: 1px solid #2A2D35;
                border-radius: 8px;
                padding: 4px;
                color: #E4E6EB;
                selection-background-color: #4FD1C5;
                selection-color: #0F1115;
            }
        """)
        self.sort_combo.currentIndexChanged.connect(self.on_sort_changed)
        toolbar_layout.addWidget(self.sort_combo)
        
        layout.addLayout(toolbar_layout)
        
        # Today view (main content)
        self.today_view = TodayView()
        layout.addWidget(self.today_view, stretch=1)
        
        # Add habit button
        add_button = QPushButton("+ Add New Habit")
        add_button.setFont(QFont("Inter", 14, QFont.Medium))
        add_button.setCursor(Qt.PointingHandCursor)
        add_button.setFixedHeight(52)
        add_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4FD1C5, stop:1 #7C83FD);
                color: #FFFFFF;
                border: none;
                border-radius: 12px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #45B8AD, stop:1 #6B6FE5);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3A9D93, stop:1 #5A5ECD);
            }
        """)
        add_button.clicked.connect(self.show_add_habit_dialog)
        layout.addWidget(add_button)
    
    def setup_menu(self):
        """Setup menu bar"""
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #1C1F26;
                border-bottom: 1px solid #2A2D35;
                padding: 6px;
                color: #E4E6EB;
            }
            QMenuBar::item {
                padding: 8px 12px;
                background: transparent;
                color: #E4E6EB;
                border-radius: 6px;
            }
            QMenuBar::item:selected {
                background-color: #4FD1C5;
                color: #0F1115;
            }
            QMenu {
                background-color: #1C1F26;
                border: 1px solid #2A2D35;
                border-radius: 8px;
                padding: 8px;
                color: #E4E6EB;
            }
            QMenu::item {
                padding: 10px 24px;
                border-radius: 6px;
                color: #E4E6EB;
            }
            QMenu::item:selected {
                background-color: #20232B;
                color: #4FD1C5;
            }
        """)
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        add_action = QAction("&New Habit", self)
        add_action.setShortcut("Ctrl+N")
        add_action.triggered.connect(self.show_add_habit_dialog)
        file_menu.addAction(add_action)
        
        refresh_action = QAction("&Refresh", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self.refresh_view)
        file_menu.addAction(refresh_action)
        
        file_menu.addSeparator()
        
        export_action = QAction("&Export Data", self)
        export_action.setShortcut("Ctrl+E")
        export_action.triggered.connect(self.export_data)
        file_menu.addAction(export_action)
        
        trash_action = QAction("🗑️ &Trash", self)
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

        stats_action = QAction("&Statistics", self)
        stats_action.setShortcut("Ctrl+S")
        stats_action.triggered.connect(self.show_statistics)
        view_menu.addAction(stats_action)

        # NEW: Calendar action
        calendar_action = QAction("&Calendar", self)
        calendar_action.setShortcut("Ctrl+K")
        calendar_action.triggered.connect(self.show_calendar)
        view_menu.addAction(calendar_action)
        
        # Settings menu
        settings_menu = menubar.addMenu("&Settings")

        preferences_action = QAction("&Preferences", self)
        preferences_action.setShortcut("Ctrl+,")
        preferences_action.triggered.connect(self.show_settings)
        settings_menu.addAction(preferences_action)

        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        shortcuts_action = QAction("&Keyboard Shortcuts", self)
        shortcuts_action.setShortcut("Ctrl+/")
        shortcuts_action.triggered.connect(self.show_shortcuts)
        help_menu.addAction(shortcuts_action)
        
        help_menu.addSeparator()
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        # Focus search bar
        search_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        search_shortcut.activated.connect(self.focus_search)
        
        # Clear search
        clear_shortcut = QShortcut(QKeySequence("Esc"), self)
        clear_shortcut.activated.connect(self.clear_search)
    
    def setup_statusbar(self):
        """Setup status bar"""
        self.statusbar = QStatusBar()
        self.statusbar.setStyleSheet("""
            QStatusBar {
                background-color: #1C1F26;
                border-top: 1px solid #2A2D35;
                color: #9AA0A6;
                padding: 6px 12px;
            }
        """)
        self.setStatusBar(self.statusbar)
        self.update_status()
    
    def update_status(self):
        """Update status bar with habit count"""
        from app.services.habit_service import get_habit_service
        habit_service = get_habit_service()
        habits = habit_service.get_all_habits()
        
        completed_today = sum(1 for h in habits if habit_service.is_habit_completed_today(h.id))
        total = len(habits)
        
        self.statusbar.showMessage(f"📊 {completed_today}/{total} habits completed today")
    
    def on_search_changed(self, text):
        """Handle search text change"""
        self.today_view.filter_habits(text)
        
    def on_sort_changed(self, index):
        """Handle sort option change"""
        sort_by = self.sort_combo.currentData()
        self.today_view.sort_habits(sort_by)
    
    def focus_search(self):
        """Focus on search bar"""
        self.search_input.setFocus()
        self.search_input.selectAll()
    
    def clear_search(self):
        """Clear search and show all habits"""
        self.search_input.clear()
        self.search_input.clearFocus()
    
    def show_add_habit_dialog(self):
        """Show dialog to add new habit"""
        dialog = AddHabitDialog(self)
        if dialog.exec():
            self.refresh_view()
            self.statusbar.showMessage("✓ Habit added successfully", 3000)
            self.update_status()
    
    def refresh_view(self):
        """Refresh the today view"""
        self.today_view.load_habits()
        self.update_status()
        self.statusbar.showMessage("↻ Refreshed", 2000)
    
    def export_data(self):
        """Export habits data"""
        dialog = ExportDialog(self)
        dialog.exec()
    
    def show_statistics(self):
        """Show statistics view"""
        stats_dialog = StatsView(self)
        stats_dialog.show()
    
    def show_trash(self):
        """Show trash dialog"""
        trash_dialog = TrashDialog(self)
        trash_dialog.exec()
        # Refresh main view in case habits were restored
        self.refresh_view()
    
    def show_shortcuts(self):
        """Show keyboard shortcuts"""
        msg = QMessageBox(self)
        msg.setWindowTitle("Keyboard Shortcuts")
        msg.setText("<h3 style='color: #4FD1C5;'>⌨️ Keyboard Shortcuts</h3>")
        msg.setInformativeText(
            "<p style='color: #E4E6EB;'><b>General</b></p>"
            "<p style='color: #9AA0A6;'>"
            "<b>Ctrl+N</b> - Add new habit<br>"
            "<b>Ctrl+F</b> - Focus search bar<br>"
            "<b>F5</b> - Refresh view<br>"
            "<b>Esc</b> - Clear search<br>"
            "<b>Ctrl+Q</b> - Quit application<br><br>"
            "</p>"
            "<p style='color: #E4E6EB;'><b>Views</b></p>"
            "<p style='color: #9AA0A6;'>"
            "<b>Ctrl+S</b> - Statistics<br>"
            "<b>Ctrl+T</b> - Trash<br><br>"
            "</p>"
            "<p style='color: #E4E6EB;'><b>Data</b></p>"
            "<p style='color: #9AA0A6;'>"
            "<b>Ctrl+E</b> - Export data<br>"
            "</p>"
        )
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #1C1F26;
                min-width: 400px;
            }
            QMessageBox QLabel {
                color: #E4E6EB;
            }
            QPushButton {
                background-color: #4FD1C5;
                color: #0F1115;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-weight: bold;
                min-width: 80px;
            }
        """)
        msg.exec()
    
    def show_about(self):
        """Show about dialog"""
        msg = QMessageBox(self)
        msg.setWindowTitle("About Habit Tracker")
        msg.setText("<h2 style='color: #4FD1C5;'>Habit Tracker v1.0</h2>")
        msg.setInformativeText(
            "<p style='color: #E4E6EB;'>A beautiful habit tracking application</p>"
            "<p style='color: #9AA0A6;'>Built with Python and PySide6</p>"
            "<p style='color: #4FD1C5; font-weight: bold;'>Track habits. Build consistency. Achieve goals.</p>"
        )
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #1C1F26;
            }
            QMessageBox QLabel {
                color: #E4E6EB;
            }
            QPushButton {
                background-color: #4FD1C5;
                color: #0F1115;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-weight: bold;
                min-width: 80px;
            }
        """)
        msg.exec()

    def apply_theme(self, theme_name):
        """Apply theme to main window and update colors"""
        from app.utils.themes import apply_theme
        
        if theme_name == 'light':
            colors = get_light_colors()
            self.setStyleSheet(f"""
                QMainWindow {{
                    background-color: {colors['bg_primary']};
                }}
            """)
        
            # Update central widget
            self.centralWidget().setStyleSheet(f"background-color: {colors['bg_primary']};")
        
            # Update header labels
            for label in self.findChildren(QLabel):
                if "Today's Habits" in label.text():
                    label.setStyleSheet(f"color: {colors['text_primary']}; background: transparent;")
                elif label.styleSheet() and "#9AA0A6" in label.styleSheet():
                    label.setStyleSheet(f"color: {colors['text_secondary']}; background: transparent;")
        
        else:  # dark theme
            colors = get_dark_colors()
            self.setStyleSheet(f"""
                QMainWindow {{
                    background-color: {colors['bg_primary']};
                }}
            """)
        
            # Update central widget
            self.centralWidget().setStyleSheet(f"background-color: {colors['bg_primary']};")
    
        # Force reload of today view
        self.today_view.load_habits()
    
    def show_settings(self):
        """Show settings dialog"""
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec()

    def show_calendar(self):
        """Show calendar view"""
        from app.ui.calendar_view import CalendarView
        calendar_dialog = CalendarView(self)
        calendar_dialog.show()