"""
Premium Sidebar Component
"""

from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QProgressBar, QWidget
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QCursor
from datetime import datetime


class PremiumSidebar(QFrame):
    """Premium sidebar with gradient background and live stats"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.setup_ui()
        self.load_profile_name()
    
    def setup_ui(self):
        """Setup premium sidebar UI"""
        self.setFixedWidth(280)
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:0.5 #764ba2, stop:1 #f093fb);
                border: none;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 12, 8, 12)
        layout.setSpacing(8)

        # ============ LOGO & BRANDING ============
        logo_container = QWidget()
        logo_container.setStyleSheet("background: transparent;")
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_layout.setSpacing(8)
        
        # Logo with icon
        logo_header = QHBoxLayout()
        logo_header.setSpacing(14)
        
        logo_icon = QFrame()
        logo_icon.setFixedSize(52, 52)
        logo_icon.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 0.3),
                    stop:1 rgba(255, 255, 255, 0.1));
                border: 2px solid rgba(255, 255, 255, 0.4);
                border-radius: 16px;
            }
        """)
        
        logo_icon_layout = QVBoxLayout(logo_icon)
        logo_icon_layout.setContentsMargins(0, 0, 0, 0)
        
        icon_label = QLabel("⚡")
        icon_label.setFont(QFont("SF Pro Display", 30))
        icon_label.setStyleSheet("color: #FFFFFF; background: transparent; border: none;")
        icon_label.setAlignment(Qt.AlignCenter)
        logo_icon_layout.addWidget(icon_label)
        
        logo_header.addWidget(logo_icon)
        
        # Logo text
        logo_text_layout = QVBoxLayout()
        logo_text_layout.setSpacing(2)
        
        title = QLabel("HabitHub")
        title.setFont(QFont("SF Pro Display", 26, QFont.Bold))
        title.setStyleSheet("color: #FFFFFF; background: transparent;")
        logo_text_layout.addWidget(title)
        
        tagline = QLabel("Build Your Best Self")
        tagline.setFont(QFont("SF Pro Text", 12))
        tagline.setStyleSheet("color: rgba(255, 255, 255, 0.85); background: transparent;")
        logo_text_layout.addWidget(tagline)
        
        logo_header.addLayout(logo_text_layout)
        logo_header.addStretch()
        
        logo_layout.addLayout(logo_header)
        
        layout.addWidget(logo_container)
        layout.addSpacing(20)
        
        # ============ NAVIGATION MENU ============
        nav_label = QLabel("NAVIGATION")
        nav_label.setFont(QFont("SF Pro Text", 11, QFont.Bold))
        nav_label.setStyleSheet("color: rgba(255, 255, 255, 0.7); background: transparent; padding-left: 8px;")
        layout.addWidget(nav_label)
        
        # layout.addSpacing(2)
        
        self.nav_buttons = {}
        nav_items = [
            ("dashboard", "Dashboard", "🏠"),
            ("goals", "Goals", "🎯"),
            ("analytics", "Analytics", "📊"),
            ("settings", "Settings", "⚙️"),
        ]
        
        for key, text, icon in nav_items:
            btn = QPushButton(f"{icon}  {text}")
            btn.setFont(QFont("SF Pro Text", 15, QFont.Medium))
            btn.setFixedHeight(54)
            btn.setCursor(Qt.PointingHandCursor)
            
            if key == "dashboard":
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: rgba(255, 255, 255, 0.3);
                        color: #FFFFFF;
                        border: 2px solid rgba(255, 255, 255, 0.4);
                        border-radius: 14px;
                        text-align: left;
                        padding-left: 20px;
                        font-weight: 700;
                    }
                    QPushButton:hover {
                        background-color: rgba(255, 255, 255, 0.4);
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        color: rgba(255, 255, 255, 0.9);
                        border: 2px solid transparent;
                        border-radius: 14px;
                        text-align: left;
                        padding-left: 20px;
                    }
                    QPushButton:hover {
                        background-color: rgba(255, 255, 255, 0.15);
                        border: 2px solid rgba(255, 255, 255, 0.2);
                        color: #FFFFFF;
                    }
                """)
            
            btn.clicked.connect(lambda checked, k=key: self.on_nav_clicked(k))
            self.nav_buttons[key] = btn
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # ============ PROFILE SECTION ============
        profile_container = QPushButton()
        profile_container.setCursor(Qt.PointingHandCursor)
        profile_container.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.2),
                    stop:1 rgba(255, 255, 255, 0.1));
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 16px;
                padding: 4px;
                text-align: left;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.3),
                    stop:1 rgba(255, 255, 255, 0.2));
                border: 2px solid rgba(255, 255, 255, 0.5);
            }
        """)
        profile_container.setFixedHeight(76)
        profile_container.clicked.connect(self.on_profile_clicked)
        
        profile_layout = QHBoxLayout(profile_container)
        profile_layout.setContentsMargins(14, 12, 14, 12)
        profile_layout.setSpacing(14)
        
        # Avatar
        avatar = QFrame()
        avatar.setFixedSize(48, 48)
        avatar.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #F59E0B, stop:1 #EF4444);
                border: 3px solid rgba(255, 255, 255, 0.4);
                border-radius: 24px;
            }
        """)
        
        avatar_layout = QVBoxLayout(avatar)
        avatar_layout.setContentsMargins(0, 0, 0, 0)
        
        avatar_text = QLabel("👤")
        avatar_text.setFont(QFont("SF Pro Display", 24))
        avatar_text.setAlignment(Qt.AlignCenter)
        avatar_text.setStyleSheet("background: transparent; border: none;")
        avatar_layout.addWidget(avatar_text)
        
        profile_layout.addWidget(avatar)
        
        # User info
        user_info_layout = QVBoxLayout()
        user_info_layout.setSpacing(4)
        
        self.profile_name_label = QLabel("Alex Morgan")
        self.profile_name_label.setFont(QFont("SF Pro Text", 15, QFont.Bold))
        self.profile_name_label.setStyleSheet("color: #FFFFFF; background: transparent;")
        user_info_layout.addWidget(self.profile_name_label)
        
        user_type = QLabel("Premium • View Profile")
        user_type.setFont(QFont("SF Pro Text", 11))
        user_type.setStyleSheet("color: rgba(255, 255, 255, 0.8); background: transparent;")
        user_info_layout.addWidget(user_type)
        
        profile_layout.addLayout(user_info_layout)
        
        # Arrow icon
        arrow = QLabel("›")
        arrow.setFont(QFont("SF Pro Display", 24, QFont.Bold))
        arrow.setStyleSheet("color: rgba(255, 255, 255, 0.6); background: transparent;")
        profile_layout.addWidget(arrow)
        
        layout.addWidget(profile_container)
    
    def update_sidebar_stats(self, completed, total):
        """Update sidebar progress statistics"""
        percentage = int((completed / total) * 100) if total > 0 else 0
        self.sidebar_progress.setValue(percentage)
        self.sidebar_stats_text.setText(f"{completed}/{total}")
        self.sidebar_percentage.setText(f"{percentage}%")
    
    def update_streak(self, days):
        """Update streak display"""
        self.streak_number.setText(f"{days} Days" if days != 1 else "1 Day")
    
    def on_nav_clicked(self, key):
        """Handle navigation clicks"""
        self.update_active_button(key)
        if not self.main_window:
            return
        
        if key == 'dashboard':
            self.main_window.show_dashboard()
        elif key == 'today':
            self.main_window.show_today_view()
        elif key == 'habits':
            self.main_window.show_habits_view()
        elif key == 'analytics':
            self.main_window.show_analytics()
        elif key == 'goals':
            self.main_window.show_goals()
        elif key == 'settings':
            self.main_window.show_settings()
    
    def update_active_button(self, active_key):
        """Update button styles to show active state"""
        active_style = """
            QPushButton {
                background-color: rgba(255, 255, 255, 0.3);
                color: #FFFFFF;
                border: 2px solid rgba(255, 255, 255, 0.4);
                border-radius: 14px;
                text-align: left;
                padding-left: 20px;
                font-weight: 700;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.4);
            }
        """
        
        inactive_style = """
            QPushButton {
                background-color: transparent;
                color: rgba(255, 255, 255, 0.9);
                border: 2px solid transparent;
                border-radius: 14px;
                text-align: left;
                padding-left: 20px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.15);
                border: 2px solid rgba(255, 255, 255, 0.2);
                color: #FFFFFF;
            }
        """
        
        for key, btn in self.nav_buttons.items():
            btn.setStyleSheet(active_style if key == active_key else inactive_style)
    
    def on_profile_clicked(self):
        """Handle profile click"""
        if self.main_window:
            self.main_window.show_profile()
    
    def update_profile_name(self, name):
        """Update profile name display"""
        if hasattr(self, 'profile_name_label'):
            self.profile_name_label.setText(name)
    
    def load_profile_name(self):
        """Load profile name from database"""
        try:
            from app.services.profile_service import get_profile_service
            profile_service = get_profile_service()
            profile = profile_service.get_profile()
            self.profile_name_label.setText(profile['name'])
        except:
            pass
