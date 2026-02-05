"""
Main application window - Dark Mode Design
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QMessageBox, QStatusBar
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QFont
from app.ui.today_view import TodayView
from app.ui.add_habit_dialog import AddHabitDialog
from app.utils.constants import WINDOW_TITLE, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT


class MainWindow(QMainWindow):
    """Main application window - Dark theme"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_menu()
        self.setup_statusbar()
    
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
        
        refresh_action = QAction("&Refresh", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self.refresh_view)
        file_menu.addAction(refresh_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
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
        self.statusbar.showMessage("Ready")
    
    def show_add_habit_dialog(self):
        """Show dialog to add new habit"""
        dialog = AddHabitDialog(self)
        if dialog.exec():
            self.refresh_view()
            self.statusbar.showMessage("✓ Habit added successfully", 3000)
    
    def refresh_view(self):
        """Refresh the today view"""
        self.today_view.load_habits()
        self.statusbar.showMessage("↻ Refreshed", 2000)
    
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
            QPushButton {
                background-color: #4FD1C5;
                color: #0F1115;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #45B8AD;
            }
        """)
        msg.exec()
