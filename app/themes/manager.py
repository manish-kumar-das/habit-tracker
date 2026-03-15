"""
Theme Manager
Handles theme switching and persistence
"""
import logging
logger = logging.getLogger(__name__)

import json
import os
import sys
from .light import LightTheme
from .dark import DarkTheme


def _get_settings_path() -> str:
    """Return a writable path for settings.json that works both in development
    and when running as a PyInstaller frozen executable."""
    if getattr(sys, "frozen", False):
        data_dir = os.path.join(
            os.path.expanduser("~"), ".local", "share", "Growthly"
        )
    else:
        # Development: project root is three levels up from this file
        # (app/themes/manager.py  →  app/themes  →  app  →  project_root)
        data_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "settings.json")


_DEFAULT_SETTINGS_PATH = _get_settings_path()


class ThemeManager:
    """
    Manages application themes
    Singleton pattern - only one instance exists
    
    Usage:
        theme_manager = get_theme_manager()
        theme_manager.set_theme("dark")
        colors = theme_manager.get_theme()
    """
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern implementation"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize theme manager"""
        if self._initialized:
            return
        
        self.current_theme_name = "light"
        self.themes = {
            "light": LightTheme(),
            "dark": DarkTheme(),
        }
        self.current = self.themes["light"]
        self._initialized = True
        
        # Callbacks for theme changes
        self._callbacks = []
        
        logger.info(f"[ThemeManager] Initialized with {len(self.themes)} themes")
    
    def get_theme(self):
        """
        Get current theme object
        
        Returns:
            BaseTheme: Current theme instance (LightTheme or DarkTheme)
        """
        return self.current
    
    def get_theme_name(self):
        """
        Get current theme name
        
        Returns:
            str: "light" or "dark"
        """
        return self.current_theme_name
    
    def set_theme(self, theme_name):
        """
        Change to specific theme
        
        Args:
            theme_name (str): "light" or "dark"
        
        Returns:
            bool: True if theme changed, False if already active
        
        Raises:
            ValueError: If theme_name is not valid
        """
        if theme_name not in self.themes:
            raise ValueError(f"Unknown theme: {theme_name}. Available: {list(self.themes.keys())}")
        
        if theme_name == self.current_theme_name:
            logger.info(f"[ThemeManager] Theme '{theme_name}' already active")
            return False  # Already active
        
        logger.info(f"[ThemeManager] Switching from '{self.current_theme_name}' to '{theme_name}'")
        
        self.current_theme_name = theme_name
        self.current = self.themes[theme_name]
        
        # Notify all listeners
        self._notify_callbacks()
        
        return True
    
    def toggle_theme(self):
        """
        Switch between light and dark
        
        Returns:
            str: New theme name
        """
        new_theme = "dark" if self.current_theme_name == "light" else "light"
        self.set_theme(new_theme)
        return new_theme
    
    def is_dark_mode(self):
        """
        Check if dark mode is active
        
        Returns:
            bool: True if dark mode, False if light mode
        """
        return self.current_theme_name == "dark"
    
    def register_callback(self, callback):
        """
        Register function to be called when theme changes
        
        Args:
            callback (callable): Function that takes theme_name as argument
                                 Example: def on_theme_change(theme_name): ...
        """
        if callback not in self._callbacks:
            self._callbacks.append(callback)
            logger.info(f"[ThemeManager] Registered callback: {callback.__name__}")
    
    def unregister_callback(self, callback):
        """
        Remove theme change callback
        
        Args:
            callback (callable): Previously registered callback function
        """
        if callback in self._callbacks:
            self._callbacks.remove(callback)
            logger.info(f"[ThemeManager] Unregistered callback: {callback.__name__}")
    
    def _notify_callbacks(self):
        """Notify all registered callbacks of theme change"""
        logger.info(f"[ThemeManager] Notifying {len(self._callbacks)} callbacks")
        for callback in self._callbacks:
            try:
                callback(self.current_theme_name)
            except Exception as e:
                logger.info(f"[ThemeManager] Error in callback {callback.__name__}: {e}")
    
    def save_preference(self, settings_path=None):
        if settings_path is None:
            settings_path = _DEFAULT_SETTINGS_PATH
        """
        Save theme preference to disk
        
        Args:
            settings_path (str): Path to settings file
        
        Returns:
            bool: True if saved successfully
        """
        try:
            settings = {}
            
            # Load existing settings if file exists
            if os.path.exists(settings_path):
                with open(settings_path, 'r') as f:
                    settings = json.load(f)
            
            # Update theme preference
            settings['theme'] = self.current_theme_name
            
            # Save to disk
            with open(settings_path, 'w') as f:
                json.dump(settings, f, indent=2)
            
            logger.info(f"[ThemeManager] Saved preference: {self.current_theme_name} to {settings_path}")
            return True
            
        except Exception as e:
            logger.info(f"[ThemeManager] Error saving preference: {e}")
            return False
    
    def load_preference(self, settings_path=None):
        if settings_path is None:
            settings_path = _DEFAULT_SETTINGS_PATH
        """
        Load theme preference from disk
        
        Args:
            settings_path (str): Path to settings file
        
        Returns:
            bool: True if theme was loaded, False otherwise
        """
        if not os.path.exists(settings_path):
            logger.info(f"[ThemeManager] No settings file found at {settings_path}")
            return False
        
        try:
            with open(settings_path, 'r') as f:
                settings = json.load(f)
            
            if 'theme' in settings:
                theme_name = settings['theme']
                logger.info(f"[ThemeManager] Loaded preference: {theme_name}")
                self.set_theme(theme_name)
                return True
            else:
                logger.info("[ThemeManager] No theme preference in settings")
                return False
                
        except Exception as e:
            logger.info(f"[ThemeManager] Error loading preference: {e}")
            return False
    
    def get_available_themes(self):
        """
        Get list of available theme names
        
        Returns:
            list: Available theme names
        """
        return list(self.themes.keys())
    
    def add_custom_theme(self, name, theme_instance):
        """
        Add a custom theme (for future extensibility)
        
        Args:
            name (str): Theme name
            theme_instance (BaseTheme): Theme instance
        
        Raises:
            ValueError: If theme doesn't inherit from BaseTheme
        """
        from .base_theme import BaseTheme
        
        if not isinstance(theme_instance, BaseTheme):
            raise ValueError("Theme must inherit from BaseTheme")
        
        # Validate theme has all required colors
        theme_instance.validate()
        
        self.themes[name] = theme_instance
        logger.info(f"[ThemeManager] Added custom theme: {name}")


# Global singleton instance
_theme_manager = None


def get_theme_manager():
    """
    Get global theme manager instance
    
    Returns:
        ThemeManager: Global theme manager singleton
    
    Usage:
        from app.themes import get_theme_manager
        
        theme = get_theme_manager()
        theme.set_theme("dark")
    """
    global _theme_manager
    if _theme_manager is None:
        _theme_manager = ThemeManager()
    return _theme_manager