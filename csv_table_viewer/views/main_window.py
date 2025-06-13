"""
Main application window
"""

import os
import logging
from typing import Optional
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QGridLayout, QScrollBar,
    QMessageBox, QFileDialog, QMenu, QAction, QActionGroup,
    QTableView, QAbstractItemView, QPushButton
)
from PyQt5.QtGui import QCloseEvent, QIcon

from core import AppSettings, ThemeManager, SHORTCUTS, CSV_FILE_FILTER
from models import CSVModel, TableModel
from controllers import FileController, EditController, ThemeController
from .dialogs import FindReplaceDialog
from utils import set_accessible_name
from core.constants import APP_VERSION

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        self._settings = AppSettings.instance()
        self._csv_model = CSVModel()
        self._table_model = TableModel(self._csv_model)
        
        self._file_controller = FileController(self._csv_model)
        self._edit_controller = EditController(self._csv_model)
        self._theme_controller = ThemeController()
        
        self._setup_ui()
        self._create_menus()
        self._csv_model.attach(self._on_model_changed)
        
        self._restore_window_state()
        theme_name = self._settings.get_theme()
        self._theme_controller.apply_theme(self, theme_name)
        self._file_controller.new_file()
        
        self._find_dialog: Optional[FindReplaceDialog] = None
        logger.info("Main window initialized")
    
    def _setup_ui(self):
        self.setWindowTitle("CSV Table Viewer")
        self.resize(1200, 800)
        self.setWindowIcon(QIcon(self._settings.get_icon()))
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        self._table = QTableView()
        self._table.setModel(self._table_model)
        
        set_accessible_name(self._table, "Large Table")
        self._table.setAlternatingRowColors(True)
        self._table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self._table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self._table.setCornerButtonEnabled(True)
        self._table.setShowGrid(True)
        # self._table.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
        self._table.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked | QAbstractItemView.EditTrigger.EditKeyPressed)
        self._table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.h_scrollbar = QScrollBar(Qt.Orientation.Horizontal)
        self.h_scrollbar.setObjectName("HorizontalScrollBar")
        self.h_scrollbar.setAccessibleName("Horizontal Scroll Bar")
        
        self.v_scrollbar = QScrollBar(Qt.Orientation.Vertical)
        self.v_scrollbar.setObjectName("VerticalScrollBar")
        self.v_scrollbar.setAccessibleName("Vertical Scroll Bar")

        # Connect external scrollbars to the table's internal scrollbars
        self.h_scrollbar.valueChanged.connect(self._table.horizontalScrollBar().setValue)
        self._table.horizontalScrollBar().valueChanged.connect(self.h_scrollbar.setValue)
        self._table.horizontalScrollBar().rangeChanged.connect(self.h_scrollbar.setRange)

        self.v_scrollbar.valueChanged.connect(self._table.verticalScrollBar().setValue)
        self._table.verticalScrollBar().valueChanged.connect(self.v_scrollbar.setValue)
        self._table.verticalScrollBar().rangeChanged.connect(self.v_scrollbar.setRange)
        
        # Attach scrollbars to the table
        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)
        grid_layout.setContentsMargins(10, 10, 10, 10) # Add margins to the grid_layout
        grid_layout.addWidget(self._table, 0, 0)
        grid_layout.addWidget(self.v_scrollbar, 0, 1)
        grid_layout.addWidget(self.h_scrollbar, 1, 0)
        grid_layout.setColumnStretch(0, 1) # Allow table to expand
        grid_layout.setRowStretch(0, 1)    # Allow table to expand

        central_widget.setLayout(grid_layout) # USE grid_layout HERE
        
        self._status_bar = self.statusBar()
        if self._status_bar:
            self._status_bar.showMessage("Ready")

    def _create_menus(self):
        menubar = self.menuBar()
        self._create_file_menu(menubar)
        self._create_edit_menu(menubar)
        self._create_view_menu(menubar)
        self._create_help_menu(menubar)
    
    def _create_file_menu(self, menubar):
        file_menu = menubar.addMenu("&File")
        
        new_action = QAction("&New", self)
        new_action.setShortcut(SHORTCUTS['new'])
        new_action.triggered.connect(self._on_new_file)
        new_window_action = QAction("New &Window", self)
        new_window_action.setShortcut(SHORTCUTS['new_window'])
        new_window_action.triggered.connect(self._on_new_window)
        open_action = QAction("&Open...", self)
        open_action.setShortcut(SHORTCUTS['open'])
        open_action.triggered.connect(self._on_open_file)
        save_action = QAction("&Save", self)
        save_action.setShortcut(SHORTCUTS['save'])
        save_action.triggered.connect(self._on_save_file)
        save_as_action = QAction("Save &As...", self)
        save_as_action.setShortcut(SHORTCUTS['save_as'])
        save_as_action.triggered.connect(self._on_save_as_file)
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(SHORTCUTS['exit'])
        exit_action.triggered.connect(self.close)
        
        file_menu.addAction(new_action)
        file_menu.addAction(new_window_action)
        file_menu.addSeparator()
        file_menu.addAction(open_action)
        self._recent_menu = file_menu.addMenu("Recent Files")
        self._update_recent_files_menu()
        file_menu.addSeparator()
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
    
    def _create_edit_menu(self, menubar):
        edit_menu = menubar.addMenu("&Edit")
        
        copy_action = QAction("&Copy", self)
        copy_action.setShortcut(SHORTCUTS['copy'])
        copy_action.triggered.connect(self._on_copy)
        paste_action = QAction("&Paste", self)
        paste_action.setShortcut(SHORTCUTS['paste'])
        paste_action.triggered.connect(self._on_paste)
        select_all_action = QAction("Select &All", self)
        select_all_action.setShortcut(SHORTCUTS['select_all'])
        select_all_action.triggered.connect(self._on_select_all)
        find_action = QAction("&Find...", self)
        find_action.setShortcut(SHORTCUTS['find'])
        find_action.triggered.connect(self._on_find)
        find_next_action = QAction("Find &Next", self)
        find_next_action.setShortcut(SHORTCUTS['find_next'])
        find_next_action.triggered.connect(self._on_find_next)
        replace_action = QAction("&Replace...", self)
        replace_action.setShortcut(SHORTCUTS['replace'])
        replace_action.triggered.connect(self._on_replace)
        
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)
        edit_menu.addSeparator()
        edit_menu.addAction(select_all_action)
        edit_menu.addSeparator()
        edit_menu.addAction(find_action)
        edit_menu.addAction(find_next_action)
        edit_menu.addAction(replace_action)
    
    def _create_view_menu(self, menubar):
        view_menu = menubar.addMenu("&View")
        resize_action = QAction("&Resize Columns to Contents", self)
        resize_action.triggered.connect(self._table.resizeColumnsToContents)
        view_menu.addAction(resize_action)
        view_menu.addSeparator()
        
        theme_menu = view_menu.addMenu("&Theme")
        theme_group = QActionGroup(self)
        current_theme = self._settings.get_theme()
        
        for theme_name in ThemeManager.get_available_themes():
            action = QAction(theme_name, self)
            action.setCheckable(True)
            theme_group.addAction(action)
            if theme_name == current_theme:
                action.setChecked(True)
            action.triggered.connect(lambda checked, name=theme_name: self._on_theme_changed(name))
            theme_menu.addAction(action)
    
    def _create_help_menu(self, menubar):
        help_menu = menubar.addMenu("&Help")
        shortcuts_action = QAction("&Keyboard Shortcuts", self)
        shortcuts_action.triggered.connect(self._on_show_shortcuts)
        about_action = QAction("&About", self)
        about_action.triggered.connect(self._on_about)
        help_menu.addAction(shortcuts_action)
        help_menu.addSeparator()
        help_menu.addAction(about_action)
    
    def _update_recent_files_menu(self):
        self._recent_menu.clear()
        recent_files = self._settings.get_recent_files()
        for i, file_path in enumerate(recent_files):
            if os.path.exists(file_path):
                action = QAction(f"&{i+1}. {os.path.basename(file_path)}", self)
                action.triggered.connect(lambda checked, path=file_path: self._on_open_recent_file(path))
                self._recent_menu.addAction(action)
    
    def _restore_window_state(self):
        if geometry := self._settings.get_window_geometry():
            self.restoreGeometry(geometry)
        if state := self._settings.get_window_state():
            self.restoreState(state)
    
    def _save_window_state(self):
        self._settings.set_window_geometry(self.saveGeometry())
        self._settings.set_window_state(self.saveState())
        self._settings.save()
    
    def closeEvent(self, event: QCloseEvent):
        if self._csv_model.is_modified:
            reply = QMessageBox.question(self, "Unsaved Changes",
                                         "You have unsaved changes. Do you want to save before closing?",
                                         QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            if reply == QMessageBox.Save:
                if not self._on_save_file():
                    event.ignore()
                    return
            elif reply == QMessageBox.Cancel:
                event.ignore()
                return
        self._save_window_state()
        event.accept()
    
    def _on_model_changed(self):
        self._update_title()
        self._table.resizeColumnsToContents()

    def _update_title(self):
        if self._csv_model.has_file:
            filename = os.path.basename(str(self._csv_model.file_path))
            modified = " *" if self._csv_model.is_modified else ""
            self.setWindowTitle(f"CSV Table Viewer - {filename}{modified}")
        else:
            modified = " *" if self._csv_model.is_modified else ""
            self.setWindowTitle(f"CSV Table Viewer - Untitled{modified}")
    
    def _on_new_file(self):
        if self._csv_model.is_modified:
            # Re-use closeEvent logic to check for saving
            dummy_event = QCloseEvent()
            self.closeEvent(dummy_event)
            if not dummy_event.isAccepted():
                return
        self._file_controller.new_file()
        if self._status_bar: self._status_bar.showMessage("New file created")
    
    def _on_new_window(self):
        MainWindow().show()
    
    def _on_open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", CSV_FILE_FILTER)
        if file_path:
            try:
                self._file_controller.open_file(file_path)
                self._settings.add_recent_file(file_path)
                self._update_recent_files_menu()
                if self._status_bar:
                    self._status_bar.showMessage(f"Opened: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open file:\n{e}")
    
    def _on_open_recent_file(self, file_path: str):
        if os.path.exists(file_path):
            try:
                self._file_controller.open_file(file_path)
                if self._status_bar: self._status_bar.showMessage(f"Opened: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open file:\n{e}")
                self._settings.remove_recent_file(file_path)
                self._update_recent_files_menu()
    
    def _on_save_file(self) -> bool:
        if self._csv_model.has_file:
            try:
                self._file_controller.save_file()
                if self._status_bar: self._status_bar.showMessage("File saved")
                return True
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file:\n{e}")
                return False
        else:
            return self._on_save_as_file()
    
    def _on_save_as_file(self) -> bool:
        file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV File", "", CSV_FILE_FILTER)
        if file_path:
            try:
                self._file_controller.save_file_as(file_path)
                self._settings.add_recent_file(file_path)
                self._update_recent_files_menu()
                if self._status_bar: self._status_bar.showMessage(f"Saved: {file_path}")
                return True
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file:\n{e}")
                return False
        return False

    def _on_copy(self):
        count = self._edit_controller.copy_cells(self._table)
        if count > 0 and self._status_bar:
            self._status_bar.showMessage(f"Copied {count} cells")

    def _on_paste(self):
        count = self._edit_controller.paste_cells(self._table)
        if count > 0 and self._status_bar:
            self._status_bar.showMessage(f"Pasted {count} cells")

    def _on_select_all(self):
        self._table.selectAll()

    def _on_find(self):
        if not self._find_dialog:
            self._find_dialog = FindReplaceDialog(self)
            self._find_dialog.find_requested.connect(self._on_find_text)
            self._find_dialog.find_next_requested.connect(self._on_find_next)
            self._find_dialog.find_all_requested.connect(self._on_find_all)
            self._find_dialog.replace_all_requested.connect(self._on_replace_all)
        self._find_dialog.show()
        self._find_dialog.raise_()
        self._find_dialog.activateWindow()
    
    def _on_replace(self):
        self._on_find()
        if self._find_dialog:
            self._find_dialog.show_replace_options()

    def _on_find_next(self):
        if self._find_dialog:
            self._on_find_text(self._find_dialog.get_find_text(),
                               self._find_dialog.is_case_sensitive(),
                               self._find_dialog.is_whole_words(),
                               find_next=True)
    
    def _on_find_text(self, text: str, case_sensitive: bool, whole_words: bool, find_next: bool = False):
        result = self._edit_controller.find_text(self._table, text, case_sensitive, whole_words, find_next)
        if result and self._status_bar:
            self._status_bar.showMessage(f"Found at Row {result[0]+1}, Column {result[1]+1}")
        elif self._status_bar:
            self._status_bar.showMessage("No match found")

    def _on_find_all(self, text: str, case_sensitive: bool, whole_words: bool):
        count = self._edit_controller.find_all(self._table, text, case_sensitive, whole_words)
        if self._status_bar:
            self._status_bar.showMessage(f"Found {count} occurrences")
    
    def _on_replace_all(self, find_text: str, replace_text: str, case_sensitive: bool, whole_words: bool):
        count = self._edit_controller.replace_all(self._table, find_text, replace_text, case_sensitive, whole_words)
        if self._status_bar:
            self._status_bar.showMessage(f"Replaced {count} occurrences")

    def _on_theme_changed(self, theme_name: str):
        self._theme_controller.apply_theme(self, theme_name)
        self._settings.set_theme(theme_name)

    def _on_show_shortcuts(self):
        QMessageBox.information(self, "Keyboard Shortcuts", """
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
        """)
    
    def _on_about(self):
        QMessageBox.about(self, "About CSV Table Viewer", f"""
        <h3>CSV Table Viewer</h3>
        <p>Version {APP_VERSION}</p>
        <p>An accessible, automatable table UI for CSV files.</p>
        <p><b>Current Theme:</b> {self._settings.get_theme()}</p>
        """)
