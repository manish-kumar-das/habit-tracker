"""
Habit Tracker Application
Main entry point
"""

import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.database import init_db
from app.ui.main_window import MainWindow


def main():
    """Main application entry point"""
    # Initialize database
    init_db()
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Habit Tracker")
    
    # Set default font
    app.setFont(QFont("SF Pro Display", 11))
    
    # Simple light theme for HabitHub UI
    app.setStyleSheet("""
        QWidget {
            background-color: #F8F9FA;
            color: #212529;
        }
    """)
    
    # Create and show main window
    window = MainWindow()
    
    # FULL SCREEN MODE
    window.showMaximized()
    
    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
