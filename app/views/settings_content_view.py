"""
Settings Content View - Premium Redesign
Beautiful settings interface with card-based design
"""
import logging
logger = logging.getLogger(__name__)


from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QFrame,
    QCheckBox,
    QTimeEdit,
    QFileDialog,
    QMessageBox,
    QGraphicsDropShadowEffect,
)
from PySide6.QtCore import Qt, QTime, QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QFont, QColor, QPainter, QLinearGradient
from datetime import datetime
from app.services.settings_service import get_settings_service


class SettingCard(QFrame):
    """Premium setting card with hover effect"""

    def __init__(self, icon, title, description, widget, parent=None):
        super().__init__(parent)
        self.setup_ui(icon, title, description, widget)

        # No longer using pos animation as it interferes with layouts and clicks
        pass

    def setup_ui(self, icon, title, description, widget):
        """Setup setting card UI"""
        self.setMinimumHeight(100)
        self.setObjectName("SettingCard")
        from app.themes import get_theme_manager
        is_dark = get_theme_manager().is_dark_mode()
        bg_card = "#252732" if is_dark else "#FFFFFF"
        border_card = "1px solid #333645" if is_dark else "1px solid rgba(0, 0, 0, 0.05)"
        bg_hover = "#2C2F3A" if is_dark else "#FDFDFF"
        
        self.setStyleSheet(f"""
            QFrame#SettingCard {{
                background-color: {bg_card};
                border: {border_card};
                border-radius: 20px;
            }}
            QFrame#SettingCard:hover {{
                background-color: {bg_hover};
                border: 1px solid rgba(102, 126, 234, 0.2);
            }}
            QLabel {{
                border: none;
                background: transparent;
            }}
        """)

        # Premium Shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 25))
        shadow.setOffset(0, 6)
        self.setGraphicsEffect(shadow)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(20)

        # Icon
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("SF Pro Display", 36))
        icon_label.setStyleSheet("background: transparent;")
        icon_label.setFixedSize(60, 60)
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)

        # Text info
        text_layout = QVBoxLayout()
        text_layout.setSpacing(6)

        from app.themes import get_theme_manager
        is_dark = get_theme_manager().is_dark_mode()
        title_color = "#F3F4F6" if is_dark else "#111827"
        desc_color = "#9CA3AF" if is_dark else "#6B7280"

        title_label = QLabel(title)
        title_label.setFont(QFont("SF Pro Display", 17, QFont.Bold))
        title_label.setStyleSheet(f"color: {title_color}; background: transparent;")
        text_layout.addWidget(title_label)

        desc_label = QLabel(description)
        desc_label.setFont(QFont("SF Pro Text", 13))
        desc_label.setStyleSheet(f"color: {desc_color}; background: transparent;")
        desc_label.setWordWrap(True)
        text_layout.addWidget(desc_label)

        layout.addLayout(text_layout, stretch=1)

        # Control widget
        if widget:
            layout.addWidget(widget)

    def enterEvent(self, event):
        super().enterEvent(event)

    def leaveEvent(self, event):
        super().leaveEvent(event)


class ToggleSwitch(QCheckBox):
    """Premium iOS-style toggle switch with animation"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(60, 32)
        self.setCursor(Qt.PointingHandCursor)

        # Check initial state
        self._thumb_pos = 32 if self.isChecked() else 4

        self.anim = QPropertyAnimation(self, b"thumb_pos")
        self.anim.setDuration(200)
        self.anim.setEasingCurve(QEasingCurve.InOutCubic)

        # Ensure the whole widget is clickable by making the indicator cover it
        # but remain invisible (we paint it ourselves in paintEvent)
        self.setStyleSheet("""
            QCheckBox::indicator {
                width: 60px;
                height: 32px;
                background: transparent;
                border: none;
            }
        """)

    def nextCheckState(self):
        super().nextCheckState()
        self.anim.stop()
        self.anim.setEndValue(32 if self.isChecked() else 4)
        self.anim.start()

    @Property(int)
    def thumb_pos(self):
        return self._thumb_pos

    @thumb_pos.setter
    def thumb_pos(self, pos):
        self._thumb_pos = pos
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        # Track
        from app.themes import get_theme_manager
        is_dark = get_theme_manager().is_dark_mode()
        
        if self.isChecked():
            # Saturated purple for dark mode
            primary = "#5C6BC0" if is_dark else "#667eea"
            secondary = "#7986CB" if is_dark else "#764ba2"
            grad = QLinearGradient(0, 0, self.width(), 0)
            grad.setColorAt(0, QColor(primary))
            grad.setColorAt(1, QColor(secondary))
            p.setBrush(grad)
        else:
            track_color = "#333645" if is_dark else "#E5E7EB"
            p.setBrush(QColor(track_color))

        p.setPen(Qt.NoPen)
        p.drawRoundedRect(0, 0, self.width(), self.height(), 16, 16)

        # Thumb
        thumb_color = "#F3F4F6" if is_dark else "white"
        p.setBrush(QColor(thumb_color))
        # Subtle thumb shadow
        p.drawEllipse(self._thumb_pos, 4, 24, 24)


class SettingsContentView(QWidget):
    """Premium Settings View"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.settings_service = get_settings_service()
        from app.themes import get_theme_manager
        self.theme_manager = get_theme_manager()
        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        """Setup settings UI"""
        is_dark = self.theme_manager.is_dark_mode()
        bg_primary = "#1A1C23" if is_dark else "#F9FAFB"
        self.setStyleSheet(f"background-color: {bg_primary};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header_bg = "#1A1C23" if is_dark else "#FFFFFF"
        self.header = QFrame()
        self.header.setMinimumHeight(120)
        self.header.setStyleSheet(f"""
            QFrame {{
                background: {header_bg};
                border: none;
            }}
        """)

        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(40, 24, 40, 24)

        # Left: Title
        title_section = QHBoxLayout()
        title_section.setSpacing(12)

        icon = QLabel("⚙️")
        icon.setFont(QFont("SF Pro Display", 32))
        icon.setStyleSheet("background: transparent;")
        title_section.addWidget(icon)

        title_text_layout = QVBoxLayout()
        title_text_layout.setSpacing(2)

        self.title_label = QLabel("Settings")
        self.title_label.setFont(QFont("SF Pro Display", 28, QFont.Bold))
        text_primary = "#F3F4F6" if is_dark else "#111827"
        self.title_label.setStyleSheet(
            f"color: {text_primary}; background: transparent; padding-bottom: 4px;"
        )
        self.title_label.setWordWrap(True)
        title_text_layout.addWidget(self.title_label)

        self.subtitle_label = QLabel("Customize your habit tracking experience")
        self.subtitle_label.setFont(QFont("SF Pro Text", 14))
        text_secondary = "#9CA3AF" if is_dark else "#6B7280"
        self.subtitle_label.setStyleSheet(
            f"color: {text_secondary}; background: transparent; padding-bottom: 2px;"
        )
        title_text_layout.addWidget(self.subtitle_label)

        title_section.addLayout(title_text_layout)

        header_layout.addLayout(title_section)
        header_layout.addStretch()

        # Right: Save button
        save_btn = QPushButton("💾 Save Changes")
        save_btn.setFont(QFont("SF Pro Text", 15, QFont.Bold))
        save_btn.setFixedHeight(50)
        save_btn.setCursor(Qt.PointingHandCursor)
        # Saturated gradient for dark mode (+10%)
        # Original: #667eea, #764ba2, #f093fb
        # Saturated: #5069f2, #7d44cf, #f682ff
        grad_start = "#5069f2" if is_dark else "#667eea"
        grad_mid = "#7d44cf" if is_dark else "#764ba2"
        grad_end = "#f682ff" if is_dark else "#f093fb"
        
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {grad_start}, stop:0.5 {grad_mid}, stop:1 {grad_end});
                color: #FFFFFF;
                border: none;
                border-radius: 12px;
                padding: 0px 32px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5568d3, stop:0.5 #6a4191, stop:1 #e07af0);
            }}
        """)
        save_btn.clicked.connect(self.save_settings)
        header_layout.addWidget(save_btn)

        layout.addWidget(self.header)

        # Content scroll
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
            QScrollBar:vertical {{
                background: {"#1A1C23" if is_dark else "#F3F4F6"};
                width: 10px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical {{
                background: #6366F1;
                border-radius: 5px;
            }}
        """)

        self.content = QWidget()
        content_bg = "#1A1C23" if is_dark else "#F9FAFB"
        self.content.setStyleSheet(f"background-color: {content_bg};")
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(40, 28, 40, 28)
        self.content_layout.setSpacing(32)
 
        self.scroll.setWidget(self.content)
        layout.addWidget(self.scroll)

        # SECTION: Notifications
        self.content_layout.addSpacing(12)
        self.add_section_header("🔔", "Notifications", "Stay on track with reminders")

        # Enable notifications
        self.notifications_check = ToggleSwitch()

        notif_card = SettingCard(
            "🔔",
            "Daily Reminders",
            "Receive daily reminders to complete your habits",
            self.notifications_check,
        )
        self.content_layout.addWidget(notif_card)

        # Notification time
        self.notification_time = QTimeEdit()
        self.notification_time.setDisplayFormat("hh:mm AP")
        self.notification_time.setFont(QFont("SF Pro Display", 15, QFont.Bold))
        self.notification_time.setFixedHeight(48)
        self.notification_time.setFixedWidth(200)
        self.notification_time.setAlignment(Qt.AlignCenter)
        self.notification_time.setCursor(Qt.PointingHandCursor)
        self.notification_time.setButtonSymbols(QTimeEdit.NoButtons)
        
        # Saturated gradient for dark mode
        time_grad_start = "#5069f2" if is_dark else "#667eea"
        time_grad_end = "#7d44cf" if is_dark else "#764ba2"
        
        # Dark, semi-transparent purple field for dark mode
        time_bg = "rgba(139, 92, 246, 0.1)" if is_dark else f"qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {time_grad_start}, stop:1 {time_grad_end})"
        time_text = "#D1D5DB" if is_dark else "#FFFFFF"
        
        self.notification_time.setStyleSheet(f"""
            QTimeEdit {{
                background: {time_bg};
                color: {time_text};
                border: none;
                border-radius: 14px;
                padding: 8px 24px;
                letter-spacing: 1px;
            }}
            QTimeEdit:hover {{
                background: {"rgba(139, 92, 246, 0.2)" if is_dark else "#5568d3"};
            }}
            QTimeEdit:focus {{
                background: {"rgba(139, 92, 246, 0.2)" if is_dark else "#5568d3"};
            }}
        """)

        time_card = SettingCard(
            "⏰",
            "Reminder Time",
            "Set the time for daily habit reminders",
            self.notification_time,
        )
        self.content_layout.addWidget(time_card)

        # # SECTION: Display
        # self.content_layout.addSpacing(12)
        # self.add_section_header("👁️", "Display", "Control what you see")

        # Show completed
        # self.show_completed_check = ToggleSwitch()

        # completed_card = SettingCard(
        #     "✅",
        #     "Show Completed Habits",
        #     "Display habits that are already completed today",
        #     self.show_completed_check,
        # )
        # self.content_layout.addWidget(completed_card)

        # SECTION: Data Management
        self.content_layout.addSpacing(12)
        self.add_section_header("💾", "Data Management", "Backup and restore your data")

        # Saturated gradient for dark mode
        primary_grad_start = "#5069f2" if is_dark else "#667eea"
        primary_grad_end = "#7d44cf" if is_dark else "#764ba2"
        
        primary_btn_style = f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {primary_grad_start}, stop:1 {primary_grad_end});
                color: #FFFFFF;
                border: none;
                border-radius: 12px;
                padding: 0px 16px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5568d3, stop:1 #6a4191);
            }}
        """
        
        # Danger zone buttons
        danger_bg = "#991B1B" if is_dark else "#EF4444"
        danger_text = "#F87171" if is_dark else "#FFFFFF"
        danger_hover_bg = "#B91C1C" if is_dark else "#DC2626"
        
        danger_btn_style = f"""
            QPushButton {{
                background: {danger_bg};
                color: {danger_text};
                border: none;
                border-radius: 12px;
                padding: 0px 16px;
            }}
            QPushButton:hover {{
                background: {danger_hover_bg};
            }}
        """

        # Export data
        export_btn = QPushButton("📤 Export Data")
        export_btn.setFont(QFont("SF Pro Text", 14, QFont.Bold))
        export_btn.setFixedHeight(48)
        export_btn.setFixedWidth(200)
        export_btn.setCursor(Qt.PointingHandCursor)
        export_btn.setStyleSheet(primary_btn_style)
        export_btn.clicked.connect(self.export_data)

        export_card = SettingCard(
            "📥",
            "Export All Data",
            "Download all your habits, logs, and statistics as JSON",
            export_btn,
        )
        self.content_layout.addWidget(export_card)

        # Import data
        import_btn = QPushButton("📥 Import Data")
        import_btn.setFont(QFont("SF Pro Text", 14, QFont.Bold))
        import_btn.setFixedHeight(48)
        import_btn.setFixedWidth(200)
        import_btn.setCursor(Qt.PointingHandCursor)
        import_btn.setStyleSheet(primary_btn_style)
        import_btn.clicked.connect(self.import_data)

        import_card = SettingCard(
            "📤",
            "Import Data",
            "Restore your data from a previously exported JSON file",
            import_btn,
        )
        self.content_layout.addWidget(import_card)

        # SECTION: Danger Zone
        self.content_layout.addSpacing(12)
        self.add_section_header(
            "⚠️", "Danger Zone", "Irreversible actions", color="#DC2626"
        )

        # View trash
        trash_btn = QPushButton("🗑️ View Trash")
        trash_btn.setFont(QFont("SF Pro Text", 14, QFont.Bold))
        trash_btn.setFixedHeight(48)
        trash_btn.setFixedWidth(200)
        trash_btn.setCursor(Qt.PointingHandCursor)
        trash_btn.setStyleSheet(primary_btn_style)
        trash_btn.clicked.connect(self.view_trash)

        trash_card = SettingCard(
            "🗑️",
            "Deleted Habits",
            "View and restore deleted habits from trash",
            trash_btn,
        )
        self.content_layout.addWidget(trash_card)

        # Clear all data
        clear_btn = QPushButton("🔥 Clear All Data")
        clear_btn.setFont(QFont("SF Pro Text", 14, QFont.Bold))
        clear_btn.setFixedHeight(48)
        clear_btn.setFixedWidth(200)
        clear_btn.setCursor(Qt.PointingHandCursor)
        clear_btn.setStyleSheet(danger_btn_style)
        clear_btn.clicked.connect(self.clear_all_data)

        clear_card = SettingCard(
            "⚠️",
            "Clear All Data",
            "Permanently delete all habits, logs, goals, and achievements",
            clear_btn,
        )
        self.content_layout.addWidget(clear_card)

        self.content_layout.addStretch()

        # Info footer
        info_frame = QFrame()
        info_frame.setObjectName("InfoFrame")
        is_dark = self.theme_manager.is_dark_mode()
        info_bg = "rgba(139, 92, 246, 0.1)" if is_dark else "rgba(99, 102, 241, 0.05)"
        info_border = "#6366F1"
        info_frame.setStyleSheet(f"""
            QFrame#InfoFrame {{
                background-color: {info_bg};
                border-left: 4px solid {info_border};
                border-radius: 12px;
            }}
            QLabel {{
                border: none;
                background: transparent;
            }}
        """)

        info_layout = QHBoxLayout(info_frame)
        info_layout.setContentsMargins(20, 16, 20, 16)
        info_layout.setSpacing(12)

        info_icon = QLabel("ℹ️")
        info_icon.setFont(QFont("SF Pro Display", 24))
        info_icon.setStyleSheet("background: transparent;")
        info_layout.addWidget(info_icon)

        info_text = QLabel("Changes will take effect after clicking 'Save Changes'")
        info_text.setFont(QFont("SF Pro Text", 13, QFont.Medium))
        text_color = "#F3F4F6" if is_dark else "#4F46E5"
        info_text.setStyleSheet(f"color: {text_color}; background: transparent;")
        info_layout.addWidget(info_text, stretch=1)

        self.content_layout.addWidget(info_frame)

    def _style_msgbox(self, msg):
        """Apply premium styling to QMessageBox based on theme"""
        from app.themes import get_theme_manager
        is_dark = get_theme_manager().is_dark_mode()
        
        if not is_dark:
            return

        bg_color = "#1A1C23"
        text_color = "#F3F4F6"
        btn_bg = "#333645"
        btn_text = "#F3F4F6"
        btn_border = "#4B5563"
        btn_hover = "#404354"

        msg.setStyleSheet(f"""
            QMessageBox {{
                background-color: {bg_color};
                border-radius: 20px;
            }}
            QLabel {{
                color: {text_color};
                font-family: 'SF Pro Text';
                font-size: 14px;
            }}
            QPushButton {{
                background-color: {btn_bg};
                color: {btn_text};
                border: 1px solid {btn_border};
                border-radius: 8px;
                padding: 6px 20px;
                min-width: 80px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {btn_hover};
            }}
            QPushButton[text="&Yes"] {{
                background-color: #EF4444;
                color: white;
                border: none;
            }}
            QPushButton[text="&Yes"]:hover {{
                background-color: #DC2626;
            }}
        """)


    def add_section_header(self, icon, title, subtitle, color="#111827"):
        """Add a section header"""
        header_frame = QFrame()
        header_frame.setStyleSheet("background: transparent;")

        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(12)

        icon_label = QLabel(icon)
        icon_label.setFont(QFont("SF Pro Display", 28))
        icon_label.setStyleSheet("background: transparent;")
        header_layout.addWidget(icon_label)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        is_dark = self.theme_manager.is_dark_mode()
        
        title_label = QLabel(title)
        title_label.setFont(QFont("SF Pro Display", 22, QFont.Bold))
        # Handle custom error color for Danger Zone
        title_text_color = "#F87171" if (is_dark and color == "#DC2626") else ("#F3F4F6" if is_dark else color)
        title_label.setStyleSheet(f"color: {title_text_color}; background: transparent;")
        text_layout.addWidget(title_label)
 
        subtitle_label = QLabel(subtitle)
        subtitle_label.setFont(QFont("SF Pro Text", 13))
        text_secondary = "#9CA3AF" if is_dark else "#6B7280"
        subtitle_label.setStyleSheet(f"color: {text_secondary}; background: transparent;")
        text_layout.addWidget(subtitle_label)

        header_layout.addLayout(text_layout)
        header_layout.addStretch()

        self.content_layout.addWidget(header_frame)

    def apply_theme(self):
        """Apply theme to the view components."""
        is_dark = self.theme_manager.is_dark_mode()
        bg_primary = "#1A1C23" if is_dark else "#F9FAFB"
        text_primary = "#F3F4F6" if is_dark else "#111827"
        text_secondary = "#9CA3AF" if is_dark else "#6B7280"
        header_bg = "#1A1C23" if is_dark else "#FFFFFF"
        
        self.setStyleSheet(f"background-color: {bg_primary};")
        
        if hasattr(self, 'header'):
            self.header.setStyleSheet(f"""
                QFrame {{
                    background: {header_bg};
                    border: none;
                }}
            """)
            
        if hasattr(self, 'content'):
            self.content.setStyleSheet(f"background-color: {bg_primary};")
            
        if hasattr(self, 'title_label'):
            self.title_label.setStyleSheet(f"color: {text_primary}; background: transparent; padding-bottom: 4px;")
            
        if hasattr(self, 'subtitle_label'):
            self.subtitle_label.setStyleSheet(f"color: {text_secondary}; background: transparent; padding-bottom: 2px;")
            
        # Refresh all SettingCards and buttons in the layout
        # This will trigger their own setup_ui style logic if we modify it,
        # but for now let's just re-iterate and update what we can.
        # Actually, setup_ui in SettingsContentView is quite monolithic.
        # To truly refresh everything, we can call setup_ui again, 
        # but let's just ensure the main surfaces are updated.
        
    def load_settings(self) -> None:
        """Load current settings"""
        try:


            # Notifications
            self.notifications_check.setChecked(
                self.settings_service.is_notifications_enabled()
            )

            # Notification time
            time_str = self.settings_service.get_notification_time()
            try:
                hour, minute = map(int, time_str.split(":"))
                self.notification_time.setTime(QTime(hour, minute))
            except Exception:
                self.notification_time.setTime(QTime(9, 0))

        except Exception as e:
            logger.info(f"Error loading settings: {e}")

    def save_settings(self):
        """Save all settings"""
        try:


            # Save notifications
            self.settings_service.set_notifications_enabled(
                self.notifications_check.isChecked()
            )

            # Save notification time
            time = self.notification_time.time()
            time_str = time.toString("HH:mm")
            self.settings_service.set_notification_time(time_str)

            # Success message
            msg = QMessageBox(self)
            msg.setWindowTitle("Settings Saved")
            msg.setText("✅ Settings saved successfully!\n\nSome changes may require restarting the app.")
            msg.setIcon(QMessageBox.Information)
            self._style_msgbox(msg)
            msg.exec()

        except Exception as e:
            err_msg = QMessageBox(self)
            err_msg.setWindowTitle("Error")
            err_msg.setText(f"Failed to save settings: {str(e)}")
            err_msg.setIcon(QMessageBox.Critical)
            err_msg.setStandardButtons(QMessageBox.Ok)
            self._style_msgbox(err_msg)
            err_msg.exec()

    def export_data(self):
        """Export all data to JSON"""
        try:
            from app.services.habit_service import get_habit_service
            from app.services.goal_service import get_goal_service
            from app.db.database import get_db_connection
            import json

            # Get file path
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Export Data",
                f"habithub_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                "JSON Files (*.json)",
            )

            if not file_path:
                return

            # Collect data
            habit_service = get_habit_service()
            goal_service = get_goal_service()

            conn = get_db_connection()
            cursor = conn.cursor()

            # Get habits
            habits = []
            for habit in habit_service.get_all_habits():
                habits.append(
                    {
                        "id": habit.id,
                        "name": habit.name,
                        "description": habit.description,
                        "category": habit.category,
                        "frequency": habit.frequency,
                        "created_at": habit.created_at,
                    }
                )

            # Get logs
            cursor.execute("SELECT * FROM habit_logs")
            logs = [dict(row) for row in cursor.fetchall()]

            # Get goals
            goals = []
            try:
                for goal in goal_service.get_all_goals(include_completed=True):
                    goals.append(
                        {
                            "id": goal.id,
                            "habit_id": goal.habit_id,
                            "goal_type": goal.goal_type,
                            "target_value": goal.target_value,
                            "current_value": goal.current_value,
                            "is_completed": goal.is_completed,
                            "created_at": goal.created_at,
                        }
                    )
            except Exception:
                pass

            # Get settings
            cursor.execute("SELECT * FROM settings")
            settings = [dict(row) for row in cursor.fetchall()]

            conn.close()

            # Create export
            export_data = {
                "export_date": datetime.now().isoformat(),
                "version": "1.0",
                "habits": habits,
                "habit_logs": logs,
                "goals": goals,
                "settings": settings,
            }

            # Write file
            with open(file_path, "w") as f:
                json.dump(export_data, f, indent=2)

            msg = QMessageBox(self)
            msg.setWindowTitle("Export Successful")
            msg.setText(f"✅ Data exported successfully!\n\nFile saved to:\n{file_path}")
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Ok)
            self._style_msgbox(msg)
            msg.exec()

        except Exception as e:
            err_msg = QMessageBox(self)
            err_msg.setWindowTitle("Export Failed")
            err_msg.setText(f"Failed to export data: {str(e)}")
            err_msg.setIcon(QMessageBox.Critical)
            err_msg.setStandardButtons(QMessageBox.Ok)
            self._style_msgbox(err_msg)
            err_msg.exec()

    def import_data(self):
        """Import data from JSON"""
        q_msg = QMessageBox(self)
        q_msg.setWindowTitle("Import Data")
        q_msg.setText("⚠️ Warning: This will replace ALL your current data!\n\nAre you sure you want to continue?")
        q_msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        q_msg.setDefaultButton(QMessageBox.No)
        q_msg.setIcon(QMessageBox.Question)
        self._style_msgbox(q_msg)
        
        if q_msg.exec() != QMessageBox.Yes:
            return

        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Import Data", "", "JSON Files (*.json)"
            )

            if not file_path:
                return

            import json
            from app.db.database import get_db_connection

            with open(file_path, "r") as f:
                data = json.load(f)

            conn = get_db_connection()
            cursor = conn.cursor()

            # Clear existing
            cursor.execute("DELETE FROM habit_logs")
            cursor.execute("DELETE FROM habits")
            cursor.execute("DELETE FROM goals")
            cursor.execute("DELETE FROM settings")

            # Import
            for habit in data.get("habits", []):
                cursor.execute(
                    """
                    INSERT INTO habits (id, name, description, category, frequency, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (
                        habit["id"],
                        habit["name"],
                        habit["description"],
                        habit["category"],
                        habit["frequency"],
                        habit["created_at"],
                    ),
                )

            for log in data.get("habit_logs", []):
                cursor.execute(
                    """
                    INSERT INTO habit_logs (habit_id, completed_date, created_at)
                    VALUES (?, ?, ?)
                """,
                    (
                        log["habit_id"],
                        log["completed_date"],
                        log.get(
                            "created_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        ),
                    ),
                )

            for goal in data.get("goals", []):
                cursor.execute(
                    """
                    INSERT INTO goals (id, habit_id, goal_type, target_value, current_value, is_completed, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        goal["id"],
                        goal["habit_id"],
                        goal["goal_type"],
                        goal["target_value"],
                        goal["current_value"],
                        goal["is_completed"],
                        goal["created_at"],
                    ),
                )

            for setting in data.get("settings", []):
                cursor.execute(
                    """
                    INSERT INTO settings (key, value)
                    VALUES (?, ?)
                """,
                    (setting["key"], setting["value"]),
                )

            conn.commit()
            conn.close()

            msg = QMessageBox(self)
            msg.setWindowTitle("Import Successful")
            msg.setText("✅ Data imported successfully!\n\nPlease restart the app to see changes.")
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Ok)
            self._style_msgbox(msg)
            msg.exec()

        except Exception as e:
            err_msg = QMessageBox(self)
            err_msg.setWindowTitle("Import Failed")
            err_msg.setText(f"Failed to import data: {str(e)}")
            err_msg.setIcon(QMessageBox.Critical)
            err_msg.setStandardButtons(QMessageBox.Ok)
            self._style_msgbox(err_msg)
            err_msg.exec()

    def view_trash(self):
        """View deleted habits in trash"""
        try:
            from app.db.database import get_db_connection

            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM deleted_habits ORDER BY deleted_at DESC")
            deleted_habits = cursor.fetchall()

            conn.close()

            if not deleted_habits:
                msg = QMessageBox(self)
                msg.setWindowTitle("Trash Empty")
                msg.setText("🗑️ Trash is empty!\n\nNo deleted habits to display.")
                msg.setIcon(QMessageBox.Information)
                msg.setStandardButtons(QMessageBox.Ok)
                self._style_msgbox(msg)
                msg.exec()
                return

            from app.views.trash_view import TrashDialog

            trash_dialog = TrashDialog(self)
            trash_dialog.exec()

        except Exception as e:
            err_msg = QMessageBox(self)
            err_msg.setWindowTitle("Error")
            err_msg.setText(f"Failed to open trash: {str(e)}")
            err_msg.setIcon(QMessageBox.Critical)
            err_msg.setStandardButtons(QMessageBox.Ok)
            self._style_msgbox(err_msg)
            err_msg.exec()

    def clear_all_data(self):
        """Clear all data"""
        msg1 = QMessageBox(self)
        msg1.setWindowTitle("Clear All Data")
        msg1.setText("⚠️ DANGER: This will permanently delete ALL your data!\n\n"
                    "This includes:\n"
                    "• All habits\n"
                    "• All completion logs\n"
                    "• All goals\n"
                    "• All achievements\n"
                    "• All settings\n\n"
                    "Are you absolutely sure?")
        msg1.setIcon(QMessageBox.Question)
        msg1.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg1.setDefaultButton(QMessageBox.No)
        self._style_msgbox(msg1)
        
        if msg1.exec() != QMessageBox.Yes:
            return

        msg2 = QMessageBox(self)
        msg2.setWindowTitle("Final Confirmation")
        msg2.setText("🔥 LAST CHANCE!\n\nThis action CANNOT be undone!\n\nType YES to confirm:")
        msg2.setIcon(QMessageBox.Warning)
        msg2.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg2.setDefaultButton(QMessageBox.No)
        self._style_msgbox(msg2)
            
        if msg2.exec() != QMessageBox.Yes:
            return

        try:
            from app.db.database import get_db_connection

            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM habit_logs")
            cursor.execute("DELETE FROM habits")
            cursor.execute("DELETE FROM deleted_habits")
            cursor.execute("DELETE FROM goals")
            cursor.execute("DELETE FROM settings")

            conn.commit()
            conn.close()

            msg3 = QMessageBox(self)
            msg3.setWindowTitle("Data Cleared")
            msg3.setText("✅ All data has been cleared!\n\nThe app will restart with fresh data.")
            msg3.setIcon(QMessageBox.Information)
            self._style_msgbox(msg3)
            msg3.exec()

            if self.main_window:
                self.main_window.close()

        except Exception as e:
            err_msg = QMessageBox(self)
            err_msg.setWindowTitle("Error")
            err_msg.setText(f"Failed to clear data: {str(e)}")
            err_msg.setIcon(QMessageBox.Critical)
            err_msg.setStandardButtons(QMessageBox.Ok)
            self._style_msgbox(err_msg)
            err_msg.exec()
