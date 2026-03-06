"""
Trash Dialog - View and restore deleted habits
Premium dialog with modern card-based design
"""

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QFrame,
    QWidget,
    QGraphicsDropShadowEffect,
    QMessageBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor
from app.services.habit_service import get_habit_service


class TrashDialog(QDialog):
    """Premium dialog for viewing and restoring deleted habits"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.habit_service = get_habit_service()
        self.setWindowTitle("🗑️ Deleted Habits")
        self.setMinimumSize(600, 500)
        self.setMaximumSize(800, 700)
        self.setup_ui()

    def setup_ui(self):
        """Setup the trash dialog UI"""
        self.setStyleSheet("""
            QDialog {
                background-color: #F9FAFB;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)

        icon_label = QLabel("🗑️")
        icon_label.setFont(QFont("SF Pro Display", 32))
        icon_label.setStyleSheet("background: transparent;")
        header_layout.addWidget(icon_label)

        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)

        title = QLabel("Deleted Habits")
        title.setFont(QFont("SF Pro Display", 24, QFont.Bold))
        title.setStyleSheet("color: #111827; background: transparent;")
        title_layout.addWidget(title)

        subtitle = QLabel("Restore or permanently remove deleted habits")
        subtitle.setFont(QFont("SF Pro Text", 13))
        subtitle.setStyleSheet("color: #6B7280; background: transparent;")
        title_layout.addWidget(subtitle)

        header_layout.addLayout(title_layout)
        header_layout.addStretch()

        # Empty Trash button
        empty_btn = QPushButton("🔥 Empty Trash")
        empty_btn.setFont(QFont("SF Pro Text", 13, QFont.Bold))
        empty_btn.setFixedHeight(42)
        empty_btn.setCursor(Qt.PointingHandCursor)
        empty_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #EF4444, stop:1 #DC2626);
                color: #FFFFFF;
                border: none;
                border-radius: 12px;
                padding: 0px 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #DC2626, stop:1 #B91C1C);
            }
        """)
        empty_btn.clicked.connect(self.empty_trash)
        header_layout.addWidget(empty_btn)

        layout.addLayout(header_layout)

        # Scroll area for deleted habits
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background: #F3F4F6;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #6366F1;
                border-radius: 4px;
            }
        """)

        self.list_container = QWidget()
        self.list_container.setStyleSheet("background-color: transparent;")
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(12)

        scroll.setWidget(self.list_container)
        layout.addWidget(scroll)

        # Close button
        close_btn = QPushButton("Close")
        close_btn.setFont(QFont("SF Pro Text", 14, QFont.Bold))
        close_btn.setFixedHeight(46)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #F3F4F6;
                color: #374151;
                border: none;
                border-radius: 12px;
                padding: 0px 32px;
            }
            QPushButton:hover {
                background-color: #E5E7EB;
            }
        """)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn, alignment=Qt.AlignRight)

        # Load items
        self.load_deleted_habits()

    def load_deleted_habits(self):
        """Load and display deleted habits"""
        # Clear existing items
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        deleted_habits = self.habit_service.get_deleted_habits(limit=50)

        if not deleted_habits:
            empty_label = QLabel("🎉 Trash is empty! No deleted habits.")
            empty_label.setFont(QFont("SF Pro Text", 15))
            empty_label.setStyleSheet("color: #6B7280; background: transparent;")
            empty_label.setAlignment(Qt.AlignCenter)
            self.list_layout.addWidget(empty_label)
            self.list_layout.addStretch()
            return

        for habit in deleted_habits:
            card = self._create_trash_card(habit)
            self.list_layout.addWidget(card)

        self.list_layout.addStretch()

    def _create_trash_card(self, habit):
        """Create a card for a deleted habit"""
        card = QFrame()
        card.setObjectName("trashCard")
        card.setMinimumHeight(90)
        card.setStyleSheet("""
            QFrame#trashCard {
                background-color: #FFFFFF;
                border: 1px solid rgba(0, 0, 0, 0.05);
                border-radius: 16px;
            }
            QFrame#trashCard:hover {
                border: 1px solid rgba(99, 102, 241, 0.2);
            }
            QLabel {
                border: none;
                background: transparent;
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 15))
        shadow.setOffset(0, 4)
        card.setGraphicsEffect(shadow)

        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(20, 16, 20, 16)
        card_layout.setSpacing(16)

        # Accent strip
        accent = QFrame()
        accent.setFixedWidth(4)
        accent.setStyleSheet("""
            QFrame {
                background-color: #EF4444;
                border-radius: 2px;
            }
        """)
        card_layout.addWidget(accent)

        # Icon
        icon_label = QLabel("🗑️")
        icon_label.setFont(QFont("SF Pro Display", 24))
        card_layout.addWidget(icon_label)

        # Info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)

        name_label = QLabel(habit["name"])
        name_label.setFont(QFont("SF Pro Display", 15, QFont.Bold))
        name_label.setStyleSheet("color: #111827;")
        info_layout.addWidget(name_label)

        details_parts = []
        if habit["category"]:
            details_parts.append(f"📂 {habit['category']}")
        if habit["frequency"]:
            details_parts.append(f"🔄 {habit['frequency']}")
        details_parts.append(f"✅ {habit['completion_count']} completions")

        details_label = QLabel(" • ".join(details_parts))
        details_label.setFont(QFont("SF Pro Text", 11))
        details_label.setStyleSheet("color: #6B7280;")
        info_layout.addWidget(details_label)

        try:
            deleted_at = habit["deleted_at"]
        except (KeyError, IndexError):
            deleted_at = "Unknown"
        time_label = QLabel(f"Deleted: {deleted_at}")
        time_label.setFont(QFont("SF Pro Text", 10))
        time_label.setStyleSheet("color: #9CA3AF;")
        info_layout.addWidget(time_label)

        card_layout.addLayout(info_layout, stretch=1)

        # Restore button
        restore_btn = QPushButton("♻️ Restore")
        restore_btn.setFont(QFont("SF Pro Text", 12, QFont.Bold))
        restore_btn.setFixedHeight(40)
        restore_btn.setFixedWidth(120)
        restore_btn.setCursor(Qt.PointingHandCursor)
        restore_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #10B981, stop:1 #059669);
                color: #FFFFFF;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #059669, stop:1 #047857);
            }
        """)
        habit_id = habit["id"]
        restore_btn.clicked.connect(lambda checked, hid=habit_id: self.restore_habit(hid))
        card_layout.addWidget(restore_btn)

        return card

    def restore_habit(self, deleted_habit_id):
        """Restore a deleted habit"""
        try:
            self.habit_service.restore_habit(deleted_habit_id)
            QMessageBox.information(
                self,
                "Habit Restored",
                "✅ Habit has been successfully restored!",
                QMessageBox.Ok,
            )
            self.load_deleted_habits()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to restore habit: {str(e)}",
                QMessageBox.Ok,
            )

    def empty_trash(self):
        """Permanently delete all trashed habits"""
        reply = QMessageBox.question(
            self,
            "Empty Trash",
            "⚠️ This will permanently delete all habits in the trash.\n\nThis action cannot be undone!\n\nAre you sure?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply != QMessageBox.Yes:
            return

        try:
            self.habit_service.empty_trash()
            QMessageBox.information(
                self,
                "Trash Emptied",
                "✅ Trash has been emptied successfully!",
                QMessageBox.Ok,
            )
            self.load_deleted_habits()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to empty trash: {str(e)}",
                QMessageBox.Ok,
            )
