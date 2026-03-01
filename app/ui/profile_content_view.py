"""
Profile Content View - Final Premium Polished Edition
Large, substantial cards with bold typography and perfect structural integrity.
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QLineEdit,
    QTextEdit,
    QMessageBox,
    QGraphicsDropShadowEffect,
    QProgressBar,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor
from app.services.habit_service import get_habit_service
from app.services.streak_service import get_streak_service
from app.services.profile_service import get_profile_service


class ElevatedShadow(QGraphicsDropShadowEffect):
    def __init__(self, parent=None, level=1):
        super().__init__(parent)
        self.set_level(level)

    def set_level(self, level):
        if level == 1:
            self.setBlurRadius(12)
            self.setOffset(0, 4)
            self.setColor(QColor(0, 0, 0, 10))
        elif level == 2:
            self.setBlurRadius(24)
            self.setOffset(0, 8)
            self.setColor(QColor(0, 0, 0, 15))
        elif level == 3:  # Minimal/Soft
            self.setBlurRadius(8)
            self.setOffset(0, 2)
            self.setColor(QColor(0, 0, 0, 8))


class XPProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(8)
        self.setMinimumWidth(200)
        self.setTextVisible(False)
        self.setStyleSheet("""
            QProgressBar {
                background-color: #F1F5F9;
                border-radius: 4px;
                border: none;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7C3AED, stop:1 #A855F7);
                border-radius: 4px;
            }
        """)


class StatCard(QFrame):
    """Refined SaaS-style stat card with horizontal layout"""

    def __init__(self, icon, value, label, color, parent=None):
        super().__init__(parent)
        self.setFixedHeight(120)
        self.setMinimumWidth(260)
        self.color = color

        self.setObjectName("statCard")
        self.setStyleSheet("""
            #statCard {
                background-color: #FFFFFF;
                border: 1px solid #F1F5F9;
                border-radius: 20px;
            }
        """)

        # Level 1 Shadow
        self.shadow = ElevatedShadow(self, level=1)
        self.setGraphicsEffect(self.shadow)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(20)

        # Icon with tinted background
        self.icon_bg = QFrame()
        self.icon_bg.setFixedSize(64, 64)
        self.icon_bg.setStyleSheet(f"""
            background-color: {color}10;
            border-radius: 16px;
        """)
        icon_layout = QVBoxLayout(self.icon_bg)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.setAlignment(Qt.AlignCenter)

        icon_lbl = QLabel(icon)
        icon_lbl.setFont(QFont("SF Pro Display", 28))
        icon_layout.addWidget(icon_lbl)
        layout.addWidget(self.icon_bg)

        # Content Column
        content_col = QVBoxLayout()
        content_col.setSpacing(2)
        content_col.setAlignment(Qt.AlignVCenter)

        self.value_label = QLabel(value)
        self.value_label.setFont(QFont("SF Pro Display", 36, QFont.Bold))
        self.value_label.setStyleSheet("color: #0F172A; background: transparent;")
        content_col.addWidget(self.value_label)

        self.label_label = QLabel(label.upper())
        self.label_label.setFont(QFont("Inter", 11, QFont.Bold))
        self.label_label.setStyleSheet("color: #64748B; letter-spacing: 0.5px;")
        content_col.addWidget(self.label_label)

        layout.addLayout(content_col)
        layout.addStretch()

    def enterEvent(self, event):
        self.shadow.set_level(2)
        self.setStyleSheet(f"""
            #statCard {{
                background-color: {self.color}05;
                border: 1px solid {self.color}30;
                border-radius: 20px;
            }}
        """)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.shadow.set_level(1)
        self.setStyleSheet("""
            #statCard {
                background-color: #FFFFFF;
                border: 1px solid #F1F5F9;
                border-radius: 20px;
            }
        """)
        super().leaveEvent(event)


class ProfileContentView(QWidget):
    """Polished Profile View - Substantial Cards & Fixed Layout"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.habit_service = get_habit_service()
        self.streak_service = get_streak_service()
        self.profile_service = get_profile_service()
        self.setup_ui()
        self.load_profile_data()

    def setup_ui(self):
        self.setStyleSheet("background-color: #F5F7FA;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(64, 48, 64, 64)
        main_layout.setSpacing(48)

        # 1. PREMIUM HEADER CARD
        header_card = QFrame()
        header_card.setFixedHeight(140)
        header_card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 20px;
                border: 1px solid #F1F5F9;
            }
        """)
        header_shadow = ElevatedShadow(header_card, level=1)
        header_card.setGraphicsEffect(header_shadow)

        header_layout = QHBoxLayout(header_card)
        header_layout.setContentsMargins(40, 0, 40, 0)
        header_layout.setSpacing(24)

        # Avatar with subtle neutral border
        avatar_container = QFrame()
        avatar_container.setFixedSize(92, 92)
        avatar_container.setStyleSheet("""
            background-color: #FFFFFF;
            border-radius: 46px;
            border: 1px solid #E5E7EB;
        """)
        avatar_shadow = ElevatedShadow(avatar_container, level=3)
        avatar_container.setGraphicsEffect(avatar_shadow)

        av_inner_layout = QVBoxLayout(avatar_container)
        av_inner_layout.setContentsMargins(0, 0, 0, 0)
        av_inner_layout.setAlignment(Qt.AlignCenter)

        avatar_lbl = QLabel("👤")
        avatar_lbl.setFont(QFont("SF Pro Display", 48))
        avatar_lbl.setStyleSheet("color: #7C3AED; background: transparent;")
        av_inner_layout.addWidget(avatar_lbl)

        header_layout.addWidget(avatar_container)

        # Name and secondary info
        info_col = QVBoxLayout()
        info_col.setSpacing(12)
        info_col.setAlignment(Qt.AlignVCenter)

        # Name Typography
        self.name_header = QLabel("Loading...")
        self.name_header.setFont(QFont("SF Pro Display", 30, QFont.Bold))
        self.name_header.setStyleSheet(
            "color: #0F172A; letter-spacing: 0.5px; background: transparent;"
        )
        info_col.addWidget(self.name_header)

        # Stats Column (XP & Bar)
        stats_sub_col = QVBoxLayout()
        stats_sub_col.setSpacing(8)

        xp_text_layout = QHBoxLayout()
        level_lbl = QLabel("Level 3")
        level_lbl.setFont(QFont("Inter", 14, QFont.DemiBold))
        level_lbl.setStyleSheet("color: #4B5563;")

        sep = QLabel("•")
        sep.setStyleSheet("color: #94A3B8; margin: 0 4px;")

        xp_lbl = QLabel("1,240 Total XP")
        xp_lbl.setFont(QFont("Inter", 14))
        xp_lbl.setStyleSheet("color: #4B5563;")

        xp_text_layout.addWidget(level_lbl)
        xp_text_layout.addWidget(sep)
        xp_text_layout.addWidget(xp_lbl)
        xp_text_layout.addStretch()

        stats_sub_col.addLayout(xp_text_layout)

        # Progress Bar aligned with percentage
        xp_row = QHBoxLayout()
        xp_row.setSpacing(16)

        self.xp_bar = XPProgressBar()
        self.xp_bar.setFixedHeight(8)
        self.xp_bar.setValue(65)
        xp_row.addWidget(self.xp_bar)

        self.xp_percent = QLabel("65%")
        self.xp_percent.setFont(QFont("Inter", 12, QFont.Bold))
        self.xp_percent.setStyleSheet("color: #7C3AED;")
        xp_row.addWidget(self.xp_percent)

        stats_sub_col.addLayout(xp_row)
        info_col.addLayout(stats_sub_col)

        header_layout.addLayout(info_col)
        header_layout.addStretch()

        # Streak Badge (Aligned with Info)
        streak_badge = QFrame()
        streak_badge.setFixedHeight(32)
        streak_badge.setCursor(Qt.PointingHandCursor)
        streak_badge.setStyleSheet("""
            QFrame {
                background-color: #F5F3FF;
                border: 1px solid #DDD6FE;
                border-radius: 16px;
            }
            QFrame:hover {
                background-color: #EDE9FE;
                border: 1px solid #C4B5FD;
            }
        """)
        badge_layout = QHBoxLayout(streak_badge)
        badge_layout.setContentsMargins(12, 0, 12, 0)

        badge_text = QLabel("🔥 3 DAY STREAK")
        badge_text.setFont(QFont("Inter", 10, QFont.Bold))
        badge_text.setStyleSheet("color: #7C3AED; letter-spacing: 0.5px;")
        badge_layout.addWidget(badge_text)

        header_layout.addWidget(streak_badge, alignment=Qt.AlignVCenter)

        main_layout.addWidget(header_card)

        # 2. STATS ROW
        self.stats_hlayout = QHBoxLayout()
        self.stats_hlayout.setSpacing(24)
        main_layout.addLayout(self.stats_hlayout)

        # 3. ACCOUNT SETTINGS CARD
        settings_card = QFrame()
        settings_card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 20px;
                border: 1px solid #F1F5F9;
            }
        """)
        settings_shadow = ElevatedShadow(settings_card, level=1)
        settings_card.setGraphicsEffect(settings_shadow)

        card_layout = QVBoxLayout(settings_card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(24)

        # Header
        title = QLabel("Account Settings")
        title.setFont(QFont("SF Pro Display", 22, QFont.DemiBold))
        title.setStyleSheet("color: #0F172A;")
        card_layout.addWidget(title)

        # We'll rely on spacing instead of a divider for a more minimal production look
        card_layout.addSpacing(8)

        # Input Fields
        self.inputs = {}
        input_container = QVBoxLayout()
        input_container.setSpacing(16)

        self.inputs["name"] = self._add_input(
            "Full Display Name", "👤", input_container
        )
        self.inputs["email"] = self._add_input("Email Address", "📧", input_container)
        self.inputs["bio"] = self._add_input(
            "Short Bio", "📝", input_container, multiline=True
        )

        card_layout.addLayout(input_container)

        # Save Button
        btn_wrapper = QHBoxLayout()
        btn_wrapper.addStretch()

        self.save_btn = QPushButton("Save Changes")
        self.save_btn.setFixedWidth(240)
        self.save_btn.setFixedHeight(50)
        self.save_btn.setFont(QFont("Inter", 14, QFont.Bold))
        self.save_btn.setCursor(Qt.PointingHandCursor)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7C3AED, stop:1 #6D28D9);
                color: white;
                border-radius: 25px;
                border: none;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #8B5CF6, stop:1 #7C3AED);
                margin-top: -2px;
            }
        """)
        btn_shadow = ElevatedShadow(self.save_btn, level=1)
        btn_shadow.setBlurRadius(15)
        btn_shadow.setColor(QColor(124, 58, 237, 30))
        self.save_btn.setGraphicsEffect(btn_shadow)
        self.save_btn.clicked.connect(self.save_profile)

        btn_wrapper.addWidget(self.save_btn)
        btn_wrapper.addStretch()

        card_layout.addLayout(btn_wrapper)
        main_layout.addWidget(settings_card)
        main_layout.addStretch()

    def _add_input(self, label, icon, parent_layout, multiline=False):
        v_box = QVBoxLayout()
        v_box.setSpacing(6)

        lbl = QLabel(label.upper())
        lbl.setFont(QFont("Inter", 11, QFont.Bold))  # Increased contrast
        lbl.setStyleSheet("color: #475569; letter-spacing: 0.5px;")
        v_box.addWidget(lbl)

        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E4E7EC;
                border-radius: 12px;
            }
            QFrame:hover {
                border: 1px solid #CBD5E1;
            }
            QFrame:focus-within {
                border: 2px solid #7C3AED;
            }
        """)

        c_layout = QHBoxLayout(container)
        c_layout.setContentsMargins(16, 4, 16, 4)

        icon_lbl = QLabel(icon)
        icon_lbl.setFont(QFont("SF Pro Display", 16))
        icon_lbl.setStyleSheet("color: #94A3B8;")
        c_layout.addWidget(icon_lbl)

        if multiline:
            edit = QTextEdit()
            edit.setFixedHeight(96)
            edit.setStyleSheet(
                "border: none; background: transparent; font-size: 15px; color: #1E293B;"
            )
        else:
            edit = QLineEdit()
            edit.setFixedHeight(46)
            edit.setStyleSheet(
                "border: none; background: transparent; font-size: 15px; color: #1E293B;"
            )

        c_layout.addWidget(edit)
        v_box.addWidget(container)
        parent_layout.addLayout(v_box)
        return edit

    def load_profile_data(self):
        profile = self.profile_service.get_profile()
        self.name_header.setText(profile["name"])
        self.inputs["name"].setText(profile["name"])
        self.inputs["email"].setText(profile["email"])
        self.inputs["bio"].setText(profile["bio"])
        self.load_statistics()

    def load_statistics(self):
        while self.stats_hlayout.count():
            item = self.stats_hlayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        habits = self.habit_service.get_all_habits()
        stats = [
            ("🎯", str(len(habits)), "Habits", "#6366F1"),
            (
                "🚀",
                str(
                    sum(
                        len(self.habit_service.get_habit_completions(h.id))
                        for h in habits
                    )
                ),
                "Total XP",
                "#10B981",
            ),
            (
                "🔥",
                str(
                    max(
                        [
                            self.streak_service.get_streak_info(h.id)["current_streak"]
                            for h in habits
                        ]
                        + [0]
                    )
                ),
                "Streak",
                "#F59E0B",
            ),
        ]

        for icon, val, lbl, col in stats:
            self.stats_hlayout.addWidget(StatCard(icon, val, lbl, col))

    def save_profile(self):
        name = self.inputs["name"].text().strip()
        email = self.inputs["email"].text().strip()
        bio = self.inputs["bio"].toPlainText().strip()

        if not name:
            QMessageBox.warning(
                self, "Validation Error", "Please provide a valid display name."
            )
            return

        try:
            self.profile_service.update_profile(name=name, email=email, bio=bio)
            self.name_header.setText(name)
            if self.main_window and hasattr(self.main_window, "sidebar"):
                self.main_window.sidebar.update_profile_name(name)
            QMessageBox.information(self, "Success", "Profile updated successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Sync Failed", f"Unexpected error: {str(e)}")
