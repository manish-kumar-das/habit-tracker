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
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor
from app.services.habit_service import get_habit_service
from app.services.streak_service import get_streak_service
from app.services.profile_service import get_profile_service


class PremiumCardShadow(QGraphicsDropShadowEffect):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setBlurRadius(40)
        self.setOffset(0, 12)
        self.setColor(QColor(0, 0, 0, 20))


class StatCard(QFrame):
    """Substantial and bold stat card with large iconography"""

    def __init__(self, icon, value, label, color, parent=None):
        super().__init__(parent)
        # Larger footprint to feel substantial
        self.setFixedSize(220, 150)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: #FFFFFF;
                border: 1px solid rgba(0, 0, 0, 0.06);
                border-radius: 28px;
            }}
            QFrame:hover {{
                border: 2px solid {color}40;
                background-color: #FAFAFF;
            }}
        """)

        # Stronger shadow for the larger card
        shadow = PremiumCardShadow(self)
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        # Header with Large Icon
        header = QHBoxLayout()
        icon_wrapper = QFrame()
        icon_wrapper.setFixedSize(56, 56)  # Large icon container
        icon_wrapper.setStyleSheet(f"""
            background-color: {color}15; 
            border-radius: 18px;
        """)
        icon_layout = QVBoxLayout(icon_wrapper)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.setAlignment(Qt.AlignCenter)

        icon_lbl = QLabel(icon)
        icon_lbl.setFont(QFont("SF Pro Display", 28))  # Much larger icon
        icon_lbl.setStyleSheet("background: transparent; border: none;")
        icon_layout.addWidget(icon_lbl)

        header.addWidget(icon_wrapper)
        header.addStretch()
        layout.addLayout(header)

        # Large Bold Value
        self.value_label = QLabel(value)
        self.value_label.setFont(QFont("SF Pro Display", 34, QFont.Bold))
        self.value_label.setStyleSheet("color: #111827; background: transparent;")
        layout.addWidget(self.value_label)

        # Clear Descriptive Label
        self.label_label = QLabel(label.upper())
        self.label_label.setFont(QFont("SF Pro Text", 11, QFont.Bold))
        self.label_label.setStyleSheet(
            "color: #9CA3AF; letter-spacing: 1.5px; background: transparent;"
        )
        layout.addWidget(self.label_label)


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
        self.setStyleSheet("background-color: #F8F9FA;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. COMPACT HERO HEADER
        header = QFrame()
        header.setFixedHeight(240)
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #6366F1, stop:1 #A855F7);
            }
        """)

        header_layout = QVBoxLayout(header)
        header_layout.setAlignment(Qt.AlignCenter)
        header_layout.setContentsMargins(0, 30, 0, 30)

        # Avatar Composition
        avatar_outer = QFrame()
        avatar_outer.setFixedSize(110, 110)
        avatar_outer.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.2);
            border-radius: 55px;
            border: 3px solid rgba(255, 255, 255, 0.4);
        """)

        avatar_layout = QVBoxLayout(avatar_outer)
        avatar_layout.setContentsMargins(0, 0, 0, 0)
        avatar_layout.setAlignment(Qt.AlignCenter)

        avatar_label = QLabel("👤")
        avatar_label.setFont(QFont("SF Pro Display", 60))
        avatar_label.setAlignment(Qt.AlignCenter)
        avatar_label.setStyleSheet(
            "color: #4F46E5; background: transparent; border: none;"
        )
        avatar_layout.addWidget(avatar_label)

        header_layout.addWidget(avatar_outer, alignment=Qt.AlignCenter)

        self.name_header = QLabel("Loading...")
        self.name_header.setFont(QFont("SF Pro Display", 32, QFont.Bold))
        self.name_header.setStyleSheet("color: white; margin-top: 15px;")
        header_layout.addWidget(self.name_header, alignment=Qt.AlignCenter)

        main_layout.addWidget(header)

        # 2. CONTENT AREA
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(40, -40, 40, 40)  # Overlap effect
        content_layout.setSpacing(32)

        # STATS ROW (Fixed Underflow)
        self.stats_hlayout = QHBoxLayout()
        self.stats_hlayout.setSpacing(24)
        # Using a centered container for stats to prevent "underflow" feel
        stats_outer = QWidget()
        stats_outer.setLayout(self.stats_hlayout)
        content_layout.addWidget(stats_outer, alignment=Qt.AlignCenter)

        # SETTINGS FORM
        settings_card = QFrame()
        settings_card.setStyleSheet(
            "QFrame { background-color: #FFFFFF; border-radius: 32px; border: 1px solid rgba(0,0,0,0.05); }"
        )

        # Shadow for main card
        card_shadow = PremiumCardShadow(settings_card)
        settings_card.setGraphicsEffect(card_shadow)

        card_layout = QVBoxLayout(settings_card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(28)

        title = QLabel("Identity & Bio")
        title.setFont(QFont("SF Pro Display", 22, QFont.Bold))
        title.setStyleSheet("color: #111827;")
        card_layout.addWidget(title)

        # Input Forms
        self.inputs = {}
        self.inputs["name"] = self._add_input("Full Name", "👤", card_layout)
        self.inputs["email"] = self._add_input("Email", "📧", card_layout)
        self.inputs["bio"] = self._add_input(
            "Personal Bio", "📝", card_layout, multiline=True
        )

        # Save Button
        self.save_btn = QPushButton("DEPLOY CHANGES")
        self.save_btn.setFont(QFont("SF Pro Text", 14, QFont.Bold))
        self.save_btn.setFixedHeight(56)
        self.save_btn.setCursor(Qt.PointingHandCursor)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6366F1, stop:1 #4F46E5);
                color: white;
                border-radius: 16px;
                border: none;
            }
            QPushButton:hover { background-color: #4F46E5; }
            QPushButton:pressed { margin-top: 2px; }
        """)
        self.save_btn.clicked.connect(self.save_profile)
        card_layout.addWidget(self.save_btn)

        content_layout.addWidget(settings_card)
        content_layout.addStretch()

        main_layout.addWidget(content_container)

    def _add_input(self, label, icon, parent_layout, multiline=False):
        v_box = QVBoxLayout()
        v_box.setSpacing(8)

        lbl = QLabel(label.upper())
        lbl.setFont(QFont("SF Pro Text", 10, QFont.Bold))
        lbl.setStyleSheet("color: #6B7280; letter-spacing: 1px;")
        v_box.addWidget(lbl)

        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: #F9FAFB;
                border: 2px solid #F1F5F9;
                border-radius: 14px;
            }
            QFrame:focus-within {
                border: 2px solid #6366F1;
                background-color: white;
            }
        """)
        c_layout = QHBoxLayout(container)
        c_layout.setContentsMargins(16, 5, 16, 5)

        icon_lbl = QLabel(icon)
        icon_lbl.setFont(QFont("SF Pro Display", 16))
        c_layout.addWidget(icon_lbl)

        if multiline:
            edit = QTextEdit()
            edit.setFixedHeight(90)
            edit.setStyleSheet(
                "border: none; background: transparent; font-size: 15px;"
            )
        else:
            edit = QLineEdit()
            edit.setFixedHeight(44)
            edit.setStyleSheet(
                "border: none; background: transparent; font-size: 15px;"
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
