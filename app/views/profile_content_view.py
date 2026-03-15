"""
Profile Content View — Clean Single-Page SaaS Dashboard
No scroll. Fits in one window. Minimal & professional.
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QLineEdit,
    QTextEdit,
    QMessageBox,
    QGraphicsDropShadowEffect,
    QSizePolicy,
    QFileDialog,
)
import os
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QColor
from app.services.habit_service import get_habit_service
from app.services.streak_service import get_streak_service
from app.services.profile_service import get_profile_service
from app.views.crop_dialog import CropDialog
from app.utils.image_utils import get_circular_pixmap
from app.themes import get_theme_manager


def _shadow(parent=None, blur=14, y=3, alpha=10):
    s = QGraphicsDropShadowEffect(parent)
    s.setBlurRadius(blur)
    s.setOffset(0, y)
    s.setColor(QColor(0, 0, 0, alpha))
    return s


# ═══════════════════════════════════════════════════════════
#  Stat Card
# ═══════════════════════════════════════════════════════════
class StatCard(QFrame):
    def __init__(self, icon, value, label, accent, parent=None):
        super().__init__(parent)
        from app.themes import get_theme_manager
        self.theme_manager = get_theme_manager()
        self.accent = accent
        self.icon = icon
        self.value = value
        self.label = label
        self.setObjectName("statCard")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.setGraphicsEffect(_shadow(self, blur=12, y=3, alpha=8))

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(8)

        # Icon circle
        self.icon_bg = QFrame()
        self.icon_bg.setFixedSize(44, 44)
        ic_lay = QVBoxLayout(self.icon_bg)
        ic_lay.setContentsMargins(0, 0, 0, 0)
        ic_lay.setAlignment(Qt.AlignCenter)
        self.ic_lbl = QLabel(icon)
        self.ic_lbl.setFont(QFont("SF Pro Display", 20))
        ic_lay.addWidget(self.ic_lbl)
        root.addWidget(self.icon_bg)

        root.addStretch()

        # Value
        self.val_lbl = QLabel(value)
        self.val_lbl.setFont(QFont("SF Pro Display", 26, QFont.Bold))
        root.addWidget(self.val_lbl)

        # Label
        self.cap = QLabel(label.upper())
        self.cap.setFont(QFont("Inter", 10, QFont.DemiBold))
        root.addWidget(self.cap)
        
        self.apply_theme()

    def apply_theme(self):
        is_dark = self.theme_manager.is_dark_mode()
        bg_card = "#2A2D38" if is_dark else "#FFFFFF"
        border_color = "#333645" if is_dark else "#E5E7EB"
        text_val = "#F3F4F6" if is_dark else "#111827"
        text_cap = "#9CA3AF" if is_dark else "#6B7280"
        
        self.setStyleSheet(f"""
            QFrame#statCard {{
                background-color: {bg_card};
                border: 1px solid {border_color};
                border-radius: 16px;
            }}
        """)
        
        self.icon_bg.setStyleSheet(f"""
            background-color: {self.accent}14;
            border-radius: 12px; border: none;
        """)
        
        self.ic_lbl.setStyleSheet("background:transparent; border:none;")
        self.val_lbl.setStyleSheet(f"color:{text_val}; background:transparent; border:none;")
        self.cap.setStyleSheet(f"color:{text_cap}; letter-spacing:0.6px; background:transparent; border:none;")

    def enterEvent(self, ev):
        is_dark = self.theme_manager.is_dark_mode()
        bg_card = "#2A2D38" if is_dark else "#FFFFFF"
        self.setStyleSheet(f"""
            QFrame#statCard {{
                background-color: {bg_card};
                border: 1px solid {self.accent}40;
                border-radius: 16px;
            }}
        """)
        super().enterEvent(ev)

    def leaveEvent(self, ev):
        self.apply_theme()
        super().leaveEvent(ev)


# ═══════════════════════════════════════════════════════════
#  Main Profile View — single page, no scroll
# ═══════════════════════════════════════════════════════════
class ProfileContentView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.habit_service = get_habit_service()
        self.streak_service = get_streak_service()
        self.profile_service = get_profile_service()
        self.theme_manager = get_theme_manager()
        self.setup_ui()
        self.load_profile_data()

    def setup_ui(self):
        colors = self.theme_manager.get_theme()
        self.setStyleSheet(f"background-color: {colors.BG_PRIMARY};")

        main = QVBoxLayout(self)
        main.setContentsMargins(40, 28, 40, 28)
        main.setSpacing(16)

        # ═══════════════════════════════════════════════
        # 1. HEADER — Avatar + Name only
        # ═══════════════════════════════════════════════
        is_dark = self.theme_manager.is_dark_mode()
        self.header = QFrame()
        self.header.setObjectName("headerCard")
        bg_card = "#252732" if is_dark else colors.BG_PRIMARY
        border_card = "#333645" if is_dark else "#E5E7EB"
        self.header.setStyleSheet(f"""
            QFrame#headerCard {{
                background-color: {bg_card};
                border: 1px solid {border_card};
                border-radius: 20px;
            }}
            QLabel {{ background:transparent; border:none; }}
        """)
        self.header.setGraphicsEffect(_shadow(self.header))

        h_lay = QHBoxLayout(self.header)
        h_lay.setContentsMargins(32, 24, 32, 24)
        h_lay.setSpacing(20)

        # Avatar — 94px Container
        self.av_container = QFrame()
        self.av_container.setFixedSize(94, 94)
        self.av_container.setStyleSheet("background: transparent; border: none;")
        self.av_container.setGraphicsEffect(_shadow(self.av_container, blur=12, y=4, alpha=15))
        
        av_l = QVBoxLayout(self.av_container)
        av_l.setContentsMargins(2, 2, 2, 2) # Padding for the border
        av_l.setAlignment(Qt.AlignCenter)
        
        self.av_label = QLabel()
        self.av_label.setFixedSize(90, 90)
        self.av_label.setAlignment(Qt.AlignCenter)
        self.av_label.setScaledContents(True)
        av_bg = "#252732" if is_dark else "#F3F4F6"
        av_border = "#333645" if is_dark else "#E5E7EB"
        self.av_label.setStyleSheet(f"""
            background-color: {av_bg};
            border: 2px solid {av_border};
            border-radius: 45px;
        """)
        
        self.av_icon = QLabel("👤")
        self.av_icon.setFont(QFont("SF Pro Display", 42))
        self.av_icon.setAlignment(Qt.AlignCenter)
        self.av_icon.setStyleSheet("background: transparent; border: none;")
        
        av_l.addWidget(self.av_label)
        
        # Icon overlay
        self.av_icon.setParent(self.av_label)
        self.av_icon.setGeometry(0, 0, 90, 90)
        
        # Change photo button (overlay)
        self.change_av_btn = QPushButton("📷")
        self.change_av_btn.setParent(self.av_container)
        self.change_av_btn.setFixedSize(32, 32)
        self.change_av_btn.move(62, 62)
        self.change_av_btn.setCursor(Qt.PointingHandCursor)
        self.change_av_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                border: 2px solid #E5E7EB;
                border-radius: 16px;
                font-size: 14px;
                padding-bottom: 2px;
            }
            QPushButton:hover {
                background-color: #F9FAFB;
                border: 2px solid #7C3AED;
            }
        """)
        self.change_av_btn.clicked.connect(self.select_avatar)
        
        h_lay.addWidget(self.av_container)

        # Name
        self.name_header = QLabel("Loading…")
        self.name_header.setFont(QFont("SF Pro Display", 30, QFont.Bold))
        text_primary = "#F3F4F6" if is_dark else "#111827"
        self.name_header.setStyleSheet(f"color:{text_primary}; letter-spacing:-0.3px;")
        h_lay.addWidget(self.name_header, stretch=1)

        main.addWidget(self.header)

        # ═══════════════════════════════════════════════
        # 2. STAT CARDS ROW
        # ═══════════════════════════════════════════════
        self.stats_row = QHBoxLayout()
        self.stats_row.setSpacing(12)
        main.addLayout(self.stats_row)

        # ═══════════════════════════════════════════════
        # 3. ACCOUNT SETTINGS
        # ═══════════════════════════════════════════════
        self.form = QFrame()
        self.form.setObjectName("formCard")
        bg_form = "#252732" if is_dark else colors.BG_PRIMARY
        border_form = "#333645" if is_dark else "#E5E7EB"
        self.form.setStyleSheet(f"""
            QFrame#formCard {{
                background-color: {bg_form};
                border: 1px solid {border_form};
                border-radius: 20px;
            }}
            QLabel {{ background:transparent; border:none; }}
        """)
        self.form.setGraphicsEffect(_shadow(self.form))

        f_lay = QVBoxLayout(self.form)
        f_lay.setContentsMargins(32, 28, 32, 28)
        f_lay.setSpacing(16)

        self.form_title = QLabel("Account Settings")
        self.form_title.setFont(QFont("SF Pro Display", 22, QFont.DemiBold))
        title_color = "#F3F4F6" if is_dark else "#111827"
        self.form_title.setStyleSheet(f"color:{title_color};")
        f_lay.addWidget(self.form_title)

        # Input fields
        self.fields_containers = {}
        self.inputs = {}
        self.inputs["name"] = self._add_field("name", "Full Display Name", "👤", f_lay)
        self.inputs["email"] = self._add_field("email", "Email Address", "📧", f_lay)
        self.inputs["bio"] = self._add_field("bio", "Short Bio", "📝", f_lay, multiline=True)

        # Save button
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        self.save_btn = QPushButton("Save Changes")
        self.save_btn.setFixedWidth(200)
        self.save_btn.setFixedHeight(44)
        self.save_btn.setFont(QFont("Inter", 13, QFont.Bold))
        self.save_btn.setCursor(Qt.PointingHandCursor)
        # Saturated vibrant purple gradient identity
        grad_start = "#4450E6" if is_dark else "#7C3AED"
        grad_end = "#5B7CFF" if is_dark else "#6D28D9"
        
        self.save_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 {grad_start}, stop:1 {grad_end});
                color: #FFFFFF; border: none; border-radius: 22px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #5C6BC0, stop:1 #4A5FCF);
            }}
        """)
        self.save_btn.clicked.connect(self.save_profile)
        btn_row.addWidget(self.save_btn)
        btn_row.addStretch()
        f_lay.addLayout(btn_row)

        main.addWidget(self.form)
        main.addStretch()

    def apply_theme(self):
        """Apply theme dynamically"""
        colors = self.theme_manager.get_theme()
        is_dark = self.theme_manager.is_dark_mode()
        
        bg_page = "#1A1C23" if is_dark else colors.BG_PRIMARY
        bg_card = "#252732" if is_dark else colors.BG_PRIMARY
        border_color = "#333645" if is_dark else "#E5E7EB"
        text_primary = "#F3F4F6" if is_dark else colors.TEXT_PRIMARY
        
        self.setStyleSheet(f"background-color: {bg_page};")
        
        if hasattr(self, 'header'):
            self.header.setStyleSheet(f"""
                QFrame#headerCard {{
                    background-color: {bg_card};
                    border: 1px solid {border_color};
                    border-radius: 20px;
                }}
                QLabel {{ background:transparent; border:none; }}
            """)
            
        if hasattr(self, 'form'):
            self.form.setStyleSheet(f"""
                QFrame#formCard {{
                    background-color: {bg_card};
                    border: 1px solid {border_color};
                    border-radius: 20px;
                }}
                QLabel {{ background:transparent; border:none; }}
            """)
            
        if hasattr(self, 'name_header'):
            self.name_header.setStyleSheet(f"color: {text_primary}; letter-spacing:-0.3px;")
            
        if hasattr(self, 'form_title'):
            self.form_title.setStyleSheet(f"color: {text_primary};")

        # Refresh metric cards
        for i in range(self.stats_row.count()):
            item = self.stats_row.itemAt(i)
            if item and item.widget():
                item.widget().apply_theme()
        
        # Refresh inputs
        if hasattr(self, 'fields_containers'):
            for field_name in ["name", "email", "bio"]:
                if field_name in self.fields_containers:
                    container, ic, edit, lbl = self.fields_containers[field_name]
                    bg_input = "#1A1C23" if is_dark else "#FFFFFF"
                    border_input = "#333645" if is_dark else "#E5E7EB"
                    container.setStyleSheet(f"""
                        QFrame#inputRow {{
                            background-color: {bg_input};
                            border: 1.5px solid {border_input};
                            border-radius: 12px;
                        }}
                        QFrame#inputRow:hover {{ border: 1.5px solid {"#4450E6" if is_dark else "#D1D5DB"}; }}
                    """)
                    
                    ic_bg = "rgba(255, 255, 255, 0.05)" if is_dark else "transparent"
                    ic.setStyleSheet(f"color:#9CA3AF; background:{ic_bg}; border-radius:4px;")
                    
                    text_input = "#9CA3AF" if is_dark else "#1E293B"
                    edit.setStyleSheet(f"border:none; background:transparent; font-size:14px; color:{text_input}; font-family:Inter;")
                    
                    label_color = "#9CA3AF" if is_dark else "#6B7280"
                    lbl.setStyleSheet(f"color:{label_color}; letter-spacing:0.5px;")

        # Refresh save button
        orig = self.save_btn.text()
        if "✓" not in orig: # Only if not in saved state
            grad_start = "#4450E6" if is_dark else "#7C3AED"
            grad_end = "#5B7CFF" if is_dark else "#6D28D9"
            self.save_btn.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                        stop:0 {grad_start}, stop:1 {grad_end});
                    color: #FFFFFF; border: none; border-radius: 22px;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                        stop:0 #5C6BC0, stop:1 #4A5FCF);
                }}
            """)

    # ─── field builder ───────────────────────────────
    def _add_field(self, field_id, label_text, icon, parent_layout, multiline=False):
        if not hasattr(self, 'fields_containers'):
            self.fields_containers = {}
            
        is_dark = self.theme_manager.is_dark_mode()
        group = QVBoxLayout()
        group.setSpacing(4)

        lbl = QLabel(label_text.upper())
        lbl.setFont(QFont("Inter", 10, QFont.Bold))
        label_color = "#9CA3AF" if is_dark else "#6B7280"
        lbl.setStyleSheet(f"color:{label_color}; letter-spacing:0.5px;")
        group.addWidget(lbl)

        container = QFrame()
        container.setObjectName("inputRow")
        bg_input = "#1A1C23" if is_dark else "#FFFFFF"
        border_input = "#333645" if is_dark else "#E5E7EB"
        container.setStyleSheet(f"""
            QFrame#inputRow {{
                background-color: {bg_input};
                border: 1.5px solid {border_input};
                border-radius: 12px;
            }}
            QFrame#inputRow:hover {{ border: 1.5px solid {"#4450E6" if is_dark else "#D1D5DB"}; }}
        """)

        row = QHBoxLayout(container)
        row.setContentsMargins(12, 2, 12, 2)
        row.setSpacing(8)

        ic = QLabel(icon)
        ic.setFont(QFont("SF Pro Display", 15))
        ic_bg = "rgba(255, 255, 255, 0.05)" if is_dark else "transparent"
        ic.setStyleSheet(f"color:#9CA3AF; background:{ic_bg}; border-radius:4px;")
        ic.setFixedWidth(26)
        ic.setAlignment(Qt.AlignCenter)
        row.addWidget(ic)

        text_color = "#9CA3AF" if is_dark else "#1E293B"
        if multiline:
            container.setFixedHeight(64)
            row.setAlignment(Qt.AlignTop)
            row.setContentsMargins(12, 10, 12, 2)
            edit = QTextEdit()
            edit.setFixedHeight(48)
            edit.setStyleSheet(
                f"border:none; background:transparent; font-size:14px; color:{text_color}; font-family:Inter;"
            )
        else:
            edit = QLineEdit()
            edit.setFixedHeight(40)
            edit.setStyleSheet(
                f"border:none; background:transparent; font-size:14px; color:{text_color}; font-family:Inter;"
            )

        row.addWidget(edit, stretch=1)
        group.addWidget(container)
        parent_layout.addLayout(group)
        self.fields_containers[field_id] = (container, ic, edit, lbl)
        return edit

    # ─── data ────────────────────────────────────────
    def load_profile_data(self):
        profile = self.profile_service.get_profile()
        self.name_header.setText(profile["name"])
        self.inputs["name"].setText(profile["name"])
        self.inputs["email"].setText(profile["email"])
        self.inputs["bio"].setText(profile["bio"])
        self.set_avatar_image(profile.get("avatar_path"))
        self._refresh_stats()

    def set_avatar_image(self, path):
        is_dark = self.theme_manager.is_dark_mode()
        av_border = "#333645" if is_dark else "#E5E7EB"
        if path and os.path.exists(path):
            pix = get_circular_pixmap(path, 90)
            if pix:
                self.av_label.setPixmap(pix)
                self.av_label.setStyleSheet(f"background: transparent; border: 1px solid {av_border}; border-radius: 45px;")
                self.av_icon.hide()
            else:
                self.av_icon.show()
                self._reset_avatar_style()
        else:
            self.av_label.clear()
            self.av_icon.show()
            self._reset_avatar_style()

    def _reset_avatar_style(self):
        is_dark = self.theme_manager.is_dark_mode()
        av_bg = "#252732" if is_dark else "#F3F4F6"
        av_border = "#333645" if is_dark else "#E5E7EB"
        self.av_label.setStyleSheet(f"""
            background-color: {av_bg};
            border: 2px solid {av_border};
            border-radius: 45px;
        """)

    def select_avatar(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Profile Photo", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if path:
            dialog = CropDialog(path, self)
            if dialog.exec():
                cropped_path = dialog.final_path
                self.profile_service.update_profile(avatar_path=cropped_path)
                self.set_avatar_image(cropped_path)
                if self.main_window and hasattr(self.main_window, "sidebar"):
                    self.main_window.sidebar.update_profile_avatar(cropped_path)

    def _refresh_stats(self):
        habits = self.habit_service.get_all_habits()

        total_habits = len(habits)
        total_xp = sum(
            len(self.habit_service.get_habit_completions(h.id)) for h in habits
        )
        best_streak = max(
            [self.streak_service.get_streak_info(h.id)["current_streak"]
             for h in habits] + [0]
        )

        # Clear previous cards
        while self.stats_row.count():
            item = self.stats_row.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        cards = [
            ("🎯", str(total_habits), "Habits", "#10B981"),
            ("🚀", str(total_xp), "Total XP", "#7C3AED"),
            ("🔥", str(best_streak), "Best Streak", "#F59E0B"),
        ]
        for icon, val, lbl, accent in cards:
            self.stats_row.addWidget(StatCard(icon, val, lbl, accent))

    # ─── save ────────────────────────────────────────
    def save_profile(self):
        name = self.inputs["name"].text().strip()
        email = self.inputs["email"].text().strip()
        bio = self.inputs["bio"].toPlainText().strip()

        if not name:
            QMessageBox.warning(self, "Validation Error",
                                "Please provide a valid display name.")
            return

        try:
            self.profile_service.update_profile(name=name, email=email, bio=bio)
            self.name_header.setText(name)

            if self.main_window and hasattr(self.main_window, "sidebar"):
                self.main_window.sidebar.update_profile_name(name)

            orig = self.save_btn.text()
            self.save_btn.setText("✓  Saved!")
            self.save_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                        stop:0 #10B981, stop:1 #059669);
                    color:#FFFFFF; border:none; border-radius:22px;
                }
            """)
            QTimer.singleShot(1800, lambda: self._reset_btn(orig))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Unexpected error: {str(e)}")

    def _reset_btn(self, text):
        try:
            # Guard: the widget may have been destroyed before the timer fires
            # (e.g. user navigated away). Accessing a deleted C++ object raises
            # RuntimeError in PySide6, so we catch and silently ignore it.
            _ = self.save_btn.text()
        except RuntimeError:
            return
        is_dark = self.theme_manager.is_dark_mode()
        self.save_btn.setText(text)
        grad_start = "#4450E6" if is_dark else "#7C3AED"
        grad_end = "#5B7CFF" if is_dark else "#6D28D9"
        
        self.save_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 {grad_start}, stop:1 {grad_end});
                color:#FFFFFF; border:none; border-radius:22px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #5C6BC0, stop:1 #4A5FCF);
            }}
        """)
