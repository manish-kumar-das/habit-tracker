"""
Statistics view - Dashboard with insights
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QWidget, QScrollArea, QFrame, QPushButton
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from app.services.stats_service import get_stats_service
from app.services.habit_service import get_habit_service


class StatCard(QFrame):
    """Single statistic card"""
    
    def __init__(self, title, value, subtitle="", icon="", parent=None):
        super().__init__(parent)
        self.setup_ui(title, value, subtitle, icon)
    
    def setup_ui(self, title, value, subtitle, icon):
        """Setup the card UI"""
        self.setFrameShape(QFrame.NoFrame)
        self.setStyleSheet("""
            StatCard {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1C1F26, stop:1 #20232B);
                border: 1px solid #2A2D35;
                border-radius: 16px;
                padding: 0px;
            }
            StatCard:hover {
                border: 1px solid #4FD1C5;
            }
        """)
        self.setMinimumHeight(140)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(8)
        
        # Icon and title row
        header_layout = QHBoxLayout()
        
        if icon:
            icon_label = QLabel(icon)
            icon_label.setFont(QFont("Inter", 28))
            icon_label.setStyleSheet("background: transparent;")
            header_layout.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Inter", 13))
        title_label.setStyleSheet("color: #9AA0A6; background: transparent;")
        header_layout.addWidget(title_label, stretch=1)
        
        layout.addLayout(header_layout)
        
        # Value
        value_label = QLabel(str(value))
        value_label.setFont(QFont("Inter", 36, QFont.Bold))
        value_label.setStyleSheet("color: #4FD1C5; background: transparent;")
        layout.addWidget(value_label)
        
        # Subtitle
        if subtitle:
            subtitle_label = QLabel(subtitle)
            subtitle_label.setFont(QFont("Inter", 12))
            subtitle_label.setStyleSheet("color: #6B6E76; background: transparent;")
            layout.addWidget(subtitle_label)


class HabitStatRow(QFrame):
    """Single habit statistics row"""
    
    def __init__(self, habit_stats, parent=None):
        super().__init__(parent)
        self.stats = habit_stats
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the row UI"""
        self.setFrameShape(QFrame.NoFrame)
        self.setStyleSheet("""
            HabitStatRow {
                background-color: #1C1F26;
                border: 1px solid #2A2D35;
                border-radius: 10px;
            }
            HabitStatRow:hover {
                background-color: #20232B;
                border: 1px solid #4FD1C5;
            }
        """)
        self.setMinimumHeight(70)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 12, 20, 12)
        layout.setSpacing(16)
        
        # Habit name
        name_layout = QVBoxLayout()
        name_layout.setSpacing(4)
        
        name_label = QLabel(self.stats['habit_name'])
        name_label.setFont(QFont("Inter", 14, QFont.Medium))
        name_label.setStyleSheet("color: #E4E6EB; background: transparent;")
        name_layout.addWidget(name_label)
        
        # Completion status
        status_text = "✓ Completed today" if self.stats['is_completed_today'] else "Not completed today"
        status_color = "#6FCF97" if self.stats['is_completed_today'] else "#9AA0A6"
        
        status_label = QLabel(status_text)
        status_label.setFont(QFont("Inter", 11))
        status_label.setStyleSheet(f"color: {status_color}; background: transparent;")
        name_layout.addWidget(status_label)
        
        layout.addLayout(name_layout, stretch=1)
        
        # Current streak
        streak_widget = QWidget()
        streak_layout = QVBoxLayout(streak_widget)
        streak_layout.setSpacing(2)
        streak_layout.setContentsMargins(0, 0, 0, 0)
        
        streak_value = QLabel(str(self.stats['current_streak']))
        streak_value.setFont(QFont("Inter", 18, QFont.Bold))
        streak_value.setStyleSheet("color: #FFB74D; background: transparent;")
        streak_value.setAlignment(Qt.AlignCenter)
        streak_layout.addWidget(streak_value)
        
        streak_label = QLabel("day streak")
        streak_label.setFont(QFont("Inter", 10))
        streak_label.setStyleSheet("color: #9AA0A6; background: transparent;")
        streak_label.setAlignment(Qt.AlignCenter)
        streak_layout.addWidget(streak_label)
        
        layout.addWidget(streak_widget)
        
        # 7-day rate
        rate_widget = QWidget()
        rate_layout = QVBoxLayout(rate_widget)
        rate_layout.setSpacing(2)
        rate_layout.setContentsMargins(0, 0, 0, 0)
        
        rate_value = QLabel(f"{self.stats['completion_rate_7d']}%")
        rate_value.setFont(QFont("Inter", 18, QFont.Bold))
        rate_value.setStyleSheet("color: #7C83FD; background: transparent;")
        rate_value.setAlignment(Qt.AlignCenter)
        rate_layout.addWidget(rate_value)
        
        rate_label = QLabel("7-day rate")
        rate_label.setFont(QFont("Inter", 10))
        rate_label.setStyleSheet("color: #9AA0A6; background: transparent;")
        rate_label.setAlignment(Qt.AlignCenter)
        rate_layout.addWidget(rate_label)
        
        layout.addWidget(rate_widget)
        
        # Total completions
        total_widget = QWidget()
        total_layout = QVBoxLayout(total_widget)
        total_layout.setSpacing(2)
        total_layout.setContentsMargins(0, 0, 0, 0)
        
        total_value = QLabel(str(self.stats['total_completions']))
        total_value.setFont(QFont("Inter", 18, QFont.Bold))
        total_value.setStyleSheet("color: #4FD1C5; background: transparent;")
        total_value.setAlignment(Qt.AlignCenter)
        total_layout.addWidget(total_value)
        
        total_label = QLabel("total")
        total_label.setFont(QFont("Inter", 10))
        total_label.setStyleSheet("color: #9AA0A6; background: transparent;")
        total_label.setAlignment(Qt.AlignCenter)
        total_layout.addWidget(total_label)
        
        layout.addWidget(total_widget)


class StatsView(QDialog):
    """Statistics view dialog"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.stats_service = get_stats_service()
        self.habit_service = get_habit_service()
        self.setup_ui()
        self.load_stats()
    
    def setup_ui(self):
        """Setup the UI"""
        self.setWindowTitle("Statistics")
        self.setModal(False)
        self.setMinimumSize(900, 700)
        self.setStyleSheet("""
            QDialog {
                background-color: #0F1115;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(24)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("📊 Statistics Dashboard")
        title.setFont(QFont("Inter", 28, QFont.Bold))
        title.setStyleSheet("color: #E4E6EB; background: transparent;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(36, 36)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setFont(QFont("Inter", 16))
        close_btn.setStyleSheet("""
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
        """)
        close_btn.clicked.connect(self.close)
        header_layout.addWidget(close_btn)
        
        layout.addLayout(header_layout)
        
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
        """)
        
        # Content widget
        content = QWidget()
        content.setStyleSheet("background-color: transparent;")
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setSpacing(24)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll.setWidget(content)
        layout.addWidget(scroll)
    
    def load_stats(self):
        """Load and display statistics"""
        # Clear existing content
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Get all habits stats
        all_stats = self.stats_service.get_all_habits_stats()
        
        if not all_stats:
            # Empty state
            empty_label = QLabel("No habits to show statistics for.\n\nAdd some habits to see your progress!")
            empty_label.setFont(QFont("Inter", 16))
            empty_label.setAlignment(Qt.AlignCenter)
            empty_label.setStyleSheet("color: #9AA0A6; background: transparent; padding: 80px;")
            self.content_layout.addWidget(empty_label)
            return
        
        # Summary cards
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(16)
        
        # Total habits
        total_habits = len(all_stats)
        total_card = StatCard("Total Habits", total_habits, "Active habits", "📝")
        cards_layout.addWidget(total_card)
        
        # Completed today
        completed_today = sum(1 for s in all_stats if s['is_completed_today'])
        today_card = StatCard("Today", completed_today, f"of {total_habits} completed", "✓")
        cards_layout.addWidget(today_card)
        
        # Best streak
        best_streak = max((s['current_streak'] for s in all_stats), default=0)
        streak_card = StatCard("Best Streak", best_streak, "days in a row", "��")
        cards_layout.addWidget(streak_card)
        
        # Total completions
        total_completions = sum(s['total_completions'] for s in all_stats)
        total_card = StatCard("Total", total_completions, "completions all time", "🎯")
        cards_layout.addWidget(total_card)
        
        self.content_layout.addLayout(cards_layout)
        
        # Section title
        habits_title = QLabel("Habit Details")
        habits_title.setFont(QFont("Inter", 20, QFont.Bold))
        habits_title.setStyleSheet("color: #E4E6EB; background: transparent; margin-top: 16px;")
        self.content_layout.addWidget(habits_title)
        
        # Individual habit stats
        for stat in all_stats:
            habit_row = HabitStatRow(stat)
            self.content_layout.addWidget(habit_row)
        
        self.content_layout.addStretch()
