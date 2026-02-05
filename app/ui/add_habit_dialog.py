"""
Add habit dialog
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QTextEdit, QComboBox, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt
from app.services.habit_service import get_habit_service
from app.utils.constants import FREQUENCY_DAILY, FREQUENCY_WEEKLY


class AddHabitDialog(QDialog):
    """Dialog for adding a new habit"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.habit_service = get_habit_service()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the dialog UI"""
        self.setWindowTitle("Add New Habit")
        self.setModal(True)
        self.setMinimumWidth(450)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Create a New Habit")
        title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                padding-bottom: 10px;
            }
        """)
        layout.addWidget(title)
        
        # Habit name
        name_label = QLabel("Habit Name *")
        name_label.setStyleSheet("font-weight: bold; color: #34495e;")
        layout.addWidget(name_label)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., Morning Exercise, Read Books, Drink Water")
        self.name_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        layout.addWidget(self.name_input)
        
        # Description
        desc_label = QLabel("Description (Optional)")
        desc_label.setStyleSheet("font-weight: bold; color: #34495e; margin-top: 10px;")
        layout.addWidget(desc_label)
        
        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Add details about your habit...")
        self.desc_input.setMaximumHeight(80)
        self.desc_input.setStyleSheet("""
            QTextEdit {
                padding: 10px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                font-size: 14px;
            }
            QTextEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        layout.addWidget(self.desc_input)
        
        # Frequency
        freq_label = QLabel("Frequency *")
        freq_label.setStyleSheet("font-weight: bold; color: #34495e; margin-top: 10px;")
        layout.addWidget(freq_label)
        
        self.frequency_combo = QComboBox()
        self.frequency_combo.addItem("Daily", FREQUENCY_DAILY)
        self.frequency_combo.addItem("Weekly", FREQUENCY_WEEKLY)
        self.frequency_combo.setStyleSheet("""
            QComboBox {
                padding: 10px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                font-size: 14px;
                background-color: white;
            }
            QComboBox:focus {
                border: 2px solid #3498db;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
        """)
        layout.addWidget(self.frequency_combo)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                padding: 10px 24px;
                border: 2px solid #95a5a6;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                color: #95a5a6;
                background-color: white;
            }
            QPushButton:hover {
                border: 2px solid #7f8c8d;
                color: #7f8c8d;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Create Habit")
        save_btn.setStyleSheet("""
            QPushButton {
                padding: 10px 24px;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                color: white;
                background-color: #27ae60;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """)
        save_btn.clicked.connect(self.save_habit)
        button_layout.addWidget(save_btn)
        
        layout.addSpacing(10)
        layout.addLayout(button_layout)
    
    def save_habit(self):
        """Validate and save the habit"""
        name = self.name_input.text().strip()
        description = self.desc_input.toPlainText().strip()
        frequency = self.frequency_combo.currentData()
        
        # Validation
        if not name:
            QMessageBox.warning(
                self,
                "Validation Error",
                "Please enter a habit name."
            )
            self.name_input.setFocus()
            return
        
        if len(name) > 100:
            QMessageBox.warning(
                self,
                "Validation Error",
                "Habit name is too long (max 100 characters)."
            )
            self.name_input.setFocus()
            return
        
        # Create habit
        try:
            self.habit_service.create_habit(name, description, frequency)
            self.accept()  # Close dialog with success
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to create habit:\n{str(e)}"
            )
