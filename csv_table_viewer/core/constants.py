"""
Application constants
"""

# Application info
APP_NAME = "CSV Table Viewer"
APP_VERSION = "1.0.0"
ORGANIZATION_NAME = "CSVViewer"

# Table defaults
INITIAL_NEW_ROWS = 50
INITIAL_NEW_COLS = 50
DEFAULT_COLUMN_WIDTH = 100
MAX_RECENT_FILES = 10

# File filters
CSV_FILE_FILTER = "CSV Files (*.csv)"
ALL_FILES_FILTER = "All Files (*.*)"

# Keyboard shortcuts
SHORTCUTS = {
    'new': 'Ctrl+N',
    'open': 'Ctrl+O',
    'save': 'Ctrl+S',
    'save_as': 'Ctrl+Shift+S',
    'copy': 'Ctrl+C',
    'paste': 'Ctrl+V',
    'find': 'Ctrl+F',
    'replace': 'Ctrl+H',
    'select_all': 'Ctrl+A',
    'new_window': 'Ctrl+Shift+N',
    'find_next': 'F3',
    'exit': 'Alt+F4'
}

# Settings keys
SETTING_RECENT_FILES = "recentFiles"
SETTING_THEME = "theme"
SETTING_WINDOW_GEOMETRY = "windowGeometry"
SETTING_WINDOW_STATE = "windowState"