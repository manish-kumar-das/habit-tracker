"""
Goals & Milestones Content View - Premium Redesign
Beautiful goal tracking with progress visualization
"""
import logging
logger = logging.getLogger(__name__)


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
from app.themes import get_theme_manager


def style_msgbox(msg):
    """Apply premium styling to QMessageBox based on theme"""
    from app.themes import get_theme_manager
    if get_theme_manager().is_dark_mode():
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #1A1C23;
                border-radius: 20px;
            }
            QLabel {
                color: #F3F4F6;
                font-family: 'SF Pro Text';
                font-size: 14px;
            }
            QPushButton {
                background-color: #333645;
                color: #F3F4F6;
                border: 1px solid #4B5563;
                border-radius: 8px;
                padding: 6px 20px;
                min-width: 80px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #404354;
            }
            QPushButton[text="&Yes"] {
                background-color: #EF4444;
                color: white;
                border: none;
            }
            QPushButton[text="&Yes"]:hover {
                background-color: #DC2626;
            }
        """)


class CircularProgressGoal(QWidget):
    """Circular progress indicator for goals"""

    def __init__(self, percentage, size=80, parent=None):
        super().__init__(parent)
        from app.themes import get_theme_manager
        self.theme_manager = get_theme_manager()
        self.percentage = percentage
        self.size = size
        self.setFixedSize(size, size)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        center = self.size / 2
        radius = (self.size - 10) / 2

        is_dark = self.theme_manager.is_dark_mode()
        colors = self.theme_manager.get_theme()
        
        # Background circle
        track_color = QColor(colors.BORDER_DEFAULT if is_dark else "#E5E7EB")
        painter.setPen(QPen(track_color, 6))
        painter.drawEllipse(
            int(center - radius), int(center - radius), int(radius * 2), int(radius * 2)
        )

        # Progress arc
        if self.percentage > 0:
            # Use a vibrant purple gradient stopped at theme colors
            gradient = QLinearGradient(0, 0, 0, self.size)
            gradient.setColorAt(0, QColor("#A78BFA")) # PUROLE_500
            gradient.setColorAt(1, QColor("#8B5CF6")) # PURPLE_400

            pen = QPen(gradient, 6)
            pen.setCapStyle(Qt.RoundCap)
            painter.setPen(pen)

            span_angle = int(-360 * (min(self.percentage, 100) / 100) * 16)
            painter.drawArc(
                int(center - radius),
                int(center - radius),
                int(radius * 2),
                int(radius * 2),
                90 * 16,
                span_angle,
            )

        # Percentage text
        text_color = QColor(colors.TEXT_PRIMARY)
        painter.setPen(text_color)
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

        # Status-based styling (Senior UX Refresh)
        days_left = self._calculate_days_left()
        theme_manager = get_theme_manager()
        colors = theme_manager.get_theme()
        is_dark = theme_manager.is_dark_mode()

        if self.goal.is_completed:
            bg_gradient = f"qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {colors.GREEN_50}, stop:1 {colors.BG_CARD})" if is_dark else "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ECFDF5, stop:1 #D1FAE5)"
            border_color = colors.GREEN_500
            status_color = colors.GREEN_500
        elif days_left <= 3 and progress_percent < 80:
            bg_gradient = f"qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {colors.RED_50}, stop:1 {colors.BG_CARD})" if is_dark else "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FEF2F2, stop:1 #FEE2E2)"
            border_color = colors.RED_500
            status_color = colors.RED_500
        elif progress_percent >= 70:
            bg_gradient = f"qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {colors.ORANGE_50}, stop:1 {colors.BG_CARD})" if is_dark else "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FEF3C7, stop:1 #FDE68A)"
            border_color = colors.ORANGE_500
            status_color = colors.ORANGE_500
        else:
            bg_gradient = colors.BG_CARD if is_dark else "#FFFFFF"
            border_color = colors.BORDER_LIGHT if is_dark else "rgba(0,0,0,0.1)"
            status_color = colors.PURPLE_500

        self.setObjectName("goalCard")
        border_rgba = "rgba(255, 255, 255, 0.1)" if is_dark else "rgba(0, 0, 0, 0.05)"
        self.setStyleSheet(f"""
            QFrame#goalCard {{
                background: {bg_gradient};
                border-radius: 20px;
                border: 1px solid {border_rgba};
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
        title.setStyleSheet(f"color: {colors.TEXT_PRIMARY};")
        info_layout.addWidget(title)

        # Habit name
        habit_label = QLabel(f"📌 {self.habit.name}")
        habit_label.setFont(QFont("SF Pro Text", 14))
        habit_label.setStyleSheet(f"color: {colors.TEXT_SECONDARY};")
        info_layout.addWidget(habit_label)

        # ===== Progress Text (CLEAN) =====
        progress_text = QLabel(
            f"{current_value} / {self.goal.target_value} {self._get_unit()}"
        )
        progress_text.setFont(QFont("SF Pro Display", 16, QFont.Bold))
        progress_text_color = colors.PURPLE_600 if is_dark else status_color
        progress_text.setStyleSheet(f"color: {progress_text_color};")
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
        progress_bar_container.setFixedHeight(12) # Slimmer, more modern
        track_bg = colors.BORDER_LIGHT if is_dark else "#E5E7EB"
        progress_bar_container.setStyleSheet(f"""
            QFrame {{
                background-color: {track_bg};
                border-radius: 6px;
            }}
        """)

        progress_bar_layout = QHBoxLayout(progress_bar_container)
        progress_bar_layout.setContentsMargins(0, 0, 0, 0)
        progress_bar_layout.setSpacing(0)

        progress_fill = QFrame()
        progress_fill.setObjectName("progressFill")
        progress_fill.setStyleSheet(f"""
            QFrame#progressFill {{
                background: {colors.GRADIENT_PURPLE};
                border-radius: 6px;
                border: none;
            }}
        """)

        # Use stretch instead of fixed width
        progress_bar_layout.addWidget(progress_fill, int(min(progress_percent, 100)))
        progress_bar_layout.addStretch(100 - int(min(progress_percent, 100)))

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
            status_badge.setStyleSheet(f"""
                QLabel {{
                    background-color: {colors.GREEN_500 if is_dark else "#10B981"};
                    color: white;
                    border-radius: 12px;
                    padding: 0px 16px;
                }}
            """)
        elif days_left <= 0:
            status_badge.setText("⏰ Overdue")
            status_badge.setStyleSheet(f"""
                QLabel {{
                    background-color: {colors.RED_500 if is_dark else "#EF4444"};
                    color: white;
                    border-radius: 12px;
                    padding: 0px 16px;
                }}
            """)
        elif days_left <= 3:
            status_badge.setText(f"⚠️ {days_left} days left!")
            status_badge.setStyleSheet(f"""
                QLabel {{
                    background-color: {colors.ORANGE_500 if is_dark else "#F59E0B"};
                    color: white;
                    border-radius: 12px;
                    padding: 0px 16px;
                }}
            """)
        elif progress_percent >= 70:
            status_badge.setText("🎯 On track")
            status_badge.setStyleSheet(f"""
                QLabel {{
                    background-color: {colors.GREEN_500 if is_dark else "#10B981"};
                    color: white;
                    border-radius: 12px;
                    padding: 0px 16px;
                }}
            """)
        else:
            status_badge.setText("📊 In progress")
            status_badge.setStyleSheet(f"""
                QLabel {{
                    background-color: {colors.PURPLE_500 if is_dark else "#6366F1"};
                    color: white;
                    border-radius: 12px;
                    padding: 0px 16px;
                }}
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
        started_label.setStyleSheet(f"color: {colors.TEXT_TERTIARY};")
        date_layout.addWidget(started_label)

        if not self.goal.is_completed:
            remaining_label = QLabel(f"{days_left} days remaining")
            remaining_label.setFont(QFont("SF Pro Text", 11, QFont.Bold))
            remaining_color = colors.PURPLE_400 if is_dark else status_color
            remaining_label.setStyleSheet(f"color: {remaining_color};")
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
        msg = QMessageBox(self)
        msg.setWindowTitle("Delete Goal")
        msg.setText("Are you sure you want to delete this goal?")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        style_msgbox(msg)
            
        reply = msg.exec()

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
        self.theme_manager = get_theme_manager()
        self.setWindowTitle("Create New Goal")
        self.setModal(True)
        self.setFixedSize(540, 620) # Slightly taller and wider for balance
        self.setup_ui()

    def setup_ui(self):
        """Setup dialog UI with theme support"""
        colors = self.theme_manager.get_theme()
        is_dark = self.theme_manager.is_dark_mode()
        
        bg_color = colors.BG_CARD
        text_primary = colors.TEXT_PRIMARY
        text_secondary = colors.TEXT_SECONDARY
        border_color = colors.BORDER_LIGHT
        input_bg = colors.BG_PRIMARY if is_dark else "#F9FAFB"

        self.setStyleSheet(f"""
            QDialog {{
                background-color: {bg_color};
                border-radius: 24px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(24)

        # Title Section
        title_layout = QHBoxLayout()
        icon = QLabel("🎯")
        icon.setFont(QFont("SF Pro Display", 32))
        icon.setFixedSize(48, 48) # Fixed size to prevent cutting
        icon.setStyleSheet("background: transparent; border: none;")
        title_layout.addWidget(icon)

        title = QLabel("Create New Goal")
        title.setFont(QFont("SF Pro Display", 26, QFont.Bold))
        title.setStyleSheet(f"color: {text_primary}; background: transparent; border: none;")
        title_layout.addWidget(title)
        title_layout.addStretch()
        layout.addLayout(title_layout)

        subtitle = QLabel("Set a target and track your progress")
        subtitle.setFont(QFont("SF Pro Text", 14))
        subtitle.setStyleSheet(f"color: {text_secondary};")
        layout.addWidget(subtitle)

        # Helper for common combo styles
        combo_style = f"""
            QComboBox {{
                background-color: {input_bg};
                border: 2px solid {border_color};
                border-radius: 12px;
                padding: 10px 16px;
                color: {text_primary};
            }}
            QComboBox:hover {{
                border: 2px solid {colors.PURPLE_500};
            }}
            QComboBox::drop-down {{
                border: none;
                padding-right: 12px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: 8px;
                selection-background-color: {colors.PURPLE_50};
                selection-color: {colors.PURPLE_500};
                outline: none;
            }}
        """

        # Habit Selector
        habit_label = QLabel("Select Habit:")
        habit_label.setFont(QFont("SF Pro Text", 14, QFont.Bold))
        habit_label.setStyleSheet(f"color: {text_primary};")
        layout.addWidget(habit_label)

        self.habit_combo = QComboBox()
        self.habit_combo.setFont(QFont("SF Pro Text", 14))
        self.habit_combo.setFixedHeight(52)
        self.habit_combo.setStyleSheet(combo_style)
        
        habits = self.habit_service.get_all_habits()
        if not habits:
            msg = QMessageBox(self)
            msg.setWindowTitle("No Habits")
            msg.setText("Please create at least one habit first.")
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            style_msgbox(msg)
            msg.exec()
            self.reject()
            return
        for habit in habits:
            self.habit_combo.addItem(habit.name, habit.id)
        layout.addWidget(self.habit_combo)

        # Goal Type
        type_label = QLabel("Goal Type:")
        type_label.setFont(QFont("SF Pro Text", 14, QFont.Bold))
        type_label.setStyleSheet(f"color: {text_primary};")
        layout.addWidget(type_label)

        self.type_combo = QComboBox()
        self.type_combo.setFont(QFont("SF Pro Text", 14))
        self.type_combo.setFixedHeight(52)
        self.type_combo.setStyleSheet(combo_style)
        self.type_combo.addItem("🔥 7 Day Streak", "7_day_streak")
        self.type_combo.addItem("🌟 30 Day Streak", "30_day_streak")
        self.type_combo.addItem("💯 100 Completions", "100_completions")
        self.type_combo.setCurrentIndex(1)
        self.type_combo.currentIndexChanged.connect(self._update_target_value)
        layout.addWidget(self.type_combo)

        # Target Value
        target_label = QLabel("Target Value:")
        target_label.setFont(QFont("SF Pro Text", 14, QFont.Bold))
        target_label.setStyleSheet(f"color: {text_primary};")
        layout.addWidget(target_label)

        self.target_spin = QSpinBox()
        self.target_spin.setFont(QFont("SF Pro Text", 14))
        self.target_spin.setFixedHeight(52)
        self.target_spin.setMinimum(1)
        self.target_spin.setMaximum(365)
        self.target_spin.setValue(30)
        self.target_spin.setStyleSheet(f"""
            QSpinBox {{
                background-color: {input_bg};
                border: 2px solid {border_color};
                border-radius: 12px;
                padding: 10px 16px;
                color: {text_primary};
            }}
            QSpinBox:hover {{
                border: 2px solid {colors.PURPLE_500};
            }}
            QSpinBox::up-button, QSpinBox::down-button {{
                width: 24px;
                border: none;
                background: transparent;
            }}
        """)
        layout.addWidget(self.target_spin)

        layout.addStretch()

        # Action Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(16)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFont(QFont("SF Pro Text", 14, QFont.Bold))
        cancel_btn.setFixedHeight(52)
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {colors.BG_PRIMARY if is_dark else "#F3F4F6"};
                color: {text_primary};
                border: 1px solid {border_color};
                border-radius: 14px;
                padding: 0px 32px;
            }}
            QPushButton:hover {{
                background-color: {colors.BORDER_LIGHT};
            }}
        """)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        create_btn = QPushButton("Create Goal")
        create_btn.setFont(QFont("SF Pro Text", 14, QFont.Bold))
        create_btn.setFixedHeight(52)
        create_btn.setCursor(Qt.PointingHandCursor)
        create_btn.setStyleSheet(f"""
            QPushButton {{
                background: {colors.GRADIENT_PURPLE};
                color: white;
                border: none;
                border-radius: 14px;
                padding: 0px 36px;
            }}
            QPushButton:hover {{
                background: {colors.GRADIENT_PURPLE_VIBRANT};
            }}
        """)
        create_btn.clicked.connect(self.accept)
        button_layout.addWidget(create_btn)

        layout.addLayout(button_layout)

    def _update_target_value(self):
        """Update target value based on goal type"""
        goal_type = self.type_combo.currentData()

        logger.info(f"[_update_target_value] Current type: {goal_type}")

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

        logger.info("\n[AddGoalDialog.get_goal_data] Returning:")
        logger.info(f"  habit_id={habit_id} (type: {type(habit_id).__name__})")
        logger.info(f"  goal_type={goal_type} (type: {type(goal_type).__name__})")
        logger.info(f"  target_value={target_value} (type: {type(target_value).__name__})")

        # Validate
        if not habit_id:
            logger.info("  ⚠️ WARNING: habit_id is None!")
        if not goal_type:
            logger.info("  ⚠️ WARNING: goal_type is None!")
        if not target_value or target_value <= 0:
            logger.info("  ⚠️ WARNING: target_value is invalid!")

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
        self.theme_manager = get_theme_manager()
        self.setup_ui()
        self.load_goals()

    def setup_ui(self):
        """Setup goals UI with premium dark mode support"""
        colors = self.theme_manager.get_theme()
        
        bg_primary = colors.BG_PRIMARY
        self.setStyleSheet(f"""
            GoalsContentView {{ 
                background-color: {bg_primary}; 
            }}
            QLabel {{ 
                border: none; 
                background: transparent; 
                text-decoration: none;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        self.header = QFrame()
        self.header.setMinimumHeight(140)
        header_bg = colors.BG_PRIMARY
        self.header.setStyleSheet(f"""
            QFrame {{
                background-color: {header_bg};
                border: none;
            }}
        """)

        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(40, 24, 40, 24)

        # Left: Title
        title_section = QHBoxLayout()
        title_section.setSpacing(12)

        icon = QLabel("🎯")
        icon.setFont(QFont("SF Pro Display", 32))
        icon.setStyleSheet("background: transparent; border: none;")
        title_section.addWidget(icon)

        title_text_layout = QVBoxLayout()
        title_text_layout.setSpacing(2)

        self.title_label = QLabel("Goals & Milestones")
        self.title_label.setFont(QFont("SF Pro Display", 28, QFont.Bold))
        self.title_label.setStyleSheet(
            f"color: {colors.TEXT_PRIMARY}; background: transparent; border: none;"
        )
        self.title_label.setWordWrap(True)
        title_text_layout.addWidget(self.title_label)

        self.subtitle_label = QLabel("Set targets and track your progress")
        self.subtitle_label.setFont(QFont("SF Pro Text", 14))
        self.subtitle_label.setStyleSheet(
            f"color: {colors.TEXT_SECONDARY}; background: transparent; border: none; text-decoration: none;"
        )
        self.subtitle_label.setWordWrap(True)
        title_text_layout.addWidget(self.subtitle_label)

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

        layout.addWidget(self.header)

        # Content scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        scroll_bg = colors.BG_PRIMARY
        scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {scroll_bg};
            }}
            QScrollBar:vertical {{
                background: {"#1A1C23" if self.theme_manager.is_dark_mode() else "transparent"};
                width: 10px;
                margin: 0px 4px 0px 0px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical {{
                background: #6366F1;
                min-height: 40px;
                border-radius: 5px;
                opacity: 0.8;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)

        self.content = QWidget()
        self.content.setObjectName("mainContent")
        self.content.setStyleSheet(f"QWidget#mainContent {{ background-color: {colors.BG_PRIMARY}; }}")
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(40, 40, 40, 40)
        self.content_layout.setSpacing(28)

        scroll.setWidget(self.content)
        layout.addWidget(scroll)

    def apply_theme(self):
        """Apply theme dynamically"""
        colors = self.theme_manager.get_theme()
        
        self.setStyleSheet(f"""
            GoalsContentView {{ 
                background-color: {colors.BG_PRIMARY}; 
            }}
            QLabel {{ 
                border: none; 
                background: transparent; 
                text-decoration: none;
            }}
        """)
        
        if hasattr(self, 'header'):
            self.header.setStyleSheet(f"""
                QFrame {{
                    background-color: {colors.BG_PRIMARY};
                    border: none;
                }}
            """)
            
        if hasattr(self, 'content'):
            self.content.setStyleSheet(f"QWidget#mainContent {{ background-color: {colors.BG_PRIMARY}; }}")
            
        if hasattr(self, 'title_label'):
            self.title_label.setStyleSheet(f"color: {colors.TEXT_PRIMARY}; background: transparent; border: none; text-decoration: none;")
            
        if hasattr(self, 'subtitle_label'):
            self.subtitle_label.setStyleSheet(f"color: {colors.TEXT_SECONDARY}; background: transparent; border: none; text-decoration: none;")

    def load_goals(self):
        """Load all goals"""
        # Clear content
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        goals = self.goal_service.get_all_goals(include_completed=True)

        if not goals:
            # Modern Empty State
            is_dark = self.theme_manager.is_dark_mode()
            colors = self.theme_manager.get_theme()
            
            empty_container = QFrame()
            empty_container.setFixedHeight(450)
            
            card_bg = colors.BG_CARD if is_dark else "white"
            border_rgba = "rgba(255, 255, 255, 0.05)" if is_dark else "rgba(0, 0, 0, 0.05)"
            
            empty_container.setStyleSheet(f"""
                QFrame {{
                    background-color: {card_bg};
                    border: 1px solid {border_rgba};
                    border-radius: 32px;
                }}
                QLabel {{
                    border: none;
                    background: transparent;
                }}
            """)
            
            # Add subtle shadow for empty state
            empty_shadow = QGraphicsDropShadowEffect()
            empty_shadow.setBlurRadius(40)
            empty_shadow.setColor(QColor(0, 0, 0, 50))
            empty_shadow.setOffset(0, 15)
            empty_container.setGraphicsEffect(empty_shadow)

            empty_layout = QVBoxLayout(empty_container)
            empty_layout.setAlignment(Qt.AlignCenter)
            empty_layout.setContentsMargins(40, 40, 40, 40)
            empty_layout.setSpacing(24)

            # Circular container for icon
            icon_container = QFrame()
            icon_container.setFixedSize(140, 140)
            icon_container.setStyleSheet(f"""
                QFrame {{
                    background: {colors.PURPLE_50 if is_dark else "#F3F4F6"};
                    border-radius: 70px;
                }}
            """)
            icon_layout = QVBoxLayout(icon_container)
            icon_layout.setAlignment(Qt.AlignCenter)
            
            emoji = QLabel("🎯")
            emoji.setFont(QFont("SF Pro Display", 64))
            emoji.setAlignment(Qt.AlignCenter)
            emoji.setStyleSheet("background: transparent;")
            icon_layout.addWidget(emoji)
            
            empty_layout.addWidget(icon_container, 0, Qt.AlignCenter)

            empty_title = QLabel("Focus Your Journey")
            empty_title.setFont(QFont("SF Pro Display", 28, QFont.Bold))
            empty_title.setAlignment(Qt.AlignCenter)
            empty_title.setStyleSheet(f"color: {colors.TEXT_PRIMARY}; background: transparent; border: none;")
            empty_layout.addWidget(empty_title)

            empty_text = QLabel(
                "Break down your habits into achievable goals.\nSet a target and watch your consistency grow."
            )
            empty_text.setFont(QFont("SF Pro Text", 15))
            empty_text.setAlignment(Qt.AlignCenter)
            empty_text.setStyleSheet(f"color: {colors.TEXT_SECONDARY}; background: transparent; border: none;")
            empty_layout.addWidget(empty_text)
            
            start_btn = QPushButton("Create Your First Goal")
            start_btn.setFont(QFont("SF Pro Text", 14, QFont.Bold))
            start_btn.setFixedSize(240, 52)
            start_btn.setCursor(Qt.PointingHandCursor)
            start_btn.setStyleSheet(f"""
                QPushButton {{
                    background: {colors.GRADIENT_PURPLE};
                    color: white;
                    border-radius: 16px;
                    border: none;
                }}
                QPushButton:hover {{
                    background: {colors.GRADIENT_PURPLE_VIBRANT};
                }}
            """)
            start_btn.clicked.connect(self.show_add_goal_dialog)
            empty_layout.addWidget(start_btn, 0, Qt.AlignCenter)

            self.content_layout.addWidget(empty_container)
            self.content_layout.addStretch()
            return

        # Separate active and completed
        active_goals = [g for g in goals if not g.is_completed]
        completed_goals = [g for g in goals if g.is_completed]

        # Active goals section
        if active_goals:
            is_dark = self.theme_manager.is_dark_mode()
            colors = self.theme_manager.get_theme()
            active_header = QLabel(f"🎯 Active Goals ({len(active_goals)})")
            active_header.setFont(QFont("SF Pro Display", 22, QFont.Bold))
            active_header.setStyleSheet(f"color: {colors.TEXT_PRIMARY}; margin-top: 10px;")
            self.content_layout.addWidget(active_header)

            for goal in active_goals:
                habit = self.habit_service.get_habit_by_id(goal.habit_id)
                if habit:
                    card = GoalCard(goal, habit, self)
                    self.content_layout.addWidget(card)

        # Completed goals section
        if completed_goals:
            self.content_layout.addSpacing(32)
            colors = self.theme_manager.get_theme()

            completed_header = QLabel(f"✅ Completed Goals ({len(completed_goals)})")
            completed_header.setFont(QFont("SF Pro Display", 22, QFont.Bold))
            completed_header.setStyleSheet(f"color: {colors.GREEN_500};")
            self.content_layout.addWidget(completed_header)

            for goal in completed_goals:
                habit = self.habit_service.get_habit_by_id(goal.habit_id)
                if habit:
                    card = GoalCard(goal, habit, self)
                    self.content_layout.addWidget(card)

        self.content_layout.addStretch()

    def show_add_goal_dialog(self):
        """Show dialog to add new goal - WITH DEBUG LOGGING"""
        logger.info("\n" + "=" * 50)
        logger.info("🎯 STARTING ADD GOAL PROCESS")
        logger.info("=" * 50)

        try:
            # Step 1: Check habits exist
            logger.info("\n[1] Checking for habits...")
            habits = self.habit_service.get_all_habits()
            logger.info(f"   ✓ Found {len(habits)} habits")

            if not habits:
                logger.info("   ✗ ERROR: No habits found!")
                msg = QMessageBox(self)
                msg.setWindowTitle("No Habits Available")
                msg.setText("⚠️ You need to create at least one habit before creating a goal.\n\nPlease go to the Dashboard and click '+ New Habit' first.")
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                style_msgbox(msg)
                msg.exec()
                return

            # Step 2: Create dialog
            logger.info("\n[2] Creating dialog...")
            dialog = AddGoalDialog(self)
            logger.info("   ✓ Dialog created successfully")

            # Step 3: Show dialog
            logger.info("\n[3] Showing dialog...")
            result = dialog.exec()
            logger.info(f"   ✓ Dialog result: {result} (1=Accepted, 0=Rejected)")

            if result != QDialog.Accepted:
                logger.info("   ℹ User cancelled dialog")
                return

            # Step 4: Get goal data
            logger.info("\n[4] Getting goal data from dialog...")
            goal_data = dialog.get_goal_data()
            logger.info("   ✓ Goal data received:")
            logger.info(f"      - Habit ID: {goal_data['habit_id']}")
            logger.info(f"      - Goal Type: {goal_data['goal_type']}")
            logger.info(f"      - Target Value: {goal_data['target_value']}")

            # Step 5: Create goal
            logger.info("\n[5] Creating goal in database...")
            goal_id = self.goal_service.create_goal(
                habit_id=goal_data["habit_id"],
                goal_type=goal_data["goal_type"],
                target_value=goal_data["target_value"],
            )
            logger.info(f"   ✓ Goal created with ID: {goal_id}")

            if not goal_id:
                raise Exception("create_goal returned None or 0")

            # Step 6: Reload goals
            logger.info("\n[6] Reloading goals list...")
            self.load_goals()
            logger.info("   ✓ Goals reloaded successfully")

            # Step 7: Success message
            logger.info("\n[7] Showing success message...")
            msg = QMessageBox(self)
            msg.setWindowTitle("Goal Created")
            msg.setText(f"✅ Goal created successfully!\n\nYour {goal_data['goal_type'].replace('_', ' ')} goal has been added.")
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Ok)
            style_msgbox(msg)
            msg.exec()

            logger.info("✅ GOAL CREATION COMPLETED SUCCESSFULLY")
            logger.info("=" * 50 + "\n")

        except Exception as e:
            logger.info("\n" + "=" * 50)
            logger.info("❌ ERROR IN GOAL CREATION")
            logger.info("=" * 50)
            logger.info(f"Error type: {type(e).__name__}")
            logger.info(f"Error message: {str(e)}")

            import traceback

            logger.info("\nFull traceback:")
            traceback.print_exc()
            logger.info("=" * 50 + "\n")

            msg = QMessageBox(self)
            msg.setWindowTitle("Error Creating Goal")
            msg.setText(f"❌ Failed to create goal:\n\n{str(e)}\n\nPlease check the console for details.")
            msg.setIcon(QMessageBox.Critical)
            msg.setStandardButtons(QMessageBox.Ok)
            style_msgbox(msg)
            msg.exec()
