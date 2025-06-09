"""
Views module containing UI components
"""
from utils import set_accessible_name
from .main_window import MainWindow
from .table_widget import CsvTableWidget
import core


__all__ = ['MainWindow', 'CsvTableWidget', 'set_accessible_name', 'core']