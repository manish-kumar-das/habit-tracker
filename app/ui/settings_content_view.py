"""
Settings Content View - Premium Redesign
Beautiful settings interface with card-based design
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QFrame,
    QCheckBox,
    QComboBox,
    QTimeEdit,
    QFileDialog,
    QMessageBox,
    QGraphicsDropShadowEffect,
)
from PySide6.QtCore import Qt, QTime, QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QFont, QColor, QPainter, QLinearGradient
from datetime import datetime
from app.services.settings_service import get_settings_service
from app.utils.constants import THEME_DARK, THEME_LIGHT


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
        self.setStyleSheet("""
            QFrame#SettingCard {
                background-color: #FFFFFF;
                border: 1px solid rgba(0, 0, 0, 0.05);
                border-radius: 20px;
            }
            QFrame#SettingCard:hover {
                background-color: #FDFDFF;
                border: 1px solid rgba(102, 126, 234, 0.2);
            }
            QLabel {
                border: none;
                background: transparent;
            }
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

        title_label = QLabel(title)
        title_label.setFont(QFont("SF Pro Display", 17, QFont.Bold))
        title_label.setStyleSheet("color: #111827; background: transparent;")
        text_layout.addWidget(title_label)

        desc_label = QLabel(description)
        desc_label.setFont(QFont("SF Pro Text", 13))
        desc_label.setStyleSheet("color: #6B7280; background: transparent;")
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
        if self.isChecked():
            grad = QLinearGradient(0, 0, self.width(), 0)
            grad.setColorAt(0, QColor("#667eea"))
            grad.setColorAt(1, QColor("#764ba2"))
            p.setBrush(grad)
        else:
            p.setBrush(QColor("#E5E7EB"))

        p.setPen(Qt.NoPen)
        p.drawRoundedRect(0, 0, self.width(), self.height(), 16, 16)

        # Thumb
        p.setBrush(QColor("white"))
        # Subtle thumb shadow
        p.drawEllipse(self._thumb_pos, 4, 24, 24)


class SettingsContentView(QWidget):
    """Premium Settings View"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.settings_service = get_settings_service()
        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        """Setup settings UI"""
        self.setStyleSheet("background-color: #F9FAFB;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = QFrame()
        header.setMinimumHeight(120)
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FFFFFF, stop:1 #F9FAFB);
                border: none;
            }
        """)

        header_layout = QHBoxLayout(header)
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

        title = QLabel("Settings")
        title.setFont(QFont("SF Pro Display", 28, QFont.Bold))
        title.setStyleSheet(
            "color: #111827; background: transparent; padding-bottom: 4px;"
        )
        title.setWordWrap(True)
        title_text_layout.addWidget(title)

        subtitle = QLabel("Customize your habit tracking experience")
        subtitle.setFont(QFont("SF Pro Text", 14))
        subtitle.setStyleSheet(
            "color: #6B7280; background: transparent; padding-bottom: 2px;"
        )
        title_text_layout.addWidget(subtitle)

        title_section.addLayout(title_text_layout)

        header_layout.addLayout(title_section)
        header_layout.addStretch()

        # Right: Save button
        save_btn = QPushButton("💾 Save Changes")
        save_btn.setFont(QFont("SF Pro Text", 15, QFont.Bold))
        save_btn.setFixedHeight(50)
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:0.5 #764ba2, stop:1 #f093fb);
                color: #FFFFFF;
                border: none;
                border-radius: 12px;
                padding: 0px 32px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5568d3, stop:0.5 #6a4191, stop:1 #e07af0);
            }
        """)
        save_btn.clicked.connect(self.save_settings)
        header_layout.addWidget(save_btn)

        layout.addWidget(header)

        # Content scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background: #F3F4F6;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #6366F1;
                border-radius: 5px;
            }
        """)

        content = QWidget()
        content.setStyleSheet("background-color: #F9FAFB;")
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setContentsMargins(40, 28, 40, 28)
        self.content_layout.setSpacing(32)

        # SECTION: Appearance
        self.add_section_header("🎨", "Appearance", "Customize the look and feel")

        # Theme
        self.theme_combo = QComboBox()
        self.theme_combo.addItem("☀️  Light Theme", THEME_LIGHT)
        self.theme_combo.addItem("🌙  Dark Theme", THEME_DARK)
        self.theme_combo.setFont(QFont("SF Pro Text", 14))
        self.theme_combo.setFixedHeight(44)
        self.theme_combo.setCursor(Qt.PointingHandCursor)
        self.theme_combo.setStyleSheet("""
            QComboBox {
                background-color: #F9FAFB;
                border: 2px solid #E5E7EB;
                border-radius: 12px;
                padding: 8px 16px;
                min-width: 180px;
            }
            QComboBox:hover {
                border: 2px solid #6366F1;
                background-color: #FFFFFF;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 12px;
            }
            QComboBox QAbstractItemView {
                background-color: #FFFFFF;
                border: 2px solid #E5E7EB;
                border-radius: 8px;
                selection-background-color: #EEF2FF;
                selection-color: #4F46E5;
            }
        """)

        theme_card = SettingCard(
            "🎨", "Theme", "Choose your preferred color theme", self.theme_combo
        )
        self.content_layout.addWidget(theme_card)

        # Compact mode
        # self.compact_check = ToggleSwitch()

        # compact_card = SettingCard(
        #     "📱",
        #     "Compact Mode",
        #     "Show more content with reduced spacing",
        #     self.compact_check,
        # )
        # self.content_layout.addWidget(compact_card)

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
        self.notification_time.setStyleSheet("""
            QTimeEdit {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: #FFFFFF;
                border: none;
                border-radius: 14px;
                padding: 8px 24px;
                letter-spacing: 1px;
            }
            QTimeEdit:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5568d3, stop:1 #6a4191);
            }
            QTimeEdit:focus {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5568d3, stop:1 #6a4191);
            }
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

        # Consistent style for card buttons
        primary_btn_style = """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                color: #FFFFFF;
                border: none;
                border-radius: 12px;
                padding: 0px 16px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5568d3, stop:1 #6a4191);
            }
        """

        danger_btn_style = """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #EF4444, stop:1 #DC2626);
                color: #FFFFFF;
                border: none;
                border-radius: 12px;
                padding: 0px 16px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #DC2626, stop:1 #B91C1C);
            }
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
        info_frame.setStyleSheet("""
            QFrame#InfoFrame {
                background-color: rgba(99, 102, 241, 0.05);
                border-left: 4px solid #6366F1;
                border-radius: 12px;
            }
            QLabel {
                border: none;
                background: transparent;
            }
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
        info_text.setStyleSheet("color: #4F46E5; background: transparent;")
        info_layout.addWidget(info_text, stretch=1)

        self.content_layout.addWidget(info_frame)

        scroll.setWidget(content)
        layout.addWidget(scroll)

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

        title_label = QLabel(title)
        title_label.setFont(QFont("SF Pro Display", 22, QFont.Bold))
        title_label.setStyleSheet(f"color: {color}; background: transparent;")
        text_layout.addWidget(title_label)

        subtitle_label = QLabel(subtitle)
        subtitle_label.setFont(QFont("SF Pro Text", 13))
        subtitle_label.setStyleSheet("color: #6B7280; background: transparent;")
        text_layout.addWidget(subtitle_label)

        header_layout.addLayout(text_layout)
        header_layout.addStretch()

        self.content_layout.addWidget(header_frame)

    def load_settings(self):
        """Load current settings"""
        try:
            # Theme
            current_theme = self.settings_service.get_theme()
            index = self.theme_combo.findData(current_theme)
            if index >= 0:
                self.theme_combo.setCurrentIndex(index)

            # Compact mode
            # self.compact_check.setChecked(self.settings_service.get_compact_mode())

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
            print(f"Error loading settings: {e}")

    def save_settings(self):
        """Save all settings"""
        try:
            # Save theme
            theme = self.theme_combo.currentData()
            self.settings_service.set_theme(theme)

            # Save compact mode
            # self.settings_service.set_compact_mode(self.compact_check.isChecked())

            # Save notifications
            self.settings_service.set_notifications_enabled(
                self.notifications_check.isChecked()
            )

            # Save notification time
            time = self.notification_time.time()
            time_str = time.toString("HH:mm")
            self.settings_service.set_notification_time(time_str)

            # Success message
            QMessageBox.information(
                self,
                "Settings Saved",
                "✅ Settings saved successfully!\n\nSome changes may require restarting the app.",
                QMessageBox.Ok,
            )

        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Failed to save settings: {str(e)}", QMessageBox.Ok
            )

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

            QMessageBox.information(
                self,
                "Export Successful",
                f"✅ Data exported successfully!\n\nFile saved to:\n{file_path}",
                QMessageBox.Ok,
            )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Export Failed",
                f"Failed to export data: {str(e)}",
                QMessageBox.Ok,
            )

    def import_data(self):
        """Import data from JSON"""
        reply = QMessageBox.question(
            self,
            "Import Data",
            "⚠️ Warning: This will replace ALL your current data!\n\nAre you sure you want to continue?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply != QMessageBox.Yes:
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

            QMessageBox.information(
                self,
                "Import Successful",
                "✅ Data imported successfully!\n\nPlease restart the app to see changes.",
                QMessageBox.Ok,
            )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Import Failed",
                f"Failed to import data: {str(e)}",
                QMessageBox.Ok,
            )

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
                QMessageBox.information(
                    self,
                    "Trash Empty",
                    "🗑️ Trash is empty!\n\nNo deleted habits to display.",
                    QMessageBox.Ok,
                )
                return

            from app.ui.trash_view import TrashDialog

            trash_dialog = TrashDialog(self)
            trash_dialog.exec()

        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Failed to open trash: {str(e)}", QMessageBox.Ok
            )

    def clear_all_data(self):
        """Clear all data"""
        reply1 = QMessageBox.question(
            self,
            "Clear All Data",
            "⚠️ DANGER: This will permanently delete ALL your data!\n\n"
            "This includes:\n"
            "• All habits\n"
            "• All completion logs\n"
            "• All goals\n"
            "• All achievements\n"
            "• All settings\n\n"
            "Are you absolutely sure?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply1 != QMessageBox.Yes:
            return

        reply2 = QMessageBox.question(
            self,
            "Final Confirmation",
            "🔥 LAST CHANCE!\n\nThis action CANNOT be undone!\n\nType YES to confirm:",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply2 != QMessageBox.Yes:
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

            QMessageBox.information(
                self,
                "Data Cleared",
                "✅ All data has been cleared!\n\nThe app will restart with fresh data.",
                QMessageBox.Ok,
            )

            if self.main_window:
                self.main_window.close()

        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Failed to clear data: {str(e)}", QMessageBox.Ok
            )
