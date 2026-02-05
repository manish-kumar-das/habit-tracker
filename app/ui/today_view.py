"""
Today's habits view - main content area
Dark mode optimized design
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, 
    QLabel, QPushButton, QScrollArea, QFrame, QMessageBox
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtGui import QFont
from app.services.habit_service import get_habit_service
from app.services.streak_service import get_streak_service


class HabitItem(QFrame):
    """Single habit item widget with dark mode design"""
    
    def __init__(self, habit, parent=None):
        super().__init__(parent)
        self.habit = habit
        self.parent_view = parent
        self.habit_service = get_habit_service()
        self.streak_service = get_streak_service()
        self.setMouseTracking(True)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the habit item UI"""
        self.setFrameShape(QFrame.NoFrame)
        self.setStyleSheet("""
            HabitItem {
                background-color: #1C1F26;
                border: 1px solid #2A2D35;
                border-radius: 12px;
                padding: 0px;
            }
            HabitItem:hover {
                background-color: #20232B;
                border: 1px solid #4FD1C5;
            }
        """)
        self.setMinimumHeight(80)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(16)
        
        # Checkbox
        self.checkbox = QCheckBox()
        self.checkbox.setFixedSize(28, 28)
        self.checkbox.setCursor(Qt.PointingHandCursor)
        self.checkbox.setStyleSheet("""
            QCheckBox {
                spacing: 0px;
            }
            QCheckBox::indicator {
                width: 28px;
                height: 28px;
                border-radius: 6px;
                border: 2px solid #4A4D56;
                background-color: #20232B;
            }
            QCheckBox::indicator:hover {
                border: 2px solid #4FD1C5;
                background-color: #2A2D35;
            }
            QCheckBox::indicator:checked {
                background-color: #6FCF97;
                border: 2px solid #6FCF97;
                image: none;
            }
            QCheckBox::indicator:checked:hover {
                background-color: #5AB67D;
                border: 2px solid #5AB67D;
            }
        """)
        
        # Check if completed today
        is_completed = self.habit_service.is_habit_completed_today(self.habit.id)
        self.checkbox.setChecked(is_completed)
        self.checkbox.stateChanged.connect(self.on_checkbox_changed)
        
        layout.addWidget(self.checkbox)
        
        # Habit info container
        info_layout = QVBoxLayout()
        info_layout.setSpacing(6)
        
        # Habit name
        name_label = QLabel(self.habit.name)
        name_label.setFont(QFont("Inter", 15, QFont.Medium))
        name_label.setStyleSheet("""
            QLabel {
                color: #E4E6EB;
                background: transparent;
            }
        """)
        info_layout.addWidget(name_label)
        
        # Description
        if self.habit.description:
            desc_label = QLabel(self.habit.description)
            desc_label.setFont(QFont("Inter", 12))
            desc_label.setStyleSheet("""
                QLabel {
                    color: #9AA0A6;
                    background: transparent;
                }
            """)
            desc_label.setWordWrap(True)
            info_layout.addWidget(desc_label)
        
        layout.addLayout(info_layout, stretch=1)
        
        # Streak info
        streak_info = self.streak_service.get_streak_info(self.habit.id)
        current_streak = streak_info['current_streak']
        
        if current_streak > 0:
            streak_label = QLabel(f"🔥 {current_streak}")
            streak_label.setFont(QFont("Inter", 14, QFont.Bold))
            streak_label.setStyleSheet("""
                QLabel {
                    color: #FFB74D;
                    background-color: rgba(255, 183, 77, 0.15);
                    padding: 8px 16px;
                    border-radius: 20px;
                }
            """)
            streak_label.setAlignment(Qt.AlignCenter)
        else:
            streak_label = QLabel("Start")
            streak_label.setFont(QFont("Inter", 12))
            streak_label.setStyleSheet("""
                QLabel {
                    color: #9AA0A6;
                    background-color: transparent;
                    padding: 8px 16px;
                    border-radius: 20px;
                    border: 1px solid #4A4D56;
                }
            """)
            streak_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(streak_label)
        
        # Delete button
        delete_btn = QPushButton("✕")
        delete_btn.setFixedSize(36, 36)
        delete_btn.setCursor(Qt.PointingHandCursor)
        delete_btn.setFont(QFont("Inter", 14))
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #4A4D56;
                border-radius: 18px;
                color: #9AA0A6;
            }
            QPushButton:hover {
                background-color: rgba(239, 83, 80, 0.2);
                border: 1px solid #EF5350;
                color: #EF5350;
            }
            QPushButton:pressed {
                background-color: rgba(239, 83, 80, 0.3);
            }
        """)
        delete_btn.clicked.connect(self.delete_habit)
        layout.addWidget(delete_btn)
    
    def on_checkbox_changed(self, state):
        """Handle checkbox state change"""
        if state == Qt.Checked:
            success = self.habit_service.mark_habit_complete(self.habit.id)
            if success and self.parent_view:
                self.parent_view.refresh()
        else:
            self.habit_service.unmark_habit_complete(self.habit.id)
            if self.parent_view:
                self.parent_view.refresh()
    
    def delete_habit(self):
        """Delete this habit"""
        msg = QMessageBox(self)
        msg.setWindowTitle("Delete Habit")
        msg.setText(f"Delete '{self.habit.name}'?")
        msg.setInformativeText("This will remove all completion history.")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #1C1F26;
            }
            QMessageBox QLabel {
                color: #E4E6EB;
            }
            QPushButton {
                background-color: #20232B;
                color: #E4E6EB;
                border: 1px solid #4A4D56;
                border-radius: 6px;
                padding: 8px 16px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #2A2D35;
                border: 1px solid #4FD1C5;
            }
        """)
        
        if msg.exec() == QMessageBox.Yes:
            self.habit_service.hard_delete_habit(self.habit.id)
            if self.parent_view:
                self.parent_view.load_habits()


class TodayView(QWidget):
    """Today's habits view - dark mode optimized"""
    
    def __init__(self):
        super().__init__()
        self.habit_service = get_habit_service()
        self.setup_ui()
        self.load_habits()
    
    def setup_ui(self):
        """Setup the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #0F1115;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #4A4D56;
                min-height: 30px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: #4FD1C5;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Container for habit items
        self.habits_container = QWidget()
        self.habits_container.setStyleSheet("background-color: transparent;")
        self.habits_layout = QVBoxLayout(self.habits_container)
        self.habits_layout.setSpacing(12)
        self.habits_layout.setContentsMargins(0, 0, 0, 0)
        self.habits_layout.addStretch()
        
        scroll.setWidget(self.habits_container)
        layout.addWidget(scroll)
    
    def load_habits(self):
        """Load and display all habits"""
        # Clear existing items
        while self.habits_layout.count() > 1:
            item = self.habits_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Get all habits
        habits = self.habit_service.get_all_habits()
        
        if not habits:
            # Empty state
            empty_widget = QWidget()
            empty_layout = QVBoxLayout(empty_widget)
            empty_layout.setAlignment(Qt.AlignCenter)
            
            emoji_label = QLabel("📝")
            emoji_label.setFont(QFont("Inter", 48))
            emoji_label.setAlignment(Qt.AlignCenter)
            emoji_label.setStyleSheet("color: #4A4D56; background: transparent;")
            empty_layout.addWidget(emoji_label)
            
            text_label = QLabel("No habits yet")
            text_label.setFont(QFont("Inter", 18, QFont.Medium))
            text_label.setAlignment(Qt.AlignCenter)
            text_label.setStyleSheet("color: #9AA0A6; background: transparent; margin-top: 16px;")
            empty_layout.addWidget(text_label)
            
            subtext = QLabel("Click 'Add New Habit' to get started")
            subtext.setFont(QFont("Inter", 13))
            subtext.setAlignment(Qt.AlignCenter)
            subtext.setStyleSheet("color: #6B6E76; background: transparent; margin-top: 8px;")
            empty_layout.addWidget(subtext)
            
            self.habits_layout.insertWidget(0, empty_widget)
        else:
            # Add habit items
            for habit in habits:
                habit_item = HabitItem(habit, self)
                self.habits_layout.insertWidget(self.habits_layout.count() - 1, habit_item)
    
    def refresh(self):
        """Refresh the view"""
        self.load_habits()
