"""
Notes dialog - Add notes when completing a habit
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QTextEdit, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from app.services.habit_service import get_habit_service


class NotesDialog(QDialog):
    """Dialog for adding notes to habit completion"""
    
    def __init__(self, habit, parent=None):
        super().__init__(parent)
        self.habit = habit
        self.habit_service = get_habit_service()
        self.notes = ""
        self.setup_ui()
        self.load_existing_notes()
    
    def setup_ui(self):
        """Setup the dialog UI"""
        self.setWindowTitle("Add Notes")
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
        title = QLabel(f"📝 Notes for {self.habit.name}")
        title.setFont(QFont("Inter", 20, QFont.Bold))
        title.setStyleSheet("color: #E4E6EB; background: transparent;")
        layout.addWidget(title)
        
        subtitle = QLabel("Add a note about completing this habit today")
        subtitle.setFont(QFont("Inter", 13))
        subtitle.setStyleSheet("color: #9AA0A6; background: transparent; margin-bottom: 8px;")
        layout.addWidget(subtitle)
        
        # Notes input
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("How did it go? Any reflections or observations...")
        self.notes_input.setFont(QFont("Inter", 13))
        self.notes_input.setMinimumHeight(150)
        self.notes_input.setStyleSheet("""
            QTextEdit {
                padding: 16px;
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
        layout.addWidget(self.notes_input)
        
        # Character count
        self.char_count = QLabel("0 characters")
        self.char_count.setFont(QFont("Inter", 11))
        self.char_count.setStyleSheet("color: #6B6E76; background: transparent;")
        self.char_count.setAlignment(Qt.AlignRight)
        self.notes_input.textChanged.connect(self.update_char_count)
        layout.addWidget(self.char_count)
        
        layout.addSpacing(8)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        skip_btn = QPushButton("Skip")
        skip_btn.setFont(QFont("Inter", 13, QFont.Medium))
        skip_btn.setFixedHeight(48)
        skip_btn.setCursor(Qt.PointingHandCursor)
        skip_btn.setStyleSheet("""
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
        skip_btn.clicked.connect(self.skip_notes)
        button_layout.addWidget(skip_btn)
        
        save_btn = QPushButton("Save & Complete")
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
        save_btn.clicked.connect(self.save_notes)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
    
    def load_existing_notes(self):
        """Load existing notes if any"""
        existing_notes = self.habit_service.get_completion_notes(self.habit.id)
        if existing_notes:
            self.notes_input.setPlainText(existing_notes)
    
    def update_char_count(self):
        """Update character count label"""
        count = len(self.notes_input.toPlainText())
        self.char_count.setText(f"{count} characters")
    
    def skip_notes(self):
        """Skip adding notes"""
        self.notes = ""
        self.accept()
    
    def save_notes(self):
        """Save notes and close"""
        self.notes = self.notes_input.toPlainText().strip()
        self.accept()
    
    def get_notes(self):
        """Get the notes text"""
        return self.notes
