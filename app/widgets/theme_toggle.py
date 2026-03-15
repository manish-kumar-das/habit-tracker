"""
Theme Toggle Button
Button widget to switch between light and dark mode
"""
import logging
logger = logging.getLogger(__name__)

from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt, Signal, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont


class ThemeToggleButton(QPushButton):
    """
    Toggle button for switching themes
    Shows moon icon in light mode, sun icon in dark mode
    
    Signals:
        theme_changed(str): Emitted when theme changes ("light" or "dark")
    
    Usage:
        toggle = ThemeToggleButton()
        toggle.theme_changed.connect(on_theme_changed)
    """
    
    theme_changed = Signal(str)  # Emits "light" or "dark"
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_dark = False
        self._setup_button()
    
    def _setup_button(self):
        """Setup button appearance and behavior"""
        self.setFixedSize(44, 44)
        self.setCursor(Qt.PointingHandCursor)
        self.setToolTip("Toggle Dark Mode")
        self.clicked.connect(self._on_clicked)
        self._update_appearance()
    
    def _update_appearance(self):
        """Update button icon and style based on current theme"""
        if self.is_dark:
            # Show moon icon
            self.setText("🌙")
            self.setStyleSheet("""
                QPushButton {
                    background-color: #2D3748;
                    border: 2px solid #374151;
                    border-radius: 22px;
                    font-size: 20px;
                }
                QPushButton:hover {
                    background-color: #374151;
                    border: 2px solid #4B5563;
                }
                QPushButton:pressed {
                    background-color: #1F2937;
                }
            """)
        else:
            # Show sun icon
            self.setText("☀️")
            self.setStyleSheet("""
                QPushButton {
                    background-color: #FFFFFF;
                    border: 2px solid #E2E8F0;
                    border-radius: 22px;
                    font-size: 20px;
                }
                QPushButton:hover {
                    background-color: #F8FAFC;
                    border: 2px solid #CBD5E1;
                }
                QPushButton:pressed {
                    background-color: #F1F5F9;
                }
            """)
    
    def _on_clicked(self):
        """Handle button click - toggle theme"""
        self.is_dark = not self.is_dark
        self._update_appearance()
        
        theme_name = "dark" if self.is_dark else "light"
        logger.info(f"[ThemeToggle] Toggled to: {theme_name}")
        
        self.theme_changed.emit(theme_name)
    
    def set_theme(self, is_dark):
        """
        Set theme programmatically (without emitting signal)
        
        Args:
            is_dark (bool): True for dark mode, False for light mode
        """
        if self.is_dark != is_dark:
            self.is_dark = is_dark
            self._update_appearance()
    
    def get_current_theme(self):
        """
        Get current theme name
        
        Returns:
            str: "light" or "dark"
        """
        return "dark" if self.is_dark else "light"


class AnimatedThemeToggle(ThemeToggleButton):
    """
    Enhanced theme toggle with rotation animation
    Button rotates when clicked for better visual feedback
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.animation = None
    
    def _on_clicked(self):
        """Handle click with rotation animation"""
        # Rotate button
        self._animate_rotation()
        
        # Call parent implementation
        super()._on_clicked()
    
    def _animate_rotation(self):
        """Animate button rotation on click"""
        # Note: QPropertyAnimation on rotation requires more complex setup
        # For simplicity, using a visual effect instead
        
        # Visual feedback: slight scale animation
        original_size = self.size()
        
        # Quick scale down
        QTimer.singleShot(0, lambda: self.setFixedSize(40, 40))
        
        # Scale back up
        QTimer.singleShot(100, lambda: self.setFixedSize(44, 44))