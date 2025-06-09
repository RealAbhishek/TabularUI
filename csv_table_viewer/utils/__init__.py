"""
Utility functions
"""

from .accessibility import set_accessible_name
from .platform_utils import configure_platform_specific, apply_window_theme

__all__ = [
    'set_accessible_name',
    'configure_platform_specific',
    'apply_window_theme'
]