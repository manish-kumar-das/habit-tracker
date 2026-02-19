"""
Premium Dashboard View - ALL ISSUES FIXED
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QScrollArea, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QFont, QCursor, QPainter, QColor, QPen, QLinearGradient, QRadialGradient
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

        rect = QRectF(
            center_x - radius,
            center_y - radius,
            radius * 2,
            radius * 2
        )

        # top inner shadow
        top_shadow = QRadialGradient(
            center_x,
            center_y - 25,
            radius + 20
        )
        top_shadow.setColorAt(0.7, QColor(0, 0, 0, 0))
        top_shadow.setColorAt(1, QColor(0, 0, 0, 40))

        painter.setBrush(top_shadow)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(rect)

        # Background ring
        bg_pen = QPen(QColor("#E0E7FF"), 18)
        bg_pen.setCapStyle(Qt.RoundCap)
        painter.setPen(bg_pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawArc(rect, 0, 360 * 16)


        # Gradient Progress Arc
        if self.percentage > 0:
            gradient = QLinearGradient(
                center_x - radius,
                center_y,
                center_x + radius,
                center_y
            )
            gradient.setColorAt(0, QColor("#667eea"))
            gradient.setColorAt(0.5, QColor("#764ba2"))
            gradient.setColorAt(1, QColor("#f093fb"))

            progress_pen = QPen(gradient, 18)
            progress_pen.setCapStyle(Qt.RoundCap)
            painter.setPen(progress_pen)

            span_angle = int(-360 * (self.percentage / 100) * 16)
            painter.drawArc(rect, 90 * 16, span_angle)

        # Soft inner highlight
        highlight = QRadialGradient(
            center_x,
            center_y - 30,
            radius
        )
        highlight.setColorAt(0, QColor(255, 255, 255, 60))
        highlight.setColorAt(1, QColor(255, 255, 255, 0))

        painter.setBrush(highlight)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(rect.adjusted(18, 18, -18, -18))


        # Percentage Text
        painter.setPen(QColor("#111827"))
        painter.setFont(QFont("SF Pro Display", 42, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, f"{int(self.percentage)}%")


class HabitCard(QFrame):
    """
    Clean Modern Habit Card
    """

    def __init__(self, habit, is_completed=False, parent=None):
        super().__init__(parent)

        self.habit = habit
        self.is_completed = is_completed
        self.parent_view = parent
        self.habit_service = get_habit_service()

        self.setObjectName("habitCard")
        self.setFixedHeight(92)
        self.setCursor(Qt.PointingHandCursor)
        

        self.setup_ui()
        self.apply_shadow()

    # UI
    def setup_ui(self):

        self.setStyleSheet("""
            QFrame#habitCard {
                background-color: #FFFFFF;
                border-radius: 18px;
            }
            QFrame#habitCard:hover {
                background-color: #F8FAFF;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 14, 20, 14)
        layout.setSpacing(14)

        # Text Section 
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)

        name_label = QLabel(self.habit.name)
        name_label.setFont(QFont("SF Pro Display", 15, QFont.DemiBold))
        name_label.setStyleSheet("color: #1F2937;")

        subtitle = QLabel(f"{self.habit.category} • {self.habit.frequency}")
        subtitle.setFont(QFont("SF Pro Text", 12))
        subtitle.setStyleSheet("color: #9CA3AF;")

        text_layout.addWidget(name_label)

        layout.addLayout(text_layout)
        layout.addStretch()

        # Button 
        self.button = QPushButton()
        self.button.setFixedHeight(36)
        self.button.setMinimumWidth(130)
        self.button.setCursor(Qt.PointingHandCursor)
        self.button.setFont(QFont("SF Pro Text", 13, QFont.DemiBold))

        layout.addWidget(self.button)

        if self.is_completed:
            self.apply_completed_style()
        else:
            self.apply_default_style()

        self.button.clicked.connect(self.mark_complete)

    # Styles
    def apply_default_style(self):
        self.button.setText("Mark Done")
        self.button.setEnabled(True)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #EEF2FF;
                color: #4F46E5;
                border-radius: 14px;
                padding: 6px 16px;
            }
            QPushButton:hover {
                background-color: #E0E7FF;
            }
        """)

    def apply_completed_style(self):
        self.setStyleSheet("""
            QFrame#habitCard {
                background-color: #F9FAFB;
                border-radius: 18px;
                border-left: 4px solid #10B981;
            }
        """)

        self.button.setText("Completed ✓")
        self.button.setEnabled(False)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #D1FAE5;
                color: #065F46;
                border-radius: 14px;
                padding: 6px 16px;
            }
        """)

    # Shadow

    def apply_shadow(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(22)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(0, 0, 0, 35))
        self.setGraphicsEffect(shadow)

    # Action
    def mark_complete(self):
        try:
            self.habit_service.mark_habit_complete(self.habit.id)

            self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
            self.fade_animation.setDuration(180)
            self.fade_animation.setStartValue(1)
            self.fade_animation.setEndValue(0.7)
            self.fade_animation.start()


            if self.parent_view and hasattr(self.parent_view, "load_dashboard"):
                self.parent_view.load_dashboard()

        except Exception as e:
            print("Error:", e)

    # Styles
    def default_style(self):
        return """
        QFrame#habitCard {
            background-color: white;
            border-radius: 18px;
        }
        QFrame#habitCard:hover {
            background-color: #F8FAFF;
        }
        """

    def completed_style(self):
        return """
        QFrame#habitCard {
            background-color: #F9FAFB;
            border-radius: 18px;
            border-left: 4px solid #10B981;
        }
        """

    def mark_done_style(self):
        return """
        QPushButton {
            background-color: #EEF2FF;
            color: #4F46E5;
            border-radius: 16px;
            padding: 6px 16px;
            font-weight: 600;
        }
        QPushButton:hover {
            background-color: #E0E7FF;
        }
        """

    def completed_button_style(self):
        return """
        QPushButton {
            background-color: #D1FAE5;
            color: #065F46;
            border-radius: 16px;
            padding: 6px 16px;
            font-weight: 600;
        }
        """

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
        # date_str = today.strftime("%A, %B %dth")
        date_str = today.strftime(f"%A, %B {self._ordinal(today.day)}")


        
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
        self.apply_card_shadow(daily_card)

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
        habits_card.setObjectName("todayCard")
        habits_card.setFixedHeight(455)
        habits_card.setStyleSheet("""
            QFrame#todayCard {
                background-color: #FFFFFF;
                border-radius: 20px;
            }
        """)
        self.apply_card_shadow(habits_card)

        habits_layout = QVBoxLayout(habits_card)
        habits_layout.setContentsMargins(30, 28, 30, 28)
        habits_layout.setSpacing(16)
        
        habits_header = QHBoxLayout()
        habits_header.setContentsMargins(26, 0 , 26,  0)
        habits_header.setSpacing(15)
        
        habits_title = QLabel("Today's Habits")
        habits_title.setFont(QFont("SF Pro Display", 22, QFont.Bold))
        habits_title.setStyleSheet("background-color: transparent; color: #111827;")
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
    
        habits_layout.addLayout(habits_header)
        habits_layout.addSpacing(10)

        # Scrollable habits
        habits_scroll = QScrollArea()
        habits_scroll.setFrameShape(QFrame.NoFrame)
        habits_scroll.setWidgetResizable(True)
        habits_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
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

        # Wrap scroll inside inner recessed container
        habit_list_container = QFrame()
        habit_list_container.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 16px;
            }
        """)
       
        # APPLY UPWARD SHADOW
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 45))
        shadow.setOffset(0, 3)
        habit_list_container.setGraphicsEffect(shadow)

        inner_layout = QVBoxLayout(habit_list_container)
        inner_layout.setContentsMargins(15, 0, 15, 0)
        inner_layout.addWidget(habits_scroll)

        habits_layout.addWidget(habit_list_container)
        
        habits_container = QWidget()
        habits_container.setStyleSheet("background: transparent;")
        self.habits_list = QVBoxLayout(habits_container)
        self.habits_list.setSpacing(16)
        self.habits_list.setContentsMargins(12, 12, 12, 12)
        self.habits_list.setAlignment(Qt.AlignTop)
        
        habits_scroll.setWidget(habits_container)
        
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
        milestone_card.setFixedHeight(310)
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
    
    def _ordinal(self, n):
        if 11 <= n % 100 <= 13:
            return f"{n}th"
        return f"{n}{['th','st','nd','rd','th','th','th','th','th','th'][n % 10]}"

    def show_add_habit(self):
        if self.main_window:
            self.main_window.show_add_habit_dialog()
    
    def load_dashboard(self):
        """Load all dashboard data"""

        # Clear existing habit cards
        while self.habits_list.count():
            item = self.habits_list.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Fetch habits
        habits = self.habit_service.get_all_habits()

        if not habits:
            self.progress_text.setText("No habits yet.\nCreate your first one!")
            self.habits_count.setText("0")
            self.circular_progress.set_percentage(0)
            self.streak_label.setText("0 Day Streak!")
            self.load_weekly_activity()
            return

        # ✅ Cache completion results (ONLY one call per habit)
        completion_map = {
            habit.id: self.habit_service.is_habit_completed_today(habit.id)
            for habit in habits
        }

        # Calculate progress
        completed = sum(1 for done in completion_map.values() if done)
        total = len(habits)
        percentage = int((completed / total) * 100) if total > 0 else 0

        self.circular_progress.set_percentage(percentage)
        self.habits_count.setText(str(total))

        left = total - completed
        if left == 0:
            self.progress_text.setText("🎉 Perfect!\nAll habits completed!")
        else:
            self.progress_text.setText(
                f"Almost there!\n{left} habit{'s' if left != 1 else ''} left."
            )

        # Separate habits using cached results
        pending = []
        completed_habits = []

        for habit in habits:
            if completion_map[habit.id]:
                completed_habits.append(habit)
            else:
                pending.append(habit)

        # Add pending first
        for habit in pending:
            card = HabitCard(habit, False, self)
            self.habits_list.addWidget(card)

        # Then completed
        for habit in completed_habits:
            card = HabitCard(habit, True, self)
            self.habits_list.addWidget(card)

        self.habits_list.addStretch()

        # Calculate max streak
        max_streak = 0
        for habit in habits:
            streak_info = self.streak_service.get_streak_info(habit.id)
            current = streak_info.get('current_streak', 0)
            max_streak = max(max_streak, current)

        self.streak_label.setText(f"{max_streak} Day Streak!")

        # Load weekly activity
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

    def apply_card_shadow(self, widget):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(35)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 8)
        widget.setGraphicsEffect(shadow)

