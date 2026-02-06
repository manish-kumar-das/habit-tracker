"""
Export data dialog
"""

import csv
import json
from datetime import datetime
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFileDialog, QMessageBox, QRadioButton, QButtonGroup
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from app.services.habit_service import get_habit_service
from app.services.stats_service import get_stats_service


class ExportDialog(QDialog):
    """Dialog for exporting habit data"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.habit_service = get_habit_service()
        self.stats_service = get_stats_service()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the dialog UI"""
        self.setWindowTitle("Export Data")
        self.setModal(True)
        self.setMinimumWidth(500)
        self.setStyleSheet("""
            QDialog {
                background-color: #1C1F26;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(24)
        layout.setContentsMargins(32, 32, 32, 32)
        
        # Title
        title = QLabel("💾 Export Your Data")
        title.setFont(QFont("Inter", 24, QFont.Bold))
        title.setStyleSheet("color: #E4E6EB; background: transparent;")
        layout.addWidget(title)
        
        subtitle = QLabel("Choose a format to export your habit data")
        subtitle.setFont(QFont("Inter", 13))
        subtitle.setStyleSheet("color: #9AA0A6; background: transparent; margin-bottom: 8px;")
        layout.addWidget(subtitle)
        
        # Format selection
        format_label = QLabel("Export Format")
        format_label.setFont(QFont("Inter", 14, QFont.Medium))
        format_label.setStyleSheet("color: #E4E6EB; background: transparent; margin-top: 16px;")
        layout.addWidget(format_label)
        
        # Radio buttons
        self.format_group = QButtonGroup()
        
        self.csv_radio = QRadioButton("CSV (Excel compatible)")
        self.csv_radio.setFont(QFont("Inter", 13))
        self.csv_radio.setStyleSheet("""
            QRadioButton {
                color: #E4E6EB;
                background: transparent;
                padding: 8px;
            }
            QRadioButton::indicator {
                width: 20px;
                height: 20px;
                border-radius: 10px;
                border: 2px solid #4A4D56;
                background-color: #20232B;
            }
            QRadioButton::indicator:checked {
                background-color: #4FD1C5;
                border: 2px solid #4FD1C5;
            }
            QRadioButton::indicator:hover {
                border: 2px solid #4FD1C5;
            }
        """)
        self.csv_radio.setChecked(True)
        self.format_group.addButton(self.csv_radio)
        layout.addWidget(self.csv_radio)
        
        csv_desc = QLabel("    Best for spreadsheets and data analysis")
        csv_desc.setFont(QFont("Inter", 11))
        csv_desc.setStyleSheet("color: #6B6E76; background: transparent;")
        layout.addWidget(csv_desc)
        
        self.json_radio = QRadioButton("JSON (Developer friendly)")
        self.json_radio.setFont(QFont("Inter", 13))
        self.json_radio.setStyleSheet("""
            QRadioButton {
                color: #E4E6EB;
                background: transparent;
                padding: 8px;
            }
            QRadioButton::indicator {
                width: 20px;
                height: 20px;
                border-radius: 10px;
                border: 2px solid #4A4D56;
                background-color: #20232B;
            }
            QRadioButton::indicator:checked {
                background-color: #4FD1C5;
                border: 2px solid #4FD1C5;
            }
            QRadioButton::indicator:hover {
                border: 2px solid #4FD1C5;
            }
        """)
        self.format_group.addButton(self.json_radio)
        layout.addWidget(self.json_radio)
        
        json_desc = QLabel("    Structured data format, easy to parse")
        json_desc.setFont(QFont("Inter", 11))
        json_desc.setStyleSheet("color: #6B6E76; background: transparent;")
        layout.addWidget(json_desc)
        
        layout.addSpacing(16)
        
        # Info box
        info_box = QLabel("📌 Export includes:\n• All habit names and descriptions\n• Completion history\n• Streak information\n• Statistics")
        info_box.setFont(QFont("Inter", 12))
        info_box.setStyleSheet("""
            QLabel {
                color: #9AA0A6;
                background-color: rgba(79, 209, 197, 0.1);
                border: 1px solid #4FD1C5;
                border-radius: 8px;
                padding: 16px;
            }
        """)
        layout.addWidget(info_box)
        
        layout.addSpacing(8)
        
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
                border: 2px solid #4A4D56;
                border-radius: 10px;
                color: #9AA0A6;
                background-color: transparent;
            }
            QPushButton:hover {
                border: 2px solid #7C83FD;
                color: #E4E6EB;
                background-color: rgba(124, 131, 253, 0.1);
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        export_btn = QPushButton("Export Data")
        export_btn.setFont(QFont("Inter", 13, QFont.Bold))
        export_btn.setFixedHeight(48)
        export_btn.setCursor(Qt.PointingHandCursor)
        export_btn.setStyleSheet("""
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
        export_btn.clicked.connect(self.export_data)
        button_layout.addWidget(export_btn)
        
        layout.addLayout(button_layout)
    
    def export_data(self):
        """Export data to selected format"""
        # Get all stats
        all_stats = self.stats_service.get_all_habits_stats()
        
        if not all_stats:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("No Data")
            msg.setText("No habits to export")
            msg.setInformativeText("Create some habits first before exporting.")
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #1C1F26;
                }
                QMessageBox QLabel {
                    color: #E4E6EB;
                }
                QPushButton {
                    background-color: #4FD1C5;
                    color: #0F1115;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 20px;
                    font-weight: bold;
                    min-width: 80px;
                }
            """)
            msg.exec()
            return
        
        # Determine file extension
        if self.csv_radio.isChecked():
            file_filter = "CSV Files (*.csv)"
            default_name = f"habits_export_{datetime.now().strftime('%Y%m%d')}.csv"
        else:
            file_filter = "JSON Files (*.json)"
            default_name = f"habits_export_{datetime.now().strftime('%Y%m%d')}.json"
        
        # Open save dialog
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Habits Data",
            default_name,
            file_filter
        )
        
        if not file_path:
            return
        
        try:
            if self.csv_radio.isChecked():
                self.export_to_csv(file_path, all_stats)
            else:
                self.export_to_json(file_path, all_stats)
            
            # Success message
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Export Successful")
            msg.setText("✓ Data exported successfully!")
            msg.setInformativeText(f"Saved to: {file_path}")
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
            self.accept()
            
        except Exception as e:
            # Error message
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Export Failed")
            msg.setText("Failed to export data")
            msg.setInformativeText(str(e))
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #1C1F26;
                }
                QMessageBox QLabel {
                    color: #E4E6EB;
                }
                QPushButton {
                    background-color: #EF5350;
                    color: #FFFFFF;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 20px;
                    font-weight: bold;
                    min-width: 80px;
                }
            """)
            msg.exec()
    
    def export_to_csv(self, file_path, stats_data):
        """Export to CSV format"""
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'Habit Name', 'Current Streak', 'Longest Streak',
                'Total Completions', '7-Day Rate (%)', '30-Day Rate (%)',
                'Completed Today', 'Created Date'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for stat in stats_data:
                writer.writerow({
                    'Habit Name': stat['habit_name'],
                    'Current Streak': stat['current_streak'],
                    'Longest Streak': stat['longest_streak'],
                    'Total Completions': stat['total_completions'],
                    '7-Day Rate (%)': stat['completion_rate_7d'],
                    '30-Day Rate (%)': stat['completion_rate_30d'],
                    'Completed Today': 'Yes' if stat['is_completed_today'] else 'No',
                    'Created Date': stat['created_at']
                })
    
    def export_to_json(self, file_path, stats_data):
        """Export to JSON format"""
        export_data = {
            'export_date': datetime.now().isoformat(),
            'total_habits': len(stats_data),
            'habits': stats_data
        }
        
        with open(file_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(export_data, jsonfile, indent=2, ensure_ascii=False)
