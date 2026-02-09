"""
Theme definitions for light and dark modes
"""

DARK_THEME = """
/* Dark Theme */
QMainWindow {
    background-color: #0F1115;
}

QWidget {
    background-color: transparent;
}

QMenuBar {
    background-color: #1C1F26;
    border-bottom: 1px solid #2A2D35;
    padding: 6px;
    color: #E4E6EB;
}

QMenuBar::item {
    padding: 8px 12px;
    background: transparent;
    color: #E4E6EB;
    border-radius: 6px;
}

QMenuBar::item:selected {
    background-color: #4FD1C5;
    color: #0F1115;
}

QMenu {
    background-color: #1C1F26;
    border: 1px solid #2A2D35;
    border-radius: 8px;
    padding: 8px;
    color: #E4E6EB;
}

QMenu::item {
    padding: 10px 24px;
    border-radius: 6px;
    color: #E4E6EB;
}

QMenu::item:selected {
    background-color: #20232B;
    color: #4FD1C5;
}

QStatusBar {
    background-color: #1C1F26;
    border-top: 1px solid #2A2D35;
    color: #9AA0A6;
    padding: 6px 12px;
}

QScrollBar:vertical {
    border: none;
    background: #0F1115;
    width: 8px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #4A4D56;
    min-height: 30px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: #4FD1C5;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QMessageBox {
    background-color: #1C1F26;
}

QMessageBox QLabel {
    color: #E4E6EB;
}

QDialog {
    background-color: #1C1F26;
}
"""

LIGHT_THEME = """
/* Light Theme */
QMainWindow {
    background-color: #F5F6FA;
}

QWidget {
    background-color: transparent;
}

QMenuBar {
    background-color: #FFFFFF;
    border-bottom: 1px solid #E0E0E0;
    padding: 6px;
    color: #2C3E50;
}

QMenuBar::item {
    padding: 8px 12px;
    background: transparent;
    color: #2C3E50;
    border-radius: 6px;
}

QMenuBar::item:selected {
    background-color: #4FD1C5;
    color: #FFFFFF;
}

QMenu {
    background-color: #FFFFFF;
    border: 1px solid #E0E0E0;
    border-radius: 8px;
    padding: 8px;
    color: #2C3E50;
}

QMenu::item {
    padding: 10px 24px;
    border-radius: 6px;
    color: #2C3E50;
}

QMenu::item:selected {
    background-color: #F0F0F0;
    color: #4FD1C5;
}

QStatusBar {
    background-color: #FFFFFF;
    border-top: 1px solid #E0E0E0;
    color: #7F8C8D;
    padding: 6px 12px;
}

QScrollBar:vertical {
    border: none;
    background: #F5F6FA;
    width: 8px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #BDC3C7;
    min-height: 30px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: #4FD1C5;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QMessageBox {
    background-color: #FFFFFF;
}

QMessageBox QLabel {
    color: #2C3E50;
}

QDialog {
    background-color: #FFFFFF;
}
"""


def get_dark_colors():
    """Get dark theme color palette"""
    return {
        'bg_primary': '#0F1115',
        'bg_secondary': '#1C1F26',
        'bg_tertiary': '#20232B',
        'border': '#2A2D35',
        'border_hover': '#4FD1C5',
        'text_primary': '#E4E6EB',
        'text_secondary': '#9AA0A6',
        'text_tertiary': '#6B6E76',
        'accent_primary': '#4FD1C5',
        'accent_secondary': '#7C83FD',
        'success': '#6FCF97',
        'warning': '#F2C94C',
        'danger': '#EF5350',
    }


def get_light_colors():
    """Get light theme color palette"""
    return {
        'bg_primary': '#F5F6FA',
        'bg_secondary': '#FFFFFF',
        'bg_tertiary': '#F8F9FA',
        'border': '#E0E0E0',
        'border_hover': '#4FD1C5',
        'text_primary': '#2C3E50',
        'text_secondary': '#7F8C8D',
        'text_tertiary': '#95A5A6',
        'accent_primary': '#4FD1C5',
        'accent_secondary': '#7C83FD',
        'success': '#27AE60',
        'warning': '#F39C12',
        'danger': '#E74C3C',
    }


def apply_theme(widget, theme_name):
    """Apply theme to a widget"""
    if theme_name == 'light':
        widget.setStyleSheet(LIGHT_THEME)
    else:
        widget.setStyleSheet(DARK_THEME)
