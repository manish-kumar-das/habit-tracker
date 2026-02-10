"""
Settings dialog with theme switcher - FIXED
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QCheckBox, QComboBox, QTimeEdit, QFrame, QMessageBox
)
from PySide6.QtCore import Qt, QTime
from PySide6.QtGui import QFont
from app.services.settings_service import get_settings_service
from app.utils.constants import THEME_DARK, THEME_LIGHT


class SettingItem(QFrame):
    """Single setting item"""
    
    def __init__(self, title, description, widget, parent=None):
        super().__init__(parent)
        self.setup_ui(title, description, widget)
    
    def setup_ui(self, title, description, widget):
        """Setup the setting item UI"""
        self.setFrameShape(QFrame.NoFrame)
        self.setStyleSheet("""
            SettingItem {
                background-color: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: 10px;
                padding: 0px;
            }
        """)
        self.setMinimumHeight(80)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(16)
        
        # Text info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Inter", 14, QFont.Medium))
        title_label.setStyleSheet("color: #E4E6EB; background: transparent;")
        info_layout.addWidget(title_label)
        
        desc_label = QLabel(description)
        desc_label.setFont(QFont("Inter", 12))
        desc_label.setStyleSheet("color: #9AA0A6; background: transparent;")
        desc_label.setWordWrap(True)
        info_layout.addWidget(desc_label)
        
        layout.addLayout(info_layout, stretch=1)
        
        # Control widget
        layout.addWidget(widget)


class SettingsDialog(QDialog):
    """Settings dialog"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.settings_service = get_settings_service()
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        """Setup the dialog UI"""
        self.setWindowTitle("Settings")
        self.setModal(True)
        self.setMinimumSize(600, 500)
        self.setStyleSheet("""
            QDialog {
                background-color: #1C1F26;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("⚙️ Settings")
        title.setFont(QFont("Inter", 28, QFont.Bold))
        title.setStyleSheet("color: #E4E6EB; background: transparent;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
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
        
        # Section: Appearance
        section_label = QLabel("Appearance")
        section_label.setFont(QFont("Inter", 18, QFont.Bold))
        section_label.setStyleSheet("color: #4FD1C5; background: transparent; margin-top: 8px;")
        layout.addWidget(section_label)
        
        # Theme selector
        self.theme_combo = QComboBox()
        self.theme_combo.addItem("🌙 Dark Mode", THEME_DARK)
        self.theme_combo.addItem("☀️ Light Mode", THEME_LIGHT)
        self.theme_combo.setFont(QFont("Inter", 13))
        self.theme_combo.setFixedHeight(44)
        self.theme_combo.setFixedWidth(200)
        self.theme_combo.setCursor(Qt.PointingHandCursor)
        self.theme_combo.setStyleSheet("""
            QComboBox {
                padding: 10px 16px;
                border: 2px solid #2A2D35;
                border-radius: 10px;
                background-color: #20232B;
                color: #E4E6EB;
            }
            QComboBox:hover {
                border: 2px solid #4FD1C5;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 12px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #9AA0A6;
                margin-right: 8px;
            }
            QComboBox QAbstractItemView {
                background-color: #20232B;
                border: 1px solid #2A2D35;
                border-radius: 8px;
                padding: 4px;
                color: #E4E6EB;
                selection-background-color: #4FD1C5;
                selection-color: #0F1115;
            }
        """)
        self.theme_combo.currentIndexChanged.connect(self.on_theme_changed)
        
        theme_item = SettingItem(
            "Color Theme",
            "Choose between dark and light mode",
            self.theme_combo
        )
        layout.addWidget(theme_item)
        
        # Section: Notifications
        section_label2 = QLabel("Notifications")
        section_label2.setFont(QFont("Inter", 18, QFont.Bold))
        section_label2.setStyleSheet("color: #4FD1C5; background: transparent; margin-top: 16px;")
        layout.addWidget(section_label2)
        
        # Enable notifications
        self.notifications_checkbox = QCheckBox()
        self.notifications_checkbox.setCursor(Qt.PointingHandCursor)
        self.notifications_checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 24px;
                height: 24px;
                border-radius: 6px;
                border: 2px solid #4A4D56;
                background-color: #20232B;
            }
            QCheckBox::indicator:hover {
                border: 2px solid #4FD1C5;
            }
            QCheckBox::indicator:checked {
                background-color: #4FD1C5;
                border: 2px solid #4FD1C5;
            }
        """)
        # DON'T connect stateChanged here - we'll save on button click
        
        notif_item = SettingItem(
            "Daily Reminders",
            "Get notified about incomplete habits",
            self.notifications_checkbox
        )
        layout.addWidget(notif_item)
        
        # Notification time
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setFixedHeight(44)
        self.time_edit.setFixedWidth(120)
        self.time_edit.setCursor(Qt.PointingHandCursor)
        self.time_edit.setStyleSheet("""
            QTimeEdit {
                padding: 10px 16px;
                border: 2px solid #2A2D35;
                border-radius: 10px;
                background-color: #20232B;
                color: #E4E6EB;
                font-size: 14px;
            }
            QTimeEdit:hover {
                border: 2px solid #4FD1C5;
            }
            QTimeEdit::up-button, QTimeEdit::down-button {
                background-color: #2A2D35;
                border-radius: 4px;
                width: 16px;
            }
            QTimeEdit::up-button:hover, QTimeEdit::down-button:hover {
                background-color: #4FD1C5;
            }
        """)
        
        time_item = SettingItem(
            "Notification Time",
            "When to send daily reminder",
            self.time_edit
        )
        layout.addWidget(time_item)
        
        layout.addStretch()
        
        # Save button
        save_btn = QPushButton("💾 Save Settings")
        save_btn.setFont(QFont("Inter", 14, QFont.Bold))
        save_btn.setFixedHeight(52)
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.setStyleSheet("""
            QPushButton {
                padding: 12px 32px;
                border: none;
                border-radius: 10px;
                color: #FFFFFF;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4FD1C5, stop:1 #7C83FD);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #45B8AD, stop:1 #6B6FE5);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3A9D93, stop:1 #5A5ECD);
            }
        """)
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)
    
    def load_settings(self):
        """Load current settings"""
        # Theme
        current_theme = self.settings_service.get_theme()
        if current_theme == THEME_LIGHT:
            self.theme_combo.setCurrentIndex(1)
        else:
            self.theme_combo.setCurrentIndex(0)
        
        # Notifications
        notif_enabled = self.settings_service.is_notifications_enabled()
        self.notifications_checkbox.setChecked(notif_enabled)
        
        # Time
        time_str = self.settings_service.get_notification_time()
        hour, minute = map(int, time_str.split(':'))
        self.time_edit.setTime(QTime(hour, minute))
    
    def on_theme_changed(self, index):
        """Handle theme change"""
        theme = self.theme_combo.currentData()
        self.settings_service.set_theme(theme)
        
        # Apply theme immediately
        if self.main_window:
            self.main_window.apply_theme(theme)
    
    def save_settings(self):
        """Save all settings"""
        # Save notifications
        enabled = self.notifications_checkbox.isChecked()
        self.settings_service.set_notifications_enabled(enabled)
        
        # Save notification time
        time = self.time_edit.time()
        time_str = time.toString("HH:mm")
        self.settings_service.set_notification_time(time_str)
        
        # Show success message
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Settings Saved")
        msg.setText("✓ Settings saved successfully!")
        msg.setInformativeText(f"Notifications: {'Enabled' if enabled else 'Disabled'}\nReminder time: {time_str}")
        msg.setStyleSheet("""
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
        msg.exec()
        
        # Reload settings to confirm
        self.load_settings()
