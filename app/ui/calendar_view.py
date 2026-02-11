"""
Calendar heatmap view - Qt-compatible modern design
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QScrollArea, QFrame, QWidget, QComboBox, QGridLayout,
    QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QCursor, QColor
from datetime import datetime, timedelta
from app.services.habit_service import get_habit_service
from app.services.streak_service import get_streak_service
from app.services.stats_service import get_stats_service


class CalendarDay(QFrame):
    """Single day cell - Modern design"""
    
    def __init__(self, date, is_completed, has_notes, is_current_month=True, parent=None):
        super().__init__(parent)
        self.date = date
        self.is_completed = is_completed
        self.has_notes = has_notes
        self.is_current_month = is_current_month
        self.is_today = date.date() == datetime.now().date()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup day cell with modern styling"""
        # Larger cells for current month
        if self.is_current_month:
            self.setFixedSize(45, 45)
        else:
            self.setFixedSize(32, 32)
        
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
        # Modern color scheme
        if self.is_completed:
            if self.has_notes:
                bg_color = "#10B981"  # Emerald green
                border_color = "#059669"
            else:
                bg_color = "#34D399"  # Light emerald
                border_color = "#10B981"
        else:
            bg_color = "#F3F4F6"  # Light gray
            border_color = "#E5E7EB"
        
        # Special styling for today
        if self.is_today:
            border_color = "#6366F1"  # Indigo
            border_width = "2px"
        else:
            border_width = "1px"
        
        self.setStyleSheet(f"""
            CalendarDay {{
                background-color: {bg_color};
                border: {border_width} solid {border_color};
                border-radius: 10px;
            }}
            CalendarDay:hover {{
                border: 2px solid #6366F1;
                background-color: {bg_color if self.is_completed else '#E0E7FF'};
            }}
        """)
        
        # Day number label
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)
        
        day_label = QLabel(str(self.date.day))
        day_label.setFont(QFont("Inter", 11 if self.is_current_month else 9, QFont.Medium))
        
        if self.is_completed:
            day_label.setStyleSheet("color: #FFFFFF; background: transparent;")
        else:
            day_label.setStyleSheet("color: #6B7280; background: transparent;")
        
        day_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(day_label)
        
        # Tooltip
        date_str = self.date.strftime("%B %d, %Y")
        if self.is_completed:
            if self.has_notes:
                tooltip = f"✅ {date_str}\nCompleted with notes"
            else:
                tooltip = f"✅ {date_str}\nCompleted"
        else:
            tooltip = f"{date_str}\nNot completed"
        
        self.setToolTip(tooltip)


class MonthCard(QFrame):
    """Month calendar card - Elevated card design"""
    
    def __init__(self, year, month, completions, notes_dates, is_current=False, parent=None):
        super().__init__(parent)
        self.year = year
        self.month = month
        self.completions = completions
        self.notes_dates = notes_dates
        self.is_current = is_current
        self.setup_ui()
    
    def setup_ui(self):
        """Setup month card"""
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        
        # Different padding for current month
        if self.is_current:
            self.setLineWidth(2)
            padding = "24px"
        else:
            self.setLineWidth(1)
            padding = "20px"
        
        self.setStyleSheet(f"""
            MonthCard {{
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 16px;
                padding: {padding};
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16 if self.is_current else 12)
        layout.setContentsMargins(
            24 if self.is_current else 20,
            24 if self.is_current else 20,
            24 if self.is_current else 20,
            24 if self.is_current else 20
        )
        
        # Header with month name and completion rate
        header_layout = QHBoxLayout()
        
        month_name = datetime(self.year, self.month, 1).strftime("%B %Y")
        title = QLabel(month_name)
        title.setFont(QFont("Inter", 20 if self.is_current else 16, QFont.Bold))
        title.setStyleSheet("color: #111827; background: transparent;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Calculate completion rate
        first_day = datetime(self.year, self.month, 1)
        if self.month == 12:
            last_day = datetime(self.year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = datetime(self.year, self.month + 1, 1) - timedelta(days=1)
        
        days_in_month = last_day.day
        completed_days = 0
        
        for day in range(1, days_in_month + 1):
            date_str = datetime(self.year, self.month, day).strftime("%Y-%m-%d")
            if date_str in self.completions:
                completed_days += 1
        
        completion_rate = int((completed_days / days_in_month) * 100) if days_in_month > 0 else 0
        
        # Completion badge
        badge = QLabel(f"{completion_rate}%")
        badge.setFont(QFont("Inter", 14 if self.is_current else 12, QFont.Bold))
        
        if completion_rate >= 80:
            badge_bg = "#D1FAE5"
            badge_color = "#059669"
        elif completion_rate >= 50:
            badge_bg = "#FEF3C7"
            badge_color = "#D97706"
        else:
            badge_bg = "#FEE2E2"
            badge_color = "#DC2626"
        
        badge.setStyleSheet(f"""
            QLabel {{
                color: {badge_color};
                background-color: {badge_bg};
                padding: 6px 12px;
                border-radius: 12px;
            }}
        """)
        header_layout.addWidget(badge)
        
        layout.addLayout(header_layout)
        
        # Day headers
        days_layout = QHBoxLayout()
        days_layout.setSpacing(4 if self.is_current else 3)
        
        days = ['M', 'T', 'W', 'T', 'F', 'S', 'S']
        for day in days:
            label = QLabel(day)
            label.setFont(QFont("Inter", 11 if self.is_current else 9, QFont.Medium))
            label.setStyleSheet("color: #9CA3AF; background: transparent;")
            label.setAlignment(Qt.AlignCenter)
            label.setFixedWidth(45 if self.is_current else 32)
            days_layout.addWidget(label)
        
        layout.addLayout(days_layout)
        
        # Calendar grid
        grid = QGridLayout()
        grid.setSpacing(6 if self.is_current else 4)
        
        first_day = datetime(self.year, self.month, 1)
        first_weekday = first_day.weekday()
        
        if self.month == 12:
            last_day = datetime(self.year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = datetime(self.year, self.month + 1, 1) - timedelta(days=1)
        
        days_in_month = last_day.day
        
        row = 0
        col = first_weekday
        
        for day in range(1, days_in_month + 1):
            date = datetime(self.year, self.month, day)
            date_str = date.strftime("%Y-%m-%d")
            
            is_completed = date_str in self.completions
            has_notes = date_str in self.notes_dates
            
            day_cell = CalendarDay(date, is_completed, has_notes, self.is_current)
            grid.addWidget(day_cell, row, col)
            
            col += 1
            if col > 6:
                col = 0
                row += 1
        
        layout.addLayout(grid)


class CalendarView(QDialog):
    """Modern calendar view"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.habit_service = get_habit_service()
        self.streak_service = get_streak_service()
        self.stats_service = get_stats_service()
        self.selected_habit = None
        self.setup_ui()
        self.load_calendar()
    
    def setup_ui(self):
        """Setup modern UI"""
        self.setWindowTitle("Calendar View")
        self.setModal(False)
        self.setMinimumSize(900, 800)
        self.setStyleSheet("""
            QDialog {
                background-color: #F9FAFB;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = QFrame()
        header.setFixedHeight(100)
        header.setFrameShape(QFrame.StyledPanel)
        header.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-bottom: 1px solid #E5E7EB;
            }
        """)
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(32, 20, 32, 20)
        
        # Title
        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)
        
        title = QLabel("📅 Progress Calendar")
        title.setFont(QFont("Inter", 24, QFont.Bold))
        title.setStyleSheet("color: #111827; background: transparent;")
        title_layout.addWidget(title)
        
        subtitle = QLabel("Track your consistency journey")
        subtitle.setFont(QFont("Inter", 13))
        subtitle.setStyleSheet("color: #6B7280; background: transparent;")
        title_layout.addWidget(subtitle)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        # Habit selector
        self.habit_combo = QComboBox()
        self.habit_combo.setFont(QFont("Inter", 13))
        self.habit_combo.setFixedHeight(48)
        self.habit_combo.setMinimumWidth(250)
        self.habit_combo.setCursor(Qt.PointingHandCursor)
        self.habit_combo.setStyleSheet("""
            QComboBox {
                padding: 12px 16px;
                border: 2px solid #E5E7EB;
                border-radius: 12px;
                background-color: #FFFFFF;
                color: #111827;
            }
            QComboBox:hover {
                border: 2px solid #6366F1;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 12px;
            }
            QComboBox::down-arrow {
                width: 0;
                height: 0;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #6B7280;
                margin-right: 8px;
            }
            QComboBox QAbstractItemView {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
                padding: 8px;
                color: #111827;
                selection-background-color: #6366F1;
                selection-color: #FFFFFF;
            }
        """)
        self.habit_combo.currentIndexChanged.connect(self.on_habit_changed)
        header_layout.addWidget(self.habit_combo)
        
        # Close button
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(48, 48)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setFont(QFont("Inter", 18))
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 2px solid #E5E7EB;
                border-radius: 24px;
                color: #6B7280;
            }
            QPushButton:hover {
                background-color: #FEE2E2;
                border: 2px solid #EF4444;
                color: #EF4444;
            }
        """)
        close_btn.clicked.connect(self.close)
        header_layout.addWidget(close_btn)
        
        layout.addWidget(header)
        
        # Content
        content = QWidget()
        content.setStyleSheet("background-color: #F9FAFB;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(32, 24, 32, 24)
        content_layout.setSpacing(20)
        
        # Streak card
        self.streak_card = QFrame()
        self.streak_card.setFrameShape(QFrame.StyledPanel)
        self.streak_card.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6366F1, stop:1 #8B5CF6);
                border-radius: 16px;
            }
        """)
        self.streak_card.setFixedHeight(120)
        
        streak_layout = QHBoxLayout(self.streak_card)
        streak_layout.setContentsMargins(24, 20, 24, 20)
        
        streak_left = QVBoxLayout()
        streak_left.setSpacing(4)
        
        streak_title = QLabel("Current Streak")
        streak_title.setFont(QFont("Inter", 14, QFont.Medium))
        streak_title.setStyleSheet("color: rgba(255, 255, 255, 0.9); background: transparent;")
        streak_left.addWidget(streak_title)
        
        self.streak_value = QLabel("0 days")
        self.streak_value.setFont(QFont("Inter", 32, QFont.Bold))
        self.streak_value.setStyleSheet("color: #FFFFFF; background: transparent;")
        streak_left.addWidget(self.streak_value)
        
        streak_layout.addLayout(streak_left)
        streak_layout.addStretch()
        
        flame_label = QLabel("🔥")
        flame_label.setFont(QFont("Inter", 48))
        flame_label.setStyleSheet("background: transparent;")
        streak_layout.addWidget(flame_label)
        
        content_layout.addWidget(self.streak_card)
        
        # Stats row
        stats_row = QHBoxLayout()
        stats_row.setSpacing(16)
        
        self.stat_cards = {}
        stat_items = [
            ("total", "Total Days", "✅", "#10B981", "#D1FAE5"),
            ("rate", "Success Rate", "📊", "#6366F1", "#E0E7FF"),
            ("best", "Best Streak", "🏆", "#F59E0B", "#FEF3C7")
        ]
        
        for key, title, emoji, color, bg in stat_items:
            card = QFrame()
            card.setFrameShape(QFrame.StyledPanel)
            card.setStyleSheet(f"""
                QFrame {{
                    background-color: #FFFFFF;
                    border-radius: 12px;
                    border-left: 4px solid {color};
                }}
            """)
            
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(16, 16, 16, 16)
            card_layout.setSpacing(8)
            
            emoji_label = QLabel(emoji)
            emoji_label.setFont(QFont("Inter", 24))
            emoji_label.setStyleSheet("background: transparent;")
            card_layout.addWidget(emoji_label)
            
            value_label = QLabel("0")
            value_label.setFont(QFont("Inter", 28, QFont.Bold))
            value_label.setStyleSheet(f"color: {color}; background: transparent;")
            card_layout.addWidget(value_label)
            
            title_label = QLabel(title)
            title_label.setFont(QFont("Inter", 11))
            title_label.setStyleSheet("color: #6B7280; background: transparent;")
            card_layout.addWidget(title_label)
            
            self.stat_cards[key] = value_label
            stats_row.addWidget(card)
        
        content_layout.addLayout(stats_row)
        
        # Legend
        legend = QFrame()
        legend.setFrameShape(QFrame.StyledPanel)
        legend.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 12px;
                border: 1px solid #E5E7EB;
            }
        """)
        legend_layout = QHBoxLayout(legend)
        legend_layout.setContentsMargins(16, 12, 16, 12)
        legend_layout.setSpacing(20)
        
        legend_title = QLabel("Legend:")
        legend_title.setFont(QFont("Inter", 12, QFont.Medium))
        legend_title.setStyleSheet("color: #111827; background: transparent;")
        legend_layout.addWidget(legend_title)
        
        legend_items = [
            ("#34D399", "Completed"),
            ("#10B981", "With notes"),
            ("#F3F4F6", "Missed")
        ]
        
        for color, text in legend_items:
            box = QFrame()
            box.setFixedSize(24, 24)
            box.setStyleSheet(f"background-color: {color}; border-radius: 6px; border: 1px solid #E5E7EB;")
            legend_layout.addWidget(box)
            
            label = QLabel(text)
            label.setFont(QFont("Inter", 11))
            label.setStyleSheet("color: #6B7280; background: transparent;")
            legend_layout.addWidget(label)
        
        legend_layout.addStretch()
        content_layout.addWidget(legend)
        
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
                background: #F3F4F6;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #D1D5DB;
                border-radius: 5px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: #9CA3AF;
            }
        """)
        
        self.months_container = QWidget()
        self.months_container.setStyleSheet("background-color: transparent;")
        self.months_layout = QVBoxLayout(self.months_container)
        self.months_layout.setSpacing(20)
        self.months_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll.setWidget(self.months_container)
        content_layout.addWidget(scroll)
        
        layout.addWidget(content)
    
    def load_calendar(self):
        """Load habits"""
        habits = self.habit_service.get_all_habits()
        
        self.habit_combo.clear()
        for habit in habits:
            from app.utils.constants import CATEGORIES
            emoji = "📌"
            for cat_name, cat_emoji in CATEGORIES:
                if cat_name == habit.category:
                    emoji = cat_emoji
                    break
            self.habit_combo.addItem(f"{emoji} {habit.name}", habit.id)
        
        if habits:
            self.selected_habit = habits[0]
            self.display_calendar()
    
    def on_habit_changed(self, index):
        """Handle habit change"""
        habit_id = self.habit_combo.currentData()
        if habit_id:
            self.selected_habit = self.habit_service.get_habit_by_id(habit_id)
            self.display_calendar()
    
    def display_calendar(self):
        """Display calendar"""
        if not self.selected_habit:
            return
        
        while self.months_layout.count():
            item = self.months_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        completions = self.habit_service.get_habit_completions(self.selected_habit.id)
        completion_set = set(completions)
        
        notes_dates = set()
        for date_str in completions:
            notes = self.habit_service.get_completion_notes(self.selected_habit.id, date_str)
            if notes:
                notes_dates.add(date_str)
        
        streak_info = self.streak_service.get_streak_info(self.selected_habit.id)
        stats = self.stats_service.get_habit_stats(self.selected_habit.id)
        
        self.streak_value.setText(f"{streak_info['current_streak']} days")
        self.stat_cards['total'].setText(str(stats['total_completions']))
        self.stat_cards['rate'].setText(f"{stats['completion_rate_30d']}%")
        self.stat_cards['best'].setText(str(streak_info['longest_streak']))
        
        today = datetime.now()
        current_month = MonthCard(
            today.year, today.month, 
            completion_set, notes_dates, 
            is_current=True
        )
        self.months_layout.addWidget(current_month)
        
        for i in range(1, 6):
            month = today.month - i
            year = today.year
            
            while month <= 0:
                month += 12
                year -= 1
            
            month_card = MonthCard(year, month, completion_set, notes_dates, is_current=False)
            self.months_layout.addWidget(month_card)
        
        self.months_layout.addStretch()
