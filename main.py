"""
Habit Tracker - Main Entry Point
A simple desktop application for tracking daily habits.
"""

import sys
from PySide6.QtWidgets import QApplication
from app.ui.main_window import MainWindow


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Set application metadata
    app.setApplicationName("Habit Tracker")
    app.setOrganizationName("YourName")
    app.setApplicationVersion("1.0.0")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
