"""
Complete HabitHub UI with Sidebar and Navbar - FIXED
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QScrollArea,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QCursor, QPainter, QColor, QPen, QLinearGradient
from datetime import datetime, timedelta
from app.services.habit_service import get_habit_service
from app.services.streak_service import get_streak_service


class Sidebar(QFrame):
    """Left sidebar navigation"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.setup_ui()
        self.load_profile_name()

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

        # Logo and Title Section
        logo_container = QWidget()
        logo_container.setStyleSheet("background: transparent;")
        logo_layout = QHBoxLayout(logo_container)
        logo_layout.setContentsMargins(8, 0, 8, 0)
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
        icon_label.setFont(QFont("SF Pro Display", 20, QFont.Bold))
        icon_label.setStyleSheet("color: #FFFFFF; background: transparent;")
        icon_label.setAlignment(Qt.AlignCenter)
        logo_icon_layout.addWidget(icon_label)

        logo_layout.addWidget(logo_icon)

        title = QLabel("HabitHub")
        title.setFont(QFont("SF Pro Display", 18, QFont.Bold))
        title.setStyleSheet("color: #212529; background: transparent;")
        logo_layout.addWidget(title)

        logo_layout.addStretch()

        layout.addWidget(logo_container)
        layout.addSpacing(32)

        # Navigation Section
        nav_label = QLabel("MENU")
        nav_label.setFont(QFont("SF Pro Text", 10, QFont.Bold))
        nav_label.setStyleSheet("color: #868E96; background: transparent; padding-left: 16px;")
        layout.addWidget(nav_label)

        layout.addSpacing(8)

        # Navigation buttons
        self.nav_buttons = {}
        nav_items = [
            ("dashboard", "Dashboard", "⊞"),
            ("today", "Today", "📅"),
            ("habits", "Habits", "⚡"),
            ("analytics", "Analytics", "📊"),
            ("goals", "Goals", "🏆"),
            ("settings", "Settings", "⚙"),
        ]

        for key, text, icon in nav_items:
            btn = QPushButton(f"{icon}  {text}")
            btn.setFont(QFont("SF Pro Text", 14, QFont.Medium))
            btn.setFixedHeight(48)
            btn.setCursor(Qt.PointingHandCursor)
    
            # Active state for dashboard
            if key == "dashboard":
                btn.setStyleSheet("""
                    QPushButton {
                    background-color: #5F3DC4;
                    color: #FFFFFF;
                    border: none;
                    border-radius: 12px;
                    text-align: left;
                    padding-left: 16px;
                    font-weight: 600;
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
    
            btn.clicked.connect(lambda checked, k=key: self.on_nav_clicked(k))
            self.nav_buttons[key] = btn
            layout.addWidget(btn)

        layout.addStretch()

        # Separator line
        separator = QFrame()
        separator.setFixedHeight(1)
        separator.setStyleSheet("background-color: #E9ECEF;")
        layout.addWidget(separator)

        layout.addSpacing(12)

        # Profile Section (Clickable)
        profile_container = QPushButton()
        profile_container.setCursor(Qt.PointingHandCursor)
        profile_container.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                border: 1px solid #E9ECEF;
                border-radius: 12px;
                padding: 4px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #F8F9FA;
                border: 1px solid #6366F1;
            }
        """)
        profile_container.setFixedHeight(64)
        profile_container.clicked.connect(self.on_profile_clicked)

        profile_layout = QHBoxLayout(profile_container)
        profile_layout.setContentsMargins(12, 8, 12, 8)
        profile_layout.setSpacing(12)

        # Avatar
        avatar = QFrame()
        avatar.setFixedSize(40, 40)
        avatar.setStyleSheet("""
            QFrame {
                background-color: #FFD43B;
                border-radius: 20px;
            }
        """)

        avatar_layout = QVBoxLayout(avatar)
        avatar_layout.setContentsMargins(0, 0, 0, 0)

        avatar_text = QLabel("👤")
        avatar_text.setFont(QFont("SF Pro Display", 20))
        avatar_text.setAlignment(Qt.AlignCenter)
        avatar_text.setStyleSheet("background: transparent;")
        avatar_layout.addWidget(avatar_text)

        profile_layout.addWidget(avatar)

        # User info
        user_info_layout = QVBoxLayout()
        user_info_layout.setSpacing(2)

        self.profile_name_label = QLabel("Alex Morgan")
        self.profile_name_label.setFont(QFont("SF Pro Text", 13, QFont.Bold))
        self.profile_name_label.setStyleSheet("color: #212529; background: transparent;")
        user_info_layout.addWidget(self.profile_name_label)


        user_type = QLabel("Premium Member")
        user_type.setFont(QFont("SF Pro Text", 11))
        user_type.setStyleSheet("color: #868E96; background: transparent;")
        user_info_layout.addWidget(user_type)

        profile_layout.addLayout(user_info_layout)

        layout.addWidget(profile_container)
        layout.addSpacing(4)

    def on_nav_clicked(self, key):
        """Handle navigation button click"""
        if not self.main_window:
            return
    
        # Update active state
        self.update_active_button(key)
    
        # Navigate to view
        if key == 'dashboard':
            self.main_window.show_dashboard()
        elif key == 'today':
            self.main_window.show_today_view()
        elif key == 'habits':
            self.main_window.show_habits_view()
        elif key == 'analytics':
            self.main_window.show_analytics()
        elif key == 'goals':
            self.main_window.show_goals()
        elif key == 'settings':
            self.main_window.show_settings()

    def update_active_button(self, active_key):
        """Update button styles to show active state"""
        active_style = """
            QPushButton {
                background-color: #5F3DC4;
                color: #FFFFFF;
                border: none;
                border-radius: 12px;
                text-align: left;
                padding-left: 16px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #5028AB;
            }
        """
    
        inactive_style = """
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
        """
    
        for key, btn in self.nav_buttons.items():
            if key == active_key:
                btn.setStyleSheet(active_style)
            else:
                btn.setStyleSheet(inactive_style)

    def show_profile(self):
        """Show profile in content area"""
        self.clear_content_area()
    
        from app.ui.profile_content_view import ProfileContentView
        profile_view = ProfileContentView(self)
        self.content_layout.addWidget(profile_view)
    
        # Don't highlight any sidebar button for profile
        if hasattr(self, 'sidebar'):
            # Keep current active button as is
            pass
    
        self.update_status_bar()

    def on_profile_clicked(self):
        """Handle profile click"""
        if self.main_window:
            self.main_window.show_profile()

    def update_profile_name(self, name):
        """Update profile name in sidebar"""
        # Find the user name label and update it
        if hasattr(self, 'profile_name_label'):
            self.profile_name_label.setText(name)


    def load_profile_name(self):
        """Load and display profile name from database"""
        try:
            from app.services.profile_service import get_profile_service
            profile_service = get_profile_service()
            profile = profile_service.get_profile()
            self.profile_name_label.setText(profile['name'])
        except:
            # Keep default if error
            pass


class TopNavbar(QFrame):
    """Top navigation bar"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.setup_ui()

    def setup_ui(self):
        """Setup navbar"""
        self.setFixedHeight(80)
        self.setStyleSheet(
            "QFrame { background-color: #FFFFFF; border-bottom: 1px solid #E9ECEF; }"
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(32, 0, 32, 0)

        # Greeting
        greeting_layout = QVBoxLayout()
        greeting_layout.setSpacing(2)

        hour = datetime.now().hour
        greeting = (
            "Good morning"
            if hour < 12
            else "Good afternoon"
            if hour < 18
            else "Good evening"
        )

        greeting_label = QLabel(f"{greeting}, Alex")
        greeting_label.setFont(QFont("SF Pro Display", 28, QFont.Bold))
        greeting_label.setStyleSheet("color: #212529;")
        greeting_layout.addWidget(greeting_label)

        today = datetime.now()
        date_str = today.strftime("%A, %B %dth")

        date_quote = QLabel(
            f'{date_str} • "Success is the sum of small efforts, repeated day in and day out."'
        )
        date_quote.setFont(QFont("SF Pro Text", 13))
        date_quote.setStyleSheet("color: #868E96;")
        greeting_layout.addWidget(date_quote)

        layout.addLayout(greeting_layout)
        layout.addStretch()

        # Notification
        notif_btn = QPushButton("🔔")
        notif_btn.setFont(QFont("SF Pro Display", 18))
        notif_btn.setFixedSize(48, 48)
        notif_btn.setCursor(Qt.PointingHandCursor)
        notif_btn.setStyleSheet("""
            QPushButton {
                background-color: #F8F9FA;
                border: 1px solid #E9ECEF;
                border-radius: 24px;
            }
            QPushButton:hover {
                background-color: #E9ECEF;
            }
        """)
        layout.addWidget(notif_btn)

        # New Habit button
        new_btn = QPushButton("+ New Habit")
        new_btn.setFont(QFont("SF Pro Text", 14, QFont.Medium))
        new_btn.setFixedHeight(48)
        new_btn.setCursor(Qt.PointingHandCursor)
        new_btn.setStyleSheet("""
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
        new_btn.clicked.connect(self.show_add_habit)
        layout.addWidget(new_btn)

    def show_add_habit(self):
        if self.main_window:
            self.main_window.show_add_habit_dialog()


class CircularProgress(QWidget):
    """Circular progress"""

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

        painter.setPen(QPen(QColor("#E9ECEF"), 18))
        painter.drawArc(
            center_x - radius, center_y - radius, radius * 2, radius * 2, 0, 360 * 16
        )

        if self.percentage > 0:
            gradient = QLinearGradient(
                center_x - radius, center_y, center_x + radius, center_y
            )
            gradient.setColorAt(0, QColor("#4C6EF5"))
            gradient.setColorAt(1, QColor("#9775FA"))

            pen = QPen(gradient, 18)
            pen.setCapStyle(Qt.RoundCap)
            painter.setPen(pen)

            span_angle = int(-360 * (self.percentage / 100) * 16)
            painter.drawArc(
                center_x - radius,
                center_y - radius,
                radius * 2,
                radius * 2,
                90 * 16,
                span_angle,
            )

        painter.setPen(QColor("#212529"))
        painter.setFont(QFont("SF Pro Display", 52, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, f"{int(self.percentage)}%")


class HabitCard(QFrame):
    """Habit card - FIXED"""

    def __init__(self, habit, is_completed, parent=None):
        super().__init__(parent)
        self.habit = habit
        self.is_completed = is_completed
        self.parent_view = parent
        self.habit_service = get_habit_service()  # FIXED: Initialize here
        self.setup_ui()

    def setup_ui(self):
        self.setFixedHeight(72)
        self.setStyleSheet("background-color: transparent;")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 8, 0, 8)
        layout.setSpacing(12)

        # Icon
        icon_frame = QFrame()
        icon_frame.setFixedSize(48, 48)

        if self.is_completed:
            icon_frame.setStyleSheet(
                "QFrame { background-color: #51CF66; border-radius: 12px; }"
            )
            icon_text, icon_color = "✓", "#FFFFFF"
        else:
            icon_frame.setStyleSheet(
                "QFrame { background-color: #FFFFFF; border: 2px solid #E9ECEF; border-radius: 12px; }"
            )
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
        info = QVBoxLayout()
        info.setSpacing(2)

        name = QLabel(self.habit.name)
        name.setFont(QFont("SF Pro Display", 15, QFont.Medium))
        name.setStyleSheet("color: #212529;")
        info.addWidget(name)

        subtitle = (
            self.habit.description if self.habit.description else self.habit.category
        )
        if len(subtitle) > 35:
            subtitle = subtitle[:35] + "..."

        sub = QLabel(subtitle)
        sub.setFont(QFont("SF Pro Text", 13))
        sub.setStyleSheet("color: #868E96;")
        info.addWidget(sub)

        layout.addLayout(info, stretch=1)

        # Status
        if self.is_completed:
            status = QLabel("Completed")
            status.setFont(QFont("SF Pro Text", 13, QFont.Medium))
            status.setStyleSheet("color: #51CF66;")
            layout.addWidget(status)
        else:
            btn = QPushButton("Mark Done")
            btn.setFont(QFont("SF Pro Text", 13, QFont.Medium))
            btn.setFixedHeight(36)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
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
            btn.clicked.connect(self.mark_complete)
            layout.addWidget(btn)

    def mark_complete(self):
        """FIXED: Mark complete"""
        try:
            self.habit_service.mark_habit_complete(self.habit.id)
            if self.parent_view and hasattr(self.parent_view, "load_data"):
                self.parent_view.load_data()
        except Exception as e:
            print(f"Error: {e}")


class CompleteHabitHubUI(QWidget):
    """Complete UI"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.habit_service = get_habit_service()
        self.streak_service = get_streak_service()
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        sidebar = Sidebar(self.main_window)
        main_layout.addWidget(sidebar)

        # Content
        content = QWidget()
        content.setStyleSheet("background-color: #F8F9FA;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Navbar
        navbar = TopNavbar(self.main_window)
        content_layout.addWidget(navbar)

        # Dashboard scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet(
            "QScrollArea { border: none; background-color: transparent; }"
        )

        dashboard = QWidget()
        dashboard_layout = QVBoxLayout(dashboard)
        dashboard_layout.setContentsMargins(32, 24, 32, 24)
        dashboard_layout.setSpacing(20)

        # Top row
        top_row = QHBoxLayout()
        top_row.setSpacing(20)

        # Daily card
        daily_card = QFrame()
        daily_card.setFixedWidth(400)
        daily_card.setStyleSheet(
            "QFrame { background-color: #FFFFFF; border-radius: 20px; }"
        )

        daily_layout = QVBoxLayout(daily_card)
        daily_layout.setContentsMargins(28, 28, 28, 28)
        daily_layout.setSpacing(20)

        daily_title = QLabel("Daily Completion")
        daily_title.setFont(QFont("SF Pro Display", 20, QFont.Bold))
        daily_title.setStyleSheet("color: #212529;")
        daily_layout.addWidget(daily_title)

        self.circular_progress = CircularProgress(0)
        daily_layout.addWidget(self.circular_progress, alignment=Qt.AlignCenter)

        self.progress_text = QLabel("Loading...")
        self.progress_text.setFont(QFont("SF Pro Text", 14))
        self.progress_text.setStyleSheet("color: #868E96;")
        self.progress_text.setAlignment(Qt.AlignCenter)
        daily_layout.addWidget(self.progress_text)

        top_row.addWidget(daily_card)

        # Today's habits
        today_card = QFrame()
        today_card.setStyleSheet(
            "QFrame { background-color: #FFFFFF; border-radius: 20px; }"
        )

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
        view_all.setStyleSheet(
            "QPushButton { background: transparent; border: none; color: #4C6EF5; }"
        )
        today_header.addWidget(view_all)

        today_layout.addLayout(today_header)

        self.habits_list = QVBoxLayout()
        today_layout.addLayout(self.habits_list)
        today_layout.addStretch()

        top_row.addWidget(today_card, stretch=1)

        dashboard_layout.addLayout(top_row)

        # Bottom row
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(20)

        # Weekly placeholder
        weekly = QFrame()
        weekly.setStyleSheet(
            "QFrame { background-color: #FFFFFF; border-radius: 20px; }"
        )
        weekly.setMinimumHeight(280)
        bottom_row.addWidget(weekly, stretch=2)

        # Milestone
        milestone = QFrame()
        milestone.setFixedWidth(400)
        milestone.setStyleSheet(
            "QFrame { background-color: #FFFFFF; border-radius: 20px; }"
        )

        milestone_layout = QVBoxLayout(milestone)
        milestone_layout.setContentsMargins(28, 28, 28, 32)
        milestone_layout.setSpacing(20)

        milestone_title = QLabel("Monthly Milestone")
        milestone_title.setFont(QFont("SF Pro Display", 20, QFont.Bold))
        milestone_title.setStyleSheet("color: #212529;")
        milestone_layout.addWidget(milestone_title)

        flame = QFrame()
        flame.setFixedSize(120, 120)
        flame.setStyleSheet(
            "QFrame { background-color: #FFF4E6; border-radius: 60px; }"
        )

        flame_layout = QVBoxLayout(flame)
        flame_layout.setContentsMargins(0, 0, 0, 0)

        flame_icon = QLabel("🔥")
        flame_icon.setFont(QFont("SF Pro Display", 56))
        flame_icon.setAlignment(Qt.AlignCenter)
        flame_layout.addWidget(flame_icon)

        milestone_layout.addWidget(flame, alignment=Qt.AlignCenter)

        self.streak_label = QLabel("0 Day Streak!")
        self.streak_label.setFont(QFont("SF Pro Display", 32, QFont.Bold))
        self.streak_label.setStyleSheet("color: #212529;")
        self.streak_label.setAlignment(Qt.AlignCenter)
        milestone_layout.addWidget(self.streak_label)

        bottom_row.addWidget(milestone)

        dashboard_layout.addLayout(bottom_row)

        scroll.setWidget(dashboard)
        content_layout.addWidget(scroll)

        main_layout.addWidget(content, stretch=1)

    def load_data(self):
        """Load data"""
        # Clear
        while self.habits_list.count():
            item = self.habits_list.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Get habits
        habits = self.habit_service.get_all_habits()

        if not habits:
            self.progress_text.setText("No habits yet. Create one!")
            return

        # Calculate
        completed = sum(
            1 for h in habits if self.habit_service.is_habit_completed_today(h.id)
        )
        total = len(habits)
        percentage = int((completed / total) * 100) if total > 0 else 0

        self.circular_progress.set_percentage(percentage)

        left = total - completed
        if left == 0:
            self.progress_text.setText("Perfect! All habits completed! 🎉")
        else:
            self.progress_text.setText(
                f"Almost there! {left} habit{'s' if left != 1 else ''} left."
            )

        # Load habits
        for habit in habits[:4]:
            is_completed = self.habit_service.is_habit_completed_today(habit.id)
            card = HabitCard(habit, is_completed, self)
            self.habits_list.addWidget(card)

        # Streak
        max_streak = 0
        for habit in habits:
            streak_info = self.streak_service.get_streak_info(habit.id)
            max_streak = max(max_streak, streak_info["current_streak"])

        self.streak_label.setText(f"{max_streak} Day Streak!")


class DashboardContent(QWidget):
    """Dashboard content without sidebar"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.habit_service = get_habit_service()
        self.streak_service = get_streak_service()
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Setup dashboard content UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Top navbar
        navbar = TopNavbar(self.main_window)
        main_layout.addWidget(navbar)
        
        # Dashboard scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        dashboard = QWidget()
        dashboard_layout = QVBoxLayout(dashboard)
        dashboard_layout.setContentsMargins(32, 24, 32, 24)
        dashboard_layout.setSpacing(20)
        
        # Top row
        top_row = QHBoxLayout()
        top_row.setSpacing(20)
        
        # Daily card
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
        
        self.circular_progress = CircularProgress(0)
        daily_layout.addWidget(self.circular_progress, alignment=Qt.AlignCenter)
        
        self.progress_text = QLabel("Loading...")
        self.progress_text.setFont(QFont("SF Pro Text", 14))
        self.progress_text.setStyleSheet("color: #868E96;")
        self.progress_text.setAlignment(Qt.AlignCenter)
        daily_layout.addWidget(self.progress_text)
        
        top_row.addWidget(daily_card)
        
        # Today's habits
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
        view_all.setStyleSheet("QPushButton { background: transparent; border: none; color: #4C6EF5; }")
        today_header.addWidget(view_all)
        
        today_layout.addLayout(today_header)
        
        self.habits_list = QVBoxLayout()
        today_layout.addLayout(self.habits_list)
        today_layout.addStretch()
        
        top_row.addWidget(today_card, stretch=1)
        
        dashboard_layout.addLayout(top_row)
        
        # Bottom row
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(20)
        
        # Weekly placeholder
        weekly = QFrame()
        weekly.setStyleSheet("QFrame { background-color: #FFFFFF; border-radius: 20px; }")
        weekly.setMinimumHeight(280)
        bottom_row.addWidget(weekly, stretch=2)
        
        # Milestone
        milestone = QFrame()
        milestone.setFixedWidth(400)
        milestone.setStyleSheet("QFrame { background-color: #FFFFFF; border-radius: 20px; }")
        
        milestone_layout = QVBoxLayout(milestone)
        milestone_layout.setContentsMargins(28, 28, 28, 32)
        milestone_layout.setSpacing(20)
        
        milestone_title = QLabel("Monthly Milestone")
        milestone_title.setFont(QFont("SF Pro Display", 20, QFont.Bold))
        milestone_title.setStyleSheet("color: #212529;")
        milestone_layout.addWidget(milestone_title)
        
        flame = QFrame()
        flame.setFixedSize(120, 120)
        flame.setStyleSheet("QFrame { background-color: #FFF4E6; border-radius: 60px; }")
        
        flame_layout = QVBoxLayout(flame)
        flame_layout.setContentsMargins(0, 0, 0, 0)
        
        flame_icon = QLabel("🔥")
        flame_icon.setFont(QFont("SF Pro Display", 56))
        flame_icon.setAlignment(Qt.AlignCenter)
        flame_layout.addWidget(flame_icon)
        
        milestone_layout.addWidget(flame, alignment=Qt.AlignCenter)
        
        self.streak_label = QLabel("0 Day Streak!")
        self.streak_label.setFont(QFont("SF Pro Display", 32, QFont.Bold))
        self.streak_label.setStyleSheet("color: #212529;")
        self.streak_label.setAlignment(Qt.AlignCenter)
        milestone_layout.addWidget(self.streak_label)
        
        bottom_row.addWidget(milestone)
        
        dashboard_layout.addLayout(bottom_row)
        
        scroll.setWidget(dashboard)
        main_layout.addWidget(scroll)
    
    def load_data(self):
        """Load data - same as CompleteHabitHubUI"""
        while self.habits_list.count():
            item = self.habits_list.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        habits = self.habit_service.get_all_habits()
        
        if not habits:
            self.progress_text.setText("No habits yet. Create one!")
            return
        
        completed = sum(1 for h in habits if self.habit_service.is_habit_completed_today(h.id))
        total = len(habits)
        percentage = int((completed / total) * 100) if total > 0 else 0
        
        self.circular_progress.set_percentage(percentage)
        
        left = total - completed
        if left == 0:
            self.progress_text.setText("Perfect! All habits completed! 🎉")
        else:
            self.progress_text.setText(f"Almost there! {left} habit{'s' if left != 1 else ''} left.")
        
        for habit in habits[:4]:
            is_completed = self.habit_service.is_habit_completed_today(habit.id)
            card = HabitCard(habit, is_completed, self)
            self.habits_list.addWidget(card)
        
        max_streak = 0
        for habit in habits:
            streak_info = self.streak_service.get_streak_info(habit.id)
            max_streak = max(max_streak, streak_info['current_streak'])
        
        self.streak_label.setText(f"{max_streak} Day Streak!")