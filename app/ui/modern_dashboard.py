"""
Exact HabitHub Dashboard Replica
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QScrollArea, QGridLayout
)
from PySide6.QtCore import Qt, QSize, QRect
from PySide6.QtGui import QFont, QCursor, QPainter, QColor, QPen, QLinearGradient
from datetime import datetime, timedelta
from app.services.habit_service import get_habit_service
from app.services.streak_service import get_streak_service


class CircularProgress(QWidget):
    """Exact circular progress from the design"""
    
    def __init__(self, percentage=0, parent=None):
        super().__init__(parent)
        self.percentage = percentage
        self.setFixedSize(240, 240)
    
    def set_percentage(self, percentage):
        self.percentage = percentage
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        center_x = self.width() // 2
        center_y = self.height() // 2
        radius = 85
        
        # Background circle (light gray)
        painter.setPen(QPen(QColor("#E9ECEF"), 18))
        painter.drawArc(
            center_x - radius, center_y - radius,
            radius * 2, radius * 2,
            0, 360 * 16
        )
        
        # Progress arc with gradient (blue to purple)
        if self.percentage > 0:
            # Create gradient
            gradient = QLinearGradient(center_x - radius, center_y, center_x + radius, center_y)
            gradient.setColorAt(0, QColor("#4C6EF5"))  # Blue
            gradient.setColorAt(1, QColor("#9775FA"))  # Purple
            
            pen = QPen(gradient, 18)
            pen.setCapStyle(Qt.RoundCap)
            painter.setPen(pen)
            
            span_angle = int(-360 * (self.percentage / 100) * 16)
            painter.drawArc(
                center_x - radius, center_y - radius,
                radius * 2, radius * 2,
                90 * 16, span_angle
            )
        
        # Center percentage text
        painter.setPen(QColor("#212529"))
        font = QFont("SF Pro Display", 52, QFont.Bold)
        painter.setFont(font)
        
        text_rect = QRect(center_x - 80, center_y - 40, 160, 60)
        painter.drawText(text_rect, Qt.AlignCenter, f"{int(self.percentage)}%")
        
        # "PROGRESS" label
        painter.setPen(QColor("#868E96"))
        font_small = QFont("SF Pro Display", 11, QFont.Medium)
        painter.setFont(font_small)
        
        label_rect = QRect(center_x - 60, center_y + 15, 120, 20)
        painter.drawText(label_rect, Qt.AlignCenter, "PROGRESS")


class HabitCard(QFrame):
    """Individual habit card for Today's Habits section"""
    
    def __init__(self, habit, is_completed, parent=None):
        super().__init__(parent)
        self.habit = habit
        self.is_completed = is_completed
        self.parent_view = parent
        self.setup_ui()
    
    def setup_ui(self):
        self.setFrameShape(QFrame.NoFrame)
        self.setFixedHeight(72)
        self.setStyleSheet("""
            HabitCard {
                background-color: transparent;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 8, 0, 8)
        layout.setSpacing(12)
        
        # Checkbox/Icon with category emoji
        icon_frame = QFrame()
        icon_frame.setFixedSize(48, 48)
        
        if self.is_completed:
            icon_frame.setStyleSheet("""
                QFrame {
                    background-color: #51CF66;
                    border-radius: 12px;
                }
            """)
        else:
            icon_frame.setStyleSheet("""
                QFrame {
                    background-color: #FFFFFF;
                    border: 2px solid #E9ECEF;
                    border-radius: 12px;
                }
            """)
        
        icon_layout = QVBoxLayout(icon_frame)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        
        # Get category emoji or checkmark
        if self.is_completed:
            icon = "✓"
            icon_color = "#FFFFFF"
        else:
            from app.utils.constants import CATEGORIES
            icon = "📌"
            for cat_name, emoji in CATEGORIES:
                if cat_name == self.habit.category:
                    icon = emoji
                    break
            icon_color = "#495057"
        
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("SF Pro Display", 22))
        icon_label.setStyleSheet(f"color: {icon_color};")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_layout.addWidget(icon_label)
        
        layout.addWidget(icon_frame)
        
        # Habit info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)
        
        # Habit name
        name_label = QLabel(self.habit.name)
        name_label.setFont(QFont("SF Pro Display", 15, QFont.Medium))
        name_label.setStyleSheet("color: #212529;")
        info_layout.addWidget(name_label)
        
        # Subtitle (time/description)
        subtitle = self.habit.description if self.habit.description else self.habit.category
        if len(subtitle) > 35:
            subtitle = subtitle[:35] + "..."
        
        subtitle_label = QLabel(subtitle)
        subtitle_label.setFont(QFont("SF Pro Text", 13))
        subtitle_label.setStyleSheet("color: #868E96;")
        info_layout.addWidget(subtitle_label)
        
        layout.addLayout(info_layout, stretch=1)
        
        # Status/Action
        if self.is_completed:
            status_label = QLabel("Completed")
            status_label.setFont(QFont("SF Pro Text", 13, QFont.Medium))
            status_label.setStyleSheet("color: #51CF66;")
            layout.addWidget(status_label)
        else:
            mark_btn = QPushButton("Mark Done")
            mark_btn.setFont(QFont("SF Pro Text", 13, QFont.Medium))
            mark_btn.setFixedHeight(36)
            mark_btn.setCursor(Qt.PointingHandCursor)
            mark_btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: 1.5px solid #DEE2E6;
                    border-radius: 8px;
                    color: #495057;
                    padding: 0px 16px;
                }
                QPushButton:hover {
                    background-color: #F8F9FA;
                    border-color: #4C6EF5;
                    color: #4C6EF5;
                }
            """)
            mark_btn.clicked.connect(self.mark_complete)
            layout.addWidget(mark_btn)
    
    def mark_complete(self):
        """Mark habit as complete"""
        self.habit_service = get_habit_service()
        self.habit_service.mark_habit_complete(self.habit.id)
        if self.parent_view:
            self.parent_view.load_data()


class WeekDayBox(QFrame):
    """Individual day box for weekly activity"""
    
    def __init__(self, day_name, is_completed, parent=None):
        super().__init__(parent)
        self.day_name = day_name
        self.is_completed = is_completed
        self.setup_ui()
    
    def setup_ui(self):
        self.setFixedSize(70, 100)
        
        if self.is_completed:
            self.setStyleSheet("""
                QFrame {
                    background-color: #51CF66;
                    border-radius: 12px;
                }
            """)
            text_color = "#FFFFFF"
        else:
            self.setStyleSheet("""
                QFrame {
                    background-color: #F8F9FA;
                    border-radius: 12px;
                }
            """)
            text_color = "#ADB5BD"
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)
        
        day_label = QLabel(self.day_name[:3].upper())
        day_label.setFont(QFont("SF Pro Text", 12, QFont.Medium))
        day_label.setStyleSheet(f"color: {text_color};")
        day_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(day_label)


class ModernDashboard(QWidget):
    """Exact HabitHub Dashboard UI"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.habit_service = get_habit_service()
        self.streak_service = get_streak_service()
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Setup the exact UI from the image"""
        self.setStyleSheet("QWidget { background-color: #F8F9FA; }")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(32, 24, 32, 24)
        main_layout.setSpacing(24)
        
        # Header with greeting
        header_layout = QVBoxLayout()
        header_layout.setSpacing(4)
        
        # Dynamic greeting
        hour = datetime.now().hour
        if hour < 12:
            greeting = "Good morning"
        elif hour < 18:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"
        
        greeting_label = QLabel(f"{greeting}, Alex")
        greeting_label.setFont(QFont("SF Pro Display", 36, QFont.Bold))
        greeting_label.setStyleSheet("color: #212529;")
        header_layout.addWidget(greeting_label)
        
        # Date and motivational quote
        today = datetime.now()
        day_suffix = "th" if 4 <= today.day <= 20 or 24 <= today.day <= 30 else ["st", "nd", "rd"][today.day % 10 - 1] if today.day % 10 <= 3 else "th"
        date_str = today.strftime(f"%A, %B %d{day_suffix}")
        
        quote_label = QLabel(f'{date_str} • "Success is the sum of small efforts, repeated day in and day out."')
        quote_label.setFont(QFont("SF Pro Text", 14))
        quote_label.setStyleSheet("color: #868E96;")
        header_layout.addWidget(quote_label)
        
        main_layout.addLayout(header_layout)
        
        # Main content area
        content_scroll = QScrollArea()
        content_scroll.setWidgetResizable(True)
        content_scroll.setFrameShape(QFrame.NoFrame)
        content_scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: transparent;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        
        # Top row: Daily Completion + Today's Habits
        top_row = QHBoxLayout()
        top_row.setSpacing(20)
        
        # Daily Completion Card
        daily_card = QFrame()
        daily_card.setFrameShape(QFrame.NoFrame)
        daily_card.setFixedWidth(400)
        daily_card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 20px;
            }
        """)
        
        daily_layout = QVBoxLayout(daily_card)
        daily_layout.setContentsMargins(28, 28, 28, 28)
        daily_layout.setSpacing(20)
        
        daily_title = QLabel("Daily Completion")
        daily_title.setFont(QFont("SF Pro Display", 20, QFont.Bold))
        daily_title.setStyleSheet("color: #212529;")
        daily_layout.addWidget(daily_title)
        
        # Circular progress
        self.circular_progress = CircularProgress(75)
        daily_layout.addWidget(self.circular_progress, alignment=Qt.AlignCenter)
        
        # Progress text
        self.progress_text = QLabel("Almost there! 2 habits left for today.")
        self.progress_text.setFont(QFont("SF Pro Text", 14))
        self.progress_text.setStyleSheet("color: #868E96;")
        self.progress_text.setAlignment(Qt.AlignCenter)
        daily_layout.addWidget(self.progress_text)
        
        top_row.addWidget(daily_card)
        
        # Today's Habits Card
        today_card = QFrame()
        today_card.setFrameShape(QFrame.NoFrame)
        today_card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 20px;
            }
        """)
        
        today_layout = QVBoxLayout(today_card)
        today_layout.setContentsMargins(28, 28, 28, 28)
        today_layout.setSpacing(16)
        
        # Header
        today_header = QHBoxLayout()
        
        today_title = QLabel("Today's Habits")
        today_title.setFont(QFont("SF Pro Display", 20, QFont.Bold))
        today_title.setStyleSheet("color: #212529;")
        today_header.addWidget(today_title)
        
        today_header.addStretch()
        
        view_all = QPushButton("View All")
        view_all.setFont(QFont("SF Pro Text", 14))
        view_all.setCursor(Qt.PointingHandCursor)
        view_all.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #4C6EF5;
            }
            QPushButton:hover {
                color: #3B5BDB;
            }
        """)
        today_header.addWidget(view_all)
        
        today_layout.addLayout(today_header)
        
        # Habits list
        self.habits_list_layout = QVBoxLayout()
        self.habits_list_layout.setSpacing(0)
        today_layout.addLayout(self.habits_list_layout)
        
        today_layout.addStretch()
        
        top_row.addWidget(today_card, stretch=1)
        
        content_layout.addLayout(top_row)
        
        # Bottom row: Weekly Activity + Monthly Milestone
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(20)
        
        # Weekly Activity Card
        weekly_card = QFrame()
        weekly_card.setFrameShape(QFrame.NoFrame)
        weekly_card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 20px;
            }
        """)
        
        weekly_layout = QVBoxLayout(weekly_card)
        weekly_layout.setContentsMargins(28, 28, 28, 28)
        weekly_layout.setSpacing(16)
        
        # Header
        weekly_header = QHBoxLayout()
        
        weekly_title = QLabel("Weekly Activity")
        weekly_title.setFont(QFont("SF Pro Display", 20, QFont.Bold))
        weekly_title.setStyleSheet("color: #212529;")
        weekly_header.addWidget(weekly_title)
        
        weekly_header.addStretch()
        
        weekly_dropdown = QLabel("Last 7 Days  ▼")
        weekly_dropdown.setFont(QFont("SF Pro Text", 13))
        weekly_dropdown.setStyleSheet("color: #868E96;")
        weekly_header.addWidget(weekly_dropdown)
        
        weekly_layout.addLayout(weekly_header)
        
        weekly_subtitle = QLabel("Consistent completion since Monday")
        weekly_subtitle.setFont(QFont("SF Pro Text", 14))
        weekly_subtitle.setStyleSheet("color: #868E96;")
        weekly_layout.addWidget(weekly_subtitle)
        
        # Week days grid
        self.week_grid = QHBoxLayout()
        self.week_grid.setSpacing(12)
        weekly_layout.addLayout(self.week_grid)
        
        weekly_layout.addStretch()
        
        bottom_row.addWidget(weekly_card, stretch=2)
        
        # Monthly Milestone Card
        milestone_card = QFrame()
        milestone_card.setFrameShape(QFrame.NoFrame)
        milestone_card.setFixedWidth(400)
        milestone_card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 20px;
            }
        """)
        
        milestone_layout = QVBoxLayout(milestone_card)
        milestone_layout.setContentsMargins(28, 28, 28, 32)
        milestone_layout.setSpacing(20)
        
        milestone_title = QLabel("Monthly Milestone")
        milestone_title.setFont(QFont("SF Pro Display", 20, QFont.Bold))
        milestone_title.setStyleSheet("color: #212529;")
        milestone_layout.addWidget(milestone_title)
        
        # Flame icon in circle
        flame_container = QFrame()
        flame_container.setFixedSize(120, 120)
        flame_container.setStyleSheet("""
            QFrame {
                background-color: #FFF4E6;
                border-radius: 60px;
            }
        """)
        
        flame_layout = QVBoxLayout(flame_container)
        flame_layout.setContentsMargins(0, 0, 0, 0)
        
        flame_label = QLabel("🔥")
        flame_label.setFont(QFont("SF Pro Display", 56))
        flame_label.setAlignment(Qt.AlignCenter)
        flame_layout.addWidget(flame_label)
        
        milestone_layout.addWidget(flame_container, alignment=Qt.AlignCenter)
        
        # Streak count
        self.streak_label = QLabel("24 Day Streak!")
        self.streak_label.setFont(QFont("SF Pro Display", 32, QFont.Bold))
        self.streak_label.setStyleSheet("color: #212529;")
        self.streak_label.setAlignment(Qt.AlignCenter)
        milestone_layout.addWidget(self.streak_label)
        
        # Motivational text
        milestone_text = QLabel("You're in the top 5% of users this\nmonth. Keep pushing!")
        milestone_text.setFont(QFont("SF Pro Text", 14))
        milestone_text.setStyleSheet("color: #868E96;")
        milestone_text.setAlignment(Qt.AlignCenter)
        milestone_layout.addWidget(milestone_text)
        
        # Target section
        target_header = QHBoxLayout()
        
        target_label = QLabel("TARGET")
        target_label.setFont(QFont("SF Pro Text", 11, QFont.Bold))
        target_label.setStyleSheet("color: #ADB5BD;")
        target_header.addWidget(target_label)
        
        target_header.addStretch()
        
        days_left_badge = QLabel("8 Left")
        days_left_badge.setFont(QFont("SF Pro Text", 12, QFont.Bold))
        days_left_badge.setStyleSheet("""
            QLabel {
                background-color: #FFE8CC;
                color: #FD7E14;
                padding: 6px 14px;
                border-radius: 10px;
            }
        """)
        target_header.addWidget(days_left_badge)
        
        milestone_layout.addLayout(target_header)
        
        target_value = QLabel("30 Days Streak")
        target_value.setFont(QFont("SF Pro Display", 18, QFont.Bold))
        target_value.setStyleSheet("color: #212529;")
        milestone_layout.addWidget(target_value)
        
        bottom_row.addWidget(milestone_card)
        
        content_layout.addLayout(bottom_row)
        
        content_scroll.setWidget(content_widget)
        main_layout.addWidget(content_scroll)
    
    def load_data(self):
        """Load dashboard data"""
        # Clear habits list
        while self.habits_list_layout.count():
            item = self.habits_list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Get habits
        habits = self.habit_service.get_all_habits()
        
        if not habits:
            return
        
        # Calculate completion percentage
        completed = sum(1 for h in habits if self.habit_service.is_habit_completed_today(h.id))
        total = len(habits)
        percentage = int((completed / total) * 100) if total > 0 else 0
        
        self.circular_progress.set_percentage(percentage)
        
        left = total - completed
        if left == 0:
            self.progress_text.setText("Perfect! All habits completed today! 🎉")
        elif left == 1:
            self.progress_text.setText("Almost there! 1 habit left for today.")
        else:
            self.progress_text.setText(f"Almost there! {left} habits left for today.")
        
        # Load habits (max 4)
        for habit in habits[:4]:
            is_completed = self.habit_service.is_habit_completed_today(habit.id)
            card = HabitCard(habit, is_completed, self)
            self.habits_list_layout.addWidget(card)
        
        # Load weekly activity
        while self.week_grid.count():
            item = self.week_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
        today = datetime.now()
        
        for i in range(7):
            date = today - timedelta(days=6-i)
            # For demo, mark some as completed
            is_completed = (i % 3 != 0)  # Simple pattern for demo
            
            day_box = WeekDayBox(days[i], is_completed)
            self.week_grid.addWidget(day_box)
        
        # Get max streak
        max_streak = 0
        for habit in habits:
            streak_info = self.streak_service.get_streak_info(habit.id)
            max_streak = max(max_streak, streak_info['current_streak'])
        
        self.streak_label.setText(f"{max_streak} Day Streak!")
