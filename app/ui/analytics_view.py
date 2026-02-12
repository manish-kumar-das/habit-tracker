"""
Advanced Analytics Dashboard - Charts and insights
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QScrollArea, QFrame, QWidget, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QCursor
from datetime import datetime, timedelta
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from app.services.habit_service import get_habit_service
from app.services.streak_service import get_streak_service
from app.services.stats_service import get_stats_service


class ChartCard(QFrame):
    """Card containing a chart"""
    
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.title = title
        self.setup_ui()
    
    def setup_ui(self):
        """Setup card UI"""
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("""
            ChartCard {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 16px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)
        
        title_label = QLabel(self.title)
        title_label.setFont(QFont("Inter", 16, QFont.Bold))
        title_label.setStyleSheet("color: #111827; background: transparent;")
        layout.addWidget(title_label)
        
        self.chart_layout = QVBoxLayout()
        layout.addLayout(self.chart_layout)
    
    def add_chart(self, canvas):
        """Add matplotlib canvas to card"""
        self.chart_layout.addWidget(canvas)


class InsightCard(QFrame):
    """Insight/tip card"""
    
    def __init__(self, icon, title, message, color="#6366F1", parent=None):
        super().__init__(parent)
        self.setup_ui(icon, title, message, color)
    
    def setup_ui(self, icon, title, message, color):
        """Setup insight card"""
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(f"""
            InsightCard {{
                background-color: #FFFFFF;
                border-radius: 12px;
                border-left: 4px solid {color};
            }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(16)
        
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Inter", 32))
        icon_label.setStyleSheet("background: transparent;")
        icon_label.setFixedSize(48, 48)
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)
        
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Inter", 14, QFont.Bold))
        title_label.setStyleSheet(f"color: {color}; background: transparent;")
        text_layout.addWidget(title_label)
        
        message_label = QLabel(message)
        message_label.setFont(QFont("Inter", 12))
        message_label.setStyleSheet("color: #6B7280; background: transparent;")
        message_label.setWordWrap(True)
        text_layout.addWidget(message_label)
        
        layout.addLayout(text_layout, stretch=1)


class AnalyticsView(QDialog):
    """Advanced Analytics Dashboard"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.habit_service = get_habit_service()
        self.streak_service = get_streak_service()
        self.stats_service = get_stats_service()
        self.selected_habit = None
        
        plt.style.use('seaborn-v0_8-pastel')
        
        self.setup_ui()
        self.load_analytics()
    
    def setup_ui(self):
        """Setup dashboard UI"""
        self.setWindowTitle("Analytics Dashboard")
        self.setModal(False)
        self.setMinimumSize(1100, 800)
        self.setStyleSheet("QDialog { background-color: #F9FAFB; }")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = QFrame()
        header.setFixedHeight(100)
        header.setFrameShape(QFrame.StyledPanel)
        header.setStyleSheet("QFrame { background-color: #FFFFFF; border-bottom: 1px solid #E5E7EB; }")
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(32, 20, 32, 20)
        
        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)
        
        title = QLabel("📊 Analytics Dashboard")
        title.setFont(QFont("Inter", 24, QFont.Bold))
        title.setStyleSheet("color: #111827; background: transparent;")
        title_layout.addWidget(title)
        
        subtitle = QLabel("Understand your habits with data")
        subtitle.setFont(QFont("Inter", 13))
        subtitle.setStyleSheet("color: #6B7280; background: transparent;")
        title_layout.addWidget(subtitle)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
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
            QComboBox:hover { border: 2px solid #6366F1; }
            QComboBox QAbstractItemView {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                selection-background-color: #6366F1;
                selection-color: #FFFFFF;
            }
        """)
        self.habit_combo.currentIndexChanged.connect(self.on_habit_changed)
        header_layout.addWidget(self.habit_combo)
        
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
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        content = QWidget()
        content.setStyleSheet("background-color: #F9FAFB;")
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setContentsMargins(32, 24, 32, 24)
        self.content_layout.setSpacing(24)
        
        scroll.setWidget(content)
        layout.addWidget(scroll)
    
    def load_analytics(self):
        """Load habits"""
        habits = self.habit_service.get_all_habits()
        
        self.habit_combo.clear()
        self.habit_combo.addItem("📊 All Habits", None)
        
        for habit in habits:
            from app.utils.constants import CATEGORIES
            emoji = "📌"
            for cat_name, cat_emoji in CATEGORIES:
                if cat_name == habit.category:
                    emoji = cat_emoji
                    break
            self.habit_combo.addItem(f"{emoji} {habit.name}", habit.id)
        
        if habits:
            self.display_analytics()
    
    def on_habit_changed(self, index):
        """Handle habit change"""
        habit_id = self.habit_combo.currentData()
        if habit_id:
            self.selected_habit = self.habit_service.get_habit_by_id(habit_id)
        else:
            self.selected_habit = None
        
        self.display_analytics()
    
    def display_analytics(self):
        """Display analytics"""
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        if self.selected_habit:
            self.display_single_habit_analytics()
        else:
            self.display_all_habits_analytics()
    
    def display_single_habit_analytics(self):
        """Display single habit analytics"""
        habit = self.selected_habit
        
        completions = self.habit_service.get_habit_completions(habit.id)
        streak_info = self.streak_service.get_streak_info(habit.id)
        stats = self.stats_service.get_habit_stats(habit.id)
        
        insights_label = QLabel("💡 Key Insights")
        insights_label.setFont(QFont("Inter", 18, QFont.Bold))
        insights_label.setStyleSheet("color: #111827; background: transparent;")
        self.content_layout.addWidget(insights_label)
        
        insights = self.generate_insights(habit, completions, streak_info, stats)
        
        for insight in insights:
            insight_card = InsightCard(
                insight['icon'],
                insight['title'],
                insight['message'],
                insight['color']
            )
            self.content_layout.addWidget(insight_card)
        
        charts_label = QLabel("📈 Detailed Analysis")
        charts_label.setFont(QFont("Inter", 18, QFont.Bold))
        charts_label.setStyleSheet("color: #111827; background: transparent; margin-top: 16px;")
        self.content_layout.addWidget(charts_label)
        
        trend_card = ChartCard("30-Day Completion Trend")
        trend_card.add_chart(self.create_trend_chart(completions))
        self.content_layout.addWidget(trend_card)
        
        weekly_card = ChartCard("Weekly Breakdown")
        weekly_card.add_chart(self.create_weekly_chart(completions))
        self.content_layout.addWidget(weekly_card)
        
        self.content_layout.addStretch()
    
    def display_all_habits_analytics(self):
        """Display all habits overview"""
        all_stats = self.stats_service.get_all_habits_stats()
        
        if not all_stats:
            empty_label = QLabel("No habits to analyze.\nAdd some habits!")
            empty_label.setFont(QFont("Inter", 16))
            empty_label.setAlignment(Qt.AlignCenter)
            empty_label.setStyleSheet("color: #9CA3AF; padding: 80px;")
            self.content_layout.addWidget(empty_label)
            return
        
        self.content_layout.addStretch()
    
    def generate_insights(self, habit, completions, streak_info, stats):
        """Generate insights"""
        insights = []
        
        current_streak = streak_info['current_streak']
        longest_streak = streak_info['longest_streak']
        
        if current_streak > 0:
            if current_streak >= longest_streak:
                insights.append({
                    'icon': '🔥',
                    'title': 'New Record!',
                    'message': f"You're on your longest streak at {current_streak} days!",
                    'color': '#F59E0B'
                })
            elif current_streak >= 7:
                insights.append({
                    'icon': '💪',
                    'title': 'Great Momentum',
                    'message': f"{current_streak}-day streak. Keep it up!",
                    'color': '#10B981'
                })
        
        rate_7d = stats['completion_rate_7d']
        rate_30d = stats['completion_rate_30d']
        
        if rate_7d > rate_30d + 10:
            insights.append({
                'icon': '📈',
                'title': 'Improving Trend',
                'message': f"7-day rate ({rate_7d}%) > 30-day ({rate_30d}%). Getting better!",
                'color': '#10B981'
            })
        
        # FIXED: Best day insight
        if completions:
            try:
                weekly_breakdown = self.stats_service.get_weekly_completion_count(habit.id)
                if weekly_breakdown and len(weekly_breakdown) > 0:
                    # Get max day
                    max_count = max(weekly_breakdown.values())
                    best_day_num = [k for k, v in weekly_breakdown.items() if v == max_count][0]
                    
                    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                    insights.append({
                        'icon': '📅',
                        'title': f'{day_names[best_day_num]} is Your Best Day',
                        'message': f"{max_count} completions on {day_names[best_day_num]}s.",
                        'color': '#6366F1'
                    })
            except:
                pass  # Skip if no weekly data
        
        return insights
    
    def create_trend_chart(self, completions):
        """30-day trend"""
        fig = Figure(figsize=(10, 4), facecolor='#FFFFFF')
        ax = fig.add_subplot(111)
        
        today = datetime.now().date()
        dates = [(today - timedelta(days=i)) for i in range(29, -1, -1)]
        
        completion_set = set(completions)
        values = [1 if date.strftime("%Y-%m-%d") in completion_set else 0 for date in dates]
        
        ax.plot(dates, values, marker='o', linewidth=2, markersize=6, color='#6366F1')
        ax.fill_between(dates, values, alpha=0.3, color='#6366F1')
        
        ax.set_xlabel('Date', fontsize=10, color='#6B7280')
        ax.set_ylabel('Completed', fontsize=10, color='#6B7280')
        ax.set_ylim(-0.1, 1.1)
        ax.set_yticks([0, 1])
        ax.set_yticklabels(['No', 'Yes'])
        ax.grid(True, alpha=0.2)
        ax.tick_params(axis='x', rotation=45, labelsize=8)
        
        fig.tight_layout()
        
        canvas = FigureCanvas(fig)
        canvas.setFixedHeight(350)
        return canvas
    
    def create_weekly_chart(self, completions):
        """Weekly breakdown"""
        fig = Figure(figsize=(10, 4), facecolor='#FFFFFF')
        ax = fig.add_subplot(111)
        
        weekly_data = {}
        for date_str in completions:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            weekday = date.weekday()
            weekly_data[weekday] = weekly_data.get(weekday, 0) + 1
        
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        counts = [weekly_data.get(i, 0) for i in range(7)]
        
        max_count = max(counts) if counts else 0
        colors = ['#10B981' if c == max_count and c > 0 else '#6366F1' for c in counts]
        
        ax.bar(days, counts, color=colors, alpha=0.8)
        ax.set_xlabel('Day of Week', fontsize=10, color='#6B7280')
        ax.set_ylabel('Total Completions', fontsize=10, color='#6B7280')
        ax.grid(axis='y', alpha=0.2)
        
        fig.tight_layout()
        
        canvas = FigureCanvas(fig)
        canvas.setFixedHeight(350)
        return canvas
