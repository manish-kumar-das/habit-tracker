"""
Theme System for Growthly
Provides light and dark mode theming

Usage:
    from app.themes import get_theme_manager
    
    theme = get_theme_manager()
    colors = theme.get_theme()
    logger.info(colors.BG_PRIMARY)
"""
import logging
logger = logging.getLogger(__name__)


from .light import LightTheme
from .dark import DarkTheme
from .manager import ThemeManager, get_theme_manager

__all__ = [
    'LightTheme',
    'DarkTheme',
    'ThemeManager',
    'get_theme_manager',
]

__version__ = '1.0.0'