"""
Goals Content View - Shows in main content area (not dialog)
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QScrollArea, QFrame, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QCursor
from app.services.goal_service import get_goal_service
from app.ui.goals_view import GoalCard, AddGoalDialog


class GoalsContentView(QWidget):
    """Goals view for content area"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.goal_service = get_goal_service()
        self.setup_ui()
        self.load_goals()
    
    def setup_ui(self):
        """Setup goals UI"""
        self.setStyleSheet("background-color: #F8F9FA;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = QFrame()
        header.setFixedHeight(100)
        header.setStyleSheet("QFrame { background-color: #FFFFFF; border-bottom: 1px solid #E5E7EB; }")
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(32, 20, 32, 20)
        
        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)
        
        title = QLabel("🎯 Goals & Milestones")
        title.setFont(QFont("SF Pro Display", 24, QFont.Bold))
        title.setStyleSheet("color: #111827; background: transparent;")
        title_layout.addWidget(title)
        
        subtitle = QLabel("Set targets and track your progress")
        subtitle.setFont(QFont("SF Pro Text", 13))
        subtitle.setStyleSheet("color: #6B7280; background: transparent;")
        title_layout.addWidget(subtitle)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        add_btn = QPushButton("+ New Goal")
        add_btn.setFont(QFont("SF Pro Text", 13, QFont.Bold))
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
        
        layout.addWidget(header)
        
        # Content scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        content = QWidget()
        content.setStyleSheet("background-color: #F8F9FA;")
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
            empty.setFont(QFont("SF Pro Text", 16))
            empty.setAlignment(Qt.AlignCenter)
            empty.setStyleSheet("color: #9CA3AF; padding: 80px;")
            self.content_layout.addWidget(empty)
            return
        
        active_goals = [g for g in all_goals if not g.is_completed]
        completed_goals = [g for g in all_goals if g.is_completed]
        
        if active_goals:
            active_label = QLabel(f"🎯 Active Goals ({len(active_goals)})")
            active_label.setFont(QFont("SF Pro Display", 18, QFont.Bold))
            active_label.setStyleSheet("color: #111827; background: transparent;")
            self.content_layout.addWidget(active_label)
            
            for goal in active_goals:
                goal_card = GoalCard(goal, self)
                self.content_layout.addWidget(goal_card)
        
        if completed_goals:
            completed_label = QLabel(f"✓ Completed Goals ({len(completed_goals)})")
            completed_label.setFont(QFont("SF Pro Display", 18, QFont.Bold))
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
