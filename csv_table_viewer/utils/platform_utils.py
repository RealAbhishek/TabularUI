"""
Platform-specific utilities
"""

import sys
import logging
from PyQt5.QtWidgets import QMainWindow

logger = logging.getLogger(__name__)


def configure_platform_specific():
    """Configure platform-specific settings"""
    if sys.platform == "win32":
        # Windows-specific configuration
        import ctypes
        try:
            # Enable DPI awareness
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception as e:
            logger.warning(f"Failed to set DPI awareness: {e}")
    
    elif sys.platform == "darwin":
        # macOS-specific configuration
        pass
    
    elif sys.platform.startswith("linux"):
        # Linux-specific configuration
        pass


def apply_window_theme(window: QMainWindow, theme_name: str):
    """Apply platform-specific window theme"""
    if sys.platform == "win32":
        try:
            import ctypes
            
            # Windows 10/11 dark title bar
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            hwnd = int(window.winId())
            
            # Enable dark mode for dark themes
            is_dark = theme_name == "Django"
            value = ctypes.c_int(1 if is_dark else 0)
            
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd,
                DWMWA_USE_IMMERSIVE_DARK_MODE,
                ctypes.byref(value),
                ctypes.sizeof(value)
            )
            
            logger.info(f"Applied Windows theme: {'dark' if is_dark else 'light'}")
            
        except Exception as e:
            logger.warning(f"Failed to apply Windows theme: {e}")