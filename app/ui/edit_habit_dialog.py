"""
Edit habit dialog - Dark Mode Design
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QTextEdit, QComboBox, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from app.services.habit_service import get_habit_service
from app.utils.constants import FREQUENCY_DAILY, FREQUENCY_WEEKLY


class EditHabitDialog(QDialog):
    """Dialog for editing an existing habit - Dark theme"""
    
    def __init__(self, habit, parent=None):
        super().__init__(parent)
        self.habit = habit
        self.habit_service = get_habit_service()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the dialog UI"""
        self.setWindowTitle("Edit Habit")
        self.setModal(True)
        self.setMinimumWidth(500)
        self.setStyleSheet("""
            QDialog {
                background-color: #1C1F26;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(32, 32, 32, 32)
        
        # Title
        title = QLabel("Edit Habit")
        title.setFont(QFont("Inter", 24, QFont.Bold))
        title.setStyleSheet("color: #E4E6EB; background: transparent;")
        layout.addWidget(title)
        
        subtitle = QLabel("Update your habit details")
        subtitle.setFont(QFont("Inter", 13))
        subtitle.setStyleSheet("color: #9AA0A6; background: transparent; margin-bottom: 8px;")
        layout.addWidget(subtitle)
        
        # Habit name
        name_label = QLabel("Habit Name")
        name_label.setFont(QFont("Inter", 13, QFont.Medium))
        name_label.setStyleSheet("color: #E4E6EB; background: transparent; margin-top: 8px;")
        layout.addWidget(name_label)
        
        self.name_input = QLineEdit()
        self.name_input.setText(self.habit.name)
        self.name_input.setFont(QFont("Inter", 14))
        self.name_input.setFixedHeight(48)
        self.name_input.setStyleSheet("""
            QLineEdit {
                padding: 12px 16px;
                border: 2px solid #2A2D35;
                border-radius: 10px;
                background-color: #20232B;
                color: #E4E6EB;
                selection-background-color: #4FD1C5;
            }
            QLineEdit:focus {
                border: 2px solid #4FD1C5;
                background-color: #1C1F26;
            }
        """)
        layout.addWidget(self.name_input)
        
        # Description
        desc_label = QLabel("Description (Optional)")
        desc_label.setFont(QFont("Inter", 13, QFont.Medium))
        desc_label.setStyleSheet("color: #E4E6EB; background: transparent; margin-top: 8px;")
        layout.addWidget(desc_label)
        
        self.desc_input = QTextEdit()
        self.desc_input.setText(self.habit.description or "")
        self.desc_input.setFont(QFont("Inter", 13))
        self.desc_input.setFixedHeight(90)
        self.desc_input.setStyleSheet("""
            QTextEdit {
                padding: 12px 16px;
                border: 2px solid #2A2D35;
                border-radius: 10px;
                background-color: #20232B;
                color: #E4E6EB;
                selection-background-color: #4FD1C5;
            }
            QTextEdit:focus {
                border: 2px solid #4FD1C5;
                background-color: #1C1F26;
            }
        """)
        layout.addWidget(self.desc_input)
        
        # Frequency
        freq_label = QLabel("Frequency")
        freq_label.setFont(QFont("Inter", 13, QFont.Medium))
        freq_label.setStyleSheet("color: #E4E6EB; background: transparent; margin-top: 8px;")
        layout.addWidget(freq_label)
        
        self.frequency_combo = QComboBox()
        self.frequency_combo.addItem("📅 Daily", FREQUENCY_DAILY)
        self.frequency_combo.addItem("📆 Weekly", FREQUENCY_WEEKLY)
        
        # Set current frequency
        if self.habit.frequency == FREQUENCY_WEEKLY:
            self.frequency_combo.setCurrentIndex(1)
        else:
            self.frequency_combo.setCurrentIndex(0)
        
        self.frequency_combo.setFont(QFont("Inter", 13))
        self.frequency_combo.setFixedHeight(48)
        self.frequency_combo.setCursor(Qt.PointingHandCursor)
        self.frequency_combo.setStyleSheet("""
            QComboBox {
                padding: 12px 16px;
                border: 2px solid #2A2D35;
                border-radius: 10px;
                background-color: #20232B;
                color: #E4E6EB;
            }
            QComboBox:hover {
                border: 2px solid #4FD1C5;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 12px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #9AA0A6;
                margin-right: 8px;
            }
            QComboBox QAbstractItemView {
                background-color: #20232B;
                border: 1px solid #2A2D35;
                border-radius: 8px;
                padding: 4px;
                color: #E4E6EB;
                selection-background-color: #4FD1C5;
                selection-color: #0F1115;
            }
        """)
        layout.addWidget(self.frequency_combo)
        
        layout.addSpacing(12)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFont(QFont("Inter", 13, QFont.Medium))
        cancel_btn.setFixedHeight(48)
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.setStyleSheet("""
            QPushButton {
                padding: 12px 32px;
                border: 2px solid #4A4D56;
                border-radius: 10px;
                color: #9AA0A6;
                background-color: transparent;
            }
            QPushButton:hover {
                border: 2px solid #7C83FD;
                color: #E4E6EB;
                background-color: rgba(124, 131, 253, 0.1);
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Save Changes")
        save_btn.setFont(QFont("Inter", 13, QFont.Bold))
        save_btn.setFixedHeight(48)
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.setStyleSheet("""
            QPushButton {
                padding: 12px 32px;
                border: none;
                border-radius: 10px;
                color: #FFFFFF;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4FD1C5, stop:1 #7C83FD);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #45B8AD, stop:1 #6B6FE5);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3A9D93, stop:1 #5A5ECD);
            }
        """)
        save_btn.clicked.connect(self.save_habit)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
    
    def save_habit(self):
        """Validate and save the habit changes"""
        name = self.name_input.text().strip()
        description = self.desc_input.toPlainText().strip()
        frequency = self.frequency_combo.currentData()
        
        if not name:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Validation Error")
            msg.setText("Please enter a habit name")
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #1C1F26;
                }
                QMessageBox QLabel {
                    color: #E4E6EB;
                }
                QPushButton {
                    background-color: #4FD1C5;
                    color: #0F1115;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 20px;
                    font-weight: bold;
                    min-width: 80px;
                }
            """)
            msg.exec()
            self.name_input.setFocus()
            return
        
        if len(name) > 100:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Validation Error")
            msg.setText("Habit name is too long (max 100 characters)")
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #1C1F26;
                }
                QMessageBox QLabel {
                    color: #E4E6EB;
                }
                QPushButton {
                    background-color: #4FD1C5;
                    color: #0F1115;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 20px;
                    font-weight: bold;
                    min-width: 80px;
                }
            """)
            msg.exec()
            self.name_input.setFocus()
            return
        
        try:
            self.habit_service.update_habit(
                self.habit.id,
                name=name,
                description=description,
                frequency=frequency
            )
            self.accept()
        except Exception as e:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to update habit:\n{str(e)}")
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #1C1F26;
                }
                QMessageBox QLabel {
                    color: #E4E6EB;
                }
                QPushButton {
                    background-color: #EF5350;
                    color: #FFFFFF;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 20px;
                    font-weight: bold;
                    min-width: 80px;
                }
            """)
            msg.exec()
