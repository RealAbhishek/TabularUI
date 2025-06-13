"""
Theme controller
"""

import logging
from PyQt5.QtWidgets import QMainWindow, QWidget

from core import ThemeManager
from utils.platform_utils import apply_window_theme

logger = logging.getLogger(__name__)


class ThemeController:
    """Controller for theme management"""
    
    def apply_theme(self, window: QMainWindow, theme_name: str):
        """Apply theme to window"""
        theme = ThemeManager.create_theme(theme_name)
        if not theme:
            logger.warning(f"Theme not found: {theme_name}")
            return
        
        window.setStyleSheet(theme.get_stylesheet())
        
        apply_window_theme(window, theme_name)
        
        logger.info(f"Applied theme: {theme_name}")