"""
Analytics Content View - Shows in main content area (not dialog)
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QScrollArea, QFrame, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QCursor
from app.services.habit_service import get_habit_service
from app.services.stats_service import get_stats_service


class AnalyticsContentView(QWidget):
    """Analytics view for content area"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.habit_service = get_habit_service()
        self.stats_service = get_stats_service()
        self.setup_ui()
        self.load_analytics()
    
    def setup_ui(self):
        """Setup analytics UI"""
        self.setStyleSheet("background-color: #F8F9FA;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = QFrame()
        header.setFixedHeight(100)
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6366F1, stop:1 #8B5CF6);
            }
        """)
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(32, 20, 32, 20)
        
        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)
        
        title = QLabel("📊 Analytics Dashboard")
        title.setFont(QFont("SF Pro Display", 24, QFont.Bold))
        title.setStyleSheet("color: #FFFFFF; background: transparent;")
        title_layout.addWidget(title)
        
        subtitle = QLabel("Track your habit performance and trends")
        subtitle.setFont(QFont("SF Pro Text", 13))
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.9); background: transparent;")
        title_layout.addWidget(subtitle)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
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
        self.content_layout.setSpacing(20)
        
        # Habit selector
        selector_layout = QHBoxLayout()
        
        label = QLabel("Select Habit:")
        label.setFont(QFont("SF Pro Text", 14, QFont.Medium))
        label.setStyleSheet("color: #212529;")
        selector_layout.addWidget(label)
        
        self.habit_combo = QComboBox()
        self.habit_combo.setFont(QFont("SF Pro Text", 13))
        self.habit_combo.setFixedHeight(44)
        self.habit_combo.setCursor(Qt.PointingHandCursor)
        self.habit_combo.setStyleSheet("""
            QComboBox {
                padding: 10px 16px;
                border: 2px solid #E5E7EB;
                border-radius: 10px;
                background-color: #FFFFFF;
                color: #111827;
                min-width: 250px;
            }
            QComboBox:hover { border: 2px solid #6366F1; }
        """)
        self.habit_combo.addItem("📊 All Habits Overview", None)
        self.habit_combo.currentIndexChanged.connect(self.on_habit_changed)
        selector_layout.addWidget(self.habit_combo)
        
        selector_layout.addStretch()
        
        self.content_layout.addLayout(selector_layout)
        
        # Stats cards container
        self.stats_container = QVBoxLayout()
        self.content_layout.addLayout(self.stats_container)
        
        self.content_layout.addStretch()
        
        scroll.setWidget(content)
        layout.addWidget(scroll)
    
    def load_analytics(self):
        """Load analytics data"""
        habits = self.habit_service.get_all_habits()
        
        # Clear combo
        self.habit_combo.clear()
        self.habit_combo.addItem("📊 All Habits Overview", None)
        
        for habit in habits:
            self.habit_combo.addItem(f"{habit.name}", habit.id)
        
        # Load initial view
        self.display_overview()
    
    def on_habit_changed(self):
        """Handle habit selection change"""
        habit_id = self.habit_combo.currentData()
        
        if habit_id is None:
            self.display_overview()
        else:
            self.display_habit_stats(habit_id)
    
    def display_overview(self):
        """Display overview of all habits"""
        # Clear stats
        while self.stats_container.count():
            item = self.stats_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        habits = self.habit_service.get_all_habits()
        
        if not habits:
            empty = QLabel("No habits to analyze yet.\nCreate habits to see analytics!")
            empty.setFont(QFont("SF Pro Text", 16))
            empty.setAlignment(Qt.AlignCenter)
            empty.setStyleSheet("color: #9CA3AF; padding: 60px;")
            self.stats_container.addWidget(empty)
            return
        
        # Stats cards row
        cards_row = QHBoxLayout()
        cards_row.setSpacing(16)
        
        # Total habits card
        total_card = self.create_stat_card("Total Habits", str(len(habits)), "🎯", "#6366F1")
        cards_row.addWidget(total_card)
        
        # Completed today
        completed_today = sum(1 for h in habits if self.habit_service.is_habit_completed_today(h.id))
        today_card = self.create_stat_card("Completed Today", f"{completed_today}/{len(habits)}", "✅", "#10B981")
        cards_row.addWidget(today_card)
        
        # Max streak
        max_streak = 0
        for habit in habits:
            from app.services.streak_service import get_streak_service
            streak_info = get_streak_service().get_streak_info(habit.id)
            max_streak = max(max_streak, streak_info['current_streak'])
        
        streak_card = self.create_stat_card("Best Streak", f"{max_streak} days", "🔥", "#F59E0B")
        cards_row.addWidget(streak_card)
        
        self.stats_container.addLayout(cards_row)
        
        # Recent habits list
        list_label = QLabel("All Habits")
        list_label.setFont(QFont("SF Pro Display", 18, QFont.Bold))
        list_label.setStyleSheet("color: #212529; margin-top: 16px;")
        self.stats_container.addWidget(list_label)
        
        for habit in habits:
            habit_card = self.create_habit_list_card(habit)
            self.stats_container.addWidget(habit_card)
    
    def display_habit_stats(self, habit_id):
        """Display stats for specific habit"""
        # Clear stats
        while self.stats_container.count():
            item = self.stats_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        habit = self.habit_service.get_habit_by_id(habit_id)
        if not habit:
            return
        
        try:
            stats = self.stats_service.get_habit_stats(habit_id)
        except:
            stats = {
                'total_completions': 0,
                'completion_rate_7d': 0,
                'completion_rate_30d': 0
            }
        
        # Stats cards
        cards_row = QHBoxLayout()
        cards_row.setSpacing(16)
        
        completions_card = self.create_stat_card("Total Completions", str(stats['total_completions']), "✅", "#10B981")
        cards_row.addWidget(completions_card)
        
        rate_7d_card = self.create_stat_card("7-Day Rate", f"{stats['completion_rate_7d']}%", "📊", "#6366F1")
        cards_row.addWidget(rate_7d_card)
        
        rate_30d_card = self.create_stat_card("30-Day Rate", f"{stats['completion_rate_30d']}%", "📈", "#8B5CF6")
        cards_row.addWidget(rate_30d_card)
        
        self.stats_container.addLayout(cards_row)
    
    def create_stat_card(self, title, value, icon, color):
        """Create a stat card"""
        card = QFrame()
        card.setFixedHeight(120)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #FFFFFF;
                border-left: 4px solid {color};
                border-radius: 12px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(8)
        
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("SF Pro Display", 32))
        icon_label.setStyleSheet("background: transparent;")
        layout.addWidget(icon_label)
        
        value_label = QLabel(value)
        value_label.setFont(QFont("SF Pro Display", 24, QFont.Bold))
        value_label.setStyleSheet(f"color: {color}; background: transparent;")
        layout.addWidget(value_label)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("SF Pro Text", 12))
        title_label.setStyleSheet("color: #6B7280; background: transparent;")
        layout.addWidget(title_label)
        
        return card
    
    def create_habit_list_card(self, habit):
        """Create habit list card"""
        card = QFrame()
        card.setFixedHeight(70)
        card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
            }
        """)
        
        layout = QHBoxLayout(card)
        layout.setContentsMargins(20, 12, 20, 12)
        
        name_label = QLabel(habit.name)
        name_label.setFont(QFont("SF Pro Text", 14, QFont.Medium))
        name_label.setStyleSheet("color: #212529;")
        layout.addWidget(name_label)
        
        layout.addStretch()
        
        category_label = QLabel(habit.category)
        category_label.setFont(QFont("SF Pro Text", 12))
        category_label.setStyleSheet("""
            QLabel {
                color: #6B7280;
                background-color: #F3F4F6;
                padding: 4px 12px;
                border-radius: 8px;
            }
        """)
        layout.addWidget(category_label)
        
        return card
