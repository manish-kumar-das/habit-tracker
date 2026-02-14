"""
Trash dialog for managing deleted habits
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QScrollArea, QFrame, QWidget, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QCursor
from app.services.habit_service import get_habit_service


class DeletedHabitItem(QFrame):
    """Single deleted habit item"""
    
    def __init__(self, deleted_habit, parent=None):
        super().__init__(parent)
        self.deleted_habit = deleted_habit
        self.parent_dialog = parent
        self.habit_service = get_habit_service()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup deleted habit item UI"""
        self.setFrameShape(QFrame.NoFrame)
        self.setStyleSheet("""
            DeletedHabitItem {
                background-color: #1C1F26;
                border: 1px solid #2A2D35;
                border-radius: 12px;
            }
            DeletedHabitItem:hover {
                background-color: #20232B;
                border: 1px solid #EF4444;
            }
        """)
        self.setMinimumHeight(80)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(16)
        
        # Info section
        info_layout = QVBoxLayout()
        info_layout.setSpacing(6)
        
        # Name with category
        try:
            category = self.deleted_habit['category']
        except (KeyError, TypeError):
            category = None
        
        if category:
            from app.utils.constants import CATEGORIES
            category_emoji = "📌"
            for cat_name, emoji in CATEGORIES:
                if cat_name == category:
                    category_emoji = emoji
                    break
            
            category_badge = QLabel(f"{category_emoji} {category}")
            category_badge.setFont(QFont("Inter", 10, QFont.Medium))
            category_badge.setStyleSheet("""
                QLabel {
                    color: #EF4444;
                    background-color: rgba(239, 68, 68, 0.1);
                    padding: 4px 10px;
                    border-radius: 10px;
                }
            """)
            info_layout.addWidget(category_badge)
        
        # Habit name
        name_label = QLabel(self.deleted_habit['name'])
        name_label.setFont(QFont("Inter", 15, QFont.Medium))
        name_label.setStyleSheet("color: #E4E6EB; background: transparent;")
        info_layout.addWidget(name_label)
        
        # Metadata
        meta_layout = QHBoxLayout()
        meta_layout.setSpacing(12)
        
        # Deleted date
        deleted_label = QLabel(f"🗑️ Deleted: {self.deleted_habit['deleted_at'][:10]}")
        deleted_label.setFont(QFont("Inter", 11))
        deleted_label.setStyleSheet("color: #9AA0A6; background: transparent;")
        meta_layout.addWidget(deleted_label)
        
        # Completion count
        try:
            count = self.deleted_habit['completion_count']
        except (KeyError, TypeError):
            count = 0
        
        count_label = QLabel(f"✅ {count} completions")
        count_label.setFont(QFont("Inter", 11))
        count_label.setStyleSheet("color: #9AA0A6; background: transparent;")
        meta_layout.addWidget(count_label)
        
        meta_layout.addStretch()
        info_layout.addLayout(meta_layout)
        
        layout.addLayout(info_layout, stretch=1)
        
        # Restore button
        restore_btn = QPushButton("↩️ Restore")
        restore_btn.setFont(QFont("Inter", 12, QFont.Medium))
        restore_btn.setFixedSize(100, 40)
        restore_btn.setCursor(Qt.PointingHandCursor)
        restore_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #4FD1C5;
                border-radius: 10px;
                color: #4FD1C5;
            }
            QPushButton:hover {
                background-color: rgba(79, 209, 197, 0.2);
            }
        """)
        restore_btn.clicked.connect(self.restore_habit)
        layout.addWidget(restore_btn)
        
        # Delete permanently button
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
        delete_btn.clicked.connect(self.delete_permanently)
        layout.addWidget(delete_btn)
    
    def restore_habit(self):
        """Restore this habit"""
        self.habit_service.restore_habit(self.deleted_habit['id'])
        if self.parent_dialog:
            self.parent_dialog.load_deleted_habits()
    
    def delete_permanently(self):
        """Delete permanently"""
        msg = QMessageBox(self)
        msg.setWindowTitle("Delete Permanently")
        msg.setText(f"Permanently delete '{self.deleted_habit['name']}'?")
        msg.setInformativeText("This action cannot be undone!")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        msg.setStyleSheet("""
            QMessageBox { background-color: #1C1F26; }
            QMessageBox QLabel { color: #E4E6EB; }
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
            conn = self.habit_service.habit_service.get_db_connection() if hasattr(self.habit_service, 'habit_service') else get_habit_service()
            from app.db.database import get_db_connection
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM deleted_habits WHERE id = ?', (self.deleted_habit['id'],))
            conn.commit()
            conn.close()
            
            if self.parent_dialog:
                self.parent_dialog.load_deleted_habits()


class TrashDialog(QDialog):
    """Dialog for managing deleted habits (trash)"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.habit_service = get_habit_service()
        self.setup_ui()
        self.load_deleted_habits()
    
    def setup_ui(self):
        """Setup dialog UI"""
        self.setWindowTitle("Trash")
        self.setModal(True)
        self.setMinimumSize(800, 600)
        self.setStyleSheet("QDialog { background-color: #0F1115; }")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(24)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("🗑️ Trash")
        title.setFont(QFont("Inter", 28, QFont.Bold))
        title.setStyleSheet("color: #E4E6EB; background: transparent;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Empty trash button
        empty_btn = QPushButton("Empty Trash")
        empty_btn.setFont(QFont("Inter", 12, QFont.Bold))
        empty_btn.setFixedHeight(44)
        empty_btn.setCursor(Qt.PointingHandCursor)
        empty_btn.setStyleSheet("""
            QPushButton {
                padding: 10px 24px;
                border: none;
                border-radius: 10px;
                color: #FFFFFF;
                background-color: #EF4444;
            }
            QPushButton:hover {
                background-color: #DC2626;
            }
        """)
        empty_btn.clicked.connect(self.empty_trash)
        header_layout.addWidget(empty_btn)
        
        # Close button
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(44, 44)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setFont(QFont("Inter", 16))
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #4A4D56;
                border-radius: 22px;
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
        
        # Subtitle
        subtitle = QLabel("Deleted habits can be restored or permanently deleted")
        subtitle.setFont(QFont("Inter", 13))
        subtitle.setStyleSheet("color: #9AA0A6; background: transparent;")
        layout.addWidget(subtitle)
        
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
        
        self.items_container = QWidget()
        self.items_container.setStyleSheet("background-color: transparent;")
        self.items_layout = QVBoxLayout(self.items_container)
        self.items_layout.setSpacing(12)
        self.items_layout.setContentsMargins(0, 0, 0, 0)
        self.items_layout.addStretch()
        
        scroll.setWidget(self.items_container)
        layout.addWidget(scroll)
    
    def load_deleted_habits(self):
        """Load deleted habits from trash"""
        # Clear existing
        while self.items_layout.count() > 1:
            item = self.items_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Get deleted habits
        deleted_habits = self.habit_service.get_deleted_habits(limit=50)
        
        if not deleted_habits:
            # Empty state
            empty_widget = QWidget()
            empty_layout = QVBoxLayout(empty_widget)
            empty_layout.setAlignment(Qt.AlignCenter)
            
            emoji_label = QLabel("🗑️")
            emoji_label.setFont(QFont("Inter", 64))
            emoji_label.setAlignment(Qt.AlignCenter)
            emoji_label.setStyleSheet("color: #4A4D56; background: transparent;")
            empty_layout.addWidget(emoji_label)
            
            text_label = QLabel("Trash is empty")
            text_label.setFont(QFont("Inter", 20, QFont.Medium))
            text_label.setAlignment(Qt.AlignCenter)
            text_label.setStyleSheet("color: #9AA0A6; background: transparent; margin-top: 16px;")
            empty_layout.addWidget(text_label)
            
            self.items_layout.insertWidget(0, empty_widget)
        else:
            # Add deleted habit items
            for deleted_habit in deleted_habits:
                item = DeletedHabitItem(deleted_habit, self)
                self.items_layout.insertWidget(self.items_layout.count() - 1, item)
    
    def empty_trash(self):
        """Empty all trash"""
        msg = QMessageBox(self)
        msg.setWindowTitle("Empty Trash")
        msg.setText("Permanently delete all habits in trash?")
        msg.setInformativeText("This action cannot be undone!")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        msg.setStyleSheet("""
            QMessageBox { background-color: #1C1F26; }
            QMessageBox QLabel { color: #E4E6EB; }
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
            self.habit_service.empty_trash()
            self.load_deleted_habits()
