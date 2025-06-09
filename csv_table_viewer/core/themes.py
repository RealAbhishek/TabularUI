"""
Theme management for the application
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class Theme(ABC):
    """Abstract base class for themes"""
    
    @abstractmethod
    def get_name(self) -> str:
        """Get theme name"""
        pass
    
    @abstractmethod
    def get_colors(self) -> Dict[str, str]:
        """Get theme colors"""
        pass
    
    @abstractmethod
    def get_stylesheet(self) -> str:
        """Get complete stylesheet for the theme"""
        pass


class DjangoTheme(Theme):
    """Django-inspired dark green theme"""
    
    def get_name(self) -> str:
        return "Django"
    
    def get_colors(self) -> Dict[str, str]:
        return {
            "main_bg": "#092e20",
            "main_fg": "white",
            "accent": "#44b78b",
            "table_bg": "#1e1e1e",
            "table_fg": "#d4d4d4",
            "table_grid": "#3c3c3c",
            "table_selection": "#264f78",
            "table_alternate": "#2d2d2d",
            "menu_bg": "#092e20",
            "menu_hover": "#44b78b",
            "input_bg": "#0d4029",
            "button_bg": "#44b78b",
            "button_hover": "#5ec49e",
            "scrollbar_bg": "#092e20",
            "scrollbar_handle": "#44b78b",
            "scrollbar_handle_hover": "#5ec49e"
        }
    
    def get_stylesheet(self) -> str:
        colors = self.get_colors()
        return f"""
        QMainWindow {{
            background-color: {colors['main_bg']};
            color: {colors['main_fg']};
        }}
        QWidget {{
            background-color: {colors['main_bg']};
            color: {colors['main_fg']};
        }}
        QMenuBar {{
            background-color: {colors['menu_bg']};
            color: {colors['main_fg']};
            border: 1px solid {colors['accent']};
        }}
        QMenuBar::item {{
            background-color: transparent;
            padding: 4px 12px;
            color: {colors['main_fg']};
        }}
        QMenuBar::item:selected {{
            background-color: {colors['menu_hover']};
        }}
        QMenu {{
            background-color: {colors['menu_bg']};
            color: {colors['main_fg']};
            border: 1px solid {colors['accent']};
        }}
        QMenu::item {{
            padding: 4px 20px;
            color: {colors['main_fg']};
        }}
        QMenu::item:selected {{
            background-color: {colors['menu_hover']};
        }}
        QScrollBar:vertical {{
            background-color: {colors['scrollbar_bg']};
            width: 15px;
            border: 1px solid {colors['accent']};
        }}
        QScrollBar::handle:vertical {{
            background-color: {colors['scrollbar_handle']};
            min-height: 20px;
            border-radius: 2px;
        }}
        QScrollBar::handle:vertical:hover {{
            background-color: {colors['scrollbar_handle_hover']};
        }}
        QScrollBar:horizontal {{
            background-color: {colors['scrollbar_bg']};
            height: 15px;
            border: 1px solid {colors['accent']};
        }}
        QScrollBar::handle:horizontal {{
            background-color: {colors['scrollbar_handle']};
            min-width: 20px;
            border-radius: 2px;
        }}
        QScrollBar::handle:horizontal:hover {{
            background-color: {colors['scrollbar_handle_hover']};
        }}
        QScrollBar::add-line, QScrollBar::sub-line {{
            background: none;
        }}
        QScrollBar::add-page, QScrollBar::sub-page {{
            background: {colors['scrollbar_bg']};
        }}
        QStatusBar {{
            background-color: {colors['main_bg']};
            color: {colors['main_fg']};
            border-top: 1px solid {colors['accent']};
        }}
        QPushButton {{
            background-color: {colors['button_bg']};
            color: white;
            border: none;
            padding: 5px 15px;
            border-radius: 3px;
        }}
        QPushButton:hover {{
            background-color: {colors['button_hover']};
        }}
        QLineEdit, QComboBox, QSpinBox {{
            background-color: {colors['input_bg']};
            color: {colors['main_fg']};
            border: 1px solid {colors['accent']};
            padding: 3px;
        }}
        QCheckBox, QRadioButton {{
            color: {colors['main_fg']};
        }}
        QDialog {{
            background-color: {colors['main_bg']};
            color: {colors['main_fg']};
        }}
        """


class Windows11Theme(Theme):
    """Windows 11-inspired light theme"""
    
    def get_name(self) -> str:
        return "Windows 11"
    
    def get_colors(self) -> Dict[str, str]:
        return {
            "main_bg": "#f3f3f3",
            "main_fg": "#202020",
            "accent": "#0078d4",
            "table_bg": "#ffffff",
            "table_fg": "#202020",
            "table_grid": "#e5e5e5",
            "table_selection": "#cce8ff",
            "table_alternate": "#f9f9f9",
            "menu_bg": "#ffffff",
            "menu_hover": "#e5f3ff",
            "input_bg": "#ffffff",
            "button_bg": "#0078d4",
            "button_hover": "#106ebe",
            "scrollbar_bg": "#f3f3f3",
            "scrollbar_handle": "#c1c1c1",
            "scrollbar_handle_hover": "#a0a0a0"
        }
    
    def get_stylesheet(self) -> str:
        colors = self.get_colors()
        return f"""
        QMainWindow {{
            background-color: {colors['main_bg']};
            color: {colors['main_fg']};
        }}
        QWidget {{
            background-color: {colors['main_bg']};
            color: {colors['main_fg']};
        }}
        QMenuBar {{
            background-color: {colors['menu_bg']};
            color: {colors['main_fg']};
            border: 1px solid {colors['accent']};
        }}
        QMenuBar::item {{
            background-color: transparent;
            padding: 4px 12px;
            color: {colors['main_fg']};
        }}
        QMenuBar::item:selected {{
            background-color: {colors['menu_hover']};
        }}
        QMenu {{
            background-color: {colors['menu_bg']};
            color: {colors['main_fg']};
            border: 1px solid {colors['accent']};
        }}
        QMenu::item {{
            padding: 4px 20px;
            color: {colors['main_fg']};
        }}
        QMenu::item:selected {{
            background-color: {colors['menu_hover']};
        }}
        QScrollBar:vertical {{
            background-color: {colors['scrollbar_bg']};
            width: 15px;
            border: 1px solid {colors['accent']};
        }}
        QScrollBar::handle:vertical {{
            background-color: {colors['scrollbar_handle']};
            min-height: 20px;
            border-radius: 2px;
        }}
        QScrollBar::handle:vertical:hover {{
            background-color: {colors['scrollbar_handle_hover']};
        }}
        QScrollBar:horizontal {{
            background-color: {colors['scrollbar_bg']};
            height: 15px;
            border: 1px solid {colors['accent']};
        }}
        QScrollBar::handle:horizontal {{
            background-color: {colors['scrollbar_handle']};
            min-width: 20px;
            border-radius: 2px;
        }}
        QScrollBar::handle:horizontal:hover {{
            background-color: {colors['scrollbar_handle_hover']};
        }}
        QScrollBar::add-line, QScrollBar::sub-line {{
            background: none;
        }}
        QScrollBar::add-page, QScrollBar::sub-page {{
            background: {colors['scrollbar_bg']};
        }}
        QStatusBar {{
            background-color: {colors['main_bg']};
            color: {colors['main_fg']};
            border-top: 1px solid {colors['accent']};
        }}
        QPushButton {{
            background-color: {colors['button_bg']};
            color: black;
            border: none;
            padding: 5px 15px;
            border-radius: 3px;
        }}
        QPushButton:hover {{
            background-color: {colors['button_hover']};
        }}
        QLineEdit, QComboBox, QSpinBox {{
            background-color: {colors['input_bg']};
            color: {colors['main_fg']};
            border: 1px solid {colors['accent']};
            padding: 3px;
        }}
        QCheckBox, QRadioButton {{
            color: {colors['main_fg']};
        }}
        QDialog {{
            background-color: {colors['main_bg']};
            color: {colors['main_fg']};
        }}
        """


class ThemeManager:
    """Factory class for managing themes"""
    
    _themes = {
        "Django": DjangoTheme,
        "Windows 11": Windows11Theme
    }
    
    @classmethod
    def create_theme(cls, theme_name: str) -> Optional[Theme]:
        """Create a theme instance by name"""
        theme_class = cls._themes.get(theme_name)
        if theme_class:
            logger.info(f"Creating theme: {theme_name}")
            return theme_class()
        logger.warning(f"Unknown theme: {theme_name}")
        return None
    
    @classmethod
    def register_theme(cls, name: str, theme_class: type) -> None:
        """Register a new theme"""
        cls._themes[name] = theme_class
        logger.info(f"Registered theme: {name}")
    
    @classmethod
    def get_available_themes(cls) -> list:
        """Get list of available theme names"""
        return list(cls._themes.keys())