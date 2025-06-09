import sys
import csv
import json
import os
from datetime import datetime
from PyQt5.QtCore import Qt, QSettings, QTimer
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QColor, QFont
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QAction, QTableWidget, QTableWidgetItem, 
    QGridLayout, QWidget, QMessageBox, QScrollBar, QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QCheckBox, QComboBox, QLineEdit, QTextEdit, QProgressBar,
    QRadioButton, QTreeWidget, QTreeWidgetItem, QListWidget, QListWidgetItem,
    QGroupBox, QMenuBar, QMenu, QDialogButtonBox, QSpinBox, QSlider, QTabWidget,
    QCalendarWidget, QDateEdit, QTimeEdit, QDial, QLCDNumber, QFontComboBox,
    QScrollArea, QSplitter, QStackedWidget, QToolBar, QStatusBar, QDockWidget,
    QHeaderView, QInputDialog, QShortcut
)

# Constants
INITIAL_NEW_ROWS = 50
INITIAL_NEW_COLS = 50
MAX_RECENT_FILES = 10

# Django-like color scheme
DJANGO_GREEN = "#092e20"
DJANGO_LIGHT_GREEN = "#6d9f8c"
TABLE_DARK_BG = "#1e1e1e"
TABLE_DARK_FG = "#d4d4d4"
TABLE_GRID_COLOR = "#3c3c3c"
TABLE_SELECTION_BG = "#264f78"
TABLE_ALTERNATE_BG = "#2d2d2d"

class FindReplaceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Find and Replace")
        self.setAccessibleName("Find and Replace Dialog")
        self.setFixedSize(450, 250)
        
        layout = QVBoxLayout()
        
        # Find section
        find_layout = QHBoxLayout()
        find_label = QLabel("Find:")
        find_label.setAccessibleName("Find Label")
        self.find_input = QLineEdit()
        self.find_input.setAccessibleName("Find Text Input")
        find_layout.addWidget(find_label)
        find_layout.addWidget(self.find_input)
        
        # Replace section
        replace_layout = QHBoxLayout()
        replace_label = QLabel("Replace:")
        replace_label.setAccessibleName("Replace Label")
        self.replace_input = QLineEdit()
        self.replace_input.setAccessibleName("Replace Text Input")
        replace_layout.addWidget(replace_label)
        replace_layout.addWidget(self.replace_input)
        
        # Options
        self.case_sensitive = QCheckBox("Case sensitive")
        self.case_sensitive.setAccessibleName("Case Sensitive Checkbox")
        self.whole_words = QCheckBox("Whole words only")
        self.whole_words.setAccessibleName("Whole Words Checkbox")
        
        # Buttons
        button_layout = QHBoxLayout()
        self.find_next_btn = QPushButton("Find Next")
        self.find_next_btn.setAccessibleName("Find Next Button")
        self.find_all_btn = QPushButton("Find All")
        self.find_all_btn.setAccessibleName("Find All Button")
        self.replace_btn = QPushButton("Replace")
        self.replace_btn.setAccessibleName("Replace Button")
        self.replace_all_btn = QPushButton("Replace All")
        self.replace_all_btn.setAccessibleName("Replace All Button")
        self.close_btn = QPushButton("Close")
        self.close_btn.setAccessibleName("Close Button")
        
        button_layout.addWidget(self.find_next_btn)
        button_layout.addWidget(self.find_all_btn)
        button_layout.addWidget(self.replace_btn)
        button_layout.addWidget(self.replace_all_btn)
        button_layout.addWidget(self.close_btn)
        
        layout.addLayout(find_layout)
        layout.addLayout(replace_layout)
        layout.addWidget(self.case_sensitive)
        layout.addWidget(self.whole_words)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.close_btn.clicked.connect(self.close)

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings (Demo)")
        self.setAccessibleName("Settings Dialog")
        self.resize(800, 600)
        
        main_layout = QVBoxLayout()
        
        # Create tab widget to organize different UI controls
        tab_widget = QTabWidget()
        tab_widget.setAccessibleName("Settings Tab Widget")
        
        # Tab 1: Basic Controls
        basic_tab = QWidget()
        basic_layout = QVBoxLayout()
        
        # Button
        button = QPushButton("Sample Button")
        button.setAccessibleName("Sample Button")
        basic_layout.addWidget(QLabel("Button Example:"))
        basic_layout.addWidget(button)
        
        # CheckBox
        checkbox = QCheckBox("Sample Checkbox")
        checkbox.setAccessibleName("Sample Checkbox")
        basic_layout.addWidget(QLabel("CheckBox Example:"))
        basic_layout.addWidget(checkbox)
        
        # ComboBox
        combobox = QComboBox()
        combobox.setAccessibleName("Sample ComboBox")
        combobox.addItems(["Option 1", "Option 2", "Option 3", "Option 4"])
        basic_layout.addWidget(QLabel("ComboBox Example:"))
        basic_layout.addWidget(combobox)
        
        # Edit (LineEdit)
        edit = QLineEdit("Sample text")
        edit.setAccessibleName("Sample Edit Field")
        basic_layout.addWidget(QLabel("Edit Field Example:"))
        basic_layout.addWidget(edit)
        
        # RadioButton Group
        radio_group = QGroupBox("RadioButton Example")
        radio_group.setAccessibleName("Radio Button Group")
        radio_layout = QVBoxLayout()
        radio1 = QRadioButton("Option A")
        radio1.setAccessibleName("Radio Button Option A")
        radio2 = QRadioButton("Option B")
        radio2.setAccessibleName("Radio Button Option B")
        radio3 = QRadioButton("Option C")
        radio3.setAccessibleName("Radio Button Option C")
        radio_layout.addWidget(radio1)
        radio_layout.addWidget(radio2)
        radio_layout.addWidget(radio3)
        radio_group.setLayout(radio_layout)
        basic_layout.addWidget(radio_group)
        
        # ProgressBar
        progress = QProgressBar()
        progress.setAccessibleName("Sample Progress Bar")
        for i in range(5):
            progress.setRange(0, 100)
            progress.setFormat(f"Progress: {i * 20}%")
            QTimer.singleShot(i * 1000, lambda p=progress, v=i * 20: p.setValue(v))
        basic_layout.addWidget(QLabel("ProgressBar Example:"))
        basic_layout.addWidget(progress)
        
        basic_layout.addStretch()
        basic_tab.setLayout(basic_layout)
        tab_widget.addTab(basic_tab, "Basic Controls")
        
        # Tab 2: Advanced Controls
        advanced_tab = QWidget()
        advanced_layout = QVBoxLayout()
        
        # DataGrid (using QTableWidget)
        datagrid = QTableWidget(3, 3)
        datagrid.setAccessibleName("Sample Data Grid")
        datagrid.setHorizontalHeaderLabels(["Column 1", "Column 2", "Column 3"])
        for i in range(3):
            for j in range(3):
                item = QTableWidgetItem(f"Cell {i},{j}")
                item.setData(Qt.AccessibleTextRole, f"Cell {i+1},{j+1}")
                datagrid.setItem(i, j, item)
        advanced_layout.addWidget(QLabel("DataGrid Example:"))
        advanced_layout.addWidget(datagrid)
        
        # List
        list_widget = QListWidget()
        list_widget.setAccessibleName("Sample List")
        for i in range(5):
            item = QListWidgetItem(f"List Item {i+1}")
            item.setData(Qt.AccessibleTextRole, f"List Item {i+1}")
            list_widget.addItem(item)
        advanced_layout.addWidget(QLabel("List Example:"))
        advanced_layout.addWidget(list_widget)
        
        # Tree
        tree = QTreeWidget()
        tree.setAccessibleName("Sample Tree")
        tree.setHeaderLabels(["Tree Structure"])
        root = QTreeWidgetItem(tree, ["Root Node"])
        root.setData(0, Qt.AccessibleTextRole, "Root Node")
        for i in range(3):
            child = QTreeWidgetItem(root, [f"Child {i+1}"])
            child.setData(0, Qt.AccessibleTextRole, f"Child {i+1}")
            for j in range(2):
                subchild = QTreeWidgetItem(child, [f"Subchild {i+1}.{j+1}"])
                subchild.setData(0, Qt.AccessibleTextRole, f"Subchild {i+1}.{j+1}")
        tree.expandAll()
        advanced_layout.addWidget(QLabel("Tree Example:"))
        advanced_layout.addWidget(tree)
        
        advanced_tab.setLayout(advanced_layout)
        tab_widget.addTab(advanced_tab, "Advanced Controls")
        
        # Tab 3: Image and Menu
        visual_tab = QWidget()
        visual_layout = QVBoxLayout()
        
        # Image
        image_label = QLabel()
        image_label.setAccessibleName("Sample Image")
        pixmap = QPixmap(100, 100)
        pixmap.fill(QColor(TABLE_DARK_FG))
        image_label.setPixmap(pixmap)
        visual_layout.addWidget(QLabel("Image Example:"))
        visual_layout.addWidget(image_label)
        
        # Menu (MenuBar with Menu and MenuItem)
        menubar = QMenuBar()
        menubar.setAccessibleName("Sample Menu Bar")
        
        file_menu = QMenu("File", menubar)
        file_menu.setAccessibleName("Sample File Menu")
        
        new_action = QAction("New", file_menu)
        new_action.setObjectName("Sample New MenuItem")
        new_action.setData("Sample New MenuItem")
        
        open_action = QAction("Open", file_menu)
        open_action.setObjectName("Sample Open MenuItem")
        open_action.setData("Sample Open MenuItem")
        
        save_action = QAction("Save", file_menu)
        save_action.setObjectName("Sample Save MenuItem")
        save_action.setData("Sample Save MenuItem")
        
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        
        edit_menu = QMenu("Edit", menubar)
        edit_menu.setAccessibleName("Sample Edit Menu")
        
        menubar.addMenu(file_menu)
        menubar.addMenu(edit_menu)
        
        visual_layout.addWidget(QLabel("Menu Example:"))
        visual_layout.addWidget(menubar)
        visual_layout.addStretch()
        
        visual_tab.setLayout(visual_layout)
        tab_widget.addTab(visual_tab, "Visual Controls")
        
        main_layout.addWidget(tab_widget)
        
        # Dialog buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.setAccessibleName("Dialog Button Box")
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(button_box)
        
        self.setLayout(main_layout)

class CsvTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAccessibleName("CSV Data Table")
        self.setAlternatingRowColors(True)
        self.setEditTriggers(QTableWidget.DoubleClicked | QTableWidget.SelectedClicked)
        self.setSelectionBehavior(QTableWidget.SelectItems)
        self.setSelectionMode(QTableWidget.ExtendedSelection)  # Allow multiple selection
        self.setCornerButtonEnabled(True)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setTabKeyNavigation(True)
        self.setShowGrid(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)
        self.setVerticalScrollMode(QTableWidget.ScrollPerPixel)
        
        # Apply dark theme to table
        self.apply_dark_theme()
        
        self.new_table()

    def apply_dark_theme(self):
        style = f"""
        QTableWidget {{
            background-color: {TABLE_DARK_BG};
            color: {TABLE_DARK_FG};
            gridline-color: {TABLE_GRID_COLOR};
            border: 1px solid {TABLE_GRID_COLOR};
        }}
        QTableWidget::item {{
            background-color: {TABLE_DARK_BG};
            color: {TABLE_DARK_FG};
            border: 1px solid {TABLE_GRID_COLOR};
        }}
        QTableWidget::item:selected {{
            background-color: {TABLE_SELECTION_BG};
        }}
        QTableWidget::item:alternate {{
            background-color: {TABLE_ALTERNATE_BG};
        }}
        QHeaderView::section {{
            background-color: {TABLE_ALTERNATE_BG};
            color: {TABLE_DARK_FG};
            border: 1px solid {TABLE_GRID_COLOR};
            padding: 4px;
        }}
        QTableCornerButton::section {{
            background-color: {TABLE_ALTERNATE_BG};
            border: 1px solid {TABLE_GRID_COLOR};
        }}
        """
        self.setStyleSheet(style)

    def new_table(self):
        self.clear()
        self.setRowCount(INITIAL_NEW_ROWS)
        self.setColumnCount(INITIAL_NEW_COLS)
        self.setHorizontalHeaderLabels([f"Column {i + 1}" for i in range(INITIAL_NEW_COLS)])
        self.setVerticalHeaderLabels([f"Row {i + 1}" for i in range(INITIAL_NEW_ROWS)])
        
        for r in range(INITIAL_NEW_ROWS):
            for c in range(INITIAL_NEW_COLS):
                item = QTableWidgetItem("")
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)
                accessible_name = f"Cell_{r+1}_{c+1}"
                item.setData(Qt.AccessibleTextRole, accessible_name)
                self.setItem(r, c, item)

    def clear_table_contents(self):
        self.clear()
        self.setRowCount(0)
        self.setColumnCount(0)
        self.setHorizontalHeaderLabels([])
        self.setVerticalHeaderLabels([])

    def load_csv(self, file_path):
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            if not data:
                self.clear_table_contents()
                return
            self.setRowCount(len(data))
            self.setColumnCount(len(data[0]))

            for row_idx, row_data in enumerate(data):
                for col_idx, value in enumerate(row_data):
                    item = QTableWidgetItem(value)
                    accessible_name = f"Cell_{row_idx+1}_{col_idx+1}"
                    item.setData(Qt.AccessibleTextRole, accessible_name)
                    item.setFlags(item.flags() | Qt.ItemIsEditable | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.setItem(row_idx, col_idx, item)

            self.setHorizontalHeaderLabels([f"Column {i + 1}" for i in range(self.columnCount())])
            self.setVerticalHeaderLabels([f"Row {i + 1}" for i in range(self.rowCount())])
            self.resizeColumnsToContents()

    def save_csv(self, file_path):
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for row in range(self.rowCount()):
                row_data = []
                for col in range(self.columnCount()):
                    item = self.item(row, col)
                    row_data.append(item.text() if item else "")
                writer.writerow(row_data)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CSV Table Viewer")
        self.setAccessibleName("CSV Table Viewer Main Window")
        self.resize(1200, 800)
        
        # Apply Django-like theme
        self.apply_django_theme()
        
        # Settings for recent files
        self.settings = QSettings("CSVViewer", "RecentFiles")
        self.recent_files = self.settings.value("recentFiles", []) or []
        self.current_file_path = None
        
        self.table = CsvTableWidget(self)

        self.h_scrollbar = QScrollBar(Qt.Horizontal)
        self.h_scrollbar.setObjectName("HorizontalScrollBar")
        self.h_scrollbar.setAccessibleName("Horizontal Scroll Bar")
        
        self.v_scrollbar = QScrollBar(Qt.Vertical)
        self.v_scrollbar.setObjectName("VerticalScrollBar")
        self.v_scrollbar.setAccessibleName("Vertical Scroll Bar")

        # Connect external scrollbars to the table's internal scrollbars
        self.h_scrollbar.valueChanged.connect(self.table.horizontalScrollBar().setValue)
        self.table.horizontalScrollBar().valueChanged.connect(self.h_scrollbar.setValue)
        self.table.horizontalScrollBar().rangeChanged.connect(self.h_scrollbar.setRange)

        self.v_scrollbar.valueChanged.connect(self.table.verticalScrollBar().setValue)
        self.table.verticalScrollBar().valueChanged.connect(self.v_scrollbar.setValue)
        self.table.verticalScrollBar().rangeChanged.connect(self.v_scrollbar.setRange)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)
        grid_layout.addWidget(self.table, 0, 0)
        grid_layout.addWidget(self.v_scrollbar, 0, 1)
        grid_layout.addWidget(self.h_scrollbar, 1, 0)

        corner_widget = QWidget() 
        corner_widget.setAccessibleName("Scroll Bar Corner Widget")
        corner_widget.setFixedSize(self.v_scrollbar.sizeHint().width(), self.h_scrollbar.sizeHint().height())
        grid_layout.addWidget(corner_widget, 1, 1)

        grid_layout.setRowStretch(0, 1)
        grid_layout.setRowStretch(1, 0)
        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 0)
        
        grid_layout.setContentsMargins(10, 10, 10, 10)

        container = QWidget()
        container.setAccessibleName("Main Container Widget")
        container.setLayout(grid_layout)
        self.setCentralWidget(container)
        
        self.create_menus()
        
        # Status bar
        self.status_bar = self.statusBar()
        self.status_bar.setAccessibleName("Status Bar")
        self.status_bar.showMessage("Ready")
        
        # Find/Replace dialog
        self.find_dialog = None

    def apply_django_theme(self):
        style = f"""
        QMainWindow {{
            background-color: {DJANGO_GREEN};
        }}
        QMenuBar {{
            background-color: {DJANGO_GREEN};
            color: white;
            border: 1px solid {DJANGO_LIGHT_GREEN};
        }}
        QMenuBar::item {{
            background-color: transparent;
            padding: 4px 12px;
        }}
        QMenuBar::item:selected {{
            background-color: {DJANGO_LIGHT_GREEN};
        }}
        QMenu {{
            background-color: {DJANGO_GREEN};
            color: white;
            border: 1px solid {DJANGO_LIGHT_GREEN};
        }}
        QMenu::item {{
            padding: 4px 20px;
        }}
        QMenu::item:selected {{
            background-color: {DJANGO_LIGHT_GREEN};
        }}
        QScrollBar:vertical {{
            background-color: {DJANGO_GREEN};
            width: 15px;
            border: 1px solid {DJANGO_LIGHT_GREEN};
        }}
        QScrollBar::handle:vertical {{
            background-color: {DJANGO_LIGHT_GREEN};
            min-height: 20px;
            border-radius: 2px;
        }}
        QScrollBar::handle:vertical:hover {{
            background-color: #5ec49e;
        }}
        QScrollBar:horizontal {{
            background-color: {DJANGO_GREEN};
            height: 15px;
            border: 1px solid {DJANGO_LIGHT_GREEN};
        }}
        QScrollBar::handle:horizontal {{
            background-color: {DJANGO_LIGHT_GREEN};
            min-width: 20px;
            border-radius: 2px;
        }}
        QScrollBar::handle:horizontal:hover {{
            background-color: #5ec49e;
        }}
        QScrollBar::add-line, QScrollBar::sub-line {{
            background: none;
        }}
        QStatusBar {{
            background-color: {DJANGO_GREEN};
            color: white;
            border-top: 1px solid {DJANGO_LIGHT_GREEN};
        }}
        QWidget {{
            background-color: {DJANGO_GREEN};
            color: white;
        }}
        QPushButton {{
            background-color: {DJANGO_LIGHT_GREEN};
            color: white;
            border: none;
            padding: 5px 15px;
            border-radius: 3px;
        }}
        QPushButton:hover {{
            background-color: #5ec49e;
        }}
        QLineEdit, QComboBox, QSpinBox {{
            background-color: #0d4029;
            color: white;
            border: 1px solid {DJANGO_LIGHT_GREEN};
            padding: 3px;
        }}
        QCheckBox, QRadioButton {{
            color: white;
        }}
        QDialog {{
            background-color: {DJANGO_GREEN};
            color: white;
        }}
        QTabWidget::pane {{
            background-color: {DJANGO_GREEN};
            border: 1px solid {DJANGO_LIGHT_GREEN};
        }}
        QTabBar::tab {{
            background-color: #0d4029;
            color: white;
            padding: 5px 10px;
            margin-right: 2px;
        }}
        QTabBar::tab:selected {{
            background-color: {DJANGO_LIGHT_GREEN};
        }}
        QTreeWidget, QListWidget {{
            background-color: #0d4029;
            color: white;
            border: 1px solid {DJANGO_LIGHT_GREEN};
        }}
        QTreeWidget::item:selected, QListWidget::item:selected {{
            background-color: {DJANGO_LIGHT_GREEN};
        }}
        QProgressBar {{
            background-color: #0d4029;
            border: 1px solid {DJANGO_LIGHT_GREEN};
            text-align: center;
        }}
        QProgressBar::chunk {{
            background-color: {DJANGO_LIGHT_GREEN};
        }}
        QGroupBox {{
            color: white;
            border: 1px solid {DJANGO_LIGHT_GREEN};
            margin-top: 10px;
            padding-top: 10px;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
        }}
        """
        self.setStyleSheet(style)

    def create_menus(self):
        menubar = self.menuBar()
        menubar.setAccessibleName("Main Menu Bar")

        # File Menu
        file_menu = menubar.addMenu("&File")
        file_menu.setAccessibleName("File Menu")

        new_action = QAction("&New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_table)
        file_menu.addAction(new_action)
        
        new_window_action = QAction("New &Window", self)
        new_window_action.setShortcut("Ctrl+Shift+N")
        new_window_action.triggered.connect(self.new_window)
        file_menu.addAction(new_window_action)

        open_action = QAction("&Open CSV...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_csv)
        file_menu.addAction(open_action)
        
        # Recent Files submenu
        self.recent_menu = QMenu("Recent Files", self)
        self.recent_menu.setAccessibleName("Recent Files Menu")
        file_menu.addMenu(self.recent_menu)
        self.update_recent_files_menu()
        
        file_menu.addSeparator()
        
        save_action = QAction("&Save", self)
        # save_action.setAccessibleName("Save File Action")
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("Save &As...", self)
        # save_as_action.setAccessibleName("Save As Action")
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_as_file)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()

        exit_action = QAction("E&xit", self)
        # exit_action.setAccessibleName("Exit Action")
        exit_action.setShortcut("Alt+F4")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit Menu
        edit_menu = menubar.addMenu("&Edit")
        edit_menu.setAccessibleName("Edit Menu")
        
        copy_action = QAction("&Copy", self)
        # copy_action.setAccessibleName("Copy Action")
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy_cells)
        edit_menu.addAction(copy_action)

        paste_action = QAction("&Paste", self)
        # paste_action.setAccessibleName("Paste Action")
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.paste_cells)
        edit_menu.addAction(paste_action)
        
        edit_menu.addSeparator()
        
        select_all_action = QAction("Select &All", self)
        # select_all_action.setAccessibleName("Select All Action")
        select_all_action.setShortcut("Ctrl+A")
        select_all_action.triggered.connect(self.select_all)
        edit_menu.addAction(select_all_action)
        
        edit_menu.addSeparator()
        
        find_action = QAction("&Find...", self)
        # find_action.setAccessibleName("Find Action")
        find_action.setShortcut("Ctrl+F")
        find_action.triggered.connect(self.show_find_dialog)
        edit_menu.addAction(find_action)
        
        find_next_action = QAction("Find &Next", self)
        # find_next_action.setAccessibleName("Find Next Action")
        find_next_action.setShortcut("F3")
        find_next_action.triggered.connect(self.find_next)
        edit_menu.addAction(find_next_action)
        
        replace_action = QAction("&Replace...", self)
        # replace_action.setAccessibleName("Replace Action")
        replace_action.setShortcut("Ctrl+H")
        replace_action.triggered.connect(self.show_find_dialog)
        edit_menu.addAction(replace_action)

        # View Menu
        view_menu = menubar.addMenu("&View")
        view_menu.setAccessibleName("View Menu")
        
        resize_action = QAction("&Resize Columns to Contents", self)
        # resize_action.setAccessibleName("Resize Columns Action")
        resize_action.triggered.connect(self.table.resizeColumnsToContents)
        view_menu.addAction(resize_action)

        # Help Menu
        help_menu = menubar.addMenu("&Help")
        help_menu.setAccessibleName("Help Menu")
        
        settings_action = QAction("&Settings", self)
        # settings_action.setAccessibleName("Settings Action")
        settings_action.triggered.connect(self.show_settings)
        help_menu.addAction(settings_action)
        
        help_menu.addSeparator()
        
        about_action = QAction("&About", self)
        # about_action.setAccessibleName("About Action")
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def new_table(self):
        self.table.new_table()
        self.current_file_path = None
        self.setWindowTitle("CSV Table Viewer - New File")
        self.statusBar().showMessage("New table created")

    def new_window(self):
        new_window = MainWindow()
        new_window.show()

    def open_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if file_path:
            try:
                self.table.load_csv(file_path)
                self.current_file_path = file_path
                self.setWindowTitle(f"CSV Table Viewer - {os.path.basename(file_path)}")
                self.statusBar().showMessage(f"Loaded: {file_path}")
                self.add_to_recent_files(file_path)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load CSV:\n{e}")

    def save_file(self):
        if self.current_file_path:
            try:
                self.table.save_csv(self.current_file_path)
                self.statusBar().showMessage(f"Saved: {self.current_file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save CSV:\n{e}")
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV File", "", "CSV Files (*.csv)")
        if file_path:
            try:
                self.table.save_csv(file_path)
                self.current_file_path = file_path
                self.setWindowTitle(f"CSV Table Viewer - {os.path.basename(file_path)}")
                self.statusBar().showMessage(f"Saved: {file_path}")
                self.add_to_recent_files(file_path)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save CSV:\n{e}")

    def add_to_recent_files(self, file_path):
        if file_path in self.recent_files:
            self.recent_files.remove(file_path)
        self.recent_files.insert(0, file_path)
        self.recent_files = self.recent_files[:MAX_RECENT_FILES]
        self.settings.setValue("recentFiles", self.recent_files)
        self.update_recent_files_menu()

    def update_recent_files_menu(self):
        self.recent_menu.clear()
        for i, file_path in enumerate(self.recent_files):
            if os.path.exists(file_path):
                action = QAction(f"{i+1}. {os.path.basename(file_path)}", self)
                # action.setAccessibleName(f"Recent File {i+1}")
                action.setData(file_path)
                action.triggered.connect(lambda checked, path=file_path: self.open_recent_file(path))
                self.recent_menu.addAction(action)

    def open_recent_file(self, file_path):
        if os.path.exists(file_path):
            try:
                self.table.load_csv(file_path)
                self.current_file_path = file_path
                self.setWindowTitle(f"CSV Table Viewer - {os.path.basename(file_path)}")
                self.statusBar().showMessage(f"Loaded: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load CSV:\n{e}")
                self.recent_files.remove(file_path)
                self.settings.setValue("recentFiles", self.recent_files)
                self.update_recent_files_menu()

    def copy_cells(self):
        selected_items = self.table.selectedItems()
        if selected_items:
            text = "\n".join([item.text() for item in selected_items])
            QApplication.clipboard().setText(text)
            self.statusBar().showMessage(f"Copied {len(selected_items)} cells")

    def paste_cells(self):
        clipboard_text = QApplication.clipboard().text()
        if clipboard_text and self.table.currentItem():
            current_row = self.table.currentRow()
            current_col = self.table.currentColumn()
            
            lines = clipboard_text.strip().split('\n')
            for i, line in enumerate(lines):
                if current_row + i < self.table.rowCount():
                    item = self.table.item(current_row + i, current_col)
                    if item:
                        item.setText(line.split('\t')[0])  # Handle tab-separated values

    def select_all(self):
        self.table.selectAll()
        self.statusBar().showMessage("All cells selected")

    def show_find_dialog(self):
        if not self.find_dialog:
            self.find_dialog = FindReplaceDialog(self)
            self.connect_find_dialog_signals()
        self.find_dialog.show()
        self.find_dialog.raise_()
        self.find_dialog.activateWindow()

    def connect_find_dialog_signals(self):
        self.find_dialog.find_next_btn.clicked.connect(self.find_next)
        self.find_dialog.find_all_btn.clicked.connect(self.find_all)
        self.find_dialog.replace_btn.clicked.connect(self.replace_current)
        self.find_dialog.replace_all_btn.clicked.connect(self.replace_all)

    def find_next(self):
        if not self.find_dialog:
            return
            
        search_text = self.find_dialog.find_input.text()
        if not search_text:
            return
            
        case_sensitive = self.find_dialog.case_sensitive.isChecked()
        current_row = self.table.currentRow() if self.table.currentRow() >= 0 else 0
        current_col = self.table.currentColumn() if self.table.currentColumn() >= 0 else 0
        
        # Search from current position
        found = False
        for row in range(current_row, self.table.rowCount()):
            start_col = current_col + 1 if row == current_row else 0
            for col in range(start_col, self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    text = item.text()
                    if not case_sensitive:
                        text = text.lower()
                        search_text = search_text.lower()
                    if search_text in text:
                        self.table.setCurrentCell(row, col)
                        found = True
                        self.statusBar().showMessage(f"Found at Row {row+1}, Column {col+1}")
                        return
        
        if not found:
            self.statusBar().showMessage("No more occurrences found")

    def find_all(self):
        if not self.find_dialog:
            return
            
        search_text = self.find_dialog.find_input.text()
        if not search_text:
            return
            
        case_sensitive = self.find_dialog.case_sensitive.isChecked()
        found_count = 0
        
        self.table.clearSelection()
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    text = item.text()
                    if not case_sensitive:
                        text = text.lower()
                        search = search_text.lower()
                    else:
                        search = search_text
                    if search in text:
                        item.setSelected(True)
                        found_count += 1
        
        self.statusBar().showMessage(f"Found {found_count} occurrences")

    def replace_current(self):
        if not self.find_dialog:
            return
            
        current_item = self.table.currentItem()
        if current_item and current_item.isSelected():
            replace_text = self.find_dialog.replace_input.text()
            current_item.setText(replace_text)
            self.find_next()

    def replace_all(self):
        if not self.find_dialog:
            return
            
        search_text = self.find_dialog.find_input.text()
        replace_text = self.find_dialog.replace_input.text()
        if not search_text:
            return
            
        case_sensitive = self.find_dialog.case_sensitive.isChecked()
        replaced_count = 0
        
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    text = item.text()
                    if not case_sensitive:
                        if search_text.lower() in text.lower():
                            # Case-insensitive replace
                            import re
                            pattern = re.compile(re.escape(search_text), re.IGNORECASE)
                            new_text = pattern.sub(replace_text, text)
                            item.setText(new_text)
                            replaced_count += 1
                    else:
                        if search_text in text:
                            new_text = text.replace(search_text, replace_text)
                            item.setText(new_text)
                            replaced_count += 1
        
        self.statusBar().showMessage(f"Replaced {replaced_count} occurrences")

    def show_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec_()

    def show_about(self):
        QMessageBox.about(self, "About CSV Table Viewer",
                          "CSV Table Viewer\n\n"
                          "An accessible, automatable table UI for large CSV files.\n"
                          "Built with PyQt5.\n\n"
                          "Features:\n"
                          "• Full accessibility support for UI automation\n"
                          "• Dark theme inspired by Django\n"
                          "• Find and replace functionality\n"
                          "• Recent files tracking\n"
                          "• Multiple window support")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for better theming
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())