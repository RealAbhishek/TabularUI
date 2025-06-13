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
        import ctypes
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception as e:
            logger.warning(f"Failed to set DPI awareness: {e}")
    
    elif sys.platform == "darwin":
        pass
    
    elif sys.platform.startswith("linux"):
        pass


def apply_window_theme(window: QMainWindow, theme_name: str):
    """Apply platform-specific window theme"""
    if sys.platform == "win32":
        try:
            import ctypes

            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            hwnd = int(window.winId())

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