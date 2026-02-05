"""
Habit Tracker - Main Entry Point
A simple desktop application for tracking daily habits.
"""

import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from app.ui.main_window import MainWindow


def load_stylesheet(app):
    """Load application stylesheet"""
    stylesheet_path = os.path.join("app", "assets", "styles", "theme.qss")
    
    if os.path.exists(stylesheet_path):
        with open(stylesheet_path, "r") as f:
            app.setStyleSheet(f.read())


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Set application metadata
    app.setApplicationName("Habit Tracker")
    app.setOrganizationName("YourName")
    app.setApplicationVersion("1.0.0")
    
    # Load stylesheet
    load_stylesheet(app)
    
    # Set application icon (if exists)
    icon_path = os.path.join("app", "assets", "icons", "app_icon.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
