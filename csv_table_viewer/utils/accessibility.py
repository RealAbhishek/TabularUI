"""
Accessibility utilities
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget


def set_accessible_name(widget: QWidget, name: str):
    """Set accessible name for a widget"""
    widget.setAccessibleName(name)
    widget.setAccessibleDescription(name)
    
    # For some widgets, also set object name
    if hasattr(widget, 'setObjectName'):
        widget.setObjectName(name.replace(' ', '_'))