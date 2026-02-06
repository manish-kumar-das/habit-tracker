"""
Today's habits view with search and sort functionality
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
    """Single habit item widget with dark mode design"""
    
    def __init__(self, habit, parent=None):
        super().__init__(parent)
        self.habit = habit
        self.parent_view = parent
        self.habit_service = get_habit_service()
        self.streak_service = get_streak_service()
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
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
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
        self.checkbox.stateChanged.connect(self.on_checkbox_changed)
        
        layout.addWidget(self.checkbox)
        
        # Habit info container
        info_layout = QVBoxLayout()
        info_layout.setSpacing(6)
        
        # Habit name
        self.name_label = QLabel(self.habit.name)
        self.name_label.setFont(QFont("Inter", 15, QFont.Medium))
        self.name_label.setStyleSheet("""
            QLabel {
                color: #E4E6EB;
                background: transparent;
            }
        """)
        info_layout.addWidget(self.name_label)
        
        # Description
        if self.habit.description:
            self.desc_label = QLabel(self.habit.description)
            self.desc_label.setFont(QFont("Inter", 12))
            self.desc_label.setStyleSheet("""
                QLabel {
                    color: #9AA0A6;
                    background: transparent;
                }
            """)
            self.desc_label.setWordWrap(True)
            info_layout.addWidget(self.desc_label)
        
        layout.addLayout(info_layout, stretch=1)
        
        # Streak info
        streak_info = self.streak_service.get_streak_info(self.habit.id)
        current_streak = streak_info['current_streak']
        
        if current_streak > 0:
            self.streak_label = QLabel(f"🔥 {current_streak}")
            self.streak_label.setFont(QFont("Inter", 14, QFont.Bold))
            self.streak_label.setStyleSheet("""
                QLabel {
                    color: #FFB74D;
                    background-color: rgba(255, 183, 77, 0.15);
                    padding: 8px 16px;
                    border-radius: 20px;
                }
            """)
            self.streak_label.setAlignment(Qt.AlignCenter)
            self.streak_label.setFixedHeight(40)
        else:
            self.streak_label = QLabel("Start")
            self.streak_label.setFont(QFont("Inter", 12))
            self.streak_label.setStyleSheet("""
                QLabel {
                    color: #9AA0A6;
                    background-color: transparent;
                    padding: 8px 16px;
                    border-radius: 20px;
                    border: 1px solid #4A4D56;
                }
            """)
            self.streak_label.setAlignment(Qt.AlignCenter)
            self.streak_label.setFixedHeight(40)
        
        layout.addWidget(self.streak_label)
        
        # Edit button
        self.edit_btn = QPushButton("✏")
        self.edit_btn.setFixedSize(36, 36)
        self.edit_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.edit_btn.setFont(QFont("Inter", 14))
        self.edit_btn.setStyleSheet("""
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
            QPushButton:pressed {
                background-color: rgba(79, 209, 197, 0.3);
            }
        """)
        self.edit_btn.clicked.connect(self.edit_habit)
        layout.addWidget(self.edit_btn)
        
        # Delete button
        self.delete_btn = QPushButton("✕")
        self.delete_btn.setFixedSize(36, 36)
        self.delete_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.delete_btn.setFont(QFont("Inter", 14))
        self.delete_btn.setStyleSheet("""
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
            QPushButton:pressed {
                background-color: rgba(239, 83, 80, 0.3);
            }
        """)
        self.delete_btn.clicked.connect(self.delete_habit)
        layout.addWidget(self.delete_btn)
    
    def mousePressEvent(self, event):
        """Handle mouse press on the entire habit item"""
        click_pos = event.pos()
        if (not self.delete_btn.geometry().contains(click_pos) and 
            not self.edit_btn.geometry().contains(click_pos)):
            self.checkbox.toggle()
        super().mousePressEvent(event)
    
    def on_checkbox_changed(self, state):
        """Handle checkbox state change"""
        if state == Qt.Checked:
            success = self.habit_service.mark_habit_complete(self.habit.id)
            if success and self.parent_view:
                self.parent_view.refresh()
        else:
            self.habit_service.unmark_habit_complete(self.habit.id)
            if self.parent_view:
                self.parent_view.refresh()
    
    def edit_habit(self):
        """Open edit dialog for this habit"""
        from app.ui.edit_habit_dialog import EditHabitDialog
        
        dialog = EditHabitDialog(self.habit, self)
        if dialog.exec():
            if self.parent_view:
                self.parent_view.load_habits()
    
    def delete_habit(self):
        """Delete this habit"""
        msg = QMessageBox(self)
        msg.setWindowTitle("Delete Habit")
        msg.setText(f"Delete '{self.habit.name}'?")
        msg.setInformativeText("This will remove all completion history.")
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
            self.habit_service.hard_delete_habit(self.habit.id)
            if self.parent_view:
                self.parent_view.load_habits()


class TodayView(QWidget):
    """Today's habits view with search and sort"""
    
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
        """Setup the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
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
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Container for habit items
        self.habits_container = QWidget()
        self.habits_container.setStyleSheet("background-color: transparent;")
        self.habits_layout = QVBoxLayout(self.habits_container)
        self.habits_layout.setSpacing(12)
        self.habits_layout.setContentsMargins(0, 0, 0, 0)
        self.habits_layout.addStretch()
        
        scroll.setWidget(self.habits_container)
        layout.addWidget(scroll)
    
    def load_habits(self):
        """Load all habits from database"""
        self.all_habits = self.habit_service.get_all_habits()
        self.apply_filter_and_sort()
    
    def filter_habits(self, search_text):
        """Filter habits by search text"""
        self.current_filter = search_text.lower()
        self.apply_filter_and_sort()
    
    def sort_habits(self, sort_by):
        """Sort habits by criteria"""
        self.current_sort = sort_by
        self.apply_filter_and_sort()
    
    def apply_filter_and_sort(self):
        """Apply both filter and sort, then display"""
        # Filter
        if self.current_filter:
            self.filtered_habits = [
                h for h in self.all_habits 
                if self.current_filter in h.name.lower() or 
                (h.description and self.current_filter in h.description.lower())
            ]
        else:
            self.filtered_habits = self.all_habits.copy()
        
        # Sort
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
        elif self.current_sort == "date_desc":
            # Already in order from database (most recent first)
            pass
        
        self.display_habits()
    
    def display_habits(self):
        """Display the filtered and sorted habits"""
        # Clear existing items
        while self.habits_layout.count() > 1:
            item = self.habits_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        if not self.filtered_habits:
            # Empty state
            empty_widget = QWidget()
            empty_layout = QVBoxLayout(empty_widget)
            empty_layout.setAlignment(Qt.AlignCenter)
            
            if self.current_filter and not self.all_habits:
                emoji = "📝"
                title = "No habits yet"
                subtitle = "Click 'Add New Habit' to get started"
            elif self.current_filter:
                emoji = "🔍"
                title = "No matches found"
                subtitle = f"No habits match '{self.current_filter}'"
            else:
                emoji = "📝"
                title = "No habits yet"
                subtitle = "Click 'Add New Habit' to get started"
            
            emoji_label = QLabel(emoji)
            emoji_label.setFont(QFont("Inter", 48))
            emoji_label.setAlignment(Qt.AlignCenter)
            emoji_label.setStyleSheet("color: #4A4D56; background: transparent;")
            empty_layout.addWidget(emoji_label)
            
            text_label = QLabel(title)
            text_label.setFont(QFont("Inter", 18, QFont.Medium))
            text_label.setAlignment(Qt.AlignCenter)
            text_label.setStyleSheet("color: #9AA0A6; background: transparent; margin-top: 16px;")
            empty_layout.addWidget(text_label)
            
            subtext = QLabel(subtitle)
            subtext.setFont(QFont("Inter", 13))
            subtext.setAlignment(Qt.AlignCenter)
            subtext.setStyleSheet("color: #6B6E76; background: transparent; margin-top: 8px;")
            empty_layout.addWidget(subtext)
            
            self.habits_layout.insertWidget(0, empty_widget)
        else:
            # Add habit items
            for habit in self.filtered_habits:
                habit_item = HabitItem(habit, self)
                self.habits_layout.insertWidget(self.habits_layout.count() - 1, habit_item)
    
    def refresh(self):
        """Refresh the view"""
        self.load_habits()
