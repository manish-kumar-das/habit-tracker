"""
Edit habit dialog with category support
"""

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QPushButton,
    QMessageBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from app.services.habit_service import get_habit_service
from app.utils.constants import FREQUENCY_DAILY, FREQUENCY_WEEKLY, CATEGORIES
from app.themes import get_theme_manager


class EditHabitDialog(QDialog):
    """Dialog for editing an existing habit"""

    def __init__(self, habit, parent=None):
        super().__init__(parent)
        self.habit = habit
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

        self.setWindowTitle("Edit Habit")
        self.setModal(True)
        self.setFixedSize(540, 720)
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
        icon = QLabel("✏️")
        icon.setFont(QFont("SF Pro Display", 32))
        icon.setStyleSheet("background: transparent; border: none;") # Fixed emoji background
        title_layout.addWidget(icon)

        title = QLabel("Edit Habit")
        title.setFont(QFont("SF Pro Display", 26, QFont.Bold))
        title.setStyleSheet(f"color: {text_primary}; background: transparent; border: none;")
        title_layout.addWidget(title)
        title_layout.addStretch()
        layout.addLayout(title_layout)

        subtitle = QLabel("Update your habit details")
        subtitle.setFont(QFont("SF Pro Text", 14))
        subtitle.setStyleSheet(f"color: {text_secondary}; background: transparent;")
        layout.addWidget(subtitle)

        # Helper for common field styles
        input_style = f"""
            QLineEdit, QTextEdit, QComboBox {{
                background-color: {input_bg};
                border: 2px solid {border_color};
                border-radius: 12px;
                padding: 10px 16px;
                color: {text_primary};
            }}
            QLineEdit:focus, QTextEdit:focus, QComboBox:hover {{
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
        self.name_input.setText(self.habit.name)
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
        current_index = 0
        for i, (category_name, emoji) in enumerate(CATEGORIES):
            self.category_combo.addItem(f"{emoji} {category_name}", category_name)
            if category_name == self.habit.category:
                current_index = i
        self.category_combo.setCurrentIndex(current_index)
        self.category_combo.setFont(QFont("SF Pro Text", 14))
        self.category_combo.setFixedHeight(52)
        self.category_combo.setCursor(Qt.PointingHandCursor)
        self.category_combo.setStyleSheet(input_style)
        layout.addWidget(self.category_combo)

        # Description - Label removed as requested
        self.desc_input = QTextEdit()
        self.desc_input.setText(self.habit.description or "")
        self.desc_input.setFont(QFont("SF Pro Text", 13))
        self.desc_input.setFixedHeight(100)
        self.desc_input.setStyleSheet(input_style)
        layout.addWidget(self.desc_input)

        # Frequency - Label removed as requested
        self.frequency_combo = QComboBox()
        self.frequency_combo.addItem("📅 Daily", FREQUENCY_DAILY)
        self.frequency_combo.addItem("📆 Weekly", FREQUENCY_WEEKLY)

        if self.habit.frequency == FREQUENCY_WEEKLY:
            self.frequency_combo.setCurrentIndex(1)
        else:
            self.frequency_combo.setCurrentIndex(0)

        self.frequency_combo.setFont(QFont("SF Pro Text", 14))
        self.frequency_combo.setFixedHeight(52)
        self.frequency_combo.setCursor(Qt.PointingHandCursor)
        self.frequency_combo.setStyleSheet(input_style)
        layout.addWidget(self.frequency_combo)

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

        save_btn = QPushButton("Save Changes")
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
        """Validate and save the habit changes"""
        name = self.name_input.text().strip()
        description = self.desc_input.toPlainText().strip()
        category = self.category_combo.currentData()
        frequency = self.frequency_combo.currentData()

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
            self.habit_service.update_habit(
                self.habit.id,
                name=name,
                description=description,
                category=category,
                frequency=frequency,
            )
            self.accept()
        except Exception as e:
            self.show_error("Error", f"Failed to update habit:\n{str(e)}")

    def show_error(self, title, message):
        """Show error message with theme support"""
        colors = self.theme_manager.get_theme()
        
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(title)
        msg.setText(message)
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
