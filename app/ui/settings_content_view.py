"""
Settings Content View - WITH EXPORT DATA & TRASH
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QScrollArea, QFrame, QLineEdit,
    QTextEdit, QMessageBox, QCheckBox, QComboBox, QTimeEdit, QFileDialog
)
from PySide6.QtCore import Qt, QTime
from PySide6.QtGui import QFont, QCursor
from app.services.settings_service import get_settings_service
from app.utils.constants import THEME_DARK, THEME_LIGHT
import json
import os
from datetime import datetime


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
        self.setMinimumHeight(100)
        
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
        if widget:
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
                QPushButton {
                    padding: 10px 20px;
                    border: none;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: bold;
                }
            """)
            layout.addWidget(widget)


class SettingsContentView(QWidget):
    """Settings view with Export & Trash"""
    
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
        
        content_layout.addSpacing(16)
        
        # Data Management Section
        data_label = QLabel("💾 Data Management")
        data_label.setFont(QFont("SF Pro Display", 18, QFont.Bold))
        data_label.setStyleSheet("color: #111827; background: transparent;")
        content_layout.addWidget(data_label)
        
        # Export Data Button
        export_btn = QPushButton("📤 Export Data")
        export_btn.setFont(QFont("SF Pro Text", 14, QFont.Bold))
        export_btn.setFixedHeight(44)
        export_btn.setCursor(Qt.PointingHandCursor)
        export_btn.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                color: #FFFFFF;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
        """)
        export_btn.clicked.connect(self.export_data)
        
        export_card = SettingCard(
            "📥",
            "Export All Data",
            "Download all your habits, logs, and statistics as JSON file",
            export_btn
        )
        content_layout.addWidget(export_card)
        
        # Import Data Button
        import_btn = QPushButton("📥 Import Data")
        import_btn.setFont(QFont("SF Pro Text", 14, QFont.Bold))
        import_btn.setFixedHeight(44)
        import_btn.setCursor(Qt.PointingHandCursor)
        import_btn.setStyleSheet("""
            QPushButton {
                background-color: #8B5CF6;
                color: #FFFFFF;
            }
            QPushButton:hover {
                background-color: #7C3AED;
            }
        """)
        import_btn.clicked.connect(self.import_data)
        
        import_card = SettingCard(
            "📤",
            "Import Data",
            "Restore your data from a previously exported JSON file",
            import_btn
        )
        content_layout.addWidget(import_card)
        
        content_layout.addSpacing(16)
        
        # Danger Zone Section
        danger_label = QLabel("⚠️ Danger Zone")
        danger_label.setFont(QFont("SF Pro Display", 18, QFont.Bold))
        danger_label.setStyleSheet("color: #DC2626; background: transparent;")
        content_layout.addWidget(danger_label)
        
        # View Trash Button
        trash_btn = QPushButton("🗑️ View Trash")
        trash_btn.setFont(QFont("SF Pro Text", 14, QFont.Bold))
        trash_btn.setFixedHeight(44)
        trash_btn.setCursor(Qt.PointingHandCursor)
        trash_btn.setStyleSheet("""
            QPushButton {
                background-color: #F59E0B;
                color: #FFFFFF;
            }
            QPushButton:hover {
                background-color: #D97706;
            }
        """)
        trash_btn.clicked.connect(self.view_trash)
        
        trash_card = SettingCard(
            "🗑️",
            "Deleted Habits",
            "View and restore deleted habits from trash",
            trash_btn
        )
        content_layout.addWidget(trash_card)
        
        # Clear All Data Button
        clear_btn = QPushButton("🔥 Clear All Data")
        clear_btn.setFont(QFont("SF Pro Text", 14, QFont.Bold))
        clear_btn.setFixedHeight(44)
        clear_btn.setCursor(Qt.PointingHandCursor)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #EF4444;
                color: #FFFFFF;
            }
            QPushButton:hover {
                background-color: #DC2626;
            }
        """)
        clear_btn.clicked.connect(self.clear_all_data)
        
        clear_card = SettingCard(
            "⚠️",
            "Clear All Data",
            "Permanently delete all habits, logs, goals, and achievements",
            clear_btn
        )
        content_layout.addWidget(clear_card)
        
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
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to save settings: {str(e)}")
            msg.exec()
    
    def export_data(self):
        """Export all data to JSON"""
        try:
            from app.services.habit_service import get_habit_service
            from app.services.goal_service import get_goal_service
            from app.services.achievement_service import get_achievement_service
            from app.db.database import get_db_connection
            
            # Get file path from user
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Export Data",
                f"habithub_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                "JSON Files (*.json)"
            )
            
            if not file_path:
                return
            
            # Collect all data
            habit_service = get_habit_service()
            goal_service = get_goal_service()
            achievement_service = get_achievement_service()
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Get habits
            habits = []
            for habit in habit_service.get_all_habits():
                habits.append({
                    'id': habit.id,
                    'name': habit.name,
                    'description': habit.description,
                    'category': habit.category,
                    'frequency': habit.frequency,
                    'created_at': habit.created_at
                })
            
            # Get habit logs
            cursor.execute('SELECT * FROM habit_logs')
            logs = [dict(row) for row in cursor.fetchall()]
            
            # Get goals
            goals = []
            try:
                for goal in goal_service.get_all_goals(include_completed=True):
                    goals.append({
                        'id': goal.id,
                        'habit_id': goal.habit_id,
                        'goal_type': goal.goal_type,
                        'target_value': goal.target_value,
                        'current_value': goal.current_value,
                        'is_completed': goal.is_completed,
                        'created_at': goal.created_at
                    })
            except:
                pass
            
            # Get achievements
            achievements = []
            try:
                cursor.execute('SELECT * FROM achievements')
                achievements = [dict(row) for row in cursor.fetchall()]
            except:
                pass
            
            # Get settings
            cursor.execute('SELECT * FROM settings')
            settings = [dict(row) for row in cursor.fetchall()]
            
            conn.close()
            
            # Create export data
            export_data = {
                'export_date': datetime.now().isoformat(),
                'version': '1.0',
                'habits': habits,
                'habit_logs': logs,
                'goals': goals,
                'achievements': achievements,
                'settings': settings
            }
            
            # Write to file
            with open(file_path, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            # Success message
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Export Successful")
            msg.setText("✅ Data exported successfully!")
            msg.setInformativeText(f"File saved to:\n{file_path}")
            msg.exec()
            
        except Exception as e:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Export Failed")
            msg.setText(f"Failed to export data: {str(e)}")
            msg.exec()
    
    def import_data(self):
        """Import data from JSON"""
        # Warning message first
        reply = QMessageBox.question(
            self,
            "Import Data",
            "⚠️ Warning: This will replace ALL your current data!\n\nAre you sure you want to continue?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        try:
            # Get file from user
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Import Data",
                "",
                "JSON Files (*.json)"
            )
            
            if not file_path:
                return
            
            # Read file
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            from app.db.database import get_db_connection
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Clear existing data
            cursor.execute('DELETE FROM habit_logs')
            cursor.execute('DELETE FROM habits')
            cursor.execute('DELETE FROM goals')
            cursor.execute('DELETE FROM achievements')
            cursor.execute('DELETE FROM settings')
            
            # Import habits
            for habit in data.get('habits', []):
                cursor.execute('''
                    INSERT INTO habits (id, name, description, category, frequency, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (habit['id'], habit['name'], habit['description'], 
                      habit['category'], habit['frequency'], habit['created_at']))
            
            # Import logs
            for log in data.get('habit_logs', []):
                cursor.execute('''
                    INSERT INTO habit_logs (habit_id, completed_date, created_at)
                    VALUES (?, ?, ?)
                ''', (log['habit_id'], log['completed_date'], log.get('created_at', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))
            
            # Import goals
            for goal in data.get('goals', []):
                cursor.execute('''
                    INSERT INTO goals (id, habit_id, goal_type, target_value, current_value, is_completed, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (goal['id'], goal['habit_id'], goal['goal_type'], goal['target_value'],
                      goal['current_value'], goal['is_completed'], goal['created_at']))
            
            # Import achievements
            for achievement in data.get('achievements', []):
                cursor.execute('''
                    INSERT INTO achievements (id, name, description, type, requirement, is_unlocked, unlocked_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (achievement['id'], achievement['name'], achievement['description'],
                      achievement['type'], achievement['requirement'], achievement['is_unlocked'],
                      achievement.get('unlocked_at')))
            
            # Import settings
            for setting in data.get('settings', []):
                cursor.execute('''
                    INSERT INTO settings (key, value)
                    VALUES (?, ?)
                ''', (setting['key'], setting['value']))
            
            conn.commit()
            conn.close()
            
            # Success message
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Import Successful")
            msg.setText("✅ Data imported successfully!")
            msg.setInformativeText("Please restart the app to see the changes.")
            msg.exec()
            
        except Exception as e:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Import Failed")
            msg.setText(f"Failed to import data: {str(e)}")
            msg.exec()
    
    def view_trash(self):
        """View deleted habits in trash"""
        try:
            from app.db.database import get_db_connection
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM deleted_habits ORDER BY deleted_at DESC')
            deleted_habits = cursor.fetchall()
            
            conn.close()
            
            if not deleted_habits:
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Trash Empty")
                msg.setText("🗑️ Trash is empty!")
                msg.setInformativeText("No deleted habits to display.")
                msg.exec()
                return
            
            # Create trash view dialog
            from app.ui.trash_view import TrashDialog
            trash_dialog = TrashDialog(self)
            trash_dialog.exec()
            
        except Exception as e:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to open trash: {str(e)}")
            msg.exec()
    
    def clear_all_data(self):
        """Clear all data (dangerous operation)"""
        # Double confirmation
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
            QMessageBox.No
        )
        
        if reply1 != QMessageBox.Yes:
            return
        
        reply2 = QMessageBox.question(
            self,
            "Final Confirmation",
            "🔥 LAST CHANCE!\n\nThis action CANNOT be undone!\n\nType YES to confirm:",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply2 != QMessageBox.Yes:
            return
        
        try:
            from app.db.database import get_db_connection
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Delete all data
            cursor.execute('DELETE FROM habit_logs')
            cursor.execute('DELETE FROM habits')
            cursor.execute('DELETE FROM deleted_habits')
            cursor.execute('DELETE FROM goals')
            cursor.execute('DELETE FROM achievements')
            cursor.execute('DELETE FROM settings')
            
            conn.commit()
            conn.close()
            
            # Success message
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Data Cleared")
            msg.setText("✅ All data has been cleared!")
            msg.setInformativeText("The app will restart with fresh data.")
            msg.exec()
            
            # Restart app
            if self.main_window:
                self.main_window.close()
            
        except Exception as e:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to clear data: {str(e)}")
            msg.exec()
