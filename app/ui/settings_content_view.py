"""
Settings Content View - Shows in main content area (not dialog)
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QScrollArea, QFrame, QCheckBox,
    QComboBox, QSpinBox, QTimeEdit, QMessageBox
)
from PySide6.QtCore import Qt, QTime
from PySide6.QtGui import QFont, QCursor
from app.services.settings_service import get_settings_service
from app.utils.constants import THEME_DARK, THEME_LIGHT


class SettingCard(QFrame):
    """Single setting card"""
    
    def __init__(self, icon, title, description, widget, parent=None):
        super().__init__(parent)
        self.setup_ui(icon, title, description, widget)
    
    def setup_ui(self, icon, title, description, widget):
        """Setup setting card UI"""
        self.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
            }
        """)
        self.setFixedHeight(100)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 16, 24, 16)
        layout.setSpacing(16)
        
        # Icon
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("SF Pro Display", 32))
        icon_label.setStyleSheet("background: transparent;")
        icon_label.setFixedSize(50, 50)
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)
        
        # Text info
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("SF Pro Text", 15, QFont.Bold))
        title_label.setStyleSheet("color: #111827; background: transparent;")
        text_layout.addWidget(title_label)
        
        desc_label = QLabel(description)
        desc_label.setFont(QFont("SF Pro Text", 12))
        desc_label.setStyleSheet("color: #6B7280; background: transparent;")
        desc_label.setWordWrap(True)
        text_layout.addWidget(desc_label)
        
        layout.addLayout(text_layout, stretch=1)
        
        # Control widget
        widget.setStyleSheet("""
            QCheckBox {
                color: #111827;
                font-size: 13px;
            }
            QCheckBox::indicator {
                width: 24px;
                height: 24px;
                border-radius: 6px;
                border: 2px solid #E5E7EB;
            }
            QCheckBox::indicator:checked {
                background-color: #6366F1;
                border: 2px solid #6366F1;
            }
            QComboBox {
                padding: 8px 16px;
                border: 2px solid #E5E7EB;
                border-radius: 8px;
                background-color: #F9FAFB;
                color: #111827;
                min-width: 150px;
            }
            QComboBox:hover { border: 2px solid #6366F1; }
            QTimeEdit {
                padding: 8px 16px;
                border: 2px solid #E5E7EB;
                border-radius: 8px;
                background-color: #F9FAFB;
                color: #111827;
                min-width: 120px;
            }
            QTimeEdit:hover { border: 2px solid #6366F1; }
        """)
        layout.addWidget(widget)


class SettingsContentView(QWidget):
    """Settings view for content area"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.settings_service = get_settings_service()
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        """Setup settings UI"""
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
        
        title = QLabel("⚙️ Settings")
        title.setFont(QFont("SF Pro Display", 24, QFont.Bold))
        title.setStyleSheet("color: #111827; background: transparent;")
        title_layout.addWidget(title)
        
        subtitle = QLabel("Customize your habit tracking experience")
        subtitle.setFont(QFont("SF Pro Text", 13))
        subtitle.setStyleSheet("color: #6B7280; background: transparent;")
        title_layout.addWidget(subtitle)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        # Save button
        save_btn = QPushButton("💾 Save Changes")
        save_btn.setFont(QFont("SF Pro Text", 13, QFont.Bold))
        save_btn.setFixedHeight(48)
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.setStyleSheet("""
            QPushButton {
                padding: 12px 24px;
                border: none;
                border-radius: 10px;
                color: #FFFFFF;
                background-color: #10B981;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        save_btn.clicked.connect(self.save_settings)
        header_layout.addWidget(save_btn)
        
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
        content_layout.setSpacing(20)
        
        # Appearance Section
        appearance_label = QLabel("🎨 Appearance")
        appearance_label.setFont(QFont("SF Pro Display", 18, QFont.Bold))
        appearance_label.setStyleSheet("color: #111827; background: transparent;")
        content_layout.addWidget(appearance_label)
        
        # Theme setting
        self.theme_combo = QComboBox()
        self.theme_combo.addItem("🌙 Dark Theme", THEME_DARK)
        self.theme_combo.addItem("☀️ Light Theme", THEME_LIGHT)
        self.theme_combo.setCursor(Qt.PointingHandCursor)
        
        theme_card = SettingCard(
            "🎨",
            "Theme",
            "Choose your preferred color theme",
            self.theme_combo
        )
        content_layout.addWidget(theme_card)
        
        # Compact mode
        self.compact_check = QCheckBox("Enable")
        self.compact_check.setCursor(Qt.PointingHandCursor)
        
        compact_card = SettingCard(
            "📱",
            "Compact Mode",
            "Show more content with reduced spacing",
            self.compact_check
        )
        content_layout.addWidget(compact_card)
        
        content_layout.addSpacing(16)
        
        # Notifications Section
        notifications_label = QLabel("🔔 Notifications")
        notifications_label.setFont(QFont("SF Pro Display", 18, QFont.Bold))
        notifications_label.setStyleSheet("color: #111827; background: transparent;")
        content_layout.addWidget(notifications_label)
        
        # Enable notifications
        self.notifications_check = QCheckBox("Enable")
        self.notifications_check.setCursor(Qt.PointingHandCursor)
        
        notif_card = SettingCard(
            "🔔",
            "Daily Reminders",
            "Receive daily reminders to complete your habits",
            self.notifications_check
        )
        content_layout.addWidget(notif_card)
        
        # Notification time
        self.notification_time = QTimeEdit()
        self.notification_time.setDisplayFormat("hh:mm AP")
        self.notification_time.setCursor(Qt.PointingHandCursor)
        
        time_card = SettingCard(
            "⏰",
            "Reminder Time",
            "Set the time for daily habit reminders",
            self.notification_time
        )
        content_layout.addWidget(time_card)
        
        content_layout.addSpacing(16)
        
        # Display Section
        display_label = QLabel("👁️ Display")
        display_label.setFont(QFont("SF Pro Display", 18, QFont.Bold))
        display_label.setStyleSheet("color: #111827; background: transparent;")
        content_layout.addWidget(display_label)
        
        # Show completed habits
        self.show_completed_check = QCheckBox("Enable")
        self.show_completed_check.setCursor(Qt.PointingHandCursor)
        
        completed_card = SettingCard(
            "✅",
            "Show Completed Habits",
            "Display habits that are already completed today",
            self.show_completed_check
        )
        content_layout.addWidget(completed_card)
        
        content_layout.addStretch()
        
        # Info section
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background-color: #EFF6FF;
                border-left: 4px solid #3B82F6;
                border-radius: 8px;
            }
        """)
        
        info_layout = QHBoxLayout(info_frame)
        info_layout.setContentsMargins(16, 12, 16, 12)
        
        info_icon = QLabel("ℹ️")
        info_icon.setFont(QFont("SF Pro Display", 20))
        info_icon.setStyleSheet("background: transparent;")
        info_layout.addWidget(info_icon)
        
        info_text = QLabel("Changes will take effect after clicking 'Save Changes'")
        info_text.setFont(QFont("SF Pro Text", 12))
        info_text.setStyleSheet("color: #1E40AF; background: transparent;")
        info_layout.addWidget(info_text, stretch=1)
        
        content_layout.addWidget(info_frame)
        
        scroll.setWidget(content)
        layout.addWidget(scroll)
    
    def load_settings(self):
        """Load current settings"""
        # Theme
        current_theme = self.settings_service.get_theme()
        index = self.theme_combo.findData(current_theme)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)
        
        # Compact mode
        self.compact_check.setChecked(self.settings_service.get_compact_mode())
        
        # Notifications
        self.notifications_check.setChecked(self.settings_service.is_notifications_enabled())
        
        # Notification time
        time_str = self.settings_service.get_notification_time()
        try:
            hour, minute = map(int, time_str.split(':'))
            self.notification_time.setTime(QTime(hour, minute))
        except:
            self.notification_time.setTime(QTime(9, 0))
        
        # Show completed
        self.show_completed_check.setChecked(self.settings_service.get_show_completed())
    
    def save_settings(self):
        """Save all settings"""
        try:
            # Save theme
            theme = self.theme_combo.currentData()
            self.settings_service.set_theme(theme)
            
            # Save compact mode
            self.settings_service.set_compact_mode(self.compact_check.isChecked())
            
            # Save notifications
            self.settings_service.set_notifications_enabled(self.notifications_check.isChecked())
            
            # Save notification time
            time = self.notification_time.time()
            time_str = time.toString("HH:mm")
            self.settings_service.set_notification_time(time_str)
            
            # Save show completed
            self.settings_service.set_show_completed(self.show_completed_check.isChecked())
            
            # Success message
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Settings Saved")
            msg.setText("✅ Settings saved successfully!")
            msg.setInformativeText("Some changes may require restarting the app.")
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
            # Error message
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to save settings: {str(e)}")
            msg.exec()
