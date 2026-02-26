"""
Goals & Milestones Content View - Premium Redesign
Beautiful goal tracking with progress visualization
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QFrame,
    QGraphicsDropShadowEffect,
    QDialog,
    QComboBox,
    QSpinBox,
    QMessageBox,
    QSizePolicy,
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
        painter.drawEllipse(
            int(center - radius), int(center - radius), int(radius * 2), int(radius * 2)
        )

        # Progress arc
        if self.percentage > 0:
            gradient = QLinearGradient(0, 0, 0, self.size)
            gradient.setColorAt(0, QColor("#667eea"))
            gradient.setColorAt(0.5, QColor("#764ba2"))
            gradient.setColorAt(1, QColor("#f093fb"))

            pen = QPen(gradient, 6)
            pen.setCapStyle(Qt.RoundCap)
            painter.setPen(pen)

            span_angle = int(-360 * (self.percentage / 100) * 16)
            painter.drawArc(
                int(center - radius),
                int(center - radius),
                int(radius * 2),
                int(radius * 2),
                90 * 16,
                span_angle,
            )

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
        self.setMinimumHeight(240)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Calculate progress
        current_value = self.goal.current_value

        progress_percent = (
            current_value / self.goal.target_value * 100
            if self.goal.target_value > 0
            else 0
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

        self.setObjectName("goalCard")
        self.setStyleSheet(f"""
            QFrame#goalCard {{
                background: {bg_gradient};
                border-radius: 20px;
                border: 1px solid rgba(0, 0, 0, 0.05);
            }}
            QLabel {{
                border: none;
                background: transparent;
            }}
        """)

        # Shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 8)
        self.setGraphicsEffect(shadow)

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
        title = QLabel(self.goal.goal_type.replace("_", " ").title())
        title.setFont(QFont("SF Pro Display", 20, QFont.Bold))
        title.setStyleSheet("color: #111827;")
        info_layout.addWidget(title)

        # Habit name
        habit_label = QLabel(f"📌 {self.habit.name}")
        habit_label.setFont(QFont("SF Pro Text", 14))
        habit_label.setStyleSheet("color: #6B7280;")
        info_layout.addWidget(habit_label)

        # ===== Progress Text (CLEAN) =====
        progress_text = QLabel(
            f"{current_value} / {self.goal.target_value} {self._get_unit()}"
        )
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

        # Accent strip (Fixes bracket glitch and provides status color)
        # Using a layout trick to place it correctly
        outer_layout = QHBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        accent_strip = QFrame()
        accent_strip.setFixedWidth(6)
        accent_strip.setStyleSheet(f"""
            QFrame {{
                background-color: {border_color};
                border-top-left-radius: 20px;
                border-bottom-left-radius: 20px;
            }}
        """)
        outer_layout.addWidget(accent_strip)

        card_content = QWidget()
        card_content.setObjectName("cardContent")
        card_content.setStyleSheet(
            "QWidget#cardContent { background: transparent; border: none; }"
        )
        outer_layout.addWidget(card_content, 1)

        layout = QVBoxLayout(card_content)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(20)

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
        progress_fill.setObjectName("progressFill")
        progress_fill.setStyleSheet("""
            QFrame#progressFill {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:0.5 #764ba2, stop:1 #f093fb);
                border-radius: 8px;
                border: none;
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

        started_label = QLabel(
            f"Started: {self.goal.created_at.split()[0] if hasattr(self.goal, 'created_at') else 'N/A'}"
        )
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
        if hasattr(self.goal, "created_at"):
            try:
                created = datetime.strptime(self.goal.created_at.split()[0], "%Y-%m-%d")
                target_date = created + timedelta(days=30)
                days_left = (target_date - datetime.now()).days
                return max(0, days_left)
            except Exception:
                return 30
        return 30

    def _get_unit(self):
        """Get unit for goal type"""
        if "streak" in self.goal.goal_type.lower():
            return "days"
        return "completions"

    def delete_goal(self):
        """Delete this goal"""
        reply = QMessageBox.question(
            self,
            "Delete Goal",
            "Are you sure you want to delete this goal?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
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
    """Dialog to add new goal - COMPLETELY FIXED"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.habit_service = get_habit_service()
        self.setWindowTitle("Create New Goal")
        self.setModal(True)
        self.setFixedSize(520, 480)
        self.setup_ui()

    def setup_ui(self):
        """Setup dialog UI"""
        self.setStyleSheet("""
            QDialog {
                background-color: #FFFFFF;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(36, 36, 36, 36)
        layout.setSpacing(24)

        # Title
        title_layout = QHBoxLayout()

        icon = QLabel("🎯")
        icon.setFont(QFont("SF Pro Display", 32))
        title_layout.addWidget(icon)

        title = QLabel("Create New Goal")
        title.setFont(QFont("SF Pro Display", 26, QFont.Bold))
        title.setStyleSheet("color: #111827;")
        title_layout.addWidget(title)

        title_layout.addStretch()

        layout.addLayout(title_layout)

        subtitle = QLabel("Set a target and track your progress")
        subtitle.setFont(QFont("SF Pro Text", 14))
        subtitle.setStyleSheet("color: #6B7280;")
        layout.addWidget(subtitle)

        layout.addSpacing(12)

        # Habit selector
        habit_label = QLabel("Select Habit:")
        habit_label.setFont(QFont("SF Pro Text", 14, QFont.Bold))
        habit_label.setStyleSheet("color: #374151;")
        layout.addWidget(habit_label)

        self.habit_combo = QComboBox()
        self.habit_combo.setFont(QFont("SF Pro Text", 14))
        self.habit_combo.setFixedHeight(48)
        self.habit_combo.setCursor(Qt.PointingHandCursor)
        self.habit_combo.setStyleSheet("""
            QComboBox {
                background-color: #F9FAFB;
                border: 2px solid #E5E7EB;
                border-radius: 12px;
                padding: 10px 16px;
                color: #111827;
            }
            QComboBox:hover {
                border: 2px solid #6366F1;
                background-color: #FFFFFF;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 12px;
            }
            QComboBox QAbstractItemView {
                background-color: #FFFFFF;
                border: 2px solid #E5E7EB;
                border-radius: 8px;
                selection-background-color: #EEF2FF;
                selection-color: #4F46E5;
                padding: 4px;
            }
        """)

        habits = self.habit_service.get_all_habits()
        if not habits:
            QMessageBox.warning(
                self,
                "No Habits",
                "Please create at least one habit before creating a goal.",
            )
            self.reject()
            return

        for habit in habits:
            self.habit_combo.addItem(habit.name, habit.id)

        layout.addWidget(self.habit_combo)

        # Goal type
        type_label = QLabel("Goal Type:")
        type_label.setFont(QFont("SF Pro Text", 14, QFont.Bold))
        type_label.setStyleSheet("color: #374151;")
        layout.addWidget(type_label)

        self.type_combo = QComboBox()
        self.type_combo.setFont(QFont("SF Pro Text", 14))
        self.type_combo.setFixedHeight(48)
        self.type_combo.setCursor(Qt.PointingHandCursor)
        self.type_combo.setStyleSheet("""
            QComboBox {
                background-color: #F9FAFB;
                border: 2px solid #E5E7EB;
                border-radius: 12px;
                padding: 10px 16px;
                color: #111827;
            }
            QComboBox:hover {
                border: 2px solid #6366F1;
                background-color: #FFFFFF;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 12px;
            }
            QComboBox QAbstractItemView {
                background-color: #FFFFFF;
                border: 2px solid #E5E7EB;
                border-radius: 8px;
                selection-background-color: #EEF2FF;
                selection-color: #4F46E5;
                padding: 4px;
            }
        """)

        # CRITICAL FIX: Store value in UserRole, not as second parameter
        self.type_combo.addItem("🔥 7 Day Streak", "7_day_streak")
        self.type_combo.addItem("🌟 30 Day Streak", "30_day_streak")
        self.type_combo.addItem("💯 100 Completions", "100_completions")

        # Set default
        self.type_combo.setCurrentIndex(1)  # 30 day streak

        self.type_combo.currentIndexChanged.connect(self._update_target_value)

        layout.addWidget(self.type_combo)

        # Target value
        target_label = QLabel("Target Value:")
        target_label.setFont(QFont("SF Pro Text", 14, QFont.Bold))
        target_label.setStyleSheet("color: #374151;")
        layout.addWidget(target_label)

        self.target_spin = QSpinBox()
        self.target_spin.setFont(QFont("SF Pro Text", 14))
        self.target_spin.setFixedHeight(48)
        self.target_spin.setMinimum(1)
        self.target_spin.setMaximum(365)
        self.target_spin.setValue(30)
        self.target_spin.setCursor(Qt.PointingHandCursor)
        self.target_spin.setStyleSheet("""
            QSpinBox {
                background-color: #F9FAFB;
                border: 2px solid #E5E7EB;
                border-radius: 12px;
                padding: 10px 16px;
                color: #111827;
            }
            QSpinBox:hover {
                border: 2px solid #6366F1;
                background-color: #FFFFFF;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 20px;
                border: none;
            }
        """)
        layout.addWidget(self.target_spin)

        layout.addStretch()

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFont(QFont("SF Pro Text", 14, QFont.Bold))
        cancel_btn.setFixedHeight(48)
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #F3F4F6;
                color: #374151;
                border: none;
                border-radius: 12px;
                padding: 0px 28px;
            }
            QPushButton:hover {
                background-color: #E5E7EB;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        create_btn = QPushButton("Create Goal")
        create_btn.setFont(QFont("SF Pro Text", 14, QFont.Bold))
        create_btn.setFixedHeight(48)
        create_btn.setCursor(Qt.PointingHandCursor)
        create_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:0.5 #764ba2, stop:1 #f093fb);
                color: #FFFFFF;
                border: none;
                border-radius: 12px;
                padding: 0px 32px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5568d3, stop:0.5 #6a4191, stop:1 #e07af0);
            }
        """)
        create_btn.clicked.connect(self.accept)
        button_layout.addWidget(create_btn)

        layout.addLayout(button_layout)

    def _update_target_value(self):
        """Update target value based on goal type"""
        goal_type = self.type_combo.currentData()

        print(f"[_update_target_value] Current type: {goal_type}")

        if goal_type == "7_day_streak":
            self.target_spin.setValue(7)
        elif goal_type == "30_day_streak":
            self.target_spin.setValue(30)
        elif goal_type == "100_completions":
            self.target_spin.setValue(100)

    def get_goal_data(self):
        """Return selected goal data - FIXED VERSION"""
        habit_id = self.habit_combo.currentData()
        goal_type = self.type_combo.currentData()
        target_value = self.target_spin.value()

        print("\n[AddGoalDialog.get_goal_data] Returning:")
        print(f"  habit_id={habit_id} (type: {type(habit_id).__name__})")
        print(f"  goal_type={goal_type} (type: {type(goal_type).__name__})")
        print(f"  target_value={target_value} (type: {type(target_value).__name__})")

        # Validate
        if not habit_id:
            print("  ⚠️ WARNING: habit_id is None!")
        if not goal_type:
            print("  ⚠️ WARNING: goal_type is None!")
        if not target_value or target_value <= 0:
            print("  ⚠️ WARNING: target_value is invalid!")

        return {
            "habit_id": habit_id,
            "goal_type": goal_type,
            "target_value": target_value,
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
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:0.5 #764ba2, stop:1 #f093fb);
                color: #FFFFFF;
                border: none;
                border-radius: 12px;
                padding: 0px 32px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5568d3, stop:0.5 #6a4191, stop:1 #e07af0);
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

            empty_text = QLabel(
                "Create your first goal to start tracking your progress!"
            )
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
        """Show dialog to add new goal - WITH DEBUG LOGGING"""
        print("\n" + "=" * 50)
        print("🎯 STARTING ADD GOAL PROCESS")
        print("=" * 50)

        try:
            # Step 1: Check habits exist
            print("\n[1] Checking for habits...")
            habits = self.habit_service.get_all_habits()
            print(f"   ✓ Found {len(habits)} habits")

            if not habits:
                print("   ✗ ERROR: No habits found!")
                QMessageBox.warning(
                    self,
                    "No Habits Available",
                    "⚠️ You need to create at least one habit before creating a goal.\n\nPlease go to the Dashboard and click '+ New Habit' first.",
                    QMessageBox.Ok,
                )
                return

            # Step 2: Create dialog
            print("\n[2] Creating dialog...")
            dialog = AddGoalDialog(self)
            print("   ✓ Dialog created successfully")

            # Step 3: Show dialog
            print("\n[3] Showing dialog...")
            result = dialog.exec()
            print(f"   ✓ Dialog result: {result} (1=Accepted, 0=Rejected)")

            if result != QDialog.Accepted:
                print("   ℹ User cancelled dialog")
                return

            # Step 4: Get goal data
            print("\n[4] Getting goal data from dialog...")
            goal_data = dialog.get_goal_data()
            print("   ✓ Goal data received:")
            print(f"      - Habit ID: {goal_data['habit_id']}")
            print(f"      - Goal Type: {goal_data['goal_type']}")
            print(f"      - Target Value: {goal_data['target_value']}")

            # Step 5: Create goal
            print("\n[5] Creating goal in database...")
            goal_id = self.goal_service.create_goal(
                habit_id=goal_data["habit_id"],
                goal_type=goal_data["goal_type"],
                target_value=goal_data["target_value"],
            )
            print(f"   ✓ Goal created with ID: {goal_id}")

            if not goal_id:
                raise Exception("create_goal returned None or 0")

            # Step 6: Reload goals
            print("\n[6] Reloading goals list...")
            self.load_goals()
            print("   ✓ Goals reloaded successfully")

            # Step 7: Success message
            print("\n[7] Showing success message...")
            QMessageBox.information(
                self,
                "Goal Created",
                f"✅ Goal created successfully!\n\nYour {goal_data['goal_type'].replace('_', ' ')} goal has been added.",
                QMessageBox.Ok,
            )

            print("✅ GOAL CREATION COMPLETED SUCCESSFULLY")
            print("=" * 50 + "\n")

        except Exception as e:
            print("\n" + "=" * 50)
            print("❌ ERROR IN GOAL CREATION")
            print("=" * 50)
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")

            import traceback

            print("\nFull traceback:")
            traceback.print_exc()
            print("=" * 50 + "\n")

            QMessageBox.critical(
                self,
                "Error Creating Goal",
                f"❌ Failed to create goal:\n\n{str(e)}\n\nPlease check the console for details.",
                QMessageBox.Ok,
            )
