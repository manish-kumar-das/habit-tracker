"""Growthly - Habit Tracking Application"""
__version__ = '1.0.0'

# Core imports
from app import main
from app.themes import get_theme_manager, LightTheme, DarkTheme

__all__ = ['main', 'get_theme_manager', 'LightTheme', 'DarkTheme']
