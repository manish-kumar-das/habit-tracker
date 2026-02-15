"""
Goals & Milestones view - Track progress towards targets
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QScrollArea, QFrame, QWidget, QProgressBar,
    QComboBox, QSpinBox, QDateEdit, QMessageBox
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QCursor
from datetime import datetime, timedelta
from app.services.goal_service import get_goal_service
from app.services.habit_service import get_habit_service


class GoalCard(QFrame):
    """Card displaying a single goal"""
    
    def __init__(self, goal, parent=None):
        super().__init__(parent)
        self.goal = goal
        self.parent_view = parent
        self.habit_service = get_habit_service()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup goal card UI"""
        self.setFrameShape(QFrame.StyledPanel)
        
        progress = self.goal.get_progress_percentage()
        
        if self.goal.is_completed:
            border_color = "#10B981"
            bg_color = "#D1FAE5"
        elif progress >= 75:
            border_color = "#F59E0B"
            bg_color = "#FEF3C7"
        elif progress >= 50:
            border_color = "#6366F1"
            bg_color = "#E0E7FF"
        else:
            border_color = "#9CA3AF"
            bg_color = "#F3F4F6"
        
        self.setStyleSheet(f"""
            GoalCard {{
                background-color: {bg_color};
                border-left: 4px solid {border_color};
                border-radius: 12px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)
        
        # Header
        header_layout = QHBoxLayout()
        
        icons = {'streak': '🔥', 'total': '✅', 'consistency': '📊', 'category': '🏷️'}
        
        icon_label = QLabel(icons.get(self.goal.goal_type, '🎯'))
        icon_label.setFont(QFont("Inter", 24))
        icon_label.setStyleSheet("background: transparent;")
        header_layout.addWidget(icon_label)
        
        desc_layout = QVBoxLayout()
        desc_layout.setSpacing(4)
        
        desc_text = QLabel(self.goal.description)
        desc_text.setFont(QFont("Inter", 14, QFont.Bold))
        desc_text.setStyleSheet("color: #111827; background: transparent;")
        desc_text.setWordWrap(True)
        desc_layout.addWidget(desc_text)
        
        if self.goal.habit_id:
            habit = self.habit_service.get_habit_by_id(self.goal.habit_id)
            if habit:
                habit_label = QLabel(f"Habit: {habit.name}")
                habit_label.setFont(QFont("Inter", 11))
                habit_label.setStyleSheet("color: #6B7280; background: transparent;")
                desc_layout.addWidget(habit_label)
        
        header_layout.addLayout(desc_layout, stretch=1)
        
        if not self.goal.is_completed:
            delete_btn = QPushButton("✕")
            delete_btn.setFixedSize(32, 32)
            delete_btn.setCursor(Qt.PointingHandCursor)
            delete_btn.setFont(QFont("Inter", 14))
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: 1px solid #E5E7EB;
                    border-radius: 16px;
                    color: #9CA3AF;
                }
                QPushButton:hover {
                    background-color: #FEE2E2;
                    border: 1px solid #EF4444;
                    color: #EF4444;
                }
            """)
            delete_btn.clicked.connect(self.delete_goal)
            header_layout.addWidget(delete_btn)
        
        layout.addLayout(header_layout)
        
        # Progress bar
        progress_bar = QProgressBar()
        progress_bar.setMaximum(100)
        progress_bar.setValue(progress)
        progress_bar.setTextVisible(True)
        progress_bar.setFormat(f"{self.goal.current_value}/{self.goal.target_value} ({progress}%)")
        progress_bar.setFixedHeight(32)
        progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid #E5E7EB;
                border-radius: 10px;
                background-color: #FFFFFF;
                text-align: center;
                color: #111827;
                font-size: 12px;
                font-weight: bold;
            }}
            QProgressBar::chunk {{
                background: {border_color};
                border-radius: 8px;
            }}
        """)
        layout.addWidget(progress_bar)
        
        # Footer
        footer_layout = QHBoxLayout()
        footer_layout.setSpacing(16)
        
        start_label = QLabel(f"Started: {self.goal.start_date}")
        start_label.setFont(QFont("Inter", 10))
        start_label.setStyleSheet("color: #6B7280; background: transparent;")
        footer_layout.addWidget(start_label)
        
        if self.goal.deadline:
            deadline_date = datetime.strptime(self.goal.deadline, "%Y-%m-%d")
            days_left = (deadline_date - datetime.now()).days
            
            if days_left > 0:
                deadline_label = QLabel(f"⏰ {days_left} days left")
                deadline_label.setFont(QFont("Inter", 10, QFont.Medium))
                deadline_label.setStyleSheet("color: #F59E0B; background: transparent;")
            else:
                deadline_label = QLabel("⏰ Deadline passed")
                deadline_label.setFont(QFont("Inter", 10, QFont.Medium))
                deadline_label.setStyleSheet("color: #EF4444; background: transparent;")
            
            footer_layout.addWidget(deadline_label)
        
        footer_layout.addStretch()
        
        if self.goal.is_completed:
            completed_label = QLabel("✓ Completed!")
            completed_label.setFont(QFont("Inter", 11, QFont.Bold))
            completed_label.setStyleSheet("""
                QLabel {
                    color: #059669;
                    background-color: #D1FAE5;
                    padding: 4px 12px;
                    border-radius: 8px;
                }
            """)
            footer_layout.addWidget(completed_label)
        
        layout.addLayout(footer_layout)
    
    def delete_goal(self):
        """Delete this goal"""
        msg = QMessageBox(self)
        msg.setWindowTitle("Delete Goal")
        msg.setText(f"Delete this goal?")
        msg.setInformativeText("This action cannot be undone.")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        
        if msg.exec() == QMessageBox.Yes:
            goal_service = get_goal_service()
            goal_service.delete_goal(self.goal.id)
            if self.parent_view:
                self.parent_view.load_goals()


class AddGoalDialog(QDialog):
    """Dialog for creating a new goal"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.habit_service = get_habit_service()
        self.goal_service = get_goal_service()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup dialog UI"""
        self.setWindowTitle("Create New Goal")
        self.setModal(True)
        self.setMinimumWidth(500)
        self.setStyleSheet("QDialog { background-color: #FFFFFF; }")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(20)
        
        title = QLabel("🎯 Create New Goal")
        title.setFont(QFont("Inter", 20, QFont.Bold))
        title.setStyleSheet("color: #111827; background: transparent;")
        layout.addWidget(title)
        
        # Habit selector
        habit_layout = QVBoxLayout()
        habit_layout.setSpacing(8)
        
        habit_label = QLabel("Select Habit:")
        habit_label.setFont(QFont("Inter", 13, QFont.Medium))
        habit_label.setStyleSheet("color: #111827; background: transparent;")
        habit_layout.addWidget(habit_label)
        
        self.habit_combo = QComboBox()
        self.habit_combo.setFont(QFont("Inter", 13))
        self.habit_combo.setFixedHeight(44)
        self.habit_combo.setCursor(Qt.PointingHandCursor)
        self.habit_combo.setStyleSheet("""
            QComboBox {
                padding: 10px 16px;
                border: 2px solid #E5E7EB;
                border-radius: 10px;
                background-color: #F9FAFB;
                color: #111827;
            }
            QComboBox:hover { border: 2px solid #6366F1; }
        """)
        
        habits = self.habit_service.get_all_habits()
        for habit in habits:
            self.habit_combo.addItem(habit.name, habit.id)
        
        habit_layout.addWidget(self.habit_combo)
        layout.addLayout(habit_layout)
        
        # Goal type
        type_layout = QVBoxLayout()
        type_layout.setSpacing(8)
        
        type_label = QLabel("Goal Type:")
        type_label.setFont(QFont("Inter", 13, QFont.Medium))
        type_label.setStyleSheet("color: #111827; background: transparent;")
        type_layout.addWidget(type_label)
        
        self.type_combo = QComboBox()
        self.type_combo.setFont(QFont("Inter", 13))
        self.type_combo.setFixedHeight(44)
        self.type_combo.setCursor(Qt.PointingHandCursor)
        self.type_combo.setStyleSheet("""
            QComboBox {
                padding: 10px 16px;
                border: 2px solid #E5E7EB;
                border-radius: 10px;
                background-color: #F9FAFB;
                color: #111827;
            }
            QComboBox:hover { border: 2px solid #6366F1; }
        """)
        
        self.type_combo.addItem("🔥 Streak Goal (Reach X-day streak)", "streak")
        self.type_combo.addItem("✅ Total Completions (Complete X times)", "total")
        self.type_combo.addItem("📊 Consistency (X% success rate)", "consistency")
        
        type_layout.addWidget(self.type_combo)
        layout.addLayout(type_layout)
        
        # Target value
        target_layout = QVBoxLayout()
        target_layout.setSpacing(8)
        
        target_label = QLabel("Target Value:")
        target_label.setFont(QFont("Inter", 13, QFont.Medium))
        target_label.setStyleSheet("color: #111827; background: transparent;")
        target_layout.addWidget(target_label)
        
        self.target_spin = QSpinBox()
        self.target_spin.setMinimum(1)
        self.target_spin.setMaximum(1000)
        self.target_spin.setValue(30)
        self.target_spin.setFont(QFont("Inter", 13))
        self.target_spin.setFixedHeight(44)
        self.target_spin.setStyleSheet("""
            QSpinBox {
                padding: 10px 16px;
                border: 2px solid #E5E7EB;
                border-radius: 10px;
                background-color: #F9FAFB;
                color: #111827;
            }
            QSpinBox:hover { border: 2px solid #6366F1; }
        """)
        
        target_layout.addWidget(self.target_spin)
        layout.addLayout(target_layout)
        
        # Deadline
        deadline_layout = QVBoxLayout()
        deadline_layout.setSpacing(8)
        
        deadline_label = QLabel("Deadline (Optional):")
        deadline_label.setFont(QFont("Inter", 13, QFont.Medium))
        deadline_label.setStyleSheet("color: #111827; background: transparent;")
        deadline_layout.addWidget(deadline_label)
        
        self.deadline_edit = QDateEdit()
        self.deadline_edit.setCalendarPopup(True)
        self.deadline_edit.setDate(QDate.currentDate().addMonths(1))
        self.deadline_edit.setFont(QFont("Inter", 13))
        self.deadline_edit.setFixedHeight(44)
        self.deadline_edit.setStyleSheet("""
            QDateEdit {
                padding: 10px 16px;
                border: 2px solid #E5E7EB;
                border-radius: 10px;
                background-color: #F9FAFB;
                color: #111827;
            }
            QDateEdit:hover { border: 2px solid #6366F1; }
        """)
        
        deadline_layout.addWidget(self.deadline_edit)
        layout.addLayout(deadline_layout)
        
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
                border: 2px solid #E5E7EB;
                border-radius: 10px;
                color: #6B7280;
                background-color: transparent;
            }
            QPushButton:hover {
                border: 2px solid #6366F1;
                color: #111827;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        create_btn = QPushButton("Create Goal")
        create_btn.setFont(QFont("Inter", 13, QFont.Bold))
        create_btn.setFixedHeight(48)
        create_btn.setCursor(Qt.PointingHandCursor)
        create_btn.setStyleSheet("""
            QPushButton {
                padding: 12px 32px;
                border: none;
                border-radius: 10px;
                color: #FFFFFF;
                background-color: #6366F1;
            }
            QPushButton:hover {
                background-color: #5558E3;
            }
        """)
        create_btn.clicked.connect(self.create_goal)
        button_layout.addWidget(create_btn)
        
        layout.addLayout(button_layout)
    
    def create_goal(self):
        """Create the goal"""
        habit_id = self.habit_combo.currentData()
        goal_type = self.type_combo.currentData()
        target_value = self.target_spin.value()
        
        if not habit_id:
            QMessageBox.warning(self, "Error", "Please select a habit!")
            return
        
        habit = self.habit_service.get_habit_by_id(habit_id)
        
        if goal_type == 'streak':
            description = f"Reach {target_value}-day streak on '{habit.name}'"
        elif goal_type == 'total':
            description = f"Complete '{habit.name}' {target_value} times"
        else:
            description = f"Maintain {target_value}% success rate on '{habit.name}'"
        
        deadline = self.deadline_edit.date().toString("yyyy-MM-dd")
        
        self.goal_service.create_goal(
            habit_id=habit_id,
            goal_type=goal_type,
            target_value=target_value,
            description=description,
            deadline=deadline
        )
        
        self.accept()


class GoalsView(QDialog):
    """Goals & Milestones view"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.goal_service = get_goal_service()
        self.setup_ui()
        self.load_goals()
    
    def setup_ui(self):
        """Setup UI"""
        self.setWindowTitle("Goals & Milestones")
        self.setModal(False)
        self.setMinimumSize(900, 700)
        self.setStyleSheet("QDialog { background-color: #F9FAFB; }")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = QFrame()
        header.setFixedHeight(100)
        header.setFrameShape(QFrame.StyledPanel)
        header.setStyleSheet("QFrame { background-color: #FFFFFF; border-bottom: 1px solid #E5E7EB; }")
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(32, 20, 32, 20)
        
        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)
        
        title = QLabel("🎯 Goals & Milestones")
        title.setFont(QFont("Inter", 24, QFont.Bold))
        title.setStyleSheet("color: #111827; background: transparent;")
        title_layout.addWidget(title)
        
        subtitle = QLabel("Set targets and track your progress")
        subtitle.setFont(QFont("Inter", 13))
        subtitle.setStyleSheet("color: #6B7280; background: transparent;")
        title_layout.addWidget(subtitle)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        add_btn = QPushButton("+ New Goal")
        add_btn.setFont(QFont("Inter", 13, QFont.Bold))
        add_btn.setFixedHeight(48)
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.setStyleSheet("""
            QPushButton {
                padding: 12px 24px;
                border: none;
                border-radius: 10px;
                color: #FFFFFF;
                background-color: #6366F1;
            }
            QPushButton:hover {
                background-color: #5558E3;
            }
        """)
        add_btn.clicked.connect(self.add_goal)
        header_layout.addWidget(add_btn)
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(48, 48)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setFont(QFont("Inter", 18))
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 2px solid #E5E7EB;
                border-radius: 24px;
                color: #6B7280;
            }
            QPushButton:hover {
                background-color: #FEE2E2;
                border: 2px solid #EF4444;
                color: #EF4444;
            }
        """)
        close_btn.clicked.connect(self.close)
        header_layout.addWidget(close_btn)
        
        layout.addWidget(header)
        
        # Content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        content = QWidget()
        content.setStyleSheet("background-color: #F9FAFB;")
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setContentsMargins(32, 24, 32, 24)
        self.content_layout.setSpacing(16)
        
        scroll.setWidget(content)
        layout.addWidget(scroll)
    
    def load_goals(self):
        """Load and display goals"""
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        self.goal_service.update_all_goals_progress()
        
        all_goals = self.goal_service.get_all_goals(include_completed=True)
        
        if not all_goals:
            empty = QLabel("No goals yet!\nClick '+ New Goal' to create your first goal.")
            empty.setFont(QFont("Inter", 16))
            empty.setAlignment(Qt.AlignCenter)
            empty.setStyleSheet("color: #9CA3AF; padding: 80px;")
            self.content_layout.addWidget(empty)
            return
        
        active_goals = [g for g in all_goals if not g.is_completed]
        completed_goals = [g for g in all_goals if g.is_completed]
        
        if active_goals:
            active_label = QLabel(f"🎯 Active Goals ({len(active_goals)})")
            active_label.setFont(QFont("Inter", 18, QFont.Bold))
            active_label.setStyleSheet("color: #111827; background: transparent;")
            self.content_layout.addWidget(active_label)
            
            for goal in active_goals:
                goal_card = GoalCard(goal, self)
                self.content_layout.addWidget(goal_card)
        
        if completed_goals:
            completed_label = QLabel(f"✓ Completed Goals ({len(completed_goals)})")
            completed_label.setFont(QFont("Inter", 18, QFont.Bold))
            completed_label.setStyleSheet("color: #059669; background: transparent; margin-top: 16px;")
            self.content_layout.addWidget(completed_label)
            
            for goal in completed_goals:
                goal_card = GoalCard(goal, self)
                self.content_layout.addWidget(goal_card)
        
        self.content_layout.addStretch()
    
    def add_goal(self):
        """Open add goal dialog"""
        dialog = AddGoalDialog(self)
        if dialog.exec():
            self.load_goals()
