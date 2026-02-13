"""
Achievements & Badges view - Display unlocked achievements
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QScrollArea, QFrame, QWidget, QProgressBar
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QFont, QCursor
from app.services.achievement_service import get_achievement_service


class AchievementCard(QFrame):
    """Single achievement card"""
    
    def __init__(self, achievement, parent=None):
        super().__init__(parent)
        self.achievement = achievement
        self.setup_ui()
    
    def setup_ui(self):
        """Setup achievement card UI"""
        self.setFrameShape(QFrame.StyledPanel)
        
        # Rarity colors
        rarity_colors = {
            'common': '#9CA3AF',
            'rare': '#3B82F6',
            'epic': '#A855F7',
            'legendary': '#F59E0B'
        }
        
        rarity_bg = {
            'common': '#F3F4F6',
            'rare': '#DBEAFE',
            'epic': '#F3E8FF',
            'legendary': '#FEF3C7'
        }
        
        border_color = rarity_colors.get(self.achievement.rarity, '#9CA3AF')
        bg_color = rarity_bg.get(self.achievement.rarity, '#F3F4F6')
        
        # Dim if locked
        if not self.achievement.is_unlocked:
            bg_color = '#F9FAFB'
            border_color = '#E5E7EB'
        
        self.setStyleSheet(f"""
            AchievementCard {{
                background-color: {bg_color};
                border: 2px solid {border_color};
                border-radius: 16px;
            }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(16)
        
        # Icon
        icon_label = QLabel(self.achievement.icon)
        icon_label.setFont(QFont("Inter", 48))
        icon_label.setStyleSheet("background: transparent;")
        icon_label.setFixedSize(80, 80)
        icon_label.setAlignment(Qt.AlignCenter)
        
        # Gray out if locked
        if not self.achievement.is_unlocked:
            icon_label.setStyleSheet("background: transparent; opacity: 0.3;")
        
        layout.addWidget(icon_label)
        
        # Info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(6)
        
        # Name
        name_label = QLabel(self.achievement.name)
        name_label.setFont(QFont("Inter", 16, QFont.Bold))
        name_label.setStyleSheet(f"color: {'#111827' if self.achievement.is_unlocked else '#9CA3AF'}; background: transparent;")
        info_layout.addWidget(name_label)
        
        # Description
        desc_label = QLabel(self.achievement.description)
        desc_label.setFont(QFont("Inter", 12))
        desc_label.setStyleSheet(f"color: {'#6B7280' if self.achievement.is_unlocked else '#D1D5DB'}; background: transparent;")
        desc_label.setWordWrap(True)
        info_layout.addWidget(desc_label)
        
        # Unlocked date
        if self.achievement.is_unlocked and self.achievement.unlocked_date:
            date_label = QLabel(f"✓ Unlocked: {self.achievement.unlocked_date}")
            date_label.setFont(QFont("Inter", 10, QFont.Medium))
            date_label.setStyleSheet("color: #059669; background: transparent;")
            info_layout.addWidget(date_label)
        else:
            locked_label = QLabel("🔒 Locked")
            locked_label.setFont(QFont("Inter", 10, QFont.Medium))
            locked_label.setStyleSheet("color: #9CA3AF; background: transparent;")
            info_layout.addWidget(locked_label)
        
        layout.addLayout(info_layout, stretch=1)
        
        # Rarity badge
        rarity_badge = QLabel(self.achievement.rarity.upper())
        rarity_badge.setFont(QFont("Inter", 10, QFont.Bold))
        rarity_badge.setStyleSheet(f"""
            QLabel {{
                color: {border_color};
                background-color: {bg_color};
                border: 2px solid {border_color};
                padding: 6px 12px;
                border-radius: 8px;
            }}
        """)
        rarity_badge.setFixedHeight(32)
        rarity_badge.setAlignment(Qt.AlignCenter)
        layout.addWidget(rarity_badge)


class AchievementsView(QDialog):
    """Achievements & Badges view"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.achievement_service = get_achievement_service()
        self.setup_ui()
        self.load_achievements()
    
    def setup_ui(self):
        """Setup UI"""
        self.setWindowTitle("Achievements & Badges")
        self.setModal(False)
        self.setMinimumSize(900, 700)
        self.setStyleSheet("QDialog { background-color: #F9FAFB; }")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = QFrame()
        header.setFixedHeight(140)
        header.setFrameShape(QFrame.StyledPanel)
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6366F1, stop:1 #8B5CF6);
            }
        """)
        
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(32, 20, 32, 20)
        header_layout.setSpacing(12)
        
        # Title row
        title_row = QHBoxLayout()
        
        title_col = QVBoxLayout()
        title_col.setSpacing(4)
        
        title = QLabel("🏆 Achievements & Badges")
        title.setFont(QFont("Inter", 24, QFont.Bold))
        title.setStyleSheet("color: #FFFFFF; background: transparent;")
        title_col.addWidget(title)
        
        subtitle = QLabel("Track your progress and unlock badges")
        subtitle.setFont(QFont("Inter", 13))
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.9); background: transparent;")
        title_col.addWidget(subtitle)
        
        title_row.addLayout(title_col)
        title_row.addStretch()
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Check Progress")
        refresh_btn.setFont(QFont("Inter", 13, QFont.Bold))
        refresh_btn.setFixedHeight(48)
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.setStyleSheet("""
            QPushButton {
                padding: 12px 24px;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                color: #FFFFFF;
                background-color: rgba(255, 255, 255, 0.1);
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
                border: 2px solid rgba(255, 255, 255, 0.5);
            }
        """)
        refresh_btn.clicked.connect(self.check_achievements)
        title_row.addWidget(refresh_btn)
        
        # Close button
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(48, 48)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setFont(QFont("Inter", 18))
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 24px;
                color: #FFFFFF;
            }
            QPushButton:hover {
                background-color: rgba(239, 68, 68, 0.3);
                border: 2px solid #EF4444;
            }
        """)
        close_btn.clicked.connect(self.close)
        title_row.addWidget(close_btn)
        
        header_layout.addLayout(title_row)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("0/0 Unlocked (0%)")
        self.progress_bar.setFixedHeight(32)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                background-color: rgba(255, 255, 255, 0.1);
                text-align: center;
                color: #FFFFFF;
                font-size: 13px;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 8px;
            }
        """)
        header_layout.addWidget(self.progress_bar)
        
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
    
    def load_achievements(self):
        """Load and display achievements"""
        # Clear existing
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Get achievements
        achievements = self.achievement_service.get_all_achievements()
        
        # Update progress bar
        stats = self.achievement_service.get_achievement_stats()
        self.progress_bar.setValue(stats['percentage'])
        self.progress_bar.setFormat(f"{stats['unlocked']}/{stats['total']} Unlocked ({stats['percentage']}%)")
        
        # Group by category
        categories = {}
        for achievement in achievements:
            if achievement.category not in categories:
                categories[achievement.category] = []
            categories[achievement.category].append(achievement)
        
        # Category names and icons
        category_info = {
            'streak': ('🔥 Streak Achievements', '#F59E0B'),
            'completion': ('✅ Completion Achievements', '#10B981'),
            'consistency': ('📊 Consistency Achievements', '#6366F1'),
            'special': ('⭐ Special Achievements', '#8B5CF6')
        }
        
        # Display by category
        for category_key in ['streak', 'completion', 'consistency', 'special']:
            if category_key in categories:
                category_name, category_color = category_info[category_key]
                
                # Category header
                header_label = QLabel(category_name)
                header_label.setFont(QFont("Inter", 18, QFont.Bold))
                header_label.setStyleSheet(f"color: {category_color}; background: transparent; margin-top: 8px;")
                self.content_layout.addWidget(header_label)
                
                # Achievement cards
                for achievement in categories[category_key]:
                    card = AchievementCard(achievement)
                    self.content_layout.addWidget(card)
        
        self.content_layout.addStretch()
    
    def check_achievements(self):
        """Check for new achievements"""
        newly_unlocked = self.achievement_service.check_and_unlock_achievements()
        
        if newly_unlocked:
            from PySide6.QtWidgets import QMessageBox
            
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("🎉 New Achievements!")
            msg.setText(f"Congratulations! You unlocked {len(newly_unlocked)} new achievement(s)!")
            msg.setInformativeText("\n".join([f"🏆 {name}" for name in newly_unlocked]))
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
        else:
            from PySide6.QtWidgets import QMessageBox
            
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Keep Going!")
            msg.setText("No new achievements yet.")
            msg.setInformativeText("Keep building your habits to unlock more badges!")
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #FFFFFF;
                }
                QMessageBox QLabel {
                    color: #111827;
                }
            """)
            msg.exec()
        
        # Reload
        self.load_achievements()
