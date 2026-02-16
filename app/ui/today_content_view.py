"""
Today Content View - Shows today's habits with proper header
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QScrollArea, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QCursor
from datetime import datetime
from app.services.habit_service import get_habit_service
from app.ui.complete_habithub_ui import HabitCard


class TodayContentView(QWidget):
    """Today's habits view for content area"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.habit_service = get_habit_service()
        self.setup_ui()
        self.load_habits()
    
    def setup_ui(self):
        """Setup today view UI"""
        self.setStyleSheet("background-color: #F8F9FA;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = QFrame()
        header.setFixedHeight(100)
        header.setStyleSheet("QFrame { background-color: #FFFFFF; border-bottom: 1px solid #E5E7EB; }")
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(32, 20, 32, 20)
        
        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)
        
        # Dynamic greeting
        hour = datetime.now().hour
        if hour < 12:
            greeting = "Good morning"
        elif hour < 18:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"
        
        title = QLabel(f"📅 Today's Habits")
        title.setFont(QFont("SF Pro Display", 24, QFont.Bold))
        title.setStyleSheet("color: #111827; background: transparent;")
        title_layout.addWidget(title)
        
        today = datetime.now()
        date_str = today.strftime("%A, %B %d, %Y")
        
        subtitle = QLabel(f"{greeting}! {date_str}")
        subtitle.setFont(QFont("SF Pro Text", 13))
        subtitle.setStyleSheet("color: #6B7280; background: transparent;")
        title_layout.addWidget(subtitle)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        # Progress indicator
        self.progress_label = QPushButton("0/0 Completed")
        self.progress_label.setFont(QFont("SF Pro Text", 13, QFont.Bold))
        self.progress_label.setFixedHeight(48)
        self.progress_label.setEnabled(False)
        self.progress_label.setStyleSheet("""
            QPushButton {
                padding: 12px 24px;
                border: 2px solid #10B981;
                border-radius: 10px;
                color: #10B981;
                background-color: #D1FAE5;
            }
            QPushButton:disabled {
                background-color: #D1FAE5;
                color: #10B981;
            }
        """)
        header_layout.addWidget(self.progress_label)
        
        layout.addWidget(header)
        
        # Content scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        content = QWidget()
        content.setStyleSheet("background-color: #F8F9FA;")
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setContentsMargins(32, 24, 32, 24)
        self.content_layout.setSpacing(16)
        
        scroll.setWidget(content)
        layout.addWidget(scroll)
    
    def load_habits(self):
        """Load today's habits"""
        # Clear content
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        habits = self.habit_service.get_all_habits()
        
        if not habits:
            # Empty state
            empty_frame = QFrame()
            empty_frame.setStyleSheet("""
                QFrame {
                    background-color: #FFFFFF;
                    border: 2px dashed #E5E7EB;
                    border-radius: 16px;
                }
            """)
            empty_frame.setMinimumHeight(200)
            
            empty_layout = QVBoxLayout(empty_frame)
            empty_layout.setAlignment(Qt.AlignCenter)
            
            emoji = QLabel("��")
            emoji.setFont(QFont("SF Pro Display", 64))
            emoji.setAlignment(Qt.AlignCenter)
            emoji.setStyleSheet("background: transparent;")
            empty_layout.addWidget(emoji)
            
            empty_title = QLabel("No Habits Yet")
            empty_title.setFont(QFont("SF Pro Display", 20, QFont.Bold))
            empty_title.setAlignment(Qt.AlignCenter)
            empty_title.setStyleSheet("color: #6B7280; background: transparent;")
            empty_layout.addWidget(empty_title)
            
            empty_text = QLabel("Click '+ New Habit' to create your first habit")
            empty_text.setFont(QFont("SF Pro Text", 14))
            empty_text.setAlignment(Qt.AlignCenter)
            empty_text.setStyleSheet("color: #9CA3AF; background: transparent;")
            empty_layout.addWidget(empty_text)
            
            self.content_layout.addWidget(empty_frame)
            self.content_layout.addStretch()
            
            self.progress_label.setText("0/0 Completed")
            return
        
        # Calculate progress
        completed = sum(1 for h in habits if self.habit_service.is_habit_completed_today(h.id))
        total = len(habits)
        
        self.progress_label.setText(f"{completed}/{total} Completed")
        
        # Group habits by completion status
        incomplete_habits = []
        completed_habits = []
        
        for habit in habits:
            is_completed = self.habit_service.is_habit_completed_today(habit.id)
            if is_completed:
                completed_habits.append((habit, is_completed))
            else:
                incomplete_habits.append((habit, is_completed))
        
        # Show incomplete first
        if incomplete_habits:
            pending_label = QLabel(f"⏳ Pending ({len(incomplete_habits)})")
            pending_label.setFont(QFont("SF Pro Display", 18, QFont.Bold))
            pending_label.setStyleSheet("color: #F59E0B; background: transparent;")
            self.content_layout.addWidget(pending_label)
            
            for habit, is_completed in incomplete_habits:
                card = HabitCard(habit, is_completed, self)
                self.content_layout.addWidget(card)
        
        # Show completed
        if completed_habits:
            completed_label = QLabel(f"✅ Completed ({len(completed_habits)})")
            completed_label.setFont(QFont("SF Pro Display", 18, QFont.Bold))
            completed_label.setStyleSheet("color: #10B981; background: transparent; margin-top: 16px;")
            self.content_layout.addWidget(completed_label)
            
            for habit, is_completed in completed_habits:
                card = HabitCard(habit, is_completed, self)
                self.content_layout.addWidget(card)
        
        self.content_layout.addStretch()
    
    def load_data(self):
        """Reload habits (called when marking complete)"""
        self.load_habits()
