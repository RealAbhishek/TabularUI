"""
Views module containing UI components
"""
from utils import set_accessible_name
from .main_window import MainWindow
import core


__all__ = ['MainWindow', 'set_accessible_name', 'core']