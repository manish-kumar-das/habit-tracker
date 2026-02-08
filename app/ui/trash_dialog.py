"""
Trash dialog - View and restore deleted habits
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QScrollArea, QFrame, QMessageBox, QWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from app.services.habit_service import get_habit_service


class DeletedHabitItem(QFrame):
    """Single deleted habit item"""
    
    def __init__(self, deleted_habit, parent_dialog, parent=None):
        super().__init__(parent)
        self.deleted_habit = deleted_habit
        self.parent_dialog = parent_dialog
        self.habit_service = get_habit_service()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the item UI"""
        self.setFrameShape(QFrame.NoFrame)
        self.setStyleSheet("""
            DeletedHabitItem {
                background-color: #1C1F26;
                border: 1px solid #2A2D35;
                border-radius: 12px;
            }
            DeletedHabitItem:hover {
                background-color: #20232B;
                border: 1px solid #F2C94C;
            }
        """)
        self.setMinimumHeight(80)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(16)
        
        # Icon
        icon_label = QLabel("🗑️")
        icon_label.setFont(QFont("Inter", 24))
        icon_label.setStyleSheet("background: transparent;")
        layout.addWidget(icon_label)
        
        # Habit info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        
        # Name
        name_label = QLabel(self.deleted_habit['name'])
        name_label.setFont(QFont("Inter", 15, QFont.Medium))
        name_label.setStyleSheet("color: #E4E6EB; background: transparent;")
        info_layout.addWidget(name_label)
        
        # Details
        details_parts = []
        if self.deleted_habit.get('category'):
            details_parts.append(f"Category: {self.deleted_habit['category']}")
        details_parts.append(f"Deleted: {self.deleted_habit['deleted_at']}")
        details_parts.append(f"{self.deleted_habit['completion_count']} completions")
        
        details_label = QLabel(" • ".join(details_parts))
        details_label.setFont(QFont("Inter", 11))
        details_label.setStyleSheet("color: #9AA0A6; background: transparent;")
        info_layout.addWidget(details_label)
        
        layout.addLayout(info_layout, stretch=1)
        
        # Restore button
        restore_btn = QPushButton("↩️ Restore")
        restore_btn.setFont(QFont("Inter", 13, QFont.Medium))
        restore_btn.setFixedHeight(40)
        restore_btn.setCursor(Qt.PointingHandCursor)
        restore_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 20px;
                border: none;
                border-radius: 8px;
                color: #FFFFFF;
                background-color: #6FCF97;
            }
            QPushButton:hover {
                background-color: #5AB67D;
            }
            QPushButton:pressed {
                background-color: #4A9D6A;
            }
        """)
        restore_btn.clicked.connect(self.restore_habit)
        layout.addWidget(restore_btn)
        
        # Permanent delete button
        delete_btn = QPushButton("✕")
        delete_btn.setFixedSize(40, 40)
        delete_btn.setCursor(Qt.PointingHandCursor)
        delete_btn.setFont(QFont("Inter", 14))
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #4A4D56;
                border-radius: 20px;
                color: #9AA0A6;
            }
            QPushButton:hover {
                background-color: rgba(239, 83, 80, 0.2);
                border: 1px solid #EF5350;
                color: #EF5350;
            }
        """)
        delete_btn.clicked.connect(self.permanent_delete)
        layout.addWidget(delete_btn)
    
    def restore_habit(self):
        """Restore this deleted habit"""
        msg = QMessageBox(self)
        msg.setWindowTitle("Restore Habit")
        msg.setText(f"Restore '{self.deleted_habit['name']}'?")
        msg.setInformativeText("The habit will be restored to your active habits list.")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.Yes)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #1C1F26;
            }
            QMessageBox QLabel {
                color: #E4E6EB;
            }
            QPushButton {
                background-color: #20232B;
                color: #E4E6EB;
                border: 1px solid #4A4D56;
                border-radius: 6px;
                padding: 8px 16px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #2A2D35;
                border: 1px solid #6FCF97;
            }
        """)
        
        if msg.exec() == QMessageBox.Yes:
            restored = self.habit_service.restore_habit(self.deleted_habit['id'])
            if restored:
                self.parent_dialog.load_deleted_habits()
                
                # Show success message
                success_msg = QMessageBox(self)
                success_msg.setIcon(QMessageBox.Information)
                success_msg.setWindowTitle("Habit Restored")
                success_msg.setText(f"✓ '{self.deleted_habit['name']}' has been restored!")
                success_msg.setStyleSheet("""
                    QMessageBox {
                        background-color: #1C1F26;
                    }
                    QMessageBox QLabel {
                        color: #E4E6EB;
                    }
                    QPushButton {
                        background-color: #6FCF97;
                        color: #0F1115;
                        border: none;
                        border-radius: 6px;
                        padding: 8px 20px;
                        font-weight: bold;
                        min-width: 80px;
                    }
                """)
                success_msg.exec()
    
    def permanent_delete(self):
        """Permanently delete this habit from trash"""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Permanent Delete")
        msg.setText(f"Permanently delete '{self.deleted_habit['name']}'?")
        msg.setInformativeText("This action cannot be undone. The habit will be removed from trash forever.")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #1C1F26;
            }
            QMessageBox QLabel {
                color: #E4E6EB;
            }
            QPushButton {
                background-color: #20232B;
                color: #E4E6EB;
                border: 1px solid #4A4D56;
                border-radius: 6px;
                padding: 8px 16px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #2A2D35;
                border: 1px solid #EF5350;
            }
        """)
        
        if msg.exec() == QMessageBox.Yes:
            # Remove from deleted_habits table
            query = "DELETE FROM deleted_habits WHERE id = ?"
            self.habit_service.db.execute(query, (self.deleted_habit['id'],))
            self.parent_dialog.load_deleted_habits()


class TrashDialog(QDialog):
    """Trash dialog - view and restore deleted habits"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.habit_service = get_habit_service()
        self.setup_ui()
        self.load_deleted_habits()
    
    def setup_ui(self):
        """Setup the dialog UI"""
        self.setWindowTitle("Trash")
        self.setModal(False)
        self.setMinimumSize(700, 500)
        self.setStyleSheet("""
            QDialog {
                background-color: #0F1115;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(24)
        
        # Header
        header_layout = QHBoxLayout()
        
        header_left = QVBoxLayout()
        header_left.setSpacing(4)
        
        title = QLabel("🗑️ Trash")
        title.setFont(QFont("Inter", 28, QFont.Bold))
        title.setStyleSheet("color: #E4E6EB; background: transparent;")
        header_left.addWidget(title)
        
        subtitle = QLabel("Recently deleted habits")
        subtitle.setFont(QFont("Inter", 14))
        subtitle.setStyleSheet("color: #9AA0A6; background: transparent;")
        header_left.addWidget(subtitle)
        
        header_layout.addLayout(header_left)
        header_layout.addStretch()
        
        # Empty trash button
        self.empty_btn = QPushButton("🗑️ Empty Trash")
        self.empty_btn.setFont(QFont("Inter", 13, QFont.Medium))
        self.empty_btn.setFixedHeight(44)
        self.empty_btn.setCursor(Qt.PointingHandCursor)
        self.empty_btn.setStyleSheet("""
            QPushButton {
                padding: 10px 20px;
                border: 2px solid #4A4D56;
                border-radius: 10px;
                color: #EF5350;
                background-color: transparent;
            }
            QPushButton:hover {
                border: 2px solid #EF5350;
                background-color: rgba(239, 83, 80, 0.1);
            }
            QPushButton:disabled {
                color: #4A4D56;
                border: 2px solid #2A2D35;
            }
        """)
        self.empty_btn.clicked.connect(self.empty_trash)
        header_layout.addWidget(self.empty_btn)
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(36, 36)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setFont(QFont("Inter", 16))
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #4A4D56;
                border-radius: 18px;
                color: #9AA0A6;
            }
            QPushButton:hover {
                background-color: rgba(239, 83, 80, 0.2);
                border: 1px solid #EF5350;
                color: #EF5350;
            }
        """)
        close_btn.clicked.connect(self.close)
        header_layout.addWidget(close_btn)
        
        layout.addLayout(header_layout)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #0F1115;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #4A4D56;
                min-height: 30px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: #4FD1C5;
            }
        """)
        
        # Content widget
        content = QWidget()
        content.setStyleSheet("background-color: transparent;")
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setSpacing(12)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.addStretch()
        
        scroll.setWidget(content)
        layout.addWidget(scroll)
    
    def load_deleted_habits(self):
        """Load and display deleted habits"""
        # Clear existing items
        while self.content_layout.count() > 1:
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Get deleted habits
        deleted_habits = self.habit_service.get_deleted_habits()
        
        if not deleted_habits:
            # Empty state
            empty_widget = QWidget()
            empty_layout = QVBoxLayout(empty_widget)
            empty_layout.setAlignment(Qt.AlignCenter)
            
            emoji_label = QLabel("✨")
            emoji_label.setFont(QFont("Inter", 48))
            emoji_label.setAlignment(Qt.AlignCenter)
            emoji_label.setStyleSheet("color: #4A4D56; background: transparent;")
            empty_layout.addWidget(emoji_label)
            
            text_label = QLabel("Trash is empty")
            text_label.setFont(QFont("Inter", 18, QFont.Medium))
            text_label.setAlignment(Qt.AlignCenter)
            text_label.setStyleSheet("color: #9AA0A6; background: transparent; margin-top: 16px;")
            empty_layout.addWidget(text_label)
            
            subtext = QLabel("Deleted habits will appear here")
            subtext.setFont(QFont("Inter", 13))
            subtext.setAlignment(Qt.AlignCenter)
            subtext.setStyleSheet("color: #6B6E76; background: transparent; margin-top: 8px;")
            empty_layout.addWidget(subtext)
            
            self.content_layout.insertWidget(0, empty_widget)
            self.empty_btn.setEnabled(False)
        else:
            # Add deleted habit items
            for deleted_habit in deleted_habits:
                item = DeletedHabitItem(deleted_habit, self)
                self.content_layout.insertWidget(self.content_layout.count() - 1, item)
            
            self.empty_btn.setEnabled(True)
    
    def empty_trash(self):
        """Permanently delete all items in trash"""
        deleted_count = len(self.habit_service.get_deleted_habits())
        
        if deleted_count == 0:
            return
        
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Empty Trash")
        msg.setText(f"Permanently delete {deleted_count} habit(s)?")
        msg.setInformativeText("This action cannot be undone. All habits in trash will be removed forever.")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #1C1F26;
            }
            QMessageBox QLabel {
                color: #E4E6EB;
            }
            QPushButton {
                background-color: #20232B;
                color: #E4E6EB;
                border: 1px solid #4A4D56;
                border-radius: 6px;
                padding: 8px 16px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #2A2D35;
                border: 1px solid #EF5350;
            }
        """)
        
        if msg.exec() == QMessageBox.Yes:
            # Delete all from trash
            query = "DELETE FROM deleted_habits"
            self.habit_service.db.execute(query)
            self.load_deleted_habits()
            
            # Show success message
            success_msg = QMessageBox(self)
            success_msg.setIcon(QMessageBox.Information)
            success_msg.setWindowTitle("Trash Emptied")
            success_msg.setText(f"✓ {deleted_count} habit(s) permanently deleted")
            success_msg.setStyleSheet("""
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
            success_msg.exec()
