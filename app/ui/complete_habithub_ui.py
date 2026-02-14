"""
Complete HabitHub UI with Sidebar and Navbar
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QScrollArea, QGridLayout
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QCursor, QPainter, QColor, QPen, QLinearGradient, QIcon
from datetime import datetime, timedelta
from app.services.habit_service import get_habit_service
from app.services.streak_service import get_streak_service


class Sidebar(QFrame):
    """Left sidebar navigation"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.setup_ui()
    
    def setup_ui(self):
        """Setup sidebar UI"""
        self.setFixedWidth(240)
        self.setStyleSheet("""
            QFrame {
                background-color: #F8F9FA;
                border-right: 1px solid #E9ECEF;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 24, 16, 24)
        layout.setSpacing(8)
        
        # Logo and title
        logo_layout = QHBoxLayout()
        logo_layout.setSpacing(12)
        
        # Logo icon
        logo_icon = QFrame()
        logo_icon.setFixedSize(40, 40)
        logo_icon.setStyleSheet("""
            QFrame {
                background-color: #5F3DC4;
                border-radius: 10px;
            }
        """)
        
        logo_icon_layout = QVBoxLayout(logo_icon)
        logo_icon_layout.setContentsMargins(0, 0, 0, 0)
        
        icon_label = QLabel("◉")
        icon_label.setFont(QFont("SF Pro Display", 20))
        icon_label.setStyleSheet("color: #FFFFFF;")
        icon_label.setAlignment(Qt.AlignCenter)
        logo_icon_layout.addWidget(icon_label)
        
        logo_layout.addWidget(logo_icon)
        
        # HabitHub text
        title = QLabel("HabitHub")
        title.setFont(QFont("SF Pro Display", 18, QFont.Bold))
        title.setStyleSheet("color: #212529;")
        logo_layout.addWidget(title)
        
        logo_layout.addStretch()
        
        layout.addLayout(logo_layout)
        
        layout.addSpacing(24)
        
        # Navigation buttons
        self.nav_buttons = {}
        
        nav_items = [
            ("dashboard", "Dashboard", "⊞", True),
            ("today", "Today", "📅", False),
            ("habits", "Habits", "⚡", False),
            ("analytics", "Analytics", "��", False),
            ("goals", "Goals", "🏆", False),
            ("settings", "Settings", "⚙", False),
        ]
        
        for key, text, icon, is_active in nav_items:
            btn = self.create_nav_button(text, icon, is_active)
            self.nav_buttons[key] = btn
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # User profile at bottom
        profile_frame = QFrame()
        profile_frame.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E9ECEF;
                border-radius: 12px;
                padding: 12px;
            }
        """)
        
        profile_layout = QHBoxLayout(profile_frame)
        profile_layout.setContentsMargins(12, 12, 12, 12)
        profile_layout.setSpacing(12)
        
        # Avatar
        avatar = QFrame()
        avatar.setFixedSize(40, 40)
        avatar.setStyleSheet("""
            QFrame {
                background-color: #FFE8CC;
                border-radius: 20px;
            }
        """)
        
        avatar_layout = QVBoxLayout(avatar)
        avatar_layout.setContentsMargins(0, 0, 0, 0)
        
        avatar_text = QLabel("👤")
        avatar_text.setFont(QFont("SF Pro Display", 20))
        avatar_text.setAlignment(Qt.AlignCenter)
        avatar_layout.addWidget(avatar_text)
        
        profile_layout.addWidget(avatar)
        
        # User info
        user_info = QVBoxLayout()
        user_info.setSpacing(2)
        
        user_name = QLabel("Alex Morgan")
        user_name.setFont(QFont("SF Pro Text", 13, QFont.Medium))
        user_name.setStyleSheet("color: #212529;")
        user_info.addWidget(user_name)
        
        user_type = QLabel("Premium Member")
        user_type.setFont(QFont("SF Pro Text", 11))
        user_type.setStyleSheet("color: #868E96;")
        user_info.addWidget(user_type)
        
        profile_layout.addLayout(user_info)
        
        layout.addWidget(profile_frame)
    
    def create_nav_button(self, text, icon, is_active):
        """Create navigation button"""
        btn = QPushButton(f"{icon}  {text}")
        btn.setFont(QFont("SF Pro Text", 14, QFont.Medium if is_active else QFont.Normal))
        btn.setFixedHeight(48)
        btn.setCursor(Qt.PointingHandCursor)
        
        if is_active:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #5F3DC4;
                    color: #FFFFFF;
                    border: none;
                    border-radius: 12px;
                    text-align: left;
                    padding-left: 16px;
                }
                QPushButton:hover {
                    background-color: #5028AB;
                }
            """)
        else:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #495057;
                    border: none;
                    border-radius: 12px;
                    text-align: left;
                    padding-left: 16px;
                }
                QPushButton:hover {
                    background-color: #F1F3F5;
                    color: #212529;
                }
            """)
        
        return btn


class TopNavbar(QFrame):
    """Top navigation bar"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.setup_ui()
    
    def setup_ui(self):
        """Setup navbar UI"""
        self.setFixedHeight(80)
        self.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-bottom: 1px solid #E9ECEF;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(32, 0, 32, 0)
        layout.setSpacing(16)
        
        # Greeting section
        greeting_layout = QVBoxLayout()
        greeting_layout.setSpacing(2)
        
        # Dynamic greeting
        hour = datetime.now().hour
        if hour < 12:
            greeting = "Good morning"
        elif hour < 18:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"
        
        greeting_label = QLabel(f"{greeting}, Alex")
        greeting_label.setFont(QFont("SF Pro Display", 28, QFont.Bold))
        greeting_label.setStyleSheet("color: #212529;")
        greeting_layout.addWidget(greeting_label)
        
        # Date and quote
        today = datetime.now()
        day_suffix = "th" if 4 <= today.day <= 20 or 24 <= today.day <= 30 else ["st", "nd", "rd"][today.day % 10 - 1] if today.day % 10 <= 3 else "th"
        date_str = today.strftime(f"%A, %B %d{day_suffix}")
        
        date_quote = QLabel(f'{date_str} • "Success is the sum of small efforts, repeated day in and day out."')
        date_quote.setFont(QFont("SF Pro Text", 13))
        date_quote.setStyleSheet("color: #868E96;")
        greeting_layout.addWidget(date_quote)
        
        layout.addLayout(greeting_layout)
        
        layout.addStretch()
        
        # Notification bell
        notif_btn = QPushButton("🔔")
        notif_btn.setFont(QFont("SF Pro Display", 18))
        notif_btn.setFixedSize(48, 48)
        notif_btn.setCursor(Qt.PointingHandCursor)
        notif_btn.setStyleSheet("""
            QPushButton {
                background-color: #F8F9FA;
                border: 1px solid #E9ECEF;
                border-radius: 24px;
                color: #495057;
            }
            QPushButton:hover {
                background-color: #E9ECEF;
            }
        """)
        layout.addWidget(notif_btn)
        
        # New Habit button
        new_habit_btn = QPushButton("+ New Habit")
        new_habit_btn.setFont(QFont("SF Pro Text", 14, QFont.Medium))
        new_habit_btn.setFixedHeight(48)
        new_habit_btn.setCursor(Qt.PointingHandCursor)
        new_habit_btn.setStyleSheet("""
            QPushButton {
                background-color: #5F3DC4;
                color: #FFFFFF;
                border: none;
                border-radius: 12px;
                padding: 0px 24px;
            }
            QPushButton:hover {
                background-color: #5028AB;
            }
        """)
        new_habit_btn.clicked.connect(self.show_add_habit)
        layout.addWidget(new_habit_btn)
    
    def show_add_habit(self):
        """Show add habit dialog"""
        if self.main_window:
            self.main_window.show_add_habit_dialog()


class CircularProgress(QWidget):
    """Circular progress indicator"""
    
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
        
        # Background circle
        painter.setPen(QPen(QColor("#E9ECEF"), 18))
        painter.drawArc(
            center_x - radius, center_y - radius,
            radius * 2, radius * 2,
            0, 360 * 16
        )
        
        # Progress arc with gradient
        if self.percentage > 0:
            gradient = QLinearGradient(center_x - radius, center_y, center_x + radius, center_y)
            gradient.setColorAt(0, QColor("#4C6EF5"))
            gradient.setColorAt(1, QColor("#9775FA"))
            
            pen = QPen(gradient, 18)
            pen.setCapStyle(Qt.RoundCap)
            painter.setPen(pen)
            
            span_angle = int(-360 * (self.percentage / 100) * 16)
            painter.drawArc(
                center_x - radius, center_y - radius,
                radius * 2, radius * 2,
                90 * 16, span_angle
            )
        
        # Center text
        painter.setPen(QColor("#212529"))
        font = QFont("SF Pro Display", 52, QFont.Bold)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignCenter, f"{int(self.percentage)}%")
        
        # "PROGRESS" label
        painter.setPen(QColor("#868E96"))
        font_small = QFont("SF Pro Display", 11, QFont.Medium)
        painter.setFont(font_small)
        
        text_rect = painter.boundingRect(self.rect(), Qt.AlignCenter, "PROGRESS")
        text_rect.moveTop(center_y + 15)
        painter.drawText(text_rect, Qt.AlignCenter, "PROGRESS")


class HabitCard(QFrame):
    """Habit card for today's list"""
    
    def __init__(self, habit, is_completed, parent=None):
        super().__init__(parent)
        self.habit = habit
        self.is_completed = is_completed
        self.parent_view = parent
        self.setup_ui()
    
    def setup_ui(self):
        self.setFrameShape(QFrame.NoFrame)
        self.setFixedHeight(72)
        self.setStyleSheet("HabitCard { background-color: transparent; }")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 8, 0, 8)
        layout.setSpacing(12)
        
        # Icon/Checkbox
        icon_frame = QFrame()
        icon_frame.setFixedSize(48, 48)
        
        if self.is_completed:
            icon_frame.setStyleSheet("QFrame { background-color: #51CF66; border-radius: 12px; }")
            icon_text = "✓"
            icon_color = "#FFFFFF"
        else:
            icon_frame.setStyleSheet("QFrame { background-color: #FFFFFF; border: 2px solid #E9ECEF; border-radius: 12px; }")
            from app.utils.constants import CATEGORIES
            icon_text = "📌"
            for cat_name, emoji in CATEGORIES:
                if cat_name == self.habit.category:
                    icon_text = emoji
                    break
            icon_color = "#495057"
        
        icon_layout = QVBoxLayout(icon_frame)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        
        icon_label = QLabel(icon_text)
        icon_label.setFont(QFont("SF Pro Display", 22))
        icon_label.setStyleSheet(f"color: {icon_color};")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_layout.addWidget(icon_label)
        
        layout.addWidget(icon_frame)
        
        # Info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)
        
        name_label = QLabel(self.habit.name)
        name_label.setFont(QFont("SF Pro Display", 15, QFont.Medium))
        name_label.setStyleSheet("color: #212529;")
        info_layout.addWidget(name_label)
        
        subtitle = self.habit.description if self.habit.description else self.habit.category
        if len(subtitle) > 35:
            subtitle = subtitle[:35] + "..."
        
        subtitle_label = QLabel(subtitle)
        subtitle_label.setFont(QFont("SF Pro Text", 13))
        subtitle_label.setStyleSheet("color: #868E96;")
        info_layout.addWidget(subtitle_label)
        
        layout.addLayout(info_layout, stretch=1)
        
        # Status
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
        """Mark habit complete"""
        from app.services.habit_service import get_habit_service
        habit_service = get_habit_service()
        habit_service.mark_habit_complete(self.habit.id)
        if self.parent_view:
            self.parent_view.load_data()


class CompleteHabitHubUI(QWidget):
    """Complete HabitHub UI with sidebar and navbar"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.habit_service = get_habit_service()
        self.streak_service = get_streak_service()
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Setup complete UI"""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = Sidebar(self.main_window)
        main_layout.addWidget(self.sidebar)
        
        # Main content area
        content_area = QWidget()
        content_area.setStyleSheet("QWidget { background-color: #F8F9FA; }")
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Top navbar
        self.navbar = TopNavbar(self.main_window)
        content_layout.addWidget(self.navbar)
        
        # Dashboard content (scrollable)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        dashboard = QWidget()
        dashboard.setStyleSheet("background-color: transparent;")
        dashboard_layout = QVBoxLayout(dashboard)
        dashboard_layout.setContentsMargins(32, 24, 32, 24)
        dashboard_layout.setSpacing(20)
        
        # Top row: Daily Completion + Today's Habits
        top_row = QHBoxLayout()
        top_row.setSpacing(20)
        
        # Daily Completion Card
        daily_card = QFrame()
        daily_card.setFixedWidth(400)
        daily_card.setStyleSheet("QFrame { background-color: #FFFFFF; border-radius: 20px; }")
        
        daily_layout = QVBoxLayout(daily_card)
        daily_layout.setContentsMargins(28, 28, 28, 28)
        daily_layout.setSpacing(20)
        
        daily_title = QLabel("Daily Completion")
        daily_title.setFont(QFont("SF Pro Display", 20, QFont.Bold))
        daily_title.setStyleSheet("color: #212529;")
        daily_layout.addWidget(daily_title)
        
        self.circular_progress = CircularProgress(75)
        daily_layout.addWidget(self.circular_progress, alignment=Qt.AlignCenter)
        
        self.progress_text = QLabel("Almost there! 2 habits left for today.")
        self.progress_text.setFont(QFont("SF Pro Text", 14))
        self.progress_text.setStyleSheet("color: #868E96;")
        self.progress_text.setAlignment(Qt.AlignCenter)
        daily_layout.addWidget(self.progress_text)
        
        top_row.addWidget(daily_card)
        
        # Today's Habits Card
        today_card = QFrame()
        today_card.setStyleSheet("QFrame { background-color: #FFFFFF; border-radius: 20px; }")
        
        today_layout = QVBoxLayout(today_card)
        today_layout.setContentsMargins(28, 28, 28, 28)
        today_layout.setSpacing(16)
        
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
        
        self.habits_list = QVBoxLayout()
        self.habits_list.setSpacing(0)
        today_layout.addLayout(self.habits_list)
        
        today_layout.addStretch()
        
        top_row.addWidget(today_card, stretch=1)
        
        dashboard_layout.addLayout(top_row)
        
        # Bottom row: Weekly Activity + Monthly Milestone
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(20)
        
        # Weekly Activity (placeholder)
        weekly_card = QFrame()
        weekly_card.setStyleSheet("QFrame { background-color: #FFFFFF; border-radius: 20px; }")
        weekly_card.setMinimumHeight(280)
        
        weekly_layout = QVBoxLayout(weekly_card)
        weekly_layout.setContentsMargins(28, 28, 28, 28)
        
        weekly_title = QLabel("Weekly Activity")
        weekly_title.setFont(QFont("SF Pro Display", 20, QFont.Bold))
        weekly_title.setStyleSheet("color: #212529;")
        weekly_layout.addWidget(weekly_title)
        
        weekly_subtitle = QLabel("Consistent completion since Monday")
        weekly_subtitle.setFont(QFont("SF Pro Text", 14))
        weekly_subtitle.setStyleSheet("color: #868E96;")
        weekly_layout.addWidget(weekly_subtitle)
        
        weekly_layout.addStretch()
        
        bottom_row.addWidget(weekly_card, stretch=2)
        
        # Monthly Milestone
        milestone_card = QFrame()
        milestone_card.setFixedWidth(400)
        milestone_card.setStyleSheet("QFrame { background-color: #FFFFFF; border-radius: 20px; }")
        
        milestone_layout = QVBoxLayout(milestone_card)
        milestone_layout.setContentsMargins(28, 28, 28, 32)
        milestone_layout.setSpacing(20)
        
        milestone_title = QLabel("Monthly Milestone")
        milestone_title.setFont(QFont("SF Pro Display", 20, QFont.Bold))
        milestone_title.setStyleSheet("color: #212529;")
        milestone_layout.addWidget(milestone_title)
        
        # Flame icon
        flame_container = QFrame()
        flame_container.setFixedSize(120, 120)
        flame_container.setStyleSheet("QFrame { background-color: #FFF4E6; border-radius: 60px; }")
        
        flame_layout = QVBoxLayout(flame_container)
        flame_layout.setContentsMargins(0, 0, 0, 0)
        
        flame_label = QLabel("🔥")
        flame_label.setFont(QFont("SF Pro Display", 56))
        flame_label.setAlignment(Qt.AlignCenter)
        flame_layout.addWidget(flame_label)
        
        milestone_layout.addWidget(flame_container, alignment=Qt.AlignCenter)
        
        self.streak_label = QLabel("24 Day Streak!")
        self.streak_label.setFont(QFont("SF Pro Display", 32, QFont.Bold))
        self.streak_label.setStyleSheet("color: #212529;")
        self.streak_label.setAlignment(Qt.AlignCenter)
        milestone_layout.addWidget(self.streak_label)
        
        milestone_text = QLabel("You're in the top 5% of users this\nmonth. Keep pushing!")
        milestone_text.setFont(QFont("SF Pro Text", 14))
        milestone_text.setStyleSheet("color: #868E96;")
        milestone_text.setAlignment(Qt.AlignCenter)
        milestone_layout.addWidget(milestone_text)
        
        target_header = QHBoxLayout()
        
        target_label = QLabel("TARGET")
        target_label.setFont(QFont("SF Pro Text", 11, QFont.Bold))
        target_label.setStyleSheet("color: #ADB5BD;")
        target_header.addWidget(target_label)
        
        target_header.addStretch()
        
        days_left = QLabel("8 Left")
        days_left.setFont(QFont("SF Pro Text", 12, QFont.Bold))
        days_left.setStyleSheet("""
            QLabel {
                background-color: #FFE8CC;
                color: #FD7E14;
                padding: 6px 14px;
                border-radius: 10px;
            }
        """)
        target_header.addWidget(days_left)
        
        milestone_layout.addLayout(target_header)
        
        target_value = QLabel("30 Days Streak")
        target_value.setFont(QFont("SF Pro Display", 18, QFont.Bold))
        target_value.setStyleSheet("color: #212529;")
        milestone_layout.addWidget(target_value)
        
        bottom_row.addWidget(milestone_card)
        
        dashboard_layout.addLayout(bottom_row)
        
        scroll.setWidget(dashboard)
        content_layout.addWidget(scroll)
        
        main_layout.addWidget(content_area, stretch=1)
    
    def load_data(self):
        """Load dashboard data"""
        # Clear habits
        while self.habits_list.count():
            item = self.habits_list.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Get habits
        habits = self.habit_service.get_all_habits()
        
        if not habits:
            return
        
        # Calculate percentage
        completed = sum(1 for h in habits if self.habit_service.is_habit_completed_today(h.id))
        total = len(habits)
        percentage = int((completed / total) * 100) if total > 0 else 0
        
        self.circular_progress.set_percentage(percentage)
        
        left = total - completed
        if left == 0:
            self.progress_text.setText("Perfect! All habits completed today! 🎉")
        else:
            self.progress_text.setText(f"Almost there! {left} habit{'s' if left != 1 else ''} left for today.")
        
        # Load habits
        for habit in habits[:4]:
            is_completed = self.habit_service.is_habit_completed_today(habit.id)
            card = HabitCard(habit, is_completed, self)
            self.habits_list.addWidget(card)
        
        # Get max streak
        max_streak = 0
        for habit in habits:
            streak_info = self.streak_service.get_streak_info(habit.id)
            max_streak = max(max_streak, streak_info['current_streak'])
        
        self.streak_label.setText(f"{max_streak} Day Streak!")
