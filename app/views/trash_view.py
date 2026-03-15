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
        from app.themes import get_theme_manager
        is_dark = get_theme_manager().is_dark_mode()
        bg_color = "#1A1C23" if is_dark else "#F9FAFB"
        
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {bg_color};
            }}
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
        text_color = "#F3F4F6" if is_dark else "#111827"
        title.setStyleSheet(f"color: {text_color}; background: transparent;")
        title_layout.addWidget(title)

        subtitle = QLabel("Restore or permanently remove deleted habits")
        subtitle.setFont(QFont("SF Pro Text", 13))
        sub_text_color = "#9CA3AF" if is_dark else "#6B7280"
        subtitle.setStyleSheet(f"color: {sub_text_color}; background: transparent;")
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
        scroll.setStyleSheet(f"""
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
        btn_bg = "#333645" if is_dark else "#F3F4F6"
        btn_hover = "#404354" if is_dark else "#E5E7EB"
        btn_text = "#F3F4F6" if is_dark else "#374151"
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {btn_bg};
                color: {btn_text};
                border: none;
                border-radius: 12px;
                padding: 0px 32px;
            }}
            QPushButton:hover {{
                background-color: {btn_hover};
            }}
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
            from app.themes import get_theme_manager
            if get_theme_manager().is_dark_mode():
                empty_label.setStyleSheet("color: #9CA3AF; background: transparent;")
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
        from app.themes import get_theme_manager
        is_dark = get_theme_manager().is_dark_mode()
        card_bg = "#252732" if is_dark else "#FFFFFF"
        border_color = "#333645" if is_dark else "rgba(0, 0, 0, 0.05)"

        card = QFrame()
        card.setObjectName("trashCard")
        card.setMinimumHeight(90)
        card.setStyleSheet(f"""
            QFrame#trashCard {{
                background-color: {card_bg};
                border: 1px solid {border_color};
                border-radius: 16px;
            }}
            QFrame#trashCard:hover {{
                border: 1px solid rgba(99, 102, 241, 0.2);
            }}
            QLabel {{
                border: none;
                background: transparent;
            }}
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
        name_text = "#F3F4F6" if is_dark else "#111827"
        name_label.setStyleSheet(f"color: {name_text};")
        info_layout.addWidget(name_label)

        details_parts = []
        if habit["category"]:
            details_parts.append(f"📂 {habit['category']}")
        if habit["frequency"]:
            details_parts.append(f"🔄 {habit['frequency']}")
        details_parts.append(f"✅ {habit['completion_count']} completions")

        details_label = QLabel(" • ".join(details_parts))
        details_label.setFont(QFont("SF Pro Text", 11))
        sub_text = "#9CA3AF" if is_dark else "#6B7280"
        details_label.setStyleSheet(f"color: {sub_text};")
        info_layout.addWidget(details_label)

        try:
            deleted_at = habit["deleted_at"]
        except (KeyError, IndexError):
            deleted_at = "Unknown"
        time_label = QLabel(f"Deleted: {deleted_at}")
        time_label.setFont(QFont("SF Pro Text", 10))
        time_label.setStyleSheet(f"color: {sub_text};")
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
            
            from app.themes import get_theme_manager
            is_dark = get_theme_manager().is_dark_mode()
            
            msg = QMessageBox(self)
            msg.setWindowTitle("Habit Restored")
            msg.setText("✅ Habit has been successfully restored!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setIcon(QMessageBox.Information)

            if is_dark:
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
                """)
            
            msg.exec_()
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
        from app.themes import get_theme_manager
        is_dark = get_theme_manager().is_dark_mode()
        
        reply_box = QMessageBox(self)
        reply_box.setWindowTitle("Empty Trash")
        reply_box.setText("⚠️ This will permanently delete all habits in the trash.\n\nThis action cannot be undone!\n\nAre you sure?")
        reply_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        reply_box.setDefaultButton(QMessageBox.No)
        reply_box.setIcon(QMessageBox.Question)

        if is_dark:
            reply_box.setStyleSheet("""
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

        if reply_box.exec_() != QMessageBox.Yes:
            return

        try:
            self.habit_service.empty_trash()
            
            success_box = QMessageBox(self)
            success_box.setWindowTitle("Trash Emptied")
            success_box.setText("✅ Trash has been emptied successfully!")
            success_box.setStandardButtons(QMessageBox.Ok)
            success_box.setIcon(QMessageBox.Information)

            if is_dark:
                success_box.setStyleSheet("""
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
                """)
            
            success_box.exec_()
            self.load_deleted_habits()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to empty trash: {str(e)}",
                QMessageBox.Ok,
            )
