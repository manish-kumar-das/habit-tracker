"""
Premium Dashboard View - ALL ISSUES FIXED
"""
import logging
logger = logging.getLogger(__name__)


import os
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QScrollArea,
    QGraphicsDropShadowEffect,
    QMessageBox,
)
from PySide6.QtCore import Qt, QPropertyAnimation, QRectF, Signal, QEvent
from PySide6.QtGui import (
    QFont,
    QPainter,
    QColor,
    QPen,
    QLinearGradient,
    QRadialGradient,
)
from datetime import datetime, timedelta
from app.services.habit_service import get_habit_service
from app.services.profile_service import get_profile_service
from app.services.settings_service import get_settings_service
from app.themes import get_theme_manager
from app.widgets.theme_toggle import AnimatedThemeToggle
from app.services.streak_service import get_streak_service


class SimpleCircularProgress(QWidget):
    def __init__(self, percentage=0, parent=None):
        super().__init__(parent)
        self.percentage = percentage
        self.setFixedSize(240, 240)
        from app.themes import get_theme_manager
        self.theme_manager = get_theme_manager()

    def set_percentage(self, percentage):
        self.percentage = percentage
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        center_x = self.width() // 2
        center_y = self.height() // 2
        radius = 85

        rect = QRectF(center_x - radius, center_y - radius, radius * 2, radius * 2)

        # top inner shadow
        top_shadow = QRadialGradient(center_x, center_y - 25, radius + 20)
        top_shadow.setColorAt(0.7, QColor(0, 0, 0, 0))
        top_shadow.setColorAt(1, QColor(0, 0, 0, 40))

        painter.setBrush(top_shadow)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(rect)

        is_dark = getattr(self, "theme_manager", None) and self.theme_manager.is_dark_mode()
        
        # Inside dark circle
        if is_dark:
            painter.setBrush(QColor("#161a22"))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(rect)

        # Background ring (Uncompleted track)
        track_color = "rgba(139, 92, 246, 0.1)" if is_dark else "#E0E7FF"
        bg_pen = QPen(QColor(track_color), 18)
        bg_pen.setCapStyle(Qt.RoundCap)
        painter.setPen(bg_pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawArc(rect, 0, 360 * 16)

        # Gradient Progress Arc
        if self.percentage > 0:
            gradient = QLinearGradient(
                center_x, center_y - radius, center_x, center_y + radius
            )
            # Saturated identity: Blue to Magenta
            if is_dark:
                gradient.setColorAt(0, QColor("#5069f2")) # Saturated blue
                gradient.setColorAt(0.5, QColor("#7d44cf")) # Saturated purple
                gradient.setColorAt(1, QColor("#f682ff")) # Saturated pink/magenta
            else:
                gradient.setColorAt(0, QColor("#667eea"))
                gradient.setColorAt(0.5, QColor("#764ba2"))
                gradient.setColorAt(1, QColor("#f093fb"))

            progress_pen = QPen(gradient, 18)
            progress_pen.setCapStyle(Qt.RoundCap)
            painter.setPen(progress_pen)

            span_angle = int(-360 * (self.percentage / 100) * 16)
            painter.drawArc(rect, 90 * 16, span_angle)

        # Soft inner highlight
        highlight = QRadialGradient(center_x, center_y - 30, radius)
        highlight.setColorAt(0, QColor(255, 255, 255, 60))
        highlight.setColorAt(1, QColor(255, 255, 255, 0))

        painter.setBrush(highlight)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(rect.adjusted(18, 18, -18, -18))

        # Percentage Text
        is_dark = getattr(self, "theme_manager", None) and self.theme_manager.is_dark_mode()
        text_color = "#F3F4F6" if is_dark else "#111827"
        painter.setPen(QColor(text_color))
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
        from app.services.streak_service import get_streak_service

        self.streak_service = get_streak_service()
        
        from app.themes import get_theme_manager
        self.theme_manager = get_theme_manager()

        self.setObjectName("habitCard")
        self.setFixedHeight(89)
        self.setCursor(Qt.PointingHandCursor)

        self.setup_ui()
        self.apply_shadow()

    # UI
    def setup_ui(self):
        is_dark = getattr(self, "theme_manager", None) and self.theme_manager.is_dark_mode()
        bg_color = "#1A1C23" if is_dark else "#FFFFFF"
        hover_bg = "#252732" if is_dark else "#F8FAFF"
        text_primary = "#F3F4F6" if is_dark else "#1F2937"
        text_secondary = "#9CA3AF" if is_dark else "#9CA3AF"
        border_style = "border: 1px solid #333645;" if is_dark else "border: none;"

        self.setStyleSheet(f"""
            QFrame#habitCard {{
                background-color: {bg_color};
                border-radius: 18px;
                {border_style}
            }}
            QFrame#habitCard:hover {{
                background-color: {hover_bg};
            }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 14, 20, 14)
        layout.setSpacing(14)

        # Text Section
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)

        name_label = QLabel(self.habit.name)
        name_label.setFont(QFont("SF Pro Display", 15, QFont.DemiBold))
        name_label.setStyleSheet(f"color: {text_primary};")

        subtitle = QLabel(f"{self.habit.category} • {self.habit.frequency}")
        subtitle.setFont(QFont("SF Pro Text", 12))
        subtitle.setStyleSheet(f"color: {text_secondary};")

        text_layout.addWidget(name_label)
        text_layout.addWidget(subtitle)

        layout.addLayout(text_layout)
        layout.addStretch()

        # ACTION BUTTONS
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(12)
        actions_layout.setAlignment(Qt.AlignVCenter)

        self.edit_btn = QPushButton("Edit")
        self.edit_btn.setFixedSize(65, 36)
        self.edit_btn.setFont(QFont("SF Pro Text", 12, QFont.Medium))
        self.edit_btn.setCursor(Qt.PointingHandCursor)
        btn_bg = "#242933" if is_dark else "#F8FAFC"
        btn_text = "#dbdee4" if is_dark else "#64748B"
        btn_border = "#374151" if is_dark else "#E2E8F0"
        btn_hover_bg = "#1A1F2E" if is_dark else "#F1F5F9"
        btn_hover_text = "#FFFFFF" if is_dark else "#334155"

        self.edit_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {btn_bg};
                color: {btn_text};
                border: 1px solid {btn_border};
                border-radius: 10px;
                padding: 0px 12px;
            }}
            QPushButton:hover {{
                background-color: {btn_hover_bg};
                color: {btn_hover_text};
                border: 1px solid #6366F1;
            }}
        """)
        self.edit_btn.clicked.connect(self.edit_habit)

        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setFixedSize(80, 36)
        self.delete_btn.setFont(QFont("SF Pro Text", 12, QFont.Medium))
        self.delete_btn.setCursor(Qt.PointingHandCursor)
        
        del_hover_bg = "#7F1D1D" if is_dark else "#FEF2F2"
        del_hover_text = "#FCA5A5" if is_dark else "#DC2626"
        del_hover_border = "#991B1B" if is_dark else "#FEE2E2"

        # Dark mode default styling for Delete button
        del_bg = "rgba(239, 68, 68, 0.1)" if is_dark else btn_bg
        del_text = "#F87171" if is_dark else btn_text
        del_border = "rgba(239, 68, 68, 0.2)" if is_dark else btn_border

        self.delete_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {del_bg};
                color: {del_text};
                border: 1px solid {del_border};
                border-radius: 10px;
                padding: 0px 12px;
            }}
            QPushButton:hover {{
                background-color: {del_hover_bg};
                color: {del_hover_text};
                border: 1px solid {del_hover_border};
            }}
        """)
        self.delete_btn.clicked.connect(self.delete_confirm)

        actions_layout.addWidget(self.edit_btn)
        actions_layout.addWidget(self.delete_btn)

        # Button
        self.button = QPushButton()
        self.button.setFixedSize(140, 36)
        self.button.setCursor(Qt.PointingHandCursor)
        self.button.setFont(QFont("SF Pro Text", 13, QFont.DemiBold))

        actions_layout.addWidget(self.button)
        layout.addLayout(actions_layout)

        if self.is_completed:
            self.apply_completed_style()
        else:
            self.apply_default_style()

        self.button.clicked.connect(self.mark_complete)

    # Styles
    def apply_default_style(self):
        is_dark = getattr(self, "theme_manager", None) and self.theme_manager.is_dark_mode()
        btn_bg = "#2D1B4E" if is_dark else "#EEF2FF"
        btn_text = "#A78BFA" if is_dark else "#4F46E5"
        btn_hover = "#3D2566" if is_dark else "#E0E7FF"
        
        self.button.setText("Mark Done")
        self.button.setEnabled(True)
        self.button.setStyleSheet(f"""
            QPushButton {{
                background-color: {btn_bg};
                color: {btn_text};
                border-radius: 14px;
                padding: 6px 16px;
                border: 1px solid {"#4F46E5" if is_dark else "transparent"};
            }}
            QPushButton:hover {{
                background-color: {btn_hover};
                border: 1px solid #6366F1;
            }}
        """)

    def apply_completed_style(self):
        is_dark = getattr(self, "theme_manager", None) and self.theme_manager.is_dark_mode()
        bg_color = "#1A1C23" if is_dark else "#F9FAFB"
        border_style = "border: 1px solid #333645; border-left: 4px solid #10B981;" if is_dark else "border: none; border-left: 4px solid #10B981;"
        
        self.setStyleSheet(f"""
            QFrame#habitCard {{
                background-color: {bg_color};
                border-radius: 18px;
                {border_style}
            }}
        """)

        self.button.setText("Completed ✓")
        self.button.setEnabled(False)
        
        btn_bg = "#064E3B" if is_dark else "#D1FAE5"
        btn_text = "#34D399" if is_dark else "#065F46"
        
        self.button.setStyleSheet(f"""
            QPushButton {{
                background-color: {btn_bg};
                color: {btn_text};
                border-radius: 14px;
                padding: 6px 16px;
                border: 1px solid {"#065F46" if is_dark else "transparent"};
            }}
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
            logger.info("Error:", e)

    def edit_habit(self):
        """Open the Edit Habit Dialog"""
        from app.views.edit_habit_dialog import EditHabitDialog

        dialog = EditHabitDialog(self.habit, self)
        if dialog.exec_():
            if self.parent_view and hasattr(self.parent_view, "load_dashboard"):
                self.parent_view.load_dashboard()

    def delete_confirm(self):
        """Show delete confirmation dialog"""
        msg = QMessageBox(self)
        msg.setWindowTitle("Delete Habit")
        msg.setText(f"Move '{self.habit.name}' to trash?")
        msg.setInformativeText("This habit will no longer show up on your dashboard.")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        msg.setIcon(QMessageBox.Question)

        # Premium styling for QMessageBox
        from app.themes import get_theme_manager
        is_dark = get_theme_manager().is_dark_mode()
        bg_color = "#1A1C23" if is_dark else "#FFFFFF"
        text_color = "#F3F4F6" if is_dark else "#1F2937"
        btn_bg = "#333645" if is_dark else "#F3F4F6"
        btn_text = "#F3F4F6" if is_dark else "#374151"
        btn_border = "#4B5563" if is_dark else "#D1D5DB"
        btn_hover = "#404354" if is_dark else "#E5E7EB"

        msg.setStyleSheet(f"""
            QMessageBox {{
                background-color: {bg_color};
                border-radius: 20px;
            }}
            QLabel {{
                color: {text_color};
                font-size: 14px;
            }}
            QPushButton {{
                background-color: {btn_bg};
                color: {btn_text};
                border: 1px solid {btn_border};
                border-radius: 8px;
                padding: 6px 20px;
                min-width: 80px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {btn_hover};
            }}
            QPushButton[text="&Yes"] {{
                background-color: #EF4444;
                color: white;
                border: none;
            }}
            QPushButton[text="&Yes"]:hover {{
                background-color: #DC2626;
            }}
        """)

        if msg.exec_() == QMessageBox.Yes:
            try:
                self.habit_service.hard_delete_habit(self.habit.id, save_to_trash=True)
                if self.parent_view and hasattr(self.parent_view, "load_dashboard"):
                    self.parent_view.load_dashboard()
            except Exception as e:
                logger.info(f"Delete Error: {e}")

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


class WeekDayCard(QWidget):
    """Weekly Activity Card - Brand Gradient Version"""

    def __init__(self, day_name, percentage, day_number, is_today=False, parent=None):
        super().__init__(parent)
        from app.themes import get_theme_manager
        self.theme_manager = get_theme_manager()
        self.percentage = percentage
        self.is_today = is_today
        self.setup_ui(day_name, percentage, day_number)

    def setup_ui(self, day_name, percentage, day_number):
        self.setFixedWidth(135)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(10)
        main_layout.setAlignment(Qt.AlignCenter)

        # CARD
        card = QFrame()
        card.setObjectName("weekDayCard")
        card.setFixedSize(135, 190)

        is_dark = getattr(self, "theme_manager", None) and self.theme_manager.is_dark_mode()
        if percentage > 0:
            # Saturated identity: Blue to Purple to Pink (from Analytics StatCard logic)
            s_start = "#5069f2" if is_dark else "#667eea"
            s_mid = "#7d44cf" if is_dark else "#764ba2"
            s_end = "#f682ff" if is_dark else "#f093fb"
            background = f"""
                qlineargradient(x1:0,y1:0,x2:0,y2:1,
                stop:0 {s_start},
                stop:0.5 {s_mid},
                stop:1 {s_end})
            """
            text_color = "#FFFFFF"
            # Highlight today with a ring or glow, but remove thick border if requested
            border = "border: none;"
        else:
            background = "#252732" if is_dark else "#F3F4F6"
            text_color = "#9CA3AF" if is_dark else "#9CA3AF"
            primary_text = "#F3F4F6" if is_dark else "#111827"
            border = f"border: 1px solid {primary_text};"

        card.setStyleSheet(f"""
            QFrame#weekDayCard {{
                background: {background};
                border-radius: 22px;
                {border}
            }}
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(12, 22, 12, 20)
        card_layout.setSpacing(12)
        card_layout.setAlignment(Qt.AlignCenter)

        # Percentage
        percent_label = QLabel(f"{percentage}%")
        percent_label.setFont(QFont("SF Pro Display", 26, QFont.Bold))
        percent_label.setStyleSheet(f"color: {text_color}; background: transparent; border: none;")
        percent_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(percent_label)

        # Progress Bar
        progress_bg = QFrame()
        progress_bg.setFixedHeight(6)

        if percentage > 0:
            progress_bg.setStyleSheet("""
                QFrame {
                    background: rgba(255,255,255,0.35);
                    border-radius: 3px;
                    border: none;
                }
            """)
        else:
            progress_bg_color = "rgba(255,255,255,0.1)" if is_dark else "#E5E7EB"
            progress_bg.setStyleSheet(f"""
                QFrame {{
                    background: {progress_bg_color};
                    border-radius: 3px;
                    border: none;
                }}
            """)

        progress_fill = QFrame(progress_bg)
        progress_fill.setGeometry(0, 0, int((percentage / 100) * 111), 6)

        progress_fill.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 3px;
                border: none;
            }
        """)

        card_layout.addWidget(progress_bg)

        main_layout.addWidget(card)

        # ---------- DAY NAME BELOW ----------
        day_label = QLabel(day_name)
        day_label.setFont(QFont("SF Pro Text", 12, QFont.Bold))
        day_label.setStyleSheet(f"color: {'#9CA3AF' if is_dark else '#6B7280'}; border: none; background: transparent;")
        day_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(day_label)

        # Date Number
        date_label = QLabel(str(day_number))
        date_label.setFont(QFont("SF Pro Display", 22, QFont.Bold))
        date_label.setStyleSheet(f"color: {text_color}; background: transparent; border: none;")
        date_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(date_label)

        # Shadow only on card
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(35)
        shadow.setOffset(0, 10)
        shadow.setColor(QColor(0, 0, 0, 35))
        card.setGraphicsEffect(shadow)


class HabitEmptyState(QFrame):
    """Modern Empty State placeholder for habits section"""

    def __init__(self, parent=None):
        super().__init__(parent)
        from app.themes import get_theme_manager
        self.theme_manager = get_theme_manager()
        is_dark = getattr(self, "theme_manager", None) and self.theme_manager.is_dark_mode()
        
        self.setMinimumHeight(280)
        self.setCursor(Qt.ArrowCursor)
        
        border_color = "#333645" if is_dark else "#E5E7EB"
        self.setStyleSheet(f"""
            QFrame {{
                background: transparent;
                border: 2px dashed {border_color};
                border-radius: 22px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(12)

        # Icon Container (Target with dart)
        icon_label = QLabel("🎯")
        icon_label.setFont(
            QFont("Segoe UI Emoji", 48)
            if os.name == "nt"
            else QFont("noto color emoji", 48)
        )
        # Fallback to generic font if specific ones aren't available
        if icon_label.font().family() == "MS Shell Dlg 2":
            icon_label.setFont(QFont("SF Pro Display", 48))

        icon_label.setStyleSheet("border: none; background: transparent;")
        layout.addWidget(icon_label, alignment=Qt.AlignCenter)

        # Title
        title = QLabel("No habits for today")
        title.setFont(QFont("SF Pro Display", 22, QFont.Bold))
        text_primary = "#F3F4F6" if is_dark else "#111827"
        title.setStyleSheet(f"color: {text_primary}; border: none; background: transparent;")
        layout.addWidget(title, alignment=Qt.AlignCenter)

        # Subtitle
        desc = QLabel("Ready to start a new streak? Create your first habit!")
        desc.setFont(QFont("SF Pro Text", 14))
        text_secondary = "#9CA3AF" if is_dark else "#6B7280"
        desc.setStyleSheet(f"color: {text_secondary}; border: none; background: transparent;")
        desc.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc, alignment=Qt.AlignCenter)

        # Action Button
        self.create_btn = QPushButton("+ New Habit")
        self.create_btn.setFixedSize(160, 48)
        self.create_btn.setFont(QFont("SF Pro Text", 13, QFont.Bold))
        self.create_btn.setCursor(Qt.PointingHandCursor)
        self.create_btn.setGraphicsEffect(None)
        is_dark = self.theme_manager.is_dark_mode()
        s_start = "#5069f2" if is_dark else "#667eea"
        s_end = "#7d44cf" if is_dark else "#764ba2"
        h_start = "#4F46E5" if is_dark else "#5568d3"
        h_end = "#7C3AED" if is_dark else "#6a4191"

        self.create_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {s_start}, stop:1 {s_end});
                color: #FFFFFF;
                border: none;
                border-radius: 12px;
                margin-top: 10px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {h_start}, stop:1 {h_end});
            }}
        """)
        layout.addWidget(self.create_btn, alignment=Qt.AlignCenter)


class DashboardContentView(QWidget):
    """Fixed premium dashboard - ALL ISSUES RESOLVED"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.habit_service = get_habit_service()
        self.streak_service = get_streak_service()
        self.profile_service = get_profile_service()
        self.settings_service = get_settings_service()
        self.theme_manager = get_theme_manager()
        self.setup_ui()
        self.apply_theme()
        self.load_dashboard()

    def setup_ui(self):
        """Setup dashboard UI"""
        is_dark = self.theme_manager.is_dark_mode()
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top navbar
        colors = self.theme_manager.get_theme()
        self.navbar = QFrame()
        self.navbar.setMinimumHeight(120)
        self.navbar.setStyleSheet(f"""
            QFrame {{
                background-color: {colors.BG_PRIMARY};
                border: none;
            }}
        """)

        navbar_layout = QHBoxLayout(self.navbar)
        navbar_layout.setContentsMargins(40, 24, 40, 24)

        # Greeting
        greeting_container = QHBoxLayout()
        greeting_container.setSpacing(12)
        greeting_container.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        hour = datetime.now().hour
        if hour < 12:
            emoji, greeting_text = "☀️", "Good morning"
        elif hour < 18:
            emoji, greeting_text = "🌤️", "Good afternoon"
        else:
            emoji, greeting_text = "🌙", "Good evening"

        emoji_label = QLabel(emoji)
        emoji_label.setFont(QFont("SF Pro Display", 28))
        emoji_label.setStyleSheet("color: #111827; background: transparent;")
        greeting_container.addWidget(emoji_label)

        greeting_layout = QVBoxLayout()
        greeting_layout.setSpacing(0)
        greeting_layout.setAlignment(Qt.AlignVCenter)

        profile = self.profile_service.get_profile()
        first_name = profile["name"].split()[0] if profile["name"] else "there"

        self.greeting_label = QLabel(f"{greeting_text}, {first_name}!")
        self.greeting_label.setFont(QFont("SF Pro Display", 28, QFont.Bold))
        text_primary = "#F3F4F6" if is_dark else "#111827"
        self.greeting_label.setStyleSheet(f"color: {text_primary}; background: transparent;")
        greeting_layout.addWidget(self.greeting_label)

        today = datetime.now()
        date_str = today.strftime(f"%A, %B {self._ordinal(today.day)}")

        date_label = QLabel(date_str)
        date_label.setFont(QFont("SF Pro Text", 14))
        text_secondary = "#9CA3AF" if is_dark else "#6B7280"
        date_label.setStyleSheet(f"color: {text_secondary}; background: transparent;")
        date_label.setWordWrap(True)
        greeting_layout.addWidget(date_label)

        greeting_container.addLayout(greeting_layout)
        navbar_layout.addLayout(greeting_container)
        navbar_layout.addStretch()

        # Theme Switcher
        self.theme_btn = AnimatedThemeToggle()
        self.theme_btn.set_theme(self.theme_manager.is_dark_mode())
        self.theme_btn.theme_changed.connect(self._on_theme_changed)
        navbar_layout.addWidget(self.theme_btn)

        # Space between theme switcher and notification bell
        navbar_layout.addSpacing(20)

        # Notification
        is_dark = self.theme_manager.is_dark_mode()
        notif_btn = QPushButton("🔔")
        notif_btn.setFont(QFont("SF Pro Display", 20))
        notif_btn.setFixedSize(50, 50)
        notif_btn.setCursor(Qt.PointingHandCursor)
        
        bg_color = "#252732" if is_dark else "#F3F4F6"
        hover_color = "#333645" if is_dark else "#E5E7EB"
        
        notif_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                border: none;
                border-radius: 25px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """)
        navbar_layout.addWidget(notif_btn)
        self.notif_btn = notif_btn
        self.notif_btn.clicked.connect(self.toggle_notifications)

        # Badge for notifications
        self.notif_badge = QLabel("!", self.notif_btn)
        self.notif_badge.setFixedSize(18, 18)
        self.notif_badge.move(32, 0)
        self.notif_badge.setAlignment(Qt.AlignCenter)
        self.notif_badge.setFont(QFont("SF Pro Text", 9, QFont.Bold))
        self.notif_badge.setStyleSheet("""
            background-color: #EF4444;
            color: white;
            border-radius: 9px;
            border: 2px solid #FFFFFF;
        """)
        self.notif_badge.hide()

        # New Habit button
        new_btn = QPushButton("+ New Habit")
        new_btn.setFont(QFont("SF Pro Text", 15, QFont.Bold))
        new_btn.setFixedHeight(50)
        new_btn.setCursor(Qt.PointingHandCursor)
        
        is_dark = self.theme_manager.is_dark_mode()
        s_start = "#5069f2" if is_dark else "#667eea"
        s_mid = "#7d44cf" if is_dark else "#764ba2"
        s_end = "#f682ff" if is_dark else "#f093fb"
        
        h_start = "#4F46E5" if is_dark else "#5568d3"
        h_mid = "#7C3AED" if is_dark else "#6a4191"
        h_end = "#9333EA" if is_dark else "#e07af0"

        new_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {s_start}, stop:0.5 {s_mid}, stop:1 {s_end});
                color: #FFFFFF;
                border: none;
                border-radius: 12px;
                padding: 0px 26px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {h_start}, stop:0.5 {h_mid}, stop:1 {h_end});
            }}
        """)
        # Space between notification and new habit button
        navbar_layout.addSpacing(20)
        
        new_btn.clicked.connect(self.show_add_habit)
        navbar_layout.addWidget(new_btn)

        main_layout.addWidget(self.navbar)

        # Notification Panel (Absolute positioning overlay)
        self.notif_panel = NotificationPanel(self)
        self.notif_panel.mark_read_btn.clicked.connect(self.mark_notifications_read)
        self.notif_panel.closed.connect(self.update_notification_badge)

        # Dashboard content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        is_dark = self.theme_manager.is_dark_mode()
        scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {"#1A1C23" if is_dark else "#F9FAFB"};
            }}
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
        daily_card.setFixedHeight(448)
        is_dark = self.theme_manager.is_dark_mode()
        daily_card.setStyleSheet(f"""
            QFrame {{
                background-color: {"#252732" if is_dark else "#FFFFFF"};
                border: 1px solid {"#333645" if is_dark else "transparent"};
                border-radius: 20px;
            }}
        """)
        self.apply_card_shadow(daily_card)

        daily_layout = QVBoxLayout(daily_card)
        daily_layout.setContentsMargins(30, 28, 30, 28)
        daily_layout.setSpacing(20)

        daily_title = QLabel("Daily Completion")
        daily_title.setFont(QFont("SF Pro Display", 22, QFont.Bold))
        text_primary = "#F3F4F6" if is_dark else "#111827"
        daily_title.setStyleSheet(f"color: {text_primary}; border: none; background: transparent;")
        daily_layout.addWidget(daily_title)

        self.circular_progress = SimpleCircularProgress(0)
        daily_layout.addWidget(self.circular_progress, alignment=Qt.AlignCenter)

        self.progress_text = QLabel("Loading...")
        self.progress_text.setFont(QFont("SF Pro Text", 15))
        text_secondary = "#9CA3AF" if is_dark else "#6B7280"
        self.progress_text.setStyleSheet(f"color: {text_secondary}; border: none; background: transparent;")
        self.progress_text.setAlignment(Qt.AlignCenter)
        self.progress_text.setWordWrap(True)
        daily_layout.addWidget(self.progress_text)
        
        self.daily_card = daily_card
        self.daily_title = daily_title

        top_row.addWidget(daily_card)

        # Today's Habits
        habits_card = QFrame()
        habits_card.setObjectName("todayCard")
        habits_card.setFixedHeight(448)
        is_dark = self.theme_manager.is_dark_mode()
        habits_card.setStyleSheet(f"""
            QFrame#todayCard {{
                background-color: {"#252732" if is_dark else "#FFFFFF"};
                border: 1px solid {"#333645" if is_dark else "transparent"};
                border-radius: 20px;
            }}
        """)
        self.apply_card_shadow(habits_card)

        habits_layout = QVBoxLayout(habits_card)
        habits_layout.setContentsMargins(30, 28, 30, 28)
        habits_layout.setSpacing(16)

        habits_header = QHBoxLayout()
        habits_header.setContentsMargins(26, 0, 26, 0)
        habits_header.setSpacing(15)

        habits_title = QLabel("Today's Habits")
        habits_title.setFont(QFont("SF Pro Display", 22, QFont.Bold))
        text_primary = "#F3F4F6" if is_dark else "#111827"
        habits_title.setStyleSheet(f"background-color: transparent; color: {text_primary};")
        habits_header.addWidget(habits_title)
        
        self.habits_card = habits_card
        self.habits_title = habits_title

        habits_header.addStretch()

        self.habits_count = QLabel("0")
        self.habits_count.setFont(QFont("SF Pro Display", 15, QFont.Bold))
        self.habits_count.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:0.5 #764ba2, stop:1 #f093fb);
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
        habits_scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
            QScrollBar:vertical {{
                background: {"#1A1C23" if is_dark else "#F3F4F6"};
                width: 10px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical {{
                background: #6366F1;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: #4F46E5;
            }}
        """)

        # Wrap scroll inside inner recessed container
        habit_list_container = QFrame()
        self.habit_list_container = habit_list_container
        habit_list_container.setStyleSheet(f"""
            QFrame {{
                background-color: {"#2C2F3A" if is_dark else "#FFFFFF"};
                border-radius: 16px;
            }}
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
        is_dark = self.theme_manager.is_dark_mode()
        weekly_card.setStyleSheet(f"""
            QFrame {{
                background-color: {"#252732" if is_dark else "#FFFFFF"};
                border: 1px solid {"#333645" if is_dark else "transparent"};
                border-radius: 20px;
            }}
        """)
        weekly_card.setFixedHeight(348)

        weekly_layout = QVBoxLayout(weekly_card)
        weekly_layout.setContentsMargins(30, 28, 30, 28)
        weekly_layout.setSpacing(20)

        weekly_header = QHBoxLayout()

        weekly_title = QLabel("Weekly Activity")
        weekly_title.setFont(QFont("SF Pro Display", 22, QFont.Bold))
        text_primary = "#F3F4F6" if is_dark else "#111827"
        weekly_title.setStyleSheet(f"color: {text_primary}; border: none; background: transparent;")
        weekly_header.addWidget(weekly_title)

        weekly_header.addStretch()

        weekly_subtitle = QLabel("Last 7 Days")
        weekly_subtitle.setFont(QFont("SF Pro Text", 13))
        text_secondary = "#9CA3AF" if is_dark else "#6B7280"
        weekly_subtitle.setStyleSheet(f"color: {text_secondary}; border: none; background: transparent;")
        weekly_header.addWidget(weekly_subtitle)
        
        self.weekly_card = weekly_card
        self.weekly_title = weekly_title
        self.weekly_subtitle = weekly_subtitle

        weekly_layout.addLayout(weekly_header)

        self.week_grid = QHBoxLayout()
        self.week_grid.setSpacing(12)
        weekly_layout.addLayout(self.week_grid)

        weekly_layout.addStretch()

        bottom_row.addWidget(weekly_card, stretch=2)

        milestone_card = QFrame()
        milestone_card.setFixedHeight(348)
        is_dark = self.theme_manager.is_dark_mode()
        # Saturated brand colors for dark mode consistent with analytics
        s_start = "#5069f2" if is_dark else "#667eea"
        s_mid = "#7d44cf" if is_dark else "#764ba2"
        s_end = "#f682ff" if is_dark else "#f093fb"
        
        milestone_card.setStyleSheet(f"""
            QFrame#streakCard {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {s_start}, stop:0.5 {s_mid}, stop:1 {s_end});
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 24px;
            }}
        """)
        milestone_card.setObjectName("streakCard")
        milestone_card.setMinimumWidth(
            380
        )  # Ensure enough space for large numbers (100+)
        self.milestone_card = milestone_card

        streak_card_shadow = QGraphicsDropShadowEffect()
        streak_card_shadow.setBlurRadius(40)
        streak_card_shadow.setColor(QColor(118, 75, 162, 120))
        streak_card_shadow.setOffset(0, 12)
        milestone_card.setGraphicsEffect(streak_card_shadow)

        ms_layout = QVBoxLayout(milestone_card)
        ms_layout.setContentsMargins(24, 20, 24, 20)
        ms_layout.setSpacing(0)

        header_row = QHBoxLayout()
        header_row.setSpacing(8)

        flame_small = QLabel("🔥")
        flame_small.setFont(QFont("SF Pro Display", 20))
        flame_small.setStyleSheet("background: transparent; border: none;")
        header_row.addWidget(flame_small)

        streak_title = QLabel("Current Streak")
        streak_title.setFont(QFont("SF Pro Display", 16, QFont.Bold))
        streak_title.setStyleSheet(
            "color: rgba(255,255,255,0.55); background: transparent; border: none;"
        )
        header_row.addWidget(streak_title)
        header_row.addStretch()

        # On-fire pill badge (shown even for 0 to maintain consistent layout)
        self.fire_badge = QLabel("  No Streak  ")
        self.fire_badge.setFont(QFont("SF Pro Text", 11, QFont.Bold))
        self.fire_badge.setStyleSheet("""
            QLabel {
                background: rgba(255, 255, 255, 0.22);
                color: #FFFFFF;
                border-radius: 10px;
                padding: 2px 12px;
                border: 1px solid rgba(255, 255, 255, 0.40);
            }
        """)
        self.fire_badge.setVisible(True)
        header_row.addWidget(self.fire_badge)

        ms_layout.addLayout(header_row)
        ms_layout.addSpacing(6)

        # ── Hero number ──
        self.streak_label = QLabel("0")
        self.streak_label.setFont(QFont("SF Pro Display", 68, QFont.Black))
        self.streak_label.setStyleSheet(
            "color: #FFFFFF; background: transparent; border: none;"
        )
        self.streak_label.setAlignment(Qt.AlignCenter)
        ms_layout.addWidget(self.streak_label)

        # ── "days" sub-label ──
        self.days_unit_label = QLabel("days in a row")
        self.days_unit_label.setFont(QFont("SF Pro Text", 13, QFont.DemiBold))
        self.days_unit_label.setStyleSheet(
            "color: rgba(255,255,255,0.45); background: transparent; border: none;"
        )
        self.days_unit_label.setAlignment(Qt.AlignCenter)
        ms_layout.addWidget(self.days_unit_label)

        ms_layout.addSpacing(10)

        # ── Motivational tagline ──
        self.streak_desc = QLabel("Start your first streak today!")
        self.streak_desc.setFont(QFont("SF Pro Text", 13, QFont.DemiBold))
        self.streak_desc.setStyleSheet(
            "color: rgba(255, 255, 255, 0.80); background: transparent; border: none;"
        )
        self.streak_desc.setAlignment(Qt.AlignCenter)
        self.streak_desc.setWordWrap(True)
        ms_layout.addWidget(self.streak_desc)

        ms_layout.addStretch()

        # ── Footer: best streak stat ──
        divider = QFrame()
        divider.setFixedHeight(1)
        divider.setStyleSheet("background: rgba(255, 255, 255, 0.25); border: none;")
        ms_layout.addWidget(divider)
        ms_layout.addSpacing(10)

        footer_row = QHBoxLayout()
        footer_row.setSpacing(6)

        trophy_lbl = QLabel("🏆")
        trophy_lbl.setFont(QFont("SF Pro Display", 15))
        trophy_lbl.setStyleSheet("background: transparent; border: none;")
        footer_row.addWidget(trophy_lbl)

        best_text_lbl = QLabel("Best streak:")
        best_text_lbl.setFont(QFont("SF Pro Text", 12))
        best_text_lbl.setStyleSheet(
            "color: rgba(255,255,255,0.45); background: transparent; border: none;"
        )
        footer_row.addWidget(best_text_lbl)

        self.best_streak_label = QLabel("0 days")
        self.best_streak_label.setFont(QFont("SF Pro Text", 12, QFont.Bold))
        self.best_streak_label.setStyleSheet(
            "color: rgba(255,255,255,0.85); background: transparent; border: none;"
        )
        footer_row.addWidget(self.best_streak_label)
        footer_row.addStretch()

        ms_layout.addLayout(footer_row)

        bottom_row.addWidget(milestone_card, stretch=1)

        content_layout.addLayout(bottom_row)

        scroll.setWidget(content)
        main_layout.addWidget(scroll)

    def _ordinal(self, n):
        if 11 <= n % 100 <= 13:
            return f"{n}th"
        return (
            f"{n}{['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th'][n % 10]}"
        )

    def show_add_habit(self):
        if self.main_window:
            self.main_window.show_add_habit_dialog()

    def _on_theme_changed(self, theme_name):
        self.theme_manager.set_theme(theme_name)
        self.theme_manager.save_preference()
        if self.main_window:
            self.main_window.apply_theme_to_all()
            
    def apply_theme(self):
        colors = self.theme_manager.get_theme()
        is_dark = getattr(self, "theme_manager", None) and self.theme_manager.is_dark_mode()
        
        bg_primary = "#1A1C23" if is_dark else colors.BG_PRIMARY
        text_primary = "#F3F4F6" if is_dark else "#111827"
        text_secondary = "#9CA3AF" if is_dark else "#6B7280"
        
        self.setStyleSheet(f"background-color: {bg_primary};")
        if hasattr(self, 'navbar'):
            self.navbar.setStyleSheet(f"""
                QFrame {{
                    background-color: {bg_primary};
                    border: none;
                }}
            """)
        
        if hasattr(self, 'greeting_label'):
            self.greeting_label.setStyleSheet(f"color: {text_primary}; background: transparent;")
        
        if hasattr(self, 'date_label'):
            self.date_label.setStyleSheet(f"color: {text_secondary}; background: transparent;")

        # Apply specific card dark styles
        card_bg = "#252732" if is_dark else "#FFFFFF"
        text_primary = "#F3F4F6" if is_dark else "#111827"
        text_secondary = "#9CA3AF" if is_dark else "#6B7280"
        border_color = "#333645" if is_dark else "transparent"
        border_style = f"border: 1px solid {border_color};" if is_dark else "border: none;"
        inner_bg = "#2C2F3A" if is_dark else "#FFFFFF"
        
        if hasattr(self, 'notif_btn'):
            bg_color = "#252732" if is_dark else "#F3F4F6"
            hover_color = "#333645" if is_dark else "#E5E7EB"
            self.notif_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {bg_color};
                    border: none;
                    border-radius: 25px;
                }}
                QPushButton:hover {{
                    background-color: {hover_color};
                }}
            """)
        
        if hasattr(self, 'notif_badge'):
            badge_border = "#252732" if is_dark else "#FFFFFF"
            self.notif_badge.setStyleSheet(f"""
                background-color: #EF4444;
                color: white;
                border-radius: 9px;
                border: 2px solid {badge_border};
            """)
        
        # Apply cards and sections...
        if hasattr(self, 'daily_card'):
            self.daily_card.setStyleSheet(f"""
                QFrame {{
                    background-color: {card_bg};
                    {border_style}
                    border-radius: 20px;
                }}
            """)
            self.daily_title.setStyleSheet(f"color: {text_primary}; border: none; background: transparent;")
            self.progress_text.setStyleSheet(f"color: {text_secondary}; border: none; background: transparent;")
            
        if hasattr(self, 'habits_card'):
            self.habits_card.setStyleSheet(f"""
                QFrame#todayCard {{
                    background-color: {card_bg};
                    {border_style}
                    border-radius: 20px;
                }}
            """)
            self.habits_title.setStyleSheet(f"background-color: transparent; color: {text_primary};")
            
        if hasattr(self, 'habit_list_container'):
            self.habit_list_container.setStyleSheet(f"""
                QFrame {{
                    background-color: {inner_bg};
                    border-radius: 16px;
                }}
            """)
            
        if hasattr(self, 'weekly_card'):
            self.weekly_card.setStyleSheet(f"""
                QFrame {{
                    background-color: {card_bg};
                    {border_style}
                    border-radius: 20px;
                }}
            """)
            self.weekly_title.setStyleSheet(f"color: {text_primary}; border: none; background: transparent;")
            self.weekly_subtitle.setStyleSheet(f"color: {text_secondary}; border: none; background: transparent;")

        if hasattr(self, 'milestone_card'):
            s_start = "#5069f2" if is_dark else "#667eea"
            s_mid = "#7d44cf" if is_dark else "#764ba2"
            s_end = "#f682ff" if is_dark else "#f093fb"
            self.milestone_card.setStyleSheet(f"""
                QFrame#streakCard {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 {s_start}, stop:0.5 {s_mid}, stop:1 {s_end});
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 24px;
                }}
            """)

        # Repaint circular progress so it updates its colors
        if hasattr(self, 'circular_progress'):
            self.circular_progress.update()
            
        # Re-render the dashboard to update inner cards with new theme
        self.load_dashboard()

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
            self.streak_label.setText("0")
            self.best_streak_label.setText("0 days")
            self.fire_badge.setVisible(False)
            self.streak_desc.setText("Start your first streak today!")

            # Add Empty State Skeleton
            empty_state = HabitEmptyState(self)
            empty_state.create_btn.clicked.connect(self.show_add_habit)
            self.habits_list.addWidget(empty_state)
            self.habits_list.addStretch()

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
            current = streak_info.get("current_streak", 0)
            max_streak = max(max_streak, current)

        self.streak_label.setText(str(max_streak))

        # Adjust font size for large streaks
        if max_streak >= 100:
            self.streak_label.setFont(QFont("SF Pro Display", 56, QFont.Black))
        else:
            self.streak_label.setFont(QFont("SF Pro Display", 68, QFont.Black))

        self.days_unit_label.setText(
            "day in a row" if max_streak == 1 else "days in a row"
        )

        # Calculate best (longest) streak across all habits
        best_streak = 0
        for habit in habits:
            streak_info = self.streak_service.get_streak_info(habit.id)
            longest = streak_info.get(
                "longest_streak", streak_info.get("current_streak", 0)
            )
            best_streak = max(best_streak, longest)

        self.best_streak_label.setText(
            f"{best_streak} day{'' if best_streak == 1 else 's'}"
        )

        # Update fire badge (streak showing tab)
        if max_streak > 0:
            self.fire_badge.setText("  🔥 On Fire!  ")
            self.fire_badge.setStyleSheet("""
                QLabel {
                    background: rgba(255, 255, 255, 0.22);
                    color: #FFFFFF;
                    border-radius: 10px;
                    padding: 2px 12px;
                    border: 1px solid rgba(255, 255, 255, 0.45);
                    font-weight: bold;
                }
            """)
        else:
            self.fire_badge.setText("  Steady  ")
            self.fire_badge.setStyleSheet("""
                QLabel {
                    background: rgba(255, 255, 255, 0.1);
                    color: rgba(255, 255, 255, 0.6);
                    border-radius: 10px;
                    padding: 2px 12px;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                }
            """)
        self.fire_badge.setVisible(True)

        # Dynamic motivational text by milestone
        if max_streak == 0:
            self.streak_desc.setText("Start your first streak today!")
        elif max_streak < 3:
            self.streak_desc.setText("Great start — keep going! 💪")
        elif max_streak < 7:
            self.streak_desc.setText("Building momentum — don't stop now!")
        elif max_streak < 14:
            self.streak_desc.setText("One week strong! You're on fire! 🔥")
        elif max_streak < 30:
            self.streak_desc.setText("Two weeks and counting! Incredible!")
        elif max_streak < 60:
            self.streak_desc.setText("A full month! You're unstoppable! 🏆")
        else:
            self.streak_desc.setText("Legendary! An absolute habit machine! 🌟")

        # Load weekly activity
        self.load_weekly_activity()
        self.update_notification_badge()

    def toggle_notifications(self):
        """Toggle notification panel"""
        if self.notif_panel.isVisible():
            self.notif_panel.hide()
        else:
            # Position panel below the button
            btn_pos = self.notif_btn.mapTo(self, self.notif_btn.rect().bottomLeft())
            self.notif_panel.move(btn_pos.x() - 300, btn_pos.y() + 10)
            self.notif_panel.load_notifications()
            self.notif_panel.show()
            self.notif_panel.raise_()

    def update_notification_badge(self):
        """Update unread notification badge"""
        from app.services.notification_service import get_notification_service
        service = get_notification_service()
        unread_count = service.get_unread_count()
        
        if unread_count > 0:
            self.notif_badge.setText(str(unread_count) if unread_count < 10 else "9+")
            self.notif_badge.show()
        else:
            self.notif_badge.hide()

    def mark_notifications_read(self):
        """Mark all notifications as read"""
        from app.services.notification_service import get_notification_service
        service = get_notification_service()
        service.mark_all_as_read()
        self.notif_panel.load_notifications()
        self.update_notification_badge()

    def load_weekly_activity(self):
        """Load weekly activity graph"""
        while self.week_grid.count():
            item = self.week_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        habits = self.habit_service.get_all_habits()
        today = datetime.now()
        days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

        for i in range(7):
            date = today - timedelta(days=6 - i)
            date_str = date.strftime("%Y-%m-%d")
            day_name = days[date.weekday()]

            completed_count = 0
            if habits:
                for habit in habits:
                    if self.habit_service.is_habit_completed_on_date(
                        habit.id, date_str
                    ):
                        completed_count += 1

            percentage = (
                int((completed_count / len(habits)) * 100) if len(habits) > 0 else 0
            )

            day_card = WeekDayCard(day_name, percentage, date.day)
            self.week_grid.addWidget(day_card)

    def apply_card_shadow(self, widget):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(35)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 8)
        widget.setGraphicsEffect(shadow)


# =============================================================================
# NOTIFICATION COMPONENTS
# =============================================================================

class NotificationItem(QFrame):
    """Premium Notification Card UI"""

    def __init__(self, notif_id, title, message, time_str, is_read=False, parent=None):
        super().__init__(parent)
        self.notif_id = notif_id
        self.setIsRead(is_read)
        self.setup_ui(title, message, time_str)

    def setIsRead(self, is_read):
        self.is_read = is_read
        from app.themes import get_theme_manager
        is_dark = get_theme_manager().is_dark_mode()
        
        if is_read:
            bg = "#1A1C23" if is_dark else "#F9FAFB"
            border = "#333645" if is_dark else "#F3F4F6"
            color = "#9CA3AF" if is_dark else "#6B7280"
            self.setStyleSheet(f"""
                QFrame {{
                    background-color: {bg};
                    border: 1px solid {border};
                    border-radius: 12px;
                }}
                QLabel {{ 
                    border: none; 
                    background: transparent;
                    color: {color};
                }}
            """)
        else:
            bg = "#252732" if is_dark else "#F0F7FF"
            border = "#6366F1" if is_dark else "#DBEAFE"
            self.setStyleSheet(f"""
                QFrame {{
                    background-color: {bg};
                    border: 1px solid {border};
                    border-radius: 12px;
                }}
                QLabel {{ 
                    border: none; 
                    background: transparent;
                }}
            """)

    def setup_ui(self, title, message, time_str):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(12)

        # Content container
        content_container = QVBoxLayout()
        content_container.setSpacing(4)

        header_row = QHBoxLayout()
        header_row.setSpacing(8)

        # Icon based on title
        icon = "🔔"
        if "Habit Completed" in title:
            icon = "✅"
        elif "Streak" in title:
            icon = "🔥"
        elif "Reminder" in title:
            icon = "📋"

        icon_label = QLabel(icon)
        icon_label.setFont(QFont("SF Pro Text", 14))
        icon_label.setFixedWidth(24)
        header_row.addWidget(icon_label)

        from app.themes import get_theme_manager
        is_dark = get_theme_manager().is_dark_mode()
        text_primary = "#F3F4F6" if is_dark else "#111827"
        text_secondary = "#9CA3AF" if is_dark else "#4B5563"

        title_label = QLabel(title)
        title_label.setFont(QFont("SF Pro Text", 13, QFont.Bold))
        title_label.setStyleSheet(f"color: {text_primary}; border: none;")
        header_row.addWidget(title_label, 1)

        time_label = QLabel(time_str)
        time_label.setFont(QFont("SF Pro Text", 10))
        time_label.setStyleSheet("color: #9CA3AF; border: none;")
        header_row.addWidget(time_label)

        content_container.addLayout(header_row)

        msg_label = QLabel(message)
        msg_label.setFont(QFont("SF Pro Text", 12))
        msg_label.setStyleSheet(f"color: {text_secondary}; border: none;")
        msg_label.setWordWrap(True)
        content_container.addWidget(msg_label)

        layout.addLayout(content_container, 1)

        # Mark as read button (only if unread)
        if not self.is_read:
            self.read_btn = QPushButton("✓")
            self.read_btn.setToolTip("Mark as read")
            self.read_btn.setFixedSize(28, 28)
            self.read_btn.setCursor(Qt.PointingHandCursor)
            self.read_btn.setStyleSheet("""
                QPushButton {
                    background-color: #E0E7FF;
                    color: #4F46E5;
                    border-radius: 14px;
                    border: none;
                    font-weight: bold;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #4F46E5;
                    color: white;
                }
            """)
            self.read_btn.clicked.connect(self.mark_read)
            layout.addWidget(self.read_btn, 0, Qt.AlignVCenter)

    def mark_read(self):
        from app.services.notification_service import get_notification_service
        service = get_notification_service()
        if service.mark_as_read(self.notif_id):
            self.setIsRead(True)
            if hasattr(self, "read_btn"):
                self.read_btn.deleteLater()
            
            # Find the panel to notify it to refresh badge
            parent = self.parent()
            while parent and not isinstance(parent, NotificationPanel):
                parent = parent.parent()
            if parent:
                parent.notify_change()


class NotificationPanel(QFrame):
    """Slide-down notification menu"""
    
    closed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(400)
        self.setFixedHeight(500)
        self.setup_ui()
        self.hide()

        if parent:
            parent.installEventFilter(self)

    def eventFilter(self, obj, event):
        """Click outside to close"""
        if event.type() == QEvent.MouseButtonPress and self.isVisible():
            if not self.geometry().contains(event.pos()):
                # Allow the toggle button to handle its own click
                if hasattr(self.parent(), "notif_btn"):
                    if self.parent().notif_btn.geometry().contains(event.pos()):
                        return False
                self.hide()
                return True
        return False

    def setup_ui(self):
        self.setObjectName("notificationPanel")
        from app.themes import get_theme_manager
        is_dark = get_theme_manager().is_dark_mode()
        bg = "#1A1C23" if is_dark else "#FFFFFF"
        border = "#333645" if is_dark else "#E5E7EB"
        self.setStyleSheet(f"""
            QFrame#notificationPanel {{
                background-color: {bg};
                border-radius: 20px;
                border: 1px solid {border};
            }}
        """)

        # Shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(50)
        shadow.setOffset(0, 15)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = QFrame()
        header.setFixedHeight(64)
        from app.themes import get_theme_manager
        is_dark = get_theme_manager().is_dark_mode()
        header_bg = "#252732" if is_dark else "#F9FAFB"
        header_border = "#333645" if is_dark else "#F3F4F6"
        header.setStyleSheet(f"""
            QFrame {{
                background-color: {header_bg};
                border-top-left-radius: 20px;
                border-top-right-radius: 20px;
                border-bottom: 1px solid {header_border};
            }}
        """)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(24, 0, 24, 0)

        title = QLabel("Notifications")
        title.setFont(QFont("SF Pro Display", 18, QFont.Bold))
        text_primary = "#F3F4F6" if is_dark else "#111827"
        title.setStyleSheet(f"color: {text_primary}; border: none; background: transparent;")
        header_layout.addWidget(title)

        header_layout.addStretch()

        self.mark_read_btn = QPushButton("Mark all as read")
        self.mark_read_btn.setCursor(Qt.PointingHandCursor)
        self.mark_read_btn.setFont(QFont("SF Pro Text", 11, QFont.Medium))
        self.mark_read_btn.setStyleSheet("""
            QPushButton {
                color: #3B82F6;
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                text-decoration: underline;
                color: #2563EB;
            }
        """)
        header_layout.addWidget(self.mark_read_btn)

        layout.addWidget(header)

        # Scroll area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setStyleSheet(f"""
            QScrollArea {{
                background: transparent; 
                border: none;
            }}
            QScrollBar:vertical {{
                border: none;
                background: {"#1A1C23" if is_dark else "#F9FAFB"};
                width: 10px;
                margin: 0px 0px 0px 0px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical {{
                background: #6366F1;
                min-height: 30px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: #4F46E5;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                border: none;
                background: none;
                height: 0px;
            }}
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{
                background: none;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
        """)

        self.list_container = QWidget()
        self.list_container.setStyleSheet("background: transparent; border: none;")
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setContentsMargins(16, 16, 16, 16)
        self.list_layout.setSpacing(12)
        self.list_layout.setAlignment(Qt.AlignTop)

        self.scroll.setWidget(self.list_container)
        layout.addWidget(self.scroll)

    def notify_change(self):
        self.closed.emit()

    def add_list_header(self, text):
        """Add a section header to the list"""
        header = QLabel(text)
        header.setFont(QFont("SF Pro Text", 12, QFont.Bold))
        header.setStyleSheet("color: #6B7280; border: none; padding-top: 8px; padding-bottom: 4px;")
        self.list_layout.addWidget(header)

    def load_notifications(self):
        from app.services.notification_service import get_notification_service
        service = get_notification_service()
        notifications = service.get_all_notifications()

        # Safely clear list
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not notifications:
            empty = QLabel("No notifications yet")
            empty.setFont(QFont("SF Pro Text", 14))
            empty.setStyleSheet("color: #9CA3AF; border: none;")
            empty.setAlignment(Qt.AlignCenter)
            empty.setMinimumHeight(120)
            self.list_layout.addWidget(empty)
        else:
            unread = [n for n in notifications if n["is_read"] == 0]
            read = [n for n in notifications if n["is_read"] == 1]

            if unread:
                self.add_list_header("New")
                for n in unread:
                    card = self._create_card(n)
                    self.list_layout.addWidget(card)
                
            if read:
                if unread:
                    self.list_layout.addSpacing(16)
                self.add_list_header("Earlier")
                for n in read:
                    card = self._create_card(n)
                    self.list_layout.addWidget(card)

        self.list_layout.addStretch()

    def _create_card(self, n):
        """Helper to create a notification card"""
        try:
            dt = datetime.fromisoformat(n["created_at"])
            time_str = dt.strftime("%I:%M %p")
        except Exception:
            time_str = "Recently"

        return NotificationItem(
            n["id"], n["title"], n["message"], time_str, n["is_read"] == 1
        )
