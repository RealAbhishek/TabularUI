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
        pass
    
    @abstractmethod
    def get_colors(self) -> Dict[str, str]:
        pass
    
    @abstractmethod
    def get_stylesheet(self) -> str:
        pass


class DjangoTheme(Theme):
    """A mixed theme with a dark green menu/title bar and a light content area."""
    
    def get_name(self) -> str:
        return "Django"
    
    def get_colors(self) -> Dict[str, str]:
        return {
            "main_bg": "#f7f9f7",
            "main_fg": "#212121",
            "accent": "#4CAF50",

            "menu_bg": "#092e20",
            "menu_fg": "white",
            "menu_hover": "#44b78b",

            "table_bg": "#E8F5E9",
            "table_fg": "#1B5E20",
            "table_grid": "#A5D6A7",
            "table_selection": "#B9F6CA",
            "header_bg": "#C8E6C9",

            "input_bg": "#A3EDAA",
            "button_bg": "#2C7A2F",
            "button_hover": "#4A9A4E",
            "scrollbar_bg": "#2b8f2b",
            "scrollbar_handle": "#2A752D",
            "scrollbar_handle_hover": "#0D5611"
        }
    
    def get_stylesheet(self) -> str:
        colors = self.get_colors()
        return f"""
        /* Main window has a light background */
        QMainWindow, QDialog, QWidget {{
            background-color: {colors['main_bg']};
            color: {colors['main_fg']};
        }}
        
        /* Menu bar is specifically styled to be dark */
        QMenuBar {{
            background-color: {colors['menu_bg']};
            color: {colors['menu_fg']};
        }}
        QMenuBar::item {{
            background-color: transparent;
            color: {colors['menu_fg']};
            padding: 4px 12px;
        }}
        QMenuBar::item:selected {{
            background-color: {colors['menu_hover']};
        }}
        
        /* Dropdown menus are also dark to match the menu bar */
        QMenu {{
            background-color: {colors['menu_bg']};
            color: {colors['menu_fg']};
            border: 1px solid {colors['accent']};
        }}
        QMenu::item:selected {{
            background-color: {colors['menu_hover']};
        }}

        /* Table view is styled to be light green */
        QTableView {{
            background-color: {colors['table_bg']};
            color: {colors['table_fg']};
            gridline-color: {colors['table_grid']};
            selection-background-color: {colors['table_selection']};
            border: 1px solid {colors['accent']};
        }}
        QHeaderView::section {{
            background-color: {colors['header_bg']};
            color: {colors['table_fg']};
            padding: 4px;
            border: 1px solid {colors['table_grid']};
        }}

        /* Other widgets */
        QStatusBar {{
            border-top: 1px solid {colors['table_grid']};
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
        """

class Windows11Theme(Theme):
    """Windows 11-inspired light theme"""
    # ... (This class remains unchanged) ...
    def get_name(self) -> str:
        return "Windows 11"
    
    def get_colors(self) -> Dict[str, str]:
        return {
            "main_bg": "#ced5da",              # Slightly softer off-white
            "main_fg": "#000000",              # Standard black text for high contrast
            "accent": "#0078d4",              # The classic Windows blue accent
            "accent_fg": "#ffffff",            # Text on accent backgrounds is white
            
            "table_fg": "#000000",             # Standard black text for tables
            "table_alternate": "#f0f0f0",      # Light gray for alternating rows
            "table_bg": "#ffffff",             # Tables are pure white
            "table_grid": "#e1e1e1",           # Lighter, more subtle grid lines
            "table_selection_bg": "#cce8ff",   # Light blue for selection
            "table_selection": "#cce8ff",      # Selection background is light blue
            "table_selection_fg": "#000000",   # Ensure selected text is still black
            "header_bg": "#f3f3f3",            # Header is slightly darker than the table
            
            "menu_bg": "#f3f3f3",              # Menus are off-white
            "menu_hover": "#e5e5e5",           # Subtle gray hover effect
            
            "input_bg": "#ffffff",             # Input fields are white
            "input_border": "#cccccc",         # Light gray border for inputs
            "input_border_focus": "#0078d4",   # Border becomes blue on focus
            
            "button_bg": "#e1e1e1",            # Standard buttons are light gray
            "button_fg": "#000000",            # Standard button text
            "button_border": "#cccccc",        # Subtle border for buttons
            "button_hover": "#e5e5e5",       # Lighter gray on hover
            "primary_button_bg": "#0078d4",     # Primary action buttons use the accent color
            "primary_button_hover_bg": "#106ebe", # Darker blue on hover
            
            "scrollbar_bg": "transparent",       # Modern scrollbar tracks are transparent
            "scrollbar_handle": "#d1d1d1",     # Light gray handle
            "scrollbar_handle_hover": "#a0a0a0"  # Darker gray handle on hover
        }
    
    def get_stylesheet(self) -> str:
        colors = self.get_colors()
        return f"""
        QMainWindow, QDialog, QWidget {{
            background-color: {colors['main_bg']};
            color: {colors['main_fg']};
        }}
        QPushButton {{
            background-color: {colors['button_bg']};
            color: white;
            border: 1px solid {colors['accent']};
            padding: 5px 15px;
            border-radius: 3px;
        }}
        QPushButton:hover {{
            background-color: {colors['button_hover']};
        }}
        QTableView {{
            background-color: {colors['table_bg']};
            color: {colors['table_fg']};
            gridline-color: {colors['table_grid']};
            selection-background-color: {colors['table_selection']};
            alternate-background-color: {colors['table_alternate']};
            border: 1px solid {colors['accent']};
        }}
        QHeaderView::section {{
            background-color: {colors['header_bg']};
            color: {colors['table_fg']};
            padding: 4px;
            border: 1px solid {colors['table_grid']};
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
        theme_class = cls._themes.get(theme_name)
        if theme_class:
            logger.info(f"Creating theme: {theme_name}")
            return theme_class()
        logger.warning(f"Unknown theme: {theme_name}")
        return None
    
    @classmethod
    def register_theme(cls, name: str, theme_class: type) -> None:
        cls._themes[name] = theme_class
        logger.info(f"Registered theme: {name}")
    
    @classmethod
    def get_available_themes(cls) -> list:
        return list(cls._themes.keys())
