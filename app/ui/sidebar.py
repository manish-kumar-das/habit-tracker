from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QFrame,
)
from PySide6.QtGui import QIcon, QFont, QCursor
from PySide6.QtCore import Qt, Signal, QSize


class Sidebar(QWidget):
    """Modern Sidebar Navigation"""

    page_changed = Signal(str)  # Emits the page name when changed

    def __init__(self):
        super().__init__()
        self.setFixedWidth(260)
        self.setStyleSheet("""
            QWidget {
                background-color: #F8F9FE;
                border-right: 1px solid #E0E0E0;
            }
        """)
        self.active_btn = None
        self.buttons = {}
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 30, 20, 30)
        layout.setSpacing(10)

        # Logo Area
        logo_layout = QHBoxLayout()
        logo_layout.setSpacing(10)

        logo_icon = QLabel("🎯")  # Using emoji as placeholder for logo
        logo_icon.setFont(QFont("Segoe UI Emoji", 24))
        logo_icon.setStyleSheet("background: transparent; border: none;")

        logo_text = QLabel("HabitHub")
        logo_text.setFont(QFont("Plus Jakarta Sans", 18, QFont.Bold))
        logo_text.setStyleSheet(
            "color: #1A365D; background: transparent; border: none;"
        )

        logo_layout.addWidget(logo_icon)
        logo_layout.addWidget(logo_text)
        logo_layout.addStretch()

        layout.addLayout(logo_layout)
        layout.addSpacing(40)

        # Navigation Buttons
        self.add_nav_button("Dashboard", "⊞", "dashboard", layout, active=True)
        self.add_nav_button("Today", "📅", "today", layout)
        self.add_nav_button("Habits", "✅", "habits", layout)
        self.add_nav_button("Analytics", "📊", "analytics", layout)
        self.add_nav_button("Goals", "🏆", "goals", layout)
        self.add_nav_button("Settings", "⚙️", "settings", layout)

        layout.addStretch()

        # User Profile Area (Bottom)
        profile_frame = QFrame()
        profile_frame.setStyleSheet("""
            QFrame {
                background-color: #E2E8F0;
                border-radius: 12px;
                padding: 10px;
                border: none;
            }
        """)
        profile_layout = QHBoxLayout(profile_frame)
        profile_layout.setContentsMargins(10, 10, 10, 10)

        avatar = QLabel("👨‍💼")
        avatar.setFont(QFont("Segoe UI Emoji", 24))
        avatar.setStyleSheet("background: transparent; border: none;")

        user_info = QVBoxLayout()
        user_info.setSpacing(2)
        name = QLabel("Alex Morgan")
        name.setFont(QFont("Plus Jakarta Sans", 14, QFont.Bold))
        name.setStyleSheet("color: #1A365D; background: transparent; border: none;")
        role = QLabel("Premium Member")
        role.setFont(QFont("Inter", 10))
        role.setStyleSheet("color: #718096; background: transparent; border: none;")

        user_info.addWidget(name)
        user_info.addWidget(role)

        profile_layout.addWidget(avatar)
        profile_layout.addLayout(user_info)

        layout.addWidget(profile_frame)

    def add_nav_button(self, text, icon, page_id, layout, active=False):
        btn = QPushButton(f"  {icon}   {text}")
        btn.setCheckable(True)
        btn.setFont(QFont("Plus Jakarta Sans", 14, QFont.Medium))
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedHeight(50)
        btn.setStyleSheet(self.get_btn_style(active))

        if active:
            btn.setChecked(True)
            self.active_btn = btn

        btn.clicked.connect(lambda: self.on_nav_clicked(btn, page_id))

        layout.addWidget(btn)
        self.buttons[page_id] = btn

    def on_nav_clicked(self, btn, page_id):
        if self.active_btn:
            self.active_btn.setChecked(False)
            self.active_btn.setStyleSheet(self.get_btn_style(False))

        btn.setChecked(True)
        btn.setStyleSheet(self.get_btn_style(True))
        self.active_btn = btn

        self.page_changed.emit(page_id)

    def get_btn_style(self, active):
        if active:
            return """
                QPushButton {
                    background-color: #3734A9;
                    color: white;
                    border-radius: 12px;
                    text-align: left;
                    padding-left: 20px;
                    border: none;
                }
            """
        else:
            return """
                QPushButton {
                    background-color: transparent;
                    color: #718096;
                    border-radius: 12px;
                    text-align: left;
                    padding-left: 20px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #E2E8F0;
                    color: #2D3748;
                }
            """
