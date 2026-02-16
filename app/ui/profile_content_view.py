"""
Profile Content View - User profile and account management
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QScrollArea, QFrame, QLineEdit,
    QTextEdit, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QCursor
from app.services.habit_service import get_habit_service
from app.services.streak_service import get_streak_service
from app.services.profile_service import get_profile_service


class StatCard(QFrame):
    """Stat card for profile"""
    
    def __init__(self, icon, value, label, color, parent=None):
        super().__init__(parent)
        self.setup_ui(icon, value, label, color)
    
    def setup_ui(self, icon, value, label, color):
        """Setup stat card"""
        self.setStyleSheet(f"""
            QFrame {{
                background-color: #FFFFFF;
                border-left: 4px solid {color};
                border-radius: 12px;
            }}
        """)
        self.setFixedSize(180, 120)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(8)
        
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("SF Pro Display", 32))
        icon_label.setStyleSheet("background: transparent;")
        layout.addWidget(icon_label)
        
        value_label = QLabel(value)
        value_label.setFont(QFont("SF Pro Display", 24, QFont.Bold))
        value_label.setStyleSheet(f"color: {color}; background: transparent;")
        layout.addWidget(value_label)
        
        label_label = QLabel(label)
        label_label.setFont(QFont("SF Pro Text", 11))
        label_label.setStyleSheet("color: #6B7280; background: transparent;")
        layout.addWidget(label_label)


class ProfileContentView(QWidget):
    """Profile view for content area"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.habit_service = get_habit_service()
        self.streak_service = get_streak_service()
        self.profile_service = get_profile_service()
        self.setup_ui()
        self.load_profile_data()
    
    def setup_ui(self):
        """Setup profile UI"""
        self.setStyleSheet("background-color: #F8F9FA;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header with gradient
        header = QFrame()
        header.setFixedHeight(200)
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6366F1, stop:1 #8B5CF6);
            }
        """)
        
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(32, 30, 32, 30)
        header_layout.setAlignment(Qt.AlignCenter)
        
        # Avatar (large)
        avatar_container = QFrame()
        avatar_container.setFixedSize(100, 100)
        avatar_container.setStyleSheet("""
            QFrame {
                background-color: #FFD43B;
                border: 4px solid #FFFFFF;
                border-radius: 50px;
            }
        """)
        
        avatar_layout = QVBoxLayout(avatar_container)
        avatar_layout.setContentsMargins(0, 0, 0, 0)
        
        avatar_icon = QLabel("👤")
        avatar_icon.setFont(QFont("SF Pro Display", 48))
        avatar_icon.setAlignment(Qt.AlignCenter)
        avatar_icon.setStyleSheet("background: transparent; border: none;")
        avatar_layout.addWidget(avatar_icon)
        
        header_layout.addWidget(avatar_container, alignment=Qt.AlignCenter)
        
        header_layout.addSpacing(16)
        
        # User name
        self.name_label = QLabel("Loading...")
        self.name_label.setFont(QFont("SF Pro Display", 28, QFont.Bold))
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setStyleSheet("color: #FFFFFF; background: transparent;")
        header_layout.addWidget(self.name_label)
        
        # Member type
        member_badge = QLabel("✨ Premium Member")
        member_badge.setFont(QFont("SF Pro Text", 14, QFont.Medium))
        member_badge.setAlignment(Qt.AlignCenter)
        member_badge.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                background-color: rgba(255, 255, 255, 0.2);
                padding: 6px 20px;
                border-radius: 20px;
            }
        """)
        header_layout.addWidget(member_badge, alignment=Qt.AlignCenter)
        
        layout.addWidget(header)
        
        # Content scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        content = QWidget()
        content.setStyleSheet("background-color: #F8F9FA;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(32, 24, 32, 24)
        content_layout.setSpacing(24)
        
        # Stats Section
        stats_label = QLabel("📊 Your Statistics")
        stats_label.setFont(QFont("SF Pro Display", 20, QFont.Bold))
        stats_label.setStyleSheet("color: #111827; background: transparent;")
        content_layout.addWidget(stats_label)
        
        # Stats cards
        self.stats_layout = QHBoxLayout()
        self.stats_layout.setSpacing(16)
        content_layout.addLayout(self.stats_layout)
        
        # Account Info Section
        info_label = QLabel("👤 Account Information")
        info_label.setFont(QFont("SF Pro Display", 20, QFont.Bold))
        info_label.setStyleSheet("color: #111827; background: transparent; margin-top: 16px;")
        content_layout.addWidget(info_label)
        
        # Info card
        info_card = QFrame()
        info_card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
            }
        """)
        
        info_layout = QVBoxLayout(info_card)
        info_layout.setContentsMargins(24, 20, 24, 20)
        info_layout.setSpacing(16)
        
        # Name field
        name_field_layout = QVBoxLayout()
        name_field_layout.setSpacing(8)
        
        name_field_label = QLabel("Display Name")
        name_field_label.setFont(QFont("SF Pro Text", 13, QFont.Medium))
        name_field_label.setStyleSheet("color: #111827; background: transparent;")
        name_field_layout.addWidget(name_field_label)
        
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter your name")
        self.name_edit.setFont(QFont("SF Pro Text", 14))
        self.name_edit.setFixedHeight(44)
        self.name_edit.setStyleSheet("""
            QLineEdit {
                padding: 10px 16px;
                border: 2px solid #E5E7EB;
                border-radius: 10px;
                background-color: #F9FAFB;
                color: #111827;
            }
            QLineEdit:focus {
                border: 2px solid #6366F1;
                background-color: #FFFFFF;
            }
        """)
        name_field_layout.addWidget(self.name_edit)
        
        info_layout.addLayout(name_field_layout)
        
        # Email field
        email_field_layout = QVBoxLayout()
        email_field_layout.setSpacing(8)
        
        email_field_label = QLabel("Email")
        email_field_label.setFont(QFont("SF Pro Text", 13, QFont.Medium))
        email_field_label.setStyleSheet("color: #111827; background: transparent;")
        email_field_layout.addWidget(email_field_label)
        
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("your.email@example.com")
        self.email_edit.setFont(QFont("SF Pro Text", 14))
        self.email_edit.setFixedHeight(44)
        self.email_edit.setStyleSheet("""
            QLineEdit {
                padding: 10px 16px;
                border: 2px solid #E5E7EB;
                border-radius: 10px;
                background-color: #F9FAFB;
                color: #111827;
            }
            QLineEdit:focus {
                border: 2px solid #6366F1;
                background-color: #FFFFFF;
            }
        """)
        email_field_layout.addWidget(self.email_edit)
        
        info_layout.addLayout(email_field_layout)
        
        # Bio field
        bio_field_layout = QVBoxLayout()
        bio_field_layout.setSpacing(8)
        
        bio_field_label = QLabel("Bio")
        bio_field_label.setFont(QFont("SF Pro Text", 13, QFont.Medium))
        bio_field_label.setStyleSheet("color: #111827; background: transparent;")
        bio_field_layout.addWidget(bio_field_label)
        
        self.bio_edit = QTextEdit()
        self.bio_edit.setPlaceholderText("Tell us about yourself...")
        self.bio_edit.setFont(QFont("SF Pro Text", 14))
        self.bio_edit.setFixedHeight(100)
        self.bio_edit.setStyleSheet("""
            QTextEdit {
                padding: 10px 16px;
                border: 2px solid #E5E7EB;
                border-radius: 10px;
                background-color: #F9FAFB;
                color: #111827;
            }
            QTextEdit:focus {
                border: 2px solid #6366F1;
                background-color: #FFFFFF;
            }
        """)
        bio_field_layout.addWidget(self.bio_edit)
        
        info_layout.addLayout(bio_field_layout)
        
        # Save button
        save_btn = QPushButton("💾 Save Changes")
        save_btn.setFont(QFont("SF Pro Text", 14, QFont.Bold))
        save_btn.setFixedHeight(48)
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.setStyleSheet("""
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
        save_btn.clicked.connect(self.save_profile)
        info_layout.addWidget(save_btn)
        
        content_layout.addWidget(info_card)
        
        content_layout.addStretch()
        
        scroll.setWidget(content)
        layout.addWidget(scroll)
    
    def load_profile_data(self):
        """Load profile data from database"""
        # Load profile
        profile = self.profile_service.get_profile()
        
        # Update header name
        self.name_label.setText(profile['name'])
        
        # Update form fields
        self.name_edit.setText(profile['name'])
        self.email_edit.setText(profile['email'])
        self.bio_edit.setText(profile['bio'])
        
        # Load statistics
        self.load_statistics()
    
    def load_statistics(self):
        """Load profile statistics"""
        # Clear stats
        while self.stats_layout.count():
            item = self.stats_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        habits = self.habit_service.get_all_habits()
        
        # Total habits
        total_card = StatCard("🎯", str(len(habits)), "Total Habits", "#6366F1")
        self.stats_layout.addWidget(total_card)
        
        # Total completions
        total_completions = 0
        for habit in habits:
            completions = self.habit_service.get_habit_completions(habit.id)
            total_completions += len(completions)
        
        completions_card = StatCard("✅", str(total_completions), "Total Completions", "#10B981")
        self.stats_layout.addWidget(completions_card)
        
        # Best streak
        max_streak = 0
        for habit in habits:
            streak_info = self.streak_service.get_streak_info(habit.id)
            max_streak = max(max_streak, streak_info['current_streak'])
        
        streak_card = StatCard("🔥", str(max_streak), "Best Streak", "#F59E0B")
        self.stats_layout.addWidget(streak_card)
        
        # Completion rate
        if habits:
            completed_today = sum(1 for h in habits if self.habit_service.is_habit_completed_today(h.id))
            rate = int((completed_today / len(habits)) * 100)
            rate_card = StatCard("📊", f"{rate}%", "Today's Rate", "#8B5CF6")
            self.stats_layout.addWidget(rate_card)
        
        self.stats_layout.addStretch()
    
    def save_profile(self):
        """Save profile changes to database"""
        name = self.name_edit.text().strip()
        email = self.email_edit.text().strip()
        bio = self.bio_edit.toPlainText().strip()
        
        if not name:
            QMessageBox.warning(self, "Error", "Name cannot be empty!")
            return
        
        try:
            # Save to database
            self.profile_service.update_profile(
                name=name,
                email=email,
                bio=bio
            )
            
            # Update header name
            self.name_label.setText(name)
            
            # Update sidebar name (if main window has sidebar)
            if self.main_window and hasattr(self.main_window, 'sidebar'):
                self.main_window.sidebar.update_profile_name(name)
            
            # Show success message
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Profile Updated")
            msg.setText("✅ Profile updated successfully!")
            msg.setInformativeText(f"Name: {name}\nEmail: {email}")
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #FFFFFF;
                }
                QMessageBox QLabel {
                    color: #111827;
                }
                QPushButton {
                    background-color: #6366F1;
                    color: #FFFFFF;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 20px;
                    font-weight: bold;
                    min-width: 80px;
                }
            """)
            msg.exec()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save profile: {str(e)}")
