"""
Simple Habits List View - Shows all habits
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from app.services.habit_service import get_habit_service


class HabitsListView(QWidget):
    """Simple view showing all habits"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.habit_service = get_habit_service()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        self.setStyleSheet("background-color: #F8F9FA;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        
        title = QLabel("All Habits")
        title.setFont(QFont("SF Pro Display", 28, QFont.Bold))
        title.setStyleSheet("color: #212529;")
        layout.addWidget(title)
        
        self.content_layout = QVBoxLayout()
        layout.addLayout(self.content_layout)
        
        layout.addStretch()
    
    def load_habits(self):
        """Load all habits"""
        # Clear
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        habits = self.habit_service.get_all_habits()
        
        if not habits:
            empty = QLabel("No habits yet. Click '+ New Habit' to create one!")
            empty.setFont(QFont("SF Pro Text", 14))
            empty.setStyleSheet("color: #868E96;")
            self.content_layout.addWidget(empty)
        else:
            for habit in habits:
                habit_label = QLabel(f"• {habit.name}")
                habit_label.setFont(QFont("SF Pro Text", 14))
                habit_label.setStyleSheet("color: #212529;")
                self.content_layout.addWidget(habit_label)
