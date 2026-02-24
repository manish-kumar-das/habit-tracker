"""
Goals & Milestones Content View - Premium Redesign
Beautiful goal tracking with progress visualization
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QScrollArea, QFrame, QGraphicsDropShadowEffect,
    QDialog, QComboBox, QSpinBox, QDialogButtonBox, QMessageBox
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtGui import QFont, QColor, QPainter, QPen, QLinearGradient
from datetime import datetime, timedelta
from app.services.goal_service import get_goal_service
from app.services.habit_service import get_habit_service


class CircularProgressGoal(QWidget):
    """Circular progress indicator for goals"""
    
    def __init__(self, percentage, size=80, parent=None):
        super().__init__(parent)
        self.percentage = percentage
        self.size = size
        self.setFixedSize(size, size)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        center = self.size / 2
        radius = (self.size - 10) / 2
        
        # Background circle
        painter.setPen(QPen(QColor("#E5E7EB"), 6))
        painter.drawEllipse(int(center - radius), int(center - radius), 
                          int(radius * 2), int(radius * 2))
        
        # Progress arc
        if self.percentage > 0:
            gradient = QLinearGradient(0, 0, self.size, self.size)
            gradient.setColorAt(0, QColor("#667eea"))
            gradient.setColorAt(1, QColor("#764ba2"))
            
            pen = QPen(gradient, 6)
            pen.setCapStyle(Qt.RoundCap)
            painter.setPen(pen)
            
            span_angle = int(-360 * (self.percentage / 100) * 16)
            painter.drawArc(int(center - radius), int(center - radius), 
                          int(radius * 2), int(radius * 2), 90 * 16, span_angle)
        
        # Percentage text
        painter.setPen(QColor("#111827"))
        painter.setFont(QFont("SF Pro Display", int(self.size / 4), QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, f"{int(self.percentage)}%")


class GoalCard(QFrame):
    """Premium goal card with animations"""
    
    def __init__(self, goal, habit, parent=None):
        super().__init__(parent)
        self.goal = goal
        self.habit = habit
        self.parent_view = parent
        self.goal_service = get_goal_service()
        self.setup_ui()
        
        # Hover animation
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(200)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
    
    def setup_ui(self):
        """Setup goal card UI"""
        self.setMinimumHeight(210)
        self.setSizePolicy(QFrame.Expanding, QFrame.Fixed)
        
        # Calculate progress
        # progress_percent = (self.goal.current_value / self.goal.target_value * 100) if self.goal.target_value > 0 else 0
        completions = getattr(self.habit, "completions", [])
        current_value = len(completions)

        # progress_percent = (
        #     current_value / self.goal.target_value * 100
        #     if self.goal.target_value > 0 else 0
        # )
        
        # Calculate progress dynamically from habit completions
        # habit = self.habit_service.get_habit_by_id(self.goal.habit_id)

        # completions = getattr(habit, "completions", [])
        # current_value = len(completions)

        progress_percent = (
            current_value / self.goal.target_value * 100
            if self.goal.target_value > 0 else 0
        )

        progress_text = QLabel(
            f"{current_value} / {self.goal.target_value} {self._get_unit()}"
        )


        # Status-based styling
        days_left = self._calculate_days_left()
        
        if self.goal.is_completed:
            bg_gradient = "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ECFDF5, stop:1 #D1FAE5)"
            border_color = "#10B981"
            status_color = "#059669"
        elif days_left <= 3 and progress_percent < 80:
            bg_gradient = "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FEF2F2, stop:1 #FEE2E2)"
            border_color = "#EF4444"
            status_color = "#DC2626"
        elif progress_percent >= 70:
            bg_gradient = "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FEF3C7, stop:1 #FDE68A)"
            border_color = "#F59E0B"
            status_color = "#D97706"
        else:
            bg_gradient = "#FFFFFF"
            border_color = "#6366F1"
            status_color = "#4F46E5"
        
        self.setStyleSheet(f"""
            QFrame {{
                background: {bg_gradient};
                border-left: 5px solid {border_color};
                border-radius: 20px;
            }}
        """)
        
        # Shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 8)
        self.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(20)
        
        # Top row: Progress circle + Info + Actions
        top_row = QHBoxLayout()
        top_row.setSpacing(24)
        
        # Left: Circular progress
        progress = CircularProgressGoal(progress_percent, size=100)
        top_row.addWidget(progress)
        
        # Middle: Goal info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(8)
        
        # Goal title
        title = QLabel(self.goal.goal_type.replace('_', ' ').title())
        title.setFont(QFont("SF Pro Display", 20, QFont.Bold))
        title.setStyleSheet("color: #111827;")
        info_layout.addWidget(title)
        
        # Habit name
        habit_label = QLabel(f"📌 {self.habit.name}")
        habit_label.setFont(QFont("SF Pro Text", 14))
        habit_label.setStyleSheet("color: #6B7280;")
        info_layout.addWidget(habit_label)
        
        
        # ===== Progress Text (CLEAN) =====
        progress_text = QLabel(f"{current_value} / {self.goal.target_value} {self._get_unit()}")
        progress_text.setFont(QFont("SF Pro Display", 16, QFont.Bold))
        progress_text.setStyleSheet(f"color: {status_color};")
        info_layout.addWidget(progress_text)
        top_row.addLayout(info_layout, 1)

        # Right: Actions
        actions_layout = QVBoxLayout()
        actions_layout.setSpacing(10)
        actions_layout.setAlignment(Qt.AlignTop)
        
        if not self.goal.is_completed:
            delete_btn = QPushButton("✕")
            delete_btn.setFixedSize(36, 36)
            delete_btn.setCursor(Qt.PointingHandCursor)
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(239, 68, 68, 0.1);
                    color: #EF4444;
                    border: none;
                    border-radius: 18px;
                    font-size: 18px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #EF4444;
                    color: #FFFFFF;
                }
            """)
            delete_btn.clicked.connect(self.delete_goal)
            actions_layout.addWidget(delete_btn)
        
        top_row.addLayout(actions_layout)
        
        layout.addLayout(top_row)
        
        # ===== Progress Bar =====
        progress_bar_container = QFrame()
        progress_bar_container.setFixedHeight(16)
        progress_bar_container.setStyleSheet("""
            QFrame {
                background-color: #E5E7EB;
                border-radius: 8px;
            }
        """)

        progress_bar_layout = QHBoxLayout(progress_bar_container)
        progress_bar_layout.setContentsMargins(0, 0, 0, 0)
        progress_bar_layout.setSpacing(0)

        progress_fill = QFrame()
        progress_fill.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 8px;
            }
        """)

        # Use stretch instead of fixed width
        progress_bar_layout.addWidget(progress_fill, int(progress_percent))
        progress_bar_layout.addStretch(100 - int(progress_percent))

        layout.addWidget(progress_bar_container)
        
        # Bottom row: Status + Date
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(20)
        
        # Status badge
        status_badge = QLabel()
        status_badge.setFont(QFont("SF Pro Text", 12, QFont.Bold))
        status_badge.setFixedHeight(32)
        status_badge.setAlignment(Qt.AlignCenter)
        
        if self.goal.is_completed:
            status_badge.setText("✓ Completed!")
            status_badge.setStyleSheet("""
                QLabel {
                    background-color: #10B981;
                    color: #FFFFFF;
                    border-radius: 16px;
                    padding: 0px 16px;
                }
            """)
        elif days_left <= 0:
            status_badge.setText("⏰ Overdue")
            status_badge.setStyleSheet("""
                QLabel {
                    background-color: #EF4444;
                    color: #FFFFFF;
                    border-radius: 16px;
                    padding: 0px 16px;
                }
            """)
        elif days_left <= 3:
            status_badge.setText(f"⚠️ {days_left} days left!")
            status_badge.setStyleSheet("""
                QLabel {
                    background-color: #F59E0B;
                    color: #FFFFFF;
                    border-radius: 16px;
                    padding: 0px 16px;
                }
            """)
        elif progress_percent >= 70:
            status_badge.setText("🎯 On track")
            status_badge.setStyleSheet("""
                QLabel {
                    background-color: #10B981;
                    color: #FFFFFF;
                    border-radius: 16px;
                    padding: 0px 16px;
                }
            """)
        else:
            status_badge.setText("📊 In progress")
            status_badge.setStyleSheet("""
                QLabel {
                    background-color: #6366F1;
                    color: #FFFFFF;
                    border-radius: 16px;
                    padding: 0px 16px;
                }
            """)
        
        bottom_row.addWidget(status_badge)
        
        bottom_row.addStretch()
        
        # Date info
        date_layout = QVBoxLayout()
        date_layout.setSpacing(2)
        
        started_label = QLabel(f"Started: {self.goal.created_at.split()[0] if hasattr(self.goal, 'created_at') else 'N/A'}")
        started_label.setFont(QFont("SF Pro Text", 11))
        started_label.setStyleSheet("color: #6B7280;")
        date_layout.addWidget(started_label)
        
        if not self.goal.is_completed:
            remaining_label = QLabel(f"{days_left} days remaining")
            remaining_label.setFont(QFont("SF Pro Text", 11, QFont.Bold))
            remaining_label.setStyleSheet(f"color: {status_color};")
            date_layout.addWidget(remaining_label)
        
        bottom_row.addLayout(date_layout)
        
        layout.addLayout(bottom_row)
    
    def _calculate_days_left(self):
        """Calculate days left for goal"""
        # Assuming 30 days for streak goals
        if hasattr(self.goal, 'created_at'):
            try:
                created = datetime.strptime(self.goal.created_at.split()[0], "%Y-%m-%d")
                target_date = created + timedelta(days=30)
                days_left = (target_date - datetime.now()).days
                return max(0, days_left)
            except:
                return 30
        return 30
    
    def _get_unit(self):
        """Get unit for goal type"""
        if 'streak' in self.goal.goal_type.lower():
            return "days"
        return "completions"
    
    def delete_goal(self):
        """Delete this goal"""
        reply = QMessageBox.question(
            self,
            "Delete Goal",
            f"Are you sure you want to delete this goal?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.goal_service.delete_goal(self.goal.id)
            if self.parent_view:
                self.parent_view.load_goals()
    
    def enterEvent(self, event):
        self.anim.stop()
        self.anim.setStartValue(self.pos())
        self.anim.setEndValue(self.pos() - QPoint(0, 4))
        self.anim.start()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self.anim.stop()
        self.anim.setStartValue(self.pos())
        self.anim.setEndValue(self.pos() + QPoint(0, 4))
        self.anim.start()
        super().leaveEvent(event)


class AddGoalDialog(QDialog):
    """Dialog to add new goal"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.habit_service = get_habit_service()
        self.setWindowTitle("Create New Goal")
        self.setFixedSize(500, 400)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup dialog UI"""
        self.setStyleSheet("""
            QDialog {
                background-color: #FFFFFF;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)
        
        # Title
        title = QLabel("🎯 Create New Goal")
        title.setFont(QFont("SF Pro Display", 24, QFont.Bold))
        title.setStyleSheet("color: #111827;")
        layout.addWidget(title)
        
        subtitle = QLabel("Set a target and track your progress")
        subtitle.setFont(QFont("SF Pro Text", 13))
        subtitle.setStyleSheet("color: #6B7280;")
        layout.addWidget(subtitle)
        
        # Habit selector
        habit_label = QLabel("Select Habit:")
        habit_label.setFont(QFont("SF Pro Text", 14, QFont.Bold))
        habit_label.setStyleSheet("color: #111827;")
        layout.addWidget(habit_label)
        
        self.habit_combo = QComboBox()
        self.habit_combo.setFont(QFont("SF Pro Text", 13))
        self.habit_combo.setFixedHeight(44)
        self.habit_combo.setStyleSheet("""
            QComboBox {
                background-color: #F9FAFB;
                border: 2px solid #E5E7EB;
                border-radius: 12px;
                padding: 8px 16px;
            }
            QComboBox:hover {
                border: 2px solid #6366F1;
            }
        """)
        
        habits = self.habit_service.get_all_habits()
        for habit in habits:
            self.habit_combo.addItem(habit.name, habit.id)
        
        layout.addWidget(self.habit_combo)
        
        # Goal type
        type_label = QLabel("Goal Type:")
        type_label.setFont(QFont("SF Pro Text", 14, QFont.Bold))
        type_label.setStyleSheet("color: #111827;")
        layout.addWidget(type_label)
        
        self.type_combo = QComboBox()
        self.type_combo.setFont(QFont("SF Pro Text", 13))
        self.type_combo.setFixedHeight(44)
        self.type_combo.setStyleSheet("""
            QComboBox {
                background-color: #F9FAFB;
                border: 2px solid #E5E7EB;
                border-radius: 12px;
                padding: 8px 16px;
            }
            QComboBox:hover {
                border: 2px solid #6366F1;
            }
        """)
        self.type_combo.addItems(["30_day_streak", "7_day_streak", "100_completions"])
        layout.addWidget(self.type_combo)
        
        # Target value
        target_label = QLabel("Target Value:")
        target_label.setFont(QFont("SF Pro Text", 14, QFont.Bold))
        target_label.setStyleSheet("color: #111827;")
        layout.addWidget(target_label)
        
        self.target_spin = QSpinBox()
        self.target_spin.setFont(QFont("SF Pro Text", 13))
        self.target_spin.setFixedHeight(44)
        self.target_spin.setMinimum(1)
        self.target_spin.setMaximum(365)
        self.target_spin.setValue(30)
        self.target_spin.setStyleSheet("""
            QSpinBox {
                background-color: #F9FAFB;
                border: 2px solid #E5E7EB;
                border-radius: 12px;
                padding: 8px 16px;
            }
            QSpinBox:hover {
                border: 2px solid #6366F1;
            }
        """)
        layout.addWidget(self.target_spin)
        
        layout.addStretch()
        
        # Buttons
        button_box = QDialogButtonBox()
        button_box.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.setStyleSheet("""
            QPushButton {
                background-color: #6366F1;
                color: #FFFFFF;
                border: none;
                border-radius: 10px;
                padding: 10px 24px;
                font-size: 14px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #4F46E5;
            }
        """)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def get_goal_data(self):
        """Return selected goal data"""
        return {
            'habit_id': self.habit_combo.currentData(),
            'goal_type': self.type_combo.currentText(),
            'target_value': self.target_spin.value()
        }


class GoalsContentView(QWidget):
    """Premium Goals & Milestones View"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.goal_service = get_goal_service()
        self.habit_service = get_habit_service()
        self.setup_ui()
        self.load_goals()
    
    def setup_ui(self):
        """Setup goals UI"""
        self.setStyleSheet("background-color: #F9FAFB;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = QFrame()
        header.setFixedHeight(120)
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FFFFFF, stop:1 #F9FAFB);
                border: none;
            }
        """)
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(40, 24, 40, 24)
        
        # Left: Title
        title_section = QHBoxLayout()
        title_section.setSpacing(12)
        
        icon = QLabel("🎯")
        icon.setFont(QFont("SF Pro Display", 32))
        icon.setStyleSheet("background: transparent;")
        title_section.addWidget(icon)
        
        title_text_layout = QVBoxLayout()
        title_text_layout.setSpacing(2)
        
        title = QLabel("Goals & Milestones")
        title.setFont(QFont("SF Pro Display", 28, QFont.Bold))
        title.setStyleSheet("color: #111827; background: transparent;")
        title_text_layout.addWidget(title)
        
        subtitle = QLabel("Set targets and track your progress")
        subtitle.setFont(QFont("SF Pro Text", 14))
        subtitle.setStyleSheet("color: #6B7280; background: transparent;")
        title_text_layout.addWidget(subtitle)
        
        title_section.addLayout(title_text_layout)
        
        header_layout.addLayout(title_section)
        header_layout.addStretch()
        
        # Right: New Goal button
        new_goal_btn = QPushButton("+ New Goal")
        new_goal_btn.setFont(QFont("SF Pro Text", 15, QFont.Bold))
        new_goal_btn.setFixedHeight(50)
        new_goal_btn.setCursor(Qt.PointingHandCursor)
        new_goal_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: #FFFFFF;
                border: none;
                border-radius: 12px;
                padding: 0px 32px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5568d3, stop:1 #6a4191);
            }
        """)
        new_goal_btn.clicked.connect(self.show_add_goal_dialog)
        header_layout.addWidget(new_goal_btn)
        
        layout.addWidget(header)
        
        # Content scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background: #F3F4F6;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #6366F1;
                border-radius: 5px;
            }
        """)
        
        content = QWidget()
        content.setStyleSheet("background-color: #F9FAFB;")
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setContentsMargins(40, 28, 40, 28)
        self.content_layout.setSpacing(24)
        
        scroll.setWidget(content)
        layout.addWidget(scroll)
    
    def load_goals(self):
        """Load all goals"""
        # Clear content
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        goals = self.goal_service.get_all_goals(include_completed=True)
        
        if not goals:
            # Empty state
            empty_container = QFrame()
            empty_container.setStyleSheet("""
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #FFFFFF, stop:1 #F9FAFB);
                    border: 3px dashed #E5E7EB;
                    border-radius: 24px;
                }
            """)
            empty_container.setMinimumHeight(300)
            
            empty_layout = QVBoxLayout(empty_container)
            empty_layout.setAlignment(Qt.AlignCenter)
            empty_layout.setSpacing(16)
            
            emoji = QLabel("🎯")
            emoji.setFont(QFont("SF Pro Display", 80))
            emoji.setAlignment(Qt.AlignCenter)
            emoji.setStyleSheet("background: transparent;")
            empty_layout.addWidget(emoji)
            
            empty_title = QLabel("No Goals Yet")
            empty_title.setFont(QFont("SF Pro Display", 26, QFont.Bold))
            empty_title.setAlignment(Qt.AlignCenter)
            empty_title.setStyleSheet("color: #374151; background: transparent;")
            empty_layout.addWidget(empty_title)
            
            empty_text = QLabel("Create your first goal to start tracking your progress!")
            empty_text.setFont(QFont("SF Pro Text", 15))
            empty_text.setAlignment(Qt.AlignCenter)
            empty_text.setStyleSheet("color: #9CA3AF; background: transparent;")
            empty_layout.addWidget(empty_text)
            
            self.content_layout.addWidget(empty_container)
            self.content_layout.addStretch()
            return
        
        # Separate active and completed
        active_goals = [g for g in goals if not g.is_completed]
        completed_goals = [g for g in goals if g.is_completed]
        
        # Active goals section
        if active_goals:
            active_header = QLabel(f"🎯 Active Goals ({len(active_goals)})")
            active_header.setFont(QFont("SF Pro Display", 22, QFont.Bold))
            active_header.setStyleSheet("color: #111827;")
            self.content_layout.addWidget(active_header)
            
            for goal in active_goals:
                habit = self.habit_service.get_habit_by_id(goal.habit_id)
                if habit:
                    card = GoalCard(goal, habit, self)
                    self.content_layout.addWidget(card)
        
        # Completed goals section
        if completed_goals:
            self.content_layout.addSpacing(20)
            
            completed_header = QLabel(f"✅ Completed Goals ({len(completed_goals)})")
            completed_header.setFont(QFont("SF Pro Display", 22, QFont.Bold))
            completed_header.setStyleSheet("color: #10B981;")
            self.content_layout.addWidget(completed_header)
            
            for goal in completed_goals:
                habit = self.habit_service.get_habit_by_id(goal.habit_id)
                if habit:
                    card = GoalCard(goal, habit, self)
                    self.content_layout.addWidget(card)
        
        self.content_layout.addStretch()
    
    def show_add_goal_dialog(self):
        """Show dialog to add new goal"""
        dialog = AddGoalDialog(self)
        if dialog.exec() == QDialog.Accepted:
            goal_data = dialog.get_goal_data()
            self.goal_service.create_goal(
                habit_id=goal_data['habit_id'],
                goal_type=goal_data['goal_type'],
                target_value=goal_data['target_value']
            )
            self.load_goals()