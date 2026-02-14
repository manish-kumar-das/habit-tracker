"""
Modern Dashboard View - Inspired by HabitHub design
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QScrollArea, QProgressBar
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QCursor, QPainter, QColor, QPen
from datetime import datetime, timedelta
from app.services.habit_service import get_habit_service
from app.services.streak_service import get_streak_service
from app.services.stats_service import get_stats_service


class CircularProgress(QWidget):
    """Circular progress indicator"""
    
    def __init__(self, percentage=0, parent=None):
        super().__init__(parent)
        self.percentage = percentage
        self.setMinimumSize(200, 200)
    
    def set_percentage(self, percentage):
        """Update percentage"""
        self.percentage = percentage
        self.update()
    
    def paintEvent(self, event):
        """Draw circular progress"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Center and radius
        center_x = self.width() // 2
        center_y = self.height() // 2
        radius = min(center_x, center_y) - 20
        
        # Background circle
        painter.setPen(QPen(QColor("#E5E7EB"), 15))
        painter.drawArc(
            center_x - radius, center_y - radius,
            radius * 2, radius * 2,
            90 * 16, -360 * 16
        )
        
        # Progress arc (gradient colors)
        if self.percentage > 0:
            # Blue to purple gradient
            pen = QPen(QColor("#6366F1"), 15)
            pen.setCapStyle(Qt.RoundCap)
            painter.setPen(pen)
            
            span_angle = int(-360 * (self.percentage / 100) * 16)
            painter.drawArc(
                center_x - radius, center_y - radius,
                radius * 2, radius * 2,
                90 * 16, span_angle
            )
        
        # Center text
        painter.setPen(QColor("#111827"))
        font = QFont("Inter", 48, QFont.Bold)
        painter.setFont(font)
        painter.drawText(
            self.rect(),
            Qt.AlignCenter,
            f"{int(self.percentage)}%"
        )
        
        # "PROGRESS" text
        font_small = QFont("Inter", 10, QFont.Medium)
        painter.setFont(font_small)
        painter.setPen(QColor("#9CA3AF"))
        painter.drawText(
            center_x - 40, center_y + 30,
            "PROGRESS"
        )


class TodayHabitCard(QFrame):
    """Single habit card for today's list"""
    
    def __init__(self, habit, is_completed, parent=None):
        super().__init__(parent)
        self.habit = habit
        self.is_completed = is_completed
        self.parent_view = parent
        self.setup_ui()
    
    def setup_ui(self):
        """Setup habit card"""
        self.setFrameShape(QFrame.NoFrame)
        self.setStyleSheet("""
            TodayHabitCard {
                background-color: #FFFFFF;
                border-radius: 12px;
            }
            TodayHabitCard:hover {
                background-color: #F9FAFB;
            }
        """)
        self.setFixedHeight(70)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)
        
        # Checkbox/Icon
        from app.utils.constants import CATEGORIES
        icon_emoji = "✅"
        for cat_name, emoji in CATEGORIES:
            if cat_name == self.habit.category:
                icon_emoji = emoji
                break
        
        icon_label = QLabel(icon_emoji)
        icon_label.setFont(QFont("Inter", 20))
        icon_label.setFixedSize(40, 40)
        icon_label.setAlignment(Qt.AlignCenter)
        
        if self.is_completed:
            icon_label.setStyleSheet("""
                QLabel {
                    background-color: #10B981;
                    border-radius: 10px;
                }
            """)
        else:
            icon_label.setStyleSheet("""
                QLabel {
                    background-color: #F3F4F6;
                    border: 2px solid #E5E7EB;
                    border-radius: 10px;
                }
            """)
        
        layout.addWidget(icon_label)
        
        # Info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)
        
        name_label = QLabel(self.habit.name)
        name_label.setFont(QFont("Inter", 14, QFont.Medium))
        name_label.setStyleSheet("color: #111827;")
        info_layout.addWidget(name_label)
        
        # Subtitle (description or category)
        subtitle = self.habit.description if self.habit.description else self.habit.category
        if len(subtitle) > 40:
            subtitle = subtitle[:40] + "..."
        
        subtitle_label = QLabel(subtitle)
        subtitle_label.setFont(QFont("Inter", 11))
        subtitle_label.setStyleSheet("color: #6B7280;")
        info_layout.addWidget(subtitle_label)
        
        layout.addLayout(info_layout, stretch=1)
        
        # Status
        if self.is_completed:
            status_label = QLabel("Completed")
            status_label.setFont(QFont("Inter", 12, QFont.Medium))
            status_label.setStyleSheet("color: #10B981;")
        else:
            status_label = QPushButton("Mark Done")
            status_label.setFont(QFont("Inter", 11, QFont.Medium))
            status_label.setFixedHeight(32)
            status_label.setCursor(Qt.PointingHandCursor)
            status_label.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: 1px solid #E5E7EB;
                    border-radius: 8px;
                    color: #6B7280;
                    padding: 6px 16px;
                }
                QPushButton:hover {
                    background-color: #F3F4F6;
                    border: 1px solid #6366F1;
                    color: #6366F1;
                }
            """)
            status_label.clicked.connect(self.mark_complete)
        
        layout.addWidget(status_label)
    
    def mark_complete(self):
        """Mark habit as complete"""
        from app.services.habit_service import get_habit_service
        habit_service = get_habit_service()
        habit_service.mark_habit_complete(self.habit.id)
        
        if self.parent_view:
            self.parent_view.load_dashboard()


class DashboardView(QWidget):
    """Modern dashboard view"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.habit_service = get_habit_service()
        self.streak_service = get_streak_service()
        self.stats_service = get_stats_service()
        self.setup_ui()
        self.load_dashboard()
    
    def setup_ui(self):
        """Setup dashboard UI"""
        self.setStyleSheet("QWidget { background-color: #F9FAFB; }")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(32, 24, 32, 24)
        main_layout.setSpacing(24)
        
        # Header
        header_layout = QVBoxLayout()
        header_layout.setSpacing(4)
        
        # Greeting
        hour = datetime.now().hour
        if hour < 12:
            greeting = "Good morning"
        elif hour < 18:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"
        
        greeting_label = QLabel(f"{greeting}, User")
        greeting_label.setFont(QFont("Inter", 32, QFont.Bold))
        greeting_label.setStyleSheet("color: #111827;")
        header_layout.addWidget(greeting_label)
        
        # Date and quote
        date_str = datetime.now().strftime("%A, %B %dth")
        quote = "Success is the sum of small efforts, repeated day in and day out."
        
        date_quote = QLabel(f'{date_str} • "{quote}"')
        date_quote.setFont(QFont("Inter", 13))
        date_quote.setStyleSheet("color: #6B7280;")
        header_layout.addWidget(date_quote)
        
        main_layout.addLayout(header_layout)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        content = QWidget()
        content.setStyleSheet("background-color: transparent;")
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(20)
        
        # Top row: Daily Completion + Today's Habits
        top_row = QHBoxLayout()
        top_row.setSpacing(20)
        
        # Daily Completion Card
        daily_card = QFrame()
        daily_card.setFrameShape(QFrame.NoFrame)
        daily_card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 16px;
            }
        """)
        daily_card.setFixedWidth(380)
        
        daily_layout = QVBoxLayout(daily_card)
        daily_layout.setContentsMargins(24, 24, 24, 24)
        daily_layout.setSpacing(16)
        
        daily_title = QLabel("Daily Completion")
        daily_title.setFont(QFont("Inter", 18, QFont.Bold))
        daily_title.setStyleSheet("color: #111827;")
        daily_layout.addWidget(daily_title)
        
        # Circular progress
        self.circular_progress = CircularProgress(0)
        daily_layout.addWidget(self.circular_progress, alignment=Qt.AlignCenter)
        
        self.progress_text = QLabel("Almost there! 2 habits left for today.")
        self.progress_text.setFont(QFont("Inter", 12))
        self.progress_text.setStyleSheet("color: #6B7280;")
        self.progress_text.setAlignment(Qt.AlignCenter)
        daily_layout.addWidget(self.progress_text)
        
        top_row.addWidget(daily_card)
        
        # Today's Habits Card
        today_card = QFrame()
        today_card.setFrameShape(QFrame.NoFrame)
        today_card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 16px;
            }
        """)
        
        today_layout = QVBoxLayout(today_card)
        today_layout.setContentsMargins(24, 24, 24, 24)
        today_layout.setSpacing(16)
        
        # Header
        today_header = QHBoxLayout()
        
        today_title = QLabel("Today's Habits")
        today_title.setFont(QFont("Inter", 18, QFont.Bold))
        today_title.setStyleSheet("color: #111827;")
        today_header.addWidget(today_title)
        
        today_header.addStretch()
        
        view_all_btn = QPushButton("View All")
        view_all_btn.setFont(QFont("Inter", 12, QFont.Medium))
        view_all_btn.setCursor(Qt.PointingHandCursor)
        view_all_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #6366F1;
            }
            QPushButton:hover {
                color: #4F46E5;
                text-decoration: underline;
            }
        """)
        today_header.addWidget(view_all_btn)
        
        today_layout.addLayout(today_header)
        
        # Habits list
        self.today_habits_layout = QVBoxLayout()
        self.today_habits_layout.setSpacing(8)
        today_layout.addLayout(self.today_habits_layout)
        
        today_layout.addStretch()
        
        top_row.addWidget(today_card, stretch=1)
        
        content_layout.addLayout(top_row)
        
        # Bottom row: Weekly Activity + Monthly Milestone
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(20)
        
        # Weekly Activity (placeholder)
        weekly_card = QFrame()
        weekly_card.setFrameShape(QFrame.NoFrame)
        weekly_card.setStyleSheet("QFrame { background-color: #FFFFFF; border-radius: 16px; }")
        weekly_card.setMinimumHeight(250)
        
        weekly_layout = QVBoxLayout(weekly_card)
        weekly_layout.setContentsMargins(24, 24, 24, 24)
        
        weekly_title = QLabel("Weekly Activity")
        weekly_title.setFont(QFont("Inter", 18, QFont.Bold))
        weekly_title.setStyleSheet("color: #111827;")
        weekly_layout.addWidget(weekly_title)
        
        weekly_subtitle = QLabel("Consistent completion since Monday")
        weekly_subtitle.setFont(QFont("Inter", 12))
        weekly_subtitle.setStyleSheet("color: #6B7280;")
        weekly_layout.addWidget(weekly_subtitle)
        
        weekly_layout.addStretch()
        
        bottom_row.addWidget(weekly_card, stretch=2)
        
        # Monthly Milestone
        milestone_card = QFrame()
        milestone_card.setFrameShape(QFrame.NoFrame)
        milestone_card.setStyleSheet("QFrame { background-color: #FFFFFF; border-radius: 16px; }")
        milestone_card.setFixedWidth(380)
        
        milestone_layout = QVBoxLayout(milestone_card)
        milestone_layout.setContentsMargins(24, 24, 24, 24)
        milestone_layout.setSpacing(16)
        
        milestone_title = QLabel("Monthly Milestone")
        milestone_title.setFont(QFont("Inter", 18, QFont.Bold))
        milestone_title.setStyleSheet("color: #111827;")
        milestone_layout.addWidget(milestone_title)
        
        # Flame icon
        flame_label = QLabel("🔥")
        flame_label.setFont(QFont("Inter", 64))
        flame_label.setAlignment(Qt.AlignCenter)
        milestone_layout.addWidget(flame_label)
        
        # Streak
        self.streak_label = QLabel("24 Day Streak!")
        self.streak_label.setFont(QFont("Inter", 28, QFont.Bold))
        self.streak_label.setStyleSheet("color: #111827;")
        self.streak_label.setAlignment(Qt.AlignCenter)
        milestone_layout.addWidget(self.streak_label)
        
        milestone_subtitle = QLabel("You're in the top 5% of users this\nmonth. Keep pushing!")
        milestone_subtitle.setFont(QFont("Inter", 12))
        milestone_subtitle.setStyleSheet("color: #6B7280;")
        milestone_subtitle.setAlignment(Qt.AlignCenter)
        milestone_layout.addWidget(milestone_subtitle)
        
        # Target
        target_layout = QHBoxLayout()
        
        target_label = QLabel("TARGET")
        target_label.setFont(QFont("Inter", 10, QFont.Bold))
        target_label.setStyleSheet("color: #9CA3AF;")
        target_layout.addWidget(target_label)
        
        target_layout.addStretch()
        
        days_left = QLabel("8 Left")
        days_left.setFont(QFont("Inter", 11, QFont.Bold))
        days_left.setStyleSheet("""
            QLabel {
                background-color: #FEF3C7;
                color: #D97706;
                padding: 4px 12px;
                border-radius: 8px;
            }
        """)
        target_layout.addWidget(days_left)
        
        milestone_layout.addLayout(target_layout)
        
        target_value = QLabel("30 Days Streak")
        target_value.setFont(QFont("Inter", 16, QFont.Bold))
        target_value.setStyleSheet("color: #111827;")
        milestone_layout.addWidget(target_value)
        
        bottom_row.addWidget(milestone_card)
        
        content_layout.addLayout(bottom_row)
        
        scroll.setWidget(content)
        main_layout.addWidget(scroll)
    
    def load_dashboard(self):
        """Load dashboard data"""
        # Clear today's habits
        while self.today_habits_layout.count():
            item = self.today_habits_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Get all habits
        habits = self.habit_service.get_all_habits()
        
        if not habits:
            return
        
        # Calculate completion percentage
        completed_count = sum(1 for h in habits if self.habit_service.is_habit_completed_today(h.id))
        total_count = len(habits)
        percentage = int((completed_count / total_count) * 100) if total_count > 0 else 0
        
        self.circular_progress.set_percentage(percentage)
        
        left = total_count - completed_count
        if left == 0:
            self.progress_text.setText("Perfect! All habits completed today! 🎉")
        else:
            self.progress_text.setText(f"Almost there! {left} habit{'s' if left != 1 else ''} left for today.")
        
        # Load today's habits (max 4)
        for i, habit in enumerate(habits[:4]):
            is_completed = self.habit_service.is_habit_completed_today(habit.id)
            card = TodayHabitCard(habit, is_completed, self)
            self.today_habits_layout.addWidget(card)
        
        # Get max streak
        max_streak = 0
        for habit in habits:
            streak_info = self.streak_service.get_streak_info(habit.id)
            max_streak = max(max_streak, streak_info['current_streak'])
        
        self.streak_label.setText(f"{max_streak} Day Streak!")
