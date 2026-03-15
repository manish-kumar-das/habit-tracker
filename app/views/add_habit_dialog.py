"""
Add habit dialog with category support
"""

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QMessageBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from app.services.habit_service import get_habit_service
from app.utils.constants import CATEGORIES
from app.themes import get_theme_manager


class AddHabitDialog(QDialog):
    """Dialog for adding a new habit with category"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.habit_service = get_habit_service()
        self.theme_manager = get_theme_manager()
        self.setup_ui()

    def setup_ui(self):
        """Setup the dialog UI with theme support"""
        colors = self.theme_manager.get_theme()
        is_dark = self.theme_manager.is_dark_mode()

        bg_color = colors.BG_CARD
        text_primary = colors.TEXT_PRIMARY
        text_secondary = colors.TEXT_SECONDARY
        border_color = colors.BORDER_LIGHT
        input_bg = colors.BG_PRIMARY if is_dark else "#F9FAFB"

        self.setWindowTitle("Add New Habit")
        self.setModal(True)
        self.setFixedSize(540, 520) # Made shorter since fields were removed
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
        icon = QLabel("✨")
        icon.setFont(QFont("SF Pro Display", 32))
        icon.setStyleSheet("background: transparent; border: none;") # Fixed emoji background
        title_layout.addWidget(icon)

        title = QLabel("Create New Habit")
        title.setFont(QFont("SF Pro Display", 26, QFont.Bold))
        title.setStyleSheet(f"color: {text_primary}; background: transparent; border: none;")
        title_layout.addWidget(title)
        title_layout.addStretch()
        layout.addLayout(title_layout)

        subtitle = QLabel("Build consistency one day at a time")
        subtitle.setFont(QFont("SF Pro Text", 14))
        subtitle.setStyleSheet(f"color: {text_secondary}; background: transparent;")
        layout.addWidget(subtitle)

        # Helper for common field styles
        input_style = f"""
            QLineEdit, QComboBox {{
                background-color: {input_bg};
                border: 2px solid {border_color};
                border-radius: 12px;
                padding: 10px 16px;
                color: {text_primary};
            }}
            QLineEdit:focus, QComboBox:hover {{
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

        # Habit name
        name_label = QLabel("Habit Name")
        name_label.setFont(QFont("SF Pro Text", 14, QFont.Bold))
        name_label.setStyleSheet(f"color: {text_primary}; background: transparent;")
        layout.addWidget(name_label)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., Morning Exercise, Read Books, Meditate")
        self.name_input.setFont(QFont("SF Pro Text", 14))
        self.name_input.setFixedHeight(52)
        self.name_input.setStyleSheet(input_style)
        layout.addWidget(self.name_input)

        # Category
        category_label = QLabel("Category")
        category_label.setFont(QFont("SF Pro Text", 14, QFont.Bold))
        category_label.setStyleSheet(f"color: {text_primary}; background: transparent;")
        layout.addWidget(category_label)

        self.category_combo = QComboBox()
        for category_name, emoji in CATEGORIES:
            self.category_combo.addItem(f"{emoji} {category_name}", category_name)
        self.category_combo.setFont(QFont("SF Pro Text", 14))
        self.category_combo.setFixedHeight(52)
        self.category_combo.setCursor(Qt.PointingHandCursor)
        self.category_combo.setStyleSheet(input_style)
        layout.addWidget(self.category_combo)

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

        save_btn = QPushButton("Create Habit")
        save_btn.setFont(QFont("SF Pro Text", 14, QFont.Bold))
        save_btn.setFixedHeight(52)
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.setStyleSheet(f"""
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
        save_btn.clicked.connect(self.save_habit)
        button_layout.addWidget(save_btn)

        layout.addLayout(button_layout)

    def save_habit(self):
        """Validate and save the habit"""
        name = self.name_input.text().strip()
        description = "" # Default empty description
        category = self.category_combo.currentData()
        frequency = "daily" # Default to daily frequency

        if not name:
            self.show_error("Validation Error", "Please enter a habit name")
            self.name_input.setFocus()
            return

        if len(name) > 100:
            self.show_error(
                "Validation Error", "Habit name is too long (max 100 characters)"
            )
            self.name_input.setFocus()
            return

        try:
            self.habit_service.create_habit(name, description, category, frequency)
            self.accept()
        except Exception as e:
            self.show_error("Error", f"Failed to create habit:\n{str(e)}")

    def show_error(self, title, message):
        """Show error message with theme support"""
        colors = self.theme_manager.get_theme()
        
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(title)
        msg.setText(message)
        
        is_dark = self.theme_manager.is_dark_mode()
        if is_dark:
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #1A1C23;
                    border-radius: 20px;
                }
                QLabel {
                    color: #F3F4F6;
                    background: transparent;
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
        else:
            msg.setStyleSheet(f"""
                QMessageBox {{
                    background-color: {colors.BG_CARD};
                }}
                QMessageBox QLabel {{
                    color: {colors.TEXT_PRIMARY};
                }}
                QPushButton {{
                    background-color: {colors.PURPLE_500};
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 20px;
                    font-weight: bold;
                    min-width: 80px;
                }}
            """)
        msg.exec()
