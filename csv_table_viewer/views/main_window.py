"""
Main application window
"""

import os
import logging
from typing import Optional
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QGridLayout, QScrollBar,
    QMessageBox, QFileDialog, QMenu, QAction, QActionGroup
)
from PyQt5.QtGui import QCloseEvent

from core import AppSettings, ThemeManager, SHORTCUTS, CSV_FILE_FILTER
from models import CSVModel
from controllers import FileController, EditController, ThemeController
from .table_widget import CsvTableWidget
from .dialogs import FindReplaceDialog
from utils import set_accessible_name

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize settings
        self._settings = AppSettings.instance()
        
        # Initialize models
        self._csv_model = CSVModel()
        
        # Initialize controllers
        self._file_controller = FileController(self._csv_model)
        self._edit_controller = EditController(self._csv_model)
        self._theme_controller = ThemeController()
        
        # Setup UI
        self._setup_ui()
        self._create_menus()
        self._create_shortcuts()
        self._setup_connections()
        
        # Restore window state
        self._restore_window_state()
        
        # Apply saved theme
        theme_name = self._settings.get_theme()
        self._theme_controller.apply_theme(self, theme_name)
        
        # Initialize with new document
        self._file_controller.new_file()
        
        # Find/Replace dialog
        self._find_dialog: Optional[FindReplaceDialog] = None
        
        logger.info("Main window initialized")
    
    def _setup_ui(self):
        """Setup the user interface"""
        self.setWindowTitle("CSV Table Viewer")
        set_accessible_name(self, "CSV Table Viewer Main Window")
        self.resize(1200, 800)
        
        # Create central widget
        central_widget = QWidget()
        set_accessible_name(central_widget, "Main Container Widget")
        self.setCentralWidget(central_widget)
        
        # Create table widget
        self._table = CsvTableWidget(self._csv_model)
        
        # Create scrollbars
        self._h_scrollbar = QScrollBar(Qt.Orientation.Horizontal)
        set_accessible_name(self._h_scrollbar, "Horizontal Scroll Bar")
        
        self._v_scrollbar = QScrollBar(Qt.Orientation.Vertical)
        set_accessible_name(self._v_scrollbar, "Vertical Scroll Bar")
        
        # Layout
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(10, 10, 10, 10)
        
        layout.addWidget(self._table, 0, 0)
        layout.addWidget(self._v_scrollbar, 0, 1)
        layout.addWidget(self._h_scrollbar, 1, 0)
        
        # Corner widget
        corner_widget = QWidget()
        set_accessible_name(corner_widget, "Scroll Bar Corner Widget")
        corner_widget.setFixedSize(
            self._v_scrollbar.sizeHint().width(),
            self._h_scrollbar.sizeHint().height()
        )
        layout.addWidget(corner_widget, 1, 1)
        
        # Set stretch factors
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 0)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 0)
        
        central_widget.setLayout(layout)
        
        # Status bar
        self._status_bar = self.statusBar()
        set_accessible_name(self._status_bar, "Status Bar")
        if self._status_bar:
            self._status_bar.showMessage("Ready")
    
    def _setup_connections(self):
        """Setup signal/slot connections"""
        # Ensure internal scrollbars exist even though they're hidden
        h_table_scrollbar = self._table.horizontalScrollBar()
        v_table_scrollbar = self._table.verticalScrollBar()
        
        if h_table_scrollbar:
            # Connect horizontal scrollbars
            self._h_scrollbar.valueChanged.connect(h_table_scrollbar.setValue)
            h_table_scrollbar.valueChanged.connect(self._h_scrollbar.setValue)
            h_table_scrollbar.rangeChanged.connect(
                lambda min, max: self._h_scrollbar.setRange(min, max)
            )
        
        if v_table_scrollbar:
            # Connect vertical scrollbars
            self._v_scrollbar.valueChanged.connect(v_table_scrollbar.setValue)
            v_table_scrollbar.valueChanged.connect(self._v_scrollbar.setValue)
            v_table_scrollbar.rangeChanged.connect(
                lambda min, max: self._v_scrollbar.setRange(min, max)
            )
        
        # Connect model changes
        self._csv_model.attach(self._on_model_changed)
    
    def _create_menus(self):
        """Create application menus"""
        menubar = self.menuBar()
        set_accessible_name(menubar, "Main Menu Bar")
        
        # File menu
        self._create_file_menu(menubar)
        
        # Edit menu
        self._create_edit_menu(menubar)
        
        # View menu
        self._create_view_menu(menubar)
        
        # Help menu
        self._create_help_menu(menubar)
    
    def _create_file_menu(self, menubar):
        """Create File menu"""
        file_menu = menubar.addMenu("&File")
        set_accessible_name(file_menu, "File Menu")
        
        # New
        new_action = QAction("&New", self)
        new_action.setShortcut(SHORTCUTS['new'])
        new_action.triggered.connect(self._on_new_file)
        file_menu.addAction(new_action)
        
        # New Window
        new_window_action = QAction("New &Window", self)
        new_window_action.setShortcut(SHORTCUTS['new_window'])
        new_window_action.triggered.connect(self._on_new_window)
        file_menu.addAction(new_window_action)
        
        file_menu.addSeparator()
        
        # Open
        open_action = QAction("&Open...", self)
        open_action.setShortcut(SHORTCUTS['open'])
        open_action.triggered.connect(self._on_open_file)
        file_menu.addAction(open_action)
        
        # Recent Files
        self._recent_menu = QMenu("Recent Files", self)
        set_accessible_name(self._recent_menu, "Recent Files Menu")
        file_menu.addMenu(self._recent_menu)
        self._update_recent_files_menu()
        
        file_menu.addSeparator()
        
        # Save
        save_action = QAction("&Save", self)
        save_action.setShortcut(SHORTCUTS['save'])
        save_action.triggered.connect(self._on_save_file)
        file_menu.addAction(save_action)
        
        # Save As
        save_as_action = QAction("Save &As...", self)
        save_as_action.setShortcut(SHORTCUTS['save_as'])
        save_as_action.triggered.connect(self._on_save_as_file)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        # Exit
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(SHORTCUTS['exit'])
        file_menu.addAction(exit_action)
    
    def _create_edit_menu(self, menubar):
        """Create Edit menu"""
        edit_menu = menubar.addMenu("&Edit")
        set_accessible_name(edit_menu, "Edit Menu")
        
        # Copy
        copy_action = QAction("&Copy", self)
        copy_action.setShortcut(SHORTCUTS['copy'])
        copy_action.triggered.connect(self._on_copy)
        edit_menu.addAction(copy_action)
        
        # Paste
        paste_action = QAction("&Paste", self)
        paste_action.setShortcut(SHORTCUTS['paste'])
        paste_action.triggered.connect(self._on_paste)
        edit_menu.addAction(paste_action)
        
        edit_menu.addSeparator()
        
        # Select All
        select_all_action = QAction("Select &All", self)
        select_all_action.setShortcut(SHORTCUTS['select_all'])
        select_all_action.triggered.connect(self._on_select_all)
        edit_menu.addAction(select_all_action)
        
        edit_menu.addSeparator()
        
        # Find
        find_action = QAction("&Find...", self)
        find_action.setShortcut(SHORTCUTS['find'])
        find_action.triggered.connect(self._on_find)
        edit_menu.addAction(find_action)
        
        # Find Next
        find_next_action = QAction("Find &Next", self)
        find_next_action.setShortcut(SHORTCUTS['find_next'])
        find_next_action.triggered.connect(self._on_find_next)
        edit_menu.addAction(find_next_action)
        
        # Replace
        replace_action = QAction("&Replace...", self)
        replace_action.setShortcut(SHORTCUTS['replace'])
        replace_action.triggered.connect(self._on_replace)
        edit_menu.addAction(replace_action)
    
    def _create_view_menu(self, menubar):
        """Create View menu"""
        view_menu = menubar.addMenu("&View")
        set_accessible_name(view_menu, "View Menu")
        
        # Resize columns
        resize_action = QAction("&Resize Columns to Contents", self)
        resize_action.triggered.connect(self._table.resizeColumnsToContents)
        view_menu.addAction(resize_action)
        
        view_menu.addSeparator()
        
        # Theme submenu
        theme_menu = QMenu("&Theme", self)
        set_accessible_name(theme_menu, "Theme Menu")
        
        theme_group = QActionGroup(self)
        current_theme = self._settings.get_theme()
        
        for theme_name in ThemeManager.get_available_themes():
            theme_action = QAction(theme_name, self)
            theme_action.setCheckable(True)
            theme_action.setChecked(theme_name == current_theme)
            theme_action.triggered.connect(
                lambda checked, name=theme_name: self._on_theme_changed(name)
            )
            theme_group.addAction(theme_action)
            theme_menu.addAction(theme_action)
        
        view_menu.addMenu(theme_menu)
    
    def _create_help_menu(self, menubar):
        """Create Help menu"""
        help_menu = menubar.addMenu("&Help")
        set_accessible_name(help_menu, "Help Menu")
        
        # Keyboard shortcuts
        shortcuts_action = QAction("&Keyboard Shortcuts", self)
        shortcuts_action.triggered.connect(self._on_show_shortcuts)
        help_menu.addAction(shortcuts_action)
        
        help_menu.addSeparator()
        
        # About
        about_action = QAction("&About", self)
        about_action.triggered.connect(self._on_about)
        help_menu.addAction(about_action)
    
    def _create_shortcuts(self):
        """Create additional keyboard shortcuts"""
        # Shortcuts are defined in menu actions
        pass
    
    def _update_recent_files_menu(self):
        """Update recent files menu"""
        self._recent_menu.clear()
        
        recent_files = self._settings.get_recent_files()
        for i, file_path in enumerate(recent_files):
            if os.path.exists(file_path):
                action = QAction(f"{i+1}. {os.path.basename(file_path)}", self)
                action.setData(file_path)
                action.triggered.connect(
                    lambda checked, path=file_path: self._on_open_recent_file(path)
                )
                self._recent_menu.addAction(action)
    
    def _restore_window_state(self):
        """Restore window geometry and state"""
        geometry = self._settings.get_window_geometry()
        if geometry:
            self.restoreGeometry(geometry)
        
        state = self._settings.get_window_state()
        if state:
            self.restoreState(state)
    
    def _save_window_state(self):
        """Save window geometry and state"""
        self._settings.set_window_geometry(self.saveGeometry())
        self._settings.set_window_state(self.saveState())
        self._settings.save()
    
    # Event handlers
    def closeEvent(self, event: QCloseEvent):
        """Handle window close event"""
        if self._csv_model.is_modified:
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                "You have unsaved changes. Do you want to save before closing?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            
            if reply == QMessageBox.Save:
                self._on_save_file()
            elif reply == QMessageBox.Cancel:
                event.ignore()
                return
        
        self._save_window_state()
        event.accept()
    
    # Slots
    def _on_model_changed(self):
        """Handle model changes"""
        self._update_title()
    
    def _update_title(self):
        """Update window title"""
        if self._csv_model.has_file:
            filename = os.path.basename(str(self._csv_model.file_path))
            modified = " *" if self._csv_model.is_modified else ""
            self.setWindowTitle(f"CSV Table Viewer - {filename}{modified}")
        else:
            modified = " *" if self._csv_model.is_modified else ""
            self.setWindowTitle(f"CSV Table Viewer - Untitled{modified}")
    
    def _on_new_file(self):
        """Create new file"""
        if self._csv_model.is_modified:
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                "You have unsaved changes. Do you want to save?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            
            if reply == QMessageBox.Save:
                self._on_save_file()
            elif reply == QMessageBox.Cancel:
                return
        
        self._file_controller.new_file()
        if self._status_bar:
            self._status_bar.showMessage("New file created")
    
    def _on_new_window(self):
        """Open new window"""
        new_window = MainWindow()
        new_window.show()
    
    def _on_open_file(self):
        """Open file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open CSV File", "", CSV_FILE_FILTER
        )
        
        if file_path:
            try:
                self._file_controller.open_file(file_path)
                self._settings.add_recent_file(file_path)
                self._update_recent_files_menu()
                if self._status_bar:
                    self._status_bar.showMessage(f"Opened: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open file:\n{str(e)}")
    
    def _on_open_recent_file(self, file_path: str):
        """Open recent file"""
        if os.path.exists(file_path):
            try:
                self._file_controller.open_file(file_path)
                if self._status_bar:
                    self._status_bar.showMessage(f"Opened: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open file:\n{str(e)}")
                self._settings.remove_recent_file(file_path)
                self._update_recent_files_menu()
    
    def _on_save_file(self):
        """Save file"""
        try:
            if self._csv_model.has_file:
                self._file_controller.save_file()
                if self._status_bar:
                    self._status_bar.showMessage("File saved")
            else:
                self._on_save_as_file()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file:\n{str(e)}")
    
    def _on_save_as_file(self):
        """Save file as"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save CSV File", "", CSV_FILE_FILTER
        )
        
        if file_path:
            try:
                self._file_controller.save_file_as(file_path)
                self._settings.add_recent_file(file_path)
                self._update_recent_files_menu()
                if self._status_bar:
                    self._status_bar.showMessage(f"Saved: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file:\n{str(e)}")
    
    def _on_copy(self):
        """Copy selected cells"""
        count = self._edit_controller.copy_cells(self._table)
        if count > 0:
            if self._status_bar:
                self._status_bar.showMessage(f"Copied {count} cells")

    def _on_paste(self):
        """Paste cells"""
        count = self._edit_controller.paste_cells(self._table)
        if count > 0:
            if self._status_bar:
                self._status_bar.showMessage(f"Pasted {count} cells")

    def _on_select_all(self):
        """Select all cells"""
        self._table.selectAll()
        if self._status_bar:
            self._status_bar.showMessage("All cells selected")

    def _on_find(self):
        """Show find dialog"""
        if not self._find_dialog:
            self._find_dialog = FindReplaceDialog(self)
            self._find_dialog.find_requested.connect(self._on_find_text)
            self._find_dialog.find_next_requested.connect(self._on_find_next)
            self._find_dialog.find_all_requested.connect(self._on_find_all)
            self._find_dialog.replace_requested.connect(self._on_replace_current)
            self._find_dialog.replace_all_requested.connect(self._on_replace_all)
        
        self._find_dialog.show()
        self._find_dialog.raise_()
        self._find_dialog.activateWindow()
    
    def _on_replace(self):
        """Show replace dialog"""
        self._on_find()  # Same dialog handles both
        if self._find_dialog:
            self._find_dialog.show_replace_options()

    def _on_find_next(self):
        """Find next occurrence"""
        if self._find_dialog:
            self._on_find_text(
                self._find_dialog.get_find_text(),
                self._find_dialog.is_case_sensitive(),
                self._find_dialog.is_whole_words(),
                find_next=True
            )
    
    def _on_find_text(self, text: str, case_sensitive: bool, 
                      whole_words: bool, find_next: bool = False):
        """Find text in table"""
        result = self._edit_controller.find_text(
            self._table, text, case_sensitive, whole_words, find_next
        )
        
        if result:
            row, col = result
            if self._status_bar:
                self._status_bar.showMessage(f"Found at Row {row+1}, Column {col+1}")
        else:
            if self._status_bar:
                self._status_bar.showMessage("No match found")

    def _on_find_all(self, text: str, case_sensitive: bool, whole_words: bool):
        """Find all occurrences"""
        count = self._edit_controller.find_all(
            self._table, text, case_sensitive, whole_words
        )
        if self._status_bar:
            self._status_bar.showMessage(f"Found {count} occurrences")

    def _on_replace_current(self, find_text: str, replace_text: str,
                           case_sensitive: bool, whole_words: bool):
        """Replace current occurrence"""
        if self._edit_controller.replace_current(
            self._table, find_text, replace_text, case_sensitive, whole_words
        ):
            self._on_find_next()
    
    def _on_replace_all(self, find_text: str, replace_text: str,
                       case_sensitive: bool, whole_words: bool):
        """Replace all occurrences"""
        count = self._edit_controller.replace_all(
            self._table, find_text, replace_text, case_sensitive, whole_words
        )
        if self._status_bar:
            self._status_bar.showMessage(f"Replaced {count} occurrences")

    def _on_theme_changed(self, theme_name: str):
        """Handle theme change"""
        self._theme_controller.apply_theme(self, theme_name)
        self._table.update_theme()
        self._settings.set_theme(theme_name)
        if self._status_bar:
            self._status_bar.showMessage(f"Applied theme: {theme_name}")

    def _on_show_shortcuts(self):
        """Show keyboard shortcuts"""
        shortcuts_html = """
        <h3>Keyboard Shortcuts</h3>
        <table>
        <tr><td><b>Ctrl+N</b></td><td>New file</td></tr>
        <tr><td><b>Ctrl+O</b></td><td>Open file</td></tr>
        <tr><td><b>Ctrl+S</b></td><td>Save file</td></tr>
        <tr><td><b>Ctrl+Shift+S</b></td><td>Save as</td></tr>
        <tr><td><b>Ctrl+F</b></td><td>Find</td></tr>
        <tr><td><b>F3</b></td><td>Find next</td></tr>
        <tr><td><b>Ctrl+H</b></td><td>Replace</td></tr>
        <tr><td><b>Ctrl+A</b></td><td>Select all</td></tr>
        <tr><td><b>Ctrl+C</b></td><td>Copy</td></tr>
        <tr><td><b>Ctrl+V</b></td><td>Paste</td></tr>
        <tr><td><b>Ctrl+Shift+N</b></td><td>New window</td></tr>
        <tr><td><b>Alt+F4</b></td><td>Exit</td></tr>
        </table>
        """
        
        msg = QMessageBox()
        msg.setWindowTitle("Keyboard Shortcuts")
        msg.setTextFormat(Qt.TextFormat.RichText)
        msg.setText(shortcuts_html)
        msg.exec_()
    
    def _on_about(self):
        """Show about dialog"""
        about_html = f"""
        <h3>CSV Table Viewer</h3>
        <p>Version 1.0.0</p>
        <p>An accessible, automatable table UI for CSV files.</p>
        <p><b>Current Theme:</b> {self._settings.get_theme()}</p>
        <h4>Features:</h4>
        <ul>
        <li>Full accessibility support</li>
        <li>Multiple themes</li>
        <li>Find and replace</li>
        <li>Recent files</li>
        <li>Multiple windows</li>
        </ul>
        """
        
        msg = QMessageBox()
        msg.setWindowTitle("About CSV Table Viewer")
        msg.setTextFormat(Qt.TextFormat.RichText)
        msg.setText(about_html)
        msg.exec_()
        