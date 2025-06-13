"""
Application settings management
"""

import json
import logging
from typing import Any, List, Optional
from PyQt5.QtCore import QSettings, QByteArray

from .constants import ORGANIZATION_NAME, APP_NAME, MAX_RECENT_FILES

logger = logging.getLogger(__name__)


class AppSettings:
    """Singleton class for managing application settings"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppSettings, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self._settings = QSettings(ORGANIZATION_NAME, APP_NAME)
        self._recent_files: List[str] = []
        self._theme_name: str = "Django"
        self._window_geometry: Optional[QByteArray] = None
        self._window_state: Optional[QByteArray] = None
        self._initialized = True
    
    @classmethod
    def instance(cls) -> 'AppSettings':
        """Get singleton instance"""
        return cls()
    
    def load(self) -> None:
        """Load settings from storage"""
        try:
            # Load recent files
            recent = self._settings.value("recentFiles", [])
            self._recent_files = recent if isinstance(recent, list) else []
            
            # Load theme
            self._theme_name = self._settings.value("theme", "Django")
            
            # Load window settings
            self._window_geometry = self._settings.value("windowGeometry")
            self._window_state = self._settings.value("windowState")
            
            logger.info("Settings loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load settings: {e}")
    
    def save(self) -> None:
        """Save settings to storage"""
        try:
            self._settings.setValue("recentFiles", self._recent_files)
            self._settings.setValue("theme", self._theme_name)
            
            if self._window_geometry:
                self._settings.setValue("windowGeometry", self._window_geometry)
            if self._window_state:
                self._settings.setValue("windowState", self._window_state)
            
            self._settings.sync()
            logger.info("Settings saved successfully")
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")
    
    # Recent files management
    def get_recent_files(self) -> List[str]:
        """Get list of recent files"""
        return self._recent_files.copy()
    
    def add_recent_file(self, file_path: str) -> None:
        """Add file to recent files list"""
        if file_path in self._recent_files:
            self._recent_files.remove(file_path)
        self._recent_files.insert(0, file_path)
        self._recent_files = self._recent_files[:MAX_RECENT_FILES]
        self.save()
    
    def remove_recent_file(self, file_path: str) -> None:
        """Remove file from recent files list"""
        if file_path in self._recent_files:
            self._recent_files.remove(file_path)
            self.save()
    
    # Theme management
    def get_theme(self) -> str:
        """Get current theme name"""
        return self._theme_name
    
    def set_theme(self, theme_name: str) -> None:
        """Set current theme"""
        self._theme_name = theme_name
        self.save()
    
    # Window settings
    def get_window_geometry(self) -> Optional[QByteArray]:
        """Get saved window geometry"""
        return self._window_geometry
    
    def set_window_geometry(self, geometry: QByteArray) -> None:
        """Save window geometry"""
        self._window_geometry = geometry
    
    def get_window_state(self) -> Optional[QByteArray]:
        """Get saved window state"""
        return self._window_state
    
    def set_window_state(self, state: QByteArray) -> None:
        """Save window state"""
        self._window_state = state

    def get_icon(self) -> str:
        """Get application icon path"""
        return "../wf.ico"