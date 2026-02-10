"""
Today's habits view - FIXED VERSION
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, 
    QLabel, QPushButton, QScrollArea, QFrame, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QCursor
from app.services.habit_service import get_habit_service
from app.services.streak_service import get_streak_service


class HabitItem(QFrame):
    """Single habit item widget"""
    
    def __init__(self, habit, parent=None):
        super().__init__(parent)
        self.habit = habit
        self.parent_view = parent
        self.habit_service = get_habit_service()
        self.streak_service = get_streak_service()
        self.is_processing = False  # Prevent multiple triggers
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the habit item UI"""
        self.setFrameShape(QFrame.NoFrame)
        self.setStyleSheet("""
            HabitItem {
                background-color: #1C1F26;
                border: 1px solid #2A2D35;
                border-radius: 12px;
            }
            HabitItem:hover {
                background-color: #20232B;
                border: 1px solid #4FD1C5;
            }
        """)
        self.setMinimumHeight(80)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(16)
        
        # Checkbox
        self.checkbox = QCheckBox()
        self.checkbox.setFixedSize(28, 28)
        self.checkbox.setCursor(QCursor(Qt.PointingHandCursor))
        self.checkbox.setStyleSheet("""
            QCheckBox {
                spacing: 0px;
            }
            QCheckBox::indicator {
                width: 28px;
                height: 28px;
                border-radius: 6px;
                border: 2px solid #4A4D56;
                background-color: #20232B;
            }
            QCheckBox::indicator:hover {
                border: 2px solid #4FD1C5;
                background-color: #2A2D35;
            }
            QCheckBox::indicator:checked {
                background-color: #6FCF97;
                border: 2px solid #6FCF97;
            }
            QCheckBox::indicator:checked:hover {
                background-color: #5AB67D;
                border: 2px solid #5AB67D;
            }
        """)
        
        # Check if completed today
        is_completed = self.habit_service.is_habit_completed_today(self.habit.id)
        self.checkbox.setChecked(is_completed)
        
        # Connect checkbox - use clicked instead of stateChanged
        self.checkbox.clicked.connect(self.on_checkbox_clicked)
        
        layout.addWidget(self.checkbox)
        
        # Habit info container
        info_layout = QVBoxLayout()
        info_layout.setSpacing(6)
        
        # Category badge
        from app.utils.constants import CATEGORIES, CATEGORY_COLORS
        category_emoji = "📌"
        for cat_name, emoji in CATEGORIES:
            if cat_name == self.habit.category:
                category_emoji = emoji
                break
        
        category_color = CATEGORY_COLORS.get(self.habit.category, "#9AA0A6")
        
        category_badge = QLabel(f"{category_emoji} {self.habit.category}")
        category_badge.setFont(QFont("Inter", 10, QFont.Medium))
        category_badge.setStyleSheet(f"""
            QLabel {{
                color: {category_color};
                background-color: rgba(79, 209, 197, 0.1);
                padding: 4px 10px;
                border-radius: 10px;
            }}
        """)
        info_layout.addWidget(category_badge)
        
        # Habit name
        name_label = QLabel(self.habit.name)
        name_label.setFont(QFont("Inter", 15, QFont.Medium))
        name_label.setStyleSheet("color: #E4E6EB; background: transparent;")
        info_layout.addWidget(name_label)
        
        # Description
        if self.habit.description:
            desc_label = QLabel(self.habit.description)
            desc_label.setFont(QFont("Inter", 12))
            desc_label.setStyleSheet("color: #9AA0A6; background: transparent;")
            desc_label.setWordWrap(True)
            info_layout.addWidget(desc_label)
        
        # Notes indicator
        notes = self.habit_service.get_completion_notes(self.habit.id)
        if notes and is_completed:
            notes_preview = notes[:50] + "..." if len(notes) > 50 else notes
            notes_label = QLabel(f"💭 {notes_preview}")
            notes_label.setFont(QFont("Inter", 11))
            notes_label.setStyleSheet("""
                QLabel {
                    color: #7C83FD;
                    background-color: rgba(124, 131, 253, 0.1);
                    padding: 6px 10px;
                    border-radius: 6px;
                }
            """)
            notes_label.setWordWrap(True)
            info_layout.addWidget(notes_label)
        
        layout.addLayout(info_layout, stretch=1)
        
        # Notes button (if completed)
        if is_completed:
            notes_btn = QPushButton("📝")
            notes_btn.setFixedSize(36, 36)
            notes_btn.setCursor(QCursor(Qt.PointingHandCursor))
            notes_btn.setFont(QFont("Inter", 14))
            notes_btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: 1px solid #4A4D56;
                    border-radius: 18px;
                    color: #9AA0A6;
                }
                QPushButton:hover {
                    background-color: rgba(124, 131, 253, 0.2);
                    border: 1px solid #7C83FD;
                    color: #7C83FD;
                }
            """)
            notes_btn.clicked.connect(self.view_notes)
            layout.addWidget(notes_btn)
        
        # Streak info
        streak_info = self.streak_service.get_streak_info(self.habit.id)
        current_streak = streak_info['current_streak']
        
        if current_streak > 0:
            streak_label = QLabel(f"�� {current_streak}")
            streak_label.setFont(QFont("Inter", 14, QFont.Bold))
            streak_label.setStyleSheet("""
                QLabel {
                    color: #FFB74D;
                    background-color: rgba(255, 183, 77, 0.15);
                    padding: 8px 16px;
                    border-radius: 20px;
                }
            """)
            streak_label.setAlignment(Qt.AlignCenter)
            streak_label.setFixedHeight(40)
        else:
            streak_label = QLabel("Start")
            streak_label.setFont(QFont("Inter", 12))
            streak_label.setStyleSheet("""
                QLabel {
                    color: #9AA0A6;
                    background-color: transparent;
                    padding: 8px 16px;
                    border-radius: 20px;
                    border: 1px solid #4A4D56;
                }
            """)
            streak_label.setAlignment(Qt.AlignCenter)
            streak_label.setFixedHeight(40)
        
        layout.addWidget(streak_label)
        
        # Edit button
        edit_btn = QPushButton("✏")
        edit_btn.setFixedSize(36, 36)
        edit_btn.setCursor(QCursor(Qt.PointingHandCursor))
        edit_btn.setFont(QFont("Inter", 14))
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #4A4D56;
                border-radius: 18px;
                color: #9AA0A6;
            }
            QPushButton:hover {
                background-color: rgba(79, 209, 197, 0.2);
                border: 1px solid #4FD1C5;
                color: #4FD1C5;
            }
        """)
        edit_btn.clicked.connect(self.edit_habit)
        layout.addWidget(edit_btn)
        
        # Delete button
        delete_btn = QPushButton("✕")
        delete_btn.setFixedSize(36, 36)
        delete_btn.setCursor(QCursor(Qt.PointingHandCursor))
        delete_btn.setFont(QFont("Inter", 14))
        delete_btn.setStyleSheet("""
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
        delete_btn.clicked.connect(self.delete_habit)
        layout.addWidget(delete_btn)
    
    def on_checkbox_clicked(self, checked):
        """Handle checkbox click"""
        if self.is_processing:
            return
        
        self.is_processing = True
        
        try:
            if checked:
                # Marking as complete - show notes dialog
                from app.ui.notes_dialog import NotesDialog
                
                notes_dialog = NotesDialog(self.habit, self)
                if notes_dialog.exec():
                    # User clicked save
                    notes = notes_dialog.get_notes()
                    success = self.habit_service.mark_habit_complete(self.habit.id, notes=notes)
                    
                    if success:
                        # Send notification
                        try:
                            from app.services.notification_service import get_notification_service
                            notif_service = get_notification_service()
                            notif_service.send_habit_completed(self.habit.name)
                            
                            streak_info = self.streak_service.get_streak_info(self.habit.id)
                            notif_service.send_streak_milestone(self.habit.name, streak_info['current_streak'])
                        except Exception as e:
                            print(f"Notification error: {e}")
                    
                    # Refresh view
                    if self.parent_view:
                        self.parent_view.refresh()
                else:
                    # User canceled - uncheck
                    self.checkbox.setChecked(False)
            else:
                # Unchecking - mark as incomplete
                self.habit_service.unmark_habit_complete(self.habit.id)
                
                # Refresh view
                if self.parent_view:
                    self.parent_view.refresh()
        
        finally:
            self.is_processing = False
    
    def view_notes(self):
        """View/edit notes"""
        from app.ui.notes_dialog import NotesDialog
        
        notes_dialog = NotesDialog(self.habit, self)
        if notes_dialog.exec():
            notes = notes_dialog.get_notes()
            self.habit_service.mark_habit_complete(self.habit.id, notes=notes)
            if self.parent_view:
                self.parent_view.refresh()
    
    def edit_habit(self):
        """Edit habit"""
        from app.ui.edit_habit_dialog import EditHabitDialog
        
        dialog = EditHabitDialog(self.habit, self)
        if dialog.exec():
            if self.parent_view:
                self.parent_view.load_habits()
    
    def delete_habit(self):
        """Delete habit"""
        msg = QMessageBox(self)
        msg.setWindowTitle("Delete Habit")
        msg.setText(f"Delete '{self.habit.name}'?")
        msg.setInformativeText("This will move the habit to trash.")
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
                border: 1px solid #4FD1C5;
            }
        """)
        
        if msg.exec() == QMessageBox.Yes:
            self.habit_service.hard_delete_habit(self.habit.id, save_to_trash=True)
            if self.parent_view:
                self.parent_view.load_habits()


class TodayView(QWidget):
    """Today's habits view"""
    
    def __init__(self):
        super().__init__()
        self.habit_service = get_habit_service()
        self.streak_service = get_streak_service()
        self.all_habits = []
        self.filtered_habits = []
        self.current_filter = ""
        self.current_sort = "date_desc"
        self.setup_ui()
        self.load_habits()
    
    def setup_ui(self):
        """Setup UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
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
        
        self.habits_container = QWidget()
        self.habits_container.setStyleSheet("background-color: transparent;")
        self.habits_layout = QVBoxLayout(self.habits_container)
        self.habits_layout.setSpacing(12)
        self.habits_layout.setContentsMargins(0, 0, 0, 0)
        self.habits_layout.addStretch()
        
        scroll.setWidget(self.habits_container)
        layout.addWidget(scroll)
    
    def load_habits(self):
        """Load habits"""
        self.all_habits = self.habit_service.get_all_habits()
        self.apply_filter_and_sort()
    
    def filter_habits(self, search_text):
        """Filter habits"""
        self.current_filter = search_text.lower()
        self.apply_filter_and_sort()
    
    def sort_habits(self, sort_by):
        """Sort habits"""
        self.current_sort = sort_by
        self.apply_filter_and_sort()
    
    def apply_filter_and_sort(self):
        """Apply filter and sort"""
        if self.current_filter:
            self.filtered_habits = [
                h for h in self.all_habits 
                if self.current_filter in h.name.lower() or 
                (h.description and self.current_filter in h.description.lower()) or
                self.current_filter in h.category.lower()
            ]
        else:
            self.filtered_habits = self.all_habits.copy()
        
        if self.current_sort == "name_asc":
            self.filtered_habits.sort(key=lambda h: h.name.lower())
        elif self.current_sort == "name_desc":
            self.filtered_habits.sort(key=lambda h: h.name.lower(), reverse=True)
        elif self.current_sort == "streak_desc":
            self.filtered_habits.sort(
                key=lambda h: self.streak_service.get_streak_info(h.id)['current_streak'],
                reverse=True
            )
        elif self.current_sort == "completion_desc":
            self.filtered_habits.sort(
                key=lambda h: len(self.habit_service.get_habit_completions(h.id)),
                reverse=True
            )
        
        self.display_habits()
    
    def display_habits(self):
        """Display habits"""
        while self.habits_layout.count() > 1:
            item = self.habits_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        if not self.filtered_habits:
            empty_widget = QWidget()
            empty_layout = QVBoxLayout(empty_widget)
            empty_layout.setAlignment(Qt.AlignCenter)
            
            emoji_label = QLabel("📝")
            emoji_label.setFont(QFont("Inter", 48))
            emoji_label.setAlignment(Qt.AlignCenter)
            emoji_label.setStyleSheet("color: #4A4D56; background: transparent;")
            empty_layout.addWidget(emoji_label)
            
            text_label = QLabel("No habits yet")
            text_label.setFont(QFont("Inter", 18, QFont.Medium))
            text_label.setAlignment(Qt.AlignCenter)
            text_label.setStyleSheet("color: #9AA0A6; background: transparent; margin-top: 16px;")
            empty_layout.addWidget(text_label)
            
            subtext = QLabel("Click 'Add New Habit' to get started")
            subtext.setFont(QFont("Inter", 13))
            subtext.setAlignment(Qt.AlignCenter)
            subtext.setStyleSheet("color: #6B6E76; background: transparent; margin-top: 8px;")
            empty_layout.addWidget(subtext)
            
            self.habits_layout.insertWidget(0, empty_widget)
        else:
            for habit in self.filtered_habits:
                habit_item = HabitItem(habit, self)
                self.habits_layout.insertWidget(self.habits_layout.count() - 1, habit_item)
    
    def refresh(self):
        """Refresh"""
        self.load_habits()
