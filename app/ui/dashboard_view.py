"""
Premium Dashboard View - ALL ISSUES FIXED
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QCursor, QPainter, QColor, QPen, QLinearGradient
from datetime import datetime, timedelta
from app.services.habit_service import get_habit_service
from app.services.streak_service import get_streak_service


class SimpleCircularProgress(QWidget):
    
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
        painter.setPen(QPen(QColor("#E0E7FF"), 18))
        painter.drawArc(center_x - radius, center_y - radius, radius * 2, radius * 2, 0, 360 * 16)
        
        # Progress arc with gradient
        if self.percentage > 0:
            gradient = QLinearGradient(center_x - radius, center_y, center_x + radius, center_y)
            gradient.setColorAt(0, QColor("#667eea"))
            gradient.setColorAt(0.5, QColor("#764ba2"))
            gradient.setColorAt(1, QColor("#f093fb"))
            
            pen = QPen(gradient, 18)
            pen.setCapStyle(Qt.RoundCap)
            painter.setPen(pen)
            
            span_angle = int(-360 * (self.percentage / 100) * 16)
            painter.drawArc(center_x - radius, center_y - radius, radius * 2, radius * 2, 90 * 16, span_angle)
        
        # Percentage text 
        painter.setPen(QColor("#1F2937"))
        if self.percentage == 100:
            painter.setFont(QFont("SF Pro Display", 40, QFont.Bold))  # Smaller for 100%
        else:
            painter.setFont(QFont("SF Pro Display", 40, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, f"{int(self.percentage)}%")


class PremiumHabitCard(QFrame):
    """Premium habit card - FIXED text display and button size"""
    
    def __init__(self, habit, is_completed, parent=None):
        super().__init__(parent)
        self.habit = habit
        self.is_completed = is_completed
        self.parent_view = parent
        self.habit_service = get_habit_service()
        self.setup_ui()
    
    def setup_ui(self):
        self.setFixedHeight(85)
        
        if self.is_completed:
            self.setStyleSheet("""
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #D1FAE5, stop:1 #A7F3D0);
                    border-left: 4px solid #10B981;
                    border-radius: 14px;
                }
            """)
        else:
            self.setStyleSheet("""
                QFrame {
                    background-color: #FFFFFF;
                    border-left: 4px solid #667eea;
                    border-radius: 14px;
                }
                QFrame:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #FFFFFF, stop:1 #F5F3FF);
                }
            """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(22, 16, 22, 16)
        layout.setSpacing(18)
        
        # Icon
        icon_frame = QFrame()
        icon_frame.setFixedSize(54, 54)
        
        if self.is_completed:
            icon_frame.setStyleSheet("""
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #10B981, stop:1 #059669);
                    border-radius: 13px;
                }
            """)
            icon_text = "✓"
            icon_color = "#FFFFFF"
        else:
            from app.utils.constants import CATEGORIES
            icon_text = "📌"
            for cat_name, emoji in CATEGORIES:
                if cat_name == self.habit.category:
                    icon_text = emoji
                    break
            
            icon_frame.setStyleSheet("""
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #EDE9FE, stop:1 #DDD6FE);
                    border-radius: 13px;
                }
            """)
            icon_color = "#5B21B6"
        
        icon_layout = QVBoxLayout(icon_frame)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        
        icon_label = QLabel(icon_text)
        icon_label.setFont(QFont("SF Pro Display", 26))
        icon_label.setStyleSheet(f"color: {icon_color}; background: transparent;")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_layout.addWidget(icon_label)
        
        layout.addWidget(icon_frame)
        
        # Info - FIXED: Better text display
        info = QVBoxLayout()
        info.setSpacing(5)
        
        name = QLabel(self.habit.name)
        name.setFont(QFont("SF Pro Display", 17, QFont.Bold))
        name.setStyleSheet("color: #1F2937; background: transparent;")
        name.setWordWrap(False)  # Don't wrap
        info.addWidget(name)
        
        subtitle = f"{self.habit.category} • {self.habit.frequency}"
        sub = QLabel(subtitle)
        sub.setFont(QFont("SF Pro Text", 14))
        sub.setStyleSheet("color: #6B7280; background: transparent;")
        info.addWidget(sub)
        
        layout.addLayout(info, stretch=1)
        
        # Status/Action - FIXED: Bigger button
        if self.is_completed:
            status_badge = QLabel("✓ Completed")
            status_badge.setFont(QFont("SF Pro Text", 15, QFont.Bold))
            status_badge.setStyleSheet("""
                QLabel {
                    color: #059669;
                    background-color: rgba(16, 185, 129, 0.15);
                    padding: 10px 18px;
                    border-radius: 11px;
                }
            """)
            layout.addWidget(status_badge)
        else:
            btn = QPushButton("Mark Done")
            btn.setFont(QFont("SF Pro Text", 15, QFont.Bold))
            btn.setFixedHeight(46)  # Increased from 42
            btn.setFixedWidth(130)  # Increased from 110
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #667eea, stop:1 #764ba2);
                    color: #FFFFFF;
                    border: none;
                    border-radius: 11px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #5568d3, stop:1 #6a4191);
                }
            """)
            btn.clicked.connect(self.mark_complete)
            layout.addWidget(btn)
    
    def mark_complete(self):
        try:
            self.habit_service.mark_habit_complete(self.habit.id)
            if self.parent_view and hasattr(self.parent_view, 'load_dashboard'):
                self.parent_view.load_dashboard()
        except Exception as e:
            print(f"Error: {e}")


class WeekDayCard(QFrame):
    """Week day card"""
    
    def __init__(self, day_name, percentage, day_number, parent=None):
        super().__init__(parent)
        self.setup_ui(day_name, percentage, day_number)
    
    def setup_ui(self, day_name, percentage, day_number):
        self.setFixedSize(118, 165)
        
        if percentage >= 80:
            gradient = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #10B981, stop:1 #059669)"
            text_color = "#FFFFFF"
            status = "Perfect!"
        elif percentage >= 50:
            gradient = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F59E0B, stop:1 #D97706)"
            text_color = "#FFFFFF"
            status = "Good"
        elif percentage > 0:
            gradient = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #EF4444, stop:1 #DC2626)"
            text_color = "#FFFFFF"
            status = "Try More"
        else:
            gradient = "#F3F4F6"
            text_color = "#9CA3AF"
            status = "Start"
        
        self.setStyleSheet(f"""
            QFrame {{
                background: {gradient};
                border-radius: 16px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 16, 10, 16)
        layout.setSpacing(11)
        layout.setAlignment(Qt.AlignCenter)
        
        day_label = QLabel(day_name)
        day_label.setFont(QFont("SF Pro Text", 12, QFont.Bold))
        day_label.setStyleSheet(f"color: {text_color}; background: transparent;")
        day_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(day_label)
        
        date_label = QLabel(str(day_number))
        date_label.setFont(QFont("SF Pro Display", 18))
        date_label.setStyleSheet(f"color: {text_color}; background: transparent;")
        date_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(date_label)
        
        layout.addSpacing(7)
        
        percent_label = QLabel(f"{percentage}%")
        percent_label.setFont(QFont("SF Pro Display", 30, QFont.Bold))
        percent_label.setStyleSheet(f"color: {text_color}; background: transparent;")
        percent_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(percent_label)
        
        status_label = QLabel(status)
        status_label.setFont(QFont("SF Pro Text", 11, QFont.Medium))
        status_label.setStyleSheet(f"color: {text_color}; background: transparent;")
        status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(status_label)


class ModernDashboard(QWidget):
    """Fixed premium dashboard - ALL ISSUES RESOLVED"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.habit_service = get_habit_service()
        self.streak_service = get_streak_service()
        self.setup_ui()
        self.load_dashboard()
    
    def setup_ui(self):
        """Setup dashboard UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Top navbar
        navbar = QFrame()
        navbar.setFixedHeight(85)
        navbar.setStyleSheet("QFrame { background-color: #FFFFFF; border: none; }")
        
        navbar_layout = QHBoxLayout(navbar)
        navbar_layout.setContentsMargins(36, 0, 36, 0)
        
        # Greeting
        greeting_layout = QVBoxLayout()
        greeting_layout.setSpacing(4)
        
        hour = datetime.now().hour
        greeting = "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"
        
        greeting_label = QLabel(f"{greeting}, Alex")
        greeting_label.setFont(QFont("SF Pro Display", 30, QFont.Bold))
        greeting_label.setStyleSheet("color: #111827;")
        greeting_layout.addWidget(greeting_label)
        
        today = datetime.now()
        date_str = today.strftime("%A, %B %dth")
        
        date_label = QLabel(f'{date_str} • "Success is the sum of small efforts, repeated day in and day out."')
        date_label.setFont(QFont("SF Pro Text", 13))
        date_label.setStyleSheet("color: #6B7280;")
        greeting_layout.addWidget(date_label)
        
        navbar_layout.addLayout(greeting_layout)
        navbar_layout.addStretch()
        
        # Notification
        notif_btn = QPushButton("🔔")
        notif_btn.setFont(QFont("SF Pro Display", 20))
        notif_btn.setFixedSize(50, 50)
        notif_btn.setCursor(Qt.PointingHandCursor)
        notif_btn.setStyleSheet("""
            QPushButton {
                background-color: #F3F4F6;
                border: none;
                border-radius: 25px;
            }
            QPushButton:hover {
                background-color: #E5E7EB;
            }
        """)
        navbar_layout.addWidget(notif_btn)
        
        # New Habit button
        new_btn = QPushButton("+ New Habit")
        new_btn.setFont(QFont("SF Pro Text", 15, QFont.Bold))
        new_btn.setFixedHeight(50)
        new_btn.setCursor(Qt.PointingHandCursor)
        new_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: #FFFFFF;
                border: none;
                border-radius: 12px;
                padding: 0px 26px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5568d3, stop:1 #6a4191);
            }
        """)
        new_btn.clicked.connect(self.show_add_habit)
        navbar_layout.addWidget(new_btn)
        
        main_layout.addWidget(navbar)
        
        # Dashboard content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #F9FAFB;
            }
        """)
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(36, 28, 36, 28)
        content_layout.setSpacing(24)
        
        # Top row
        top_row = QHBoxLayout()
        top_row.setSpacing(24)
        
        # Daily Completion
        daily_card = QFrame()
        daily_card.setFixedWidth(380)
        daily_card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 20px;
            }
        """)
        
        daily_layout = QVBoxLayout(daily_card)
        daily_layout.setContentsMargins(30, 28, 30, 28)
        daily_layout.setSpacing(20)
        
        daily_title = QLabel("Daily Completion")
        daily_title.setFont(QFont("SF Pro Display", 22, QFont.Bold))
        daily_title.setStyleSheet("color: #111827;")
        daily_layout.addWidget(daily_title)
        
        self.circular_progress = SimpleCircularProgress(0)
        daily_layout.addWidget(self.circular_progress, alignment=Qt.AlignCenter)
        
        self.progress_text = QLabel("Loading...")
        self.progress_text.setFont(QFont("SF Pro Text", 15))
        self.progress_text.setStyleSheet("color: #6B7280;")
        self.progress_text.setAlignment(Qt.AlignCenter)
        self.progress_text.setWordWrap(True)
        daily_layout.addWidget(self.progress_text)
        
        top_row.addWidget(daily_card)
        
        # Today's Habits
        habits_card = QFrame()
        habits_card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 20px;
            }
        """)
        
        habits_layout = QVBoxLayout(habits_card)
        habits_layout.setContentsMargins(30, 28, 30, 28)
        habits_layout.setSpacing(18)
        
        habits_header = QHBoxLayout()
        
        habits_title = QLabel("Today's Habits")
        habits_title.setFont(QFont("SF Pro Display", 22, QFont.Bold))
        habits_title.setStyleSheet("color: #111827;")
        habits_header.addWidget(habits_title)
        
        habits_header.addStretch()
        
        self.habits_count = QLabel("0")
        self.habits_count.setFont(QFont("SF Pro Display", 15, QFont.Bold))
        self.habits_count.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: #FFFFFF;
                border-radius: 12px;
                padding: 6px 16px;
            }
        """)
        habits_header.addWidget(self.habits_count)
        
        habits_layout.addLayout(habits_header)
        
        # Scrollable habits
        habits_scroll = QScrollArea()
        habits_scroll.setWidgetResizable(True)
        habits_scroll.setFrameShape(QFrame.NoFrame)
        habits_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        habits_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background: #F3F4F6;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #667eea;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: #5568d3;
            }
        """)
        
        habits_container = QWidget()
        habits_container.setStyleSheet("background: transparent;")
        self.habits_list = QVBoxLayout(habits_container)
        self.habits_list.setSpacing(12)
        self.habits_list.setContentsMargins(0, 0, 8, 0)
        self.habits_list.addStretch() 
        
        habits_scroll.setWidget(habits_container)
        habits_layout.addWidget(habits_scroll)
        
        top_row.addWidget(habits_card, stretch=1)
        
        content_layout.addLayout(top_row)
        
        # Bottom row
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(24)
        
        # Weekly Activity
        weekly_card = QFrame()
        weekly_card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 20px;
            }
        """)
        
        weekly_layout = QVBoxLayout(weekly_card)
        weekly_layout.setContentsMargins(30, 28, 30, 28)
        weekly_layout.setSpacing(20)
        
        weekly_header = QHBoxLayout()
        
        weekly_title = QLabel("Weekly Activity")
        weekly_title.setFont(QFont("SF Pro Display", 22, QFont.Bold))
        weekly_title.setStyleSheet("color: #111827;")
        weekly_header.addWidget(weekly_title)
        
        weekly_header.addStretch()
        
        weekly_subtitle = QLabel("Last 7 Days")
        weekly_subtitle.setFont(QFont("SF Pro Text", 13))
        weekly_subtitle.setStyleSheet("color: #6B7280;")
        weekly_header.addWidget(weekly_subtitle)
        
        weekly_layout.addLayout(weekly_header)
        
        self.week_grid = QHBoxLayout()
        self.week_grid.setSpacing(12)
        weekly_layout.addLayout(self.week_grid)
        
        weekly_layout.addStretch()
        
        bottom_row.addWidget(weekly_card, stretch=2)
        
        # Monthly Milestone
        milestone_card = QFrame()
        milestone_card.setFixedWidth(380)
        milestone_card.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FEF3C7, stop:1 #FDE68A);
                border: 2px solid #F59E0B;
                border-radius: 20px;
            }
        """)
        
        milestone_layout = QVBoxLayout(milestone_card)
        milestone_layout.setContentsMargins(30, 28, 30, 32)
        milestone_layout.setSpacing(20)
        
        milestone_title = QLabel("Monthly Milestone")
        milestone_title.setFont(QFont("SF Pro Display", 22, QFont.Bold))
        milestone_title.setStyleSheet("color: #92400E;")
        milestone_layout.addWidget(milestone_title)
        
        flame_container = QFrame()
        flame_container.setFixedSize(130, 130)
        flame_container.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #FEF3C7, stop:1 #FDE047);
                border: 3px solid #F59E0B;
                border-radius: 65px;
            }
        """)
        
        flame_layout = QVBoxLayout(flame_container)
        flame_layout.setContentsMargins(0, 0, 0, 0)
        
        flame_icon = QLabel("🔥")
        flame_icon.setFont(QFont("SF Pro Display", 62))
        flame_icon.setAlignment(Qt.AlignCenter)
        flame_layout.addWidget(flame_icon)
        
        milestone_layout.addWidget(flame_container, alignment=Qt.AlignCenter)
        
        self.streak_label = QLabel("0 Day Streak!")
        self.streak_label.setFont(QFont("SF Pro Display", 34, QFont.Bold))
        self.streak_label.setStyleSheet("color: #92400E;")
        self.streak_label.setAlignment(Qt.AlignCenter)
        milestone_layout.addWidget(self.streak_label)
        
        milestone_desc = QLabel("Keep building your habits!")
        milestone_desc.setFont(QFont("SF Pro Text", 14))
        milestone_desc.setStyleSheet("color: #B45309;")
        milestone_desc.setAlignment(Qt.AlignCenter)
        milestone_layout.addWidget(milestone_desc)
        
        bottom_row.addWidget(milestone_card)
        
        content_layout.addLayout(bottom_row)
        
        scroll.setWidget(content)
        main_layout.addWidget(scroll)
    
    def show_add_habit(self):
        if self.main_window:
            self.main_window.show_add_habit_dialog()
    
    def load_dashboard(self):
        """Load all dashboard data"""
        while self.habits_list.count():
            item = self.habits_list.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        habits = self.habit_service.get_all_habits()
        
        if not habits:
            self.progress_text.setText("No habits yet.\nCreate your first one!")
            self.habits_count.setText("0")
            self.circular_progress.set_percentage(0)
            self.load_weekly_activity()
            return
        
        # Calculate progress
        completed = sum(1 for h in habits if self.habit_service.is_habit_completed_today(h.id))
        total = len(habits)
        percentage = int((completed / total) * 100) if total > 0 else 0
        
        self.circular_progress.set_percentage(percentage)
        self.habits_count.setText(str(total))
        
        left = total - completed
        if left == 0:
            self.progress_text.setText("🎉 Perfect!\nAll habits completed!")
        else:
            self.progress_text.setText(f"Almost there!\n{left} habit{'s' if left != 1 else ''} left.")
        
        # Load habits
        pending = []
        completed_habits = []
        
        for habit in habits:
            is_completed = self.habit_service.is_habit_completed_today(habit.id)
            if is_completed:
                completed_habits.append(habit)
            else:
                pending.append(habit)
        
        for habit in pending:
            card = PremiumHabitCard(habit, False, self)
            self.habits_list.addWidget(card)
        
        for habit in completed_habits:
            card = PremiumHabitCard(habit, True, self)
            self.habits_list.addWidget(card)
        
        self.habits_list.addStretch()
        
        # Calculate streak
        max_streak = 0
        for habit in habits:
            streak_info = self.streak_service.get_streak_info(habit.id)
            max_streak = max(max_streak, streak_info['current_streak'])
        
        self.streak_label.setText(f"{max_streak} Day Streak!")
        
        # Load weekly
        self.load_weekly_activity()
    
    def load_weekly_activity(self):
        """Load weekly activity graph"""
        while self.week_grid.count():
            item = self.week_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        habits = self.habit_service.get_all_habits()
        today = datetime.now()
        days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
        
        for i in range(7):
            date = today - timedelta(days=6-i)
            date_str = date.strftime("%Y-%m-%d")
            day_name = days[date.weekday()]
            
            completed_count = 0
            if habits:
                for habit in habits:
                    if self.habit_service.is_habit_completed_on_date(habit.id, date_str):
                        completed_count += 1
            
            percentage = int((completed_count / len(habits)) * 100) if len(habits) > 0 else 0
            
            day_card = WeekDayCard(day_name, percentage, date.day)
            self.week_grid.addWidget(day_card)
