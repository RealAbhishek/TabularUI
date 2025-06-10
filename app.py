import sys
import csv
import json
import os
from datetime import datetime
from PyQt5.QtCore import Qt, QSettings, QTimer, QDate, QTime
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QColor, QFont
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QAction, QTableWidget, QTableWidgetItem, 
    QGridLayout, QWidget, QMessageBox, QScrollBar, QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QCheckBox, QComboBox, QLineEdit, QTextEdit, QProgressBar,
    QRadioButton, QTreeWidget, QTreeWidgetItem, QListWidget, QListWidgetItem,
    QGroupBox, QMenuBar, QMenu, QDialogButtonBox, QSpinBox, QSlider, QTabWidget,
    QCalendarWidget, QDateEdit, QTimeEdit, QDial, QLCDNumber, QFontComboBox,
    QScrollArea, QSplitter, QStackedWidget, QToolBar, QStatusBar, QDockWidget,
    QHeaderView, QInputDialog, QShortcut, QActionGroup, QTextBrowser
)

# Constants
INITIAL_NEW_ROWS = 50
INITIAL_NEW_COLS = 50
MAX_RECENT_FILES = 10

# Theme configurations
THEMES = {
    "Django": {
        "name": "Django",
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
    },
    "Windows 11": {
        "name": "Windows 11",
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
}

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
        self.resize(900, 700)
        
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
        
        # SpinBox
        spinbox = QSpinBox()
        spinbox.setAccessibleName("Sample SpinBox")
        spinbox.setRange(0, 100)
        spinbox.setValue(50)
        basic_layout.addWidget(QLabel("SpinBox Example:"))
        basic_layout.addWidget(spinbox)
        
        # Slider
        slider = QSlider(Qt.Horizontal)
        slider.setAccessibleName("Sample Slider")
        slider.setRange(0, 100)
        slider.setValue(30)
        basic_layout.addWidget(QLabel("Slider Example:"))
        basic_layout.addWidget(slider)
        
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
        progress.setValue(45)
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
                item.setData(Qt.AccessibleTextRole, f"DataGrid Cell {i+1},{j+1}")
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
        
        # Tab 3: Date and Time Controls
        datetime_tab = QWidget()
        datetime_layout = QVBoxLayout()
        
        # CalendarWidget
        calendar = QCalendarWidget()
        calendar.setAccessibleName("Sample Calendar Widget")
        datetime_layout.addWidget(QLabel("Calendar Widget Example:"))
        datetime_layout.addWidget(calendar)
        
        # DateEdit
        date_edit = QDateEdit()
        date_edit.setAccessibleName("Sample Date Edit")
        date_edit.setDate(QDate.currentDate())
        date_edit.setCalendarPopup(True)
        datetime_layout.addWidget(QLabel("Date Edit Example:"))
        datetime_layout.addWidget(date_edit)
        
        # TimeEdit
        time_edit = QTimeEdit()
        time_edit.setAccessibleName("Sample Time Edit")
        time_edit.setTime(QTime.currentTime())
        datetime_layout.addWidget(QLabel("Time Edit Example:"))
        datetime_layout.addWidget(time_edit)
        
        datetime_layout.addStretch()
        datetime_tab.setLayout(datetime_layout)
        tab_widget.addTab(datetime_tab, "Date/Time Controls")
        
        # Tab 4: Special Controls
        special_tab = QWidget()
        special_layout = QVBoxLayout()
        
        # Dial
        dial = QDial()
        dial.setAccessibleName("Sample Dial")
        dial.setRange(0, 100)
        dial.setValue(75)
        special_layout.addWidget(QLabel("Dial Example:"))
        special_layout.addWidget(dial)
        
        # LCD Number
        lcd = QLCDNumber()
        lcd.setAccessibleName("Sample LCD Number")
        lcd.display(42)
        special_layout.addWidget(QLabel("LCD Number Example:"))
        special_layout.addWidget(lcd)
        
        # Font ComboBox
        font_combo = QFontComboBox()
        font_combo.setAccessibleName("Sample Font ComboBox")
        special_layout.addWidget(QLabel("Font ComboBox Example:"))
        special_layout.addWidget(font_combo)
        
        special_layout.addStretch()
        special_tab.setLayout(special_layout)
        tab_widget.addTab(special_tab, "Special Controls")
        
        # Tab 5: Container Controls
        container_tab = QWidget()
        container_layout = QVBoxLayout()
        
        # ScrollArea
        scroll_area = QScrollArea()
        scroll_area.setAccessibleName("Sample Scroll Area")
        scroll_content = QWidget()
        scroll_content_layout = QVBoxLayout()
        for i in range(10):
            scroll_content_layout.addWidget(QLabel(f"Scrollable content line {i+1}"))
        scroll_content.setLayout(scroll_content_layout)
        scroll_area.setWidget(scroll_content)
        scroll_area.setWidgetResizable(True)
        scroll_area.setMaximumHeight(150)
        container_layout.addWidget(QLabel("Scroll Area Example:"))
        container_layout.addWidget(scroll_area)
        
        # Splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.setAccessibleName("Sample Splitter")
        left_widget = QTextEdit("Left panel")
        left_widget.setAccessibleName("Splitter Left Panel")
        right_widget = QTextEdit("Right panel")
        right_widget.setAccessibleName("Splitter Right Panel")
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        container_layout.addWidget(QLabel("Splitter Example:"))
        container_layout.addWidget(splitter)
        
        # StackedWidget
        stacked = QStackedWidget()
        stacked.setAccessibleName("Sample Stacked Widget")
        page1 = QLabel("Page 1 Content")
        page1.setAccessibleName("Stacked Widget Page 1")
        page2 = QLabel("Page 2 Content")
        page2.setAccessibleName("Stacked Widget Page 2")
        stacked.addWidget(page1)
        stacked.addWidget(page2)
        container_layout.addWidget(QLabel("Stacked Widget Example:"))
        container_layout.addWidget(stacked)
        
        container_tab.setLayout(container_layout)
        tab_widget.addTab(container_tab, "Container Controls")
        
        # Tab 6: Visual Controls and Bars
        visual_tab = QWidget()
        visual_layout = QVBoxLayout()
        
        # Image
        image_label = QLabel()
        image_label.setAccessibleName("Sample Image")
        pixmap = QPixmap(100, 100)
        pixmap.fill(QColor("#44b78b"))
        image_label.setPixmap(pixmap)
        visual_layout.addWidget(QLabel("Image Example:"))
        visual_layout.addWidget(image_label)
        
        # ToolBar
        toolbar = QToolBar()
        toolbar.setAccessibleName("Sample Tool Bar")
        toolbar.addAction("Tool 1")
        toolbar.addAction("Tool 2")
        toolbar.addSeparator()
        toolbar.addAction("Tool 3")
        visual_layout.addWidget(QLabel("ToolBar Example:"))
        visual_layout.addWidget(toolbar)
        
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
        self.setSelectionMode(QTableWidget.ExtendedSelection)
        self.setCornerButtonEnabled(True)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setTabKeyNavigation(True)
        self.setShowGrid(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)
        self.setVerticalScrollMode(QTableWidget.ScrollPerPixel)
        
        self.new_table()

    def apply_theme(self, theme):
        style = f"""
        QTableWidget {{
            background-color: {theme['table_bg']};
            color: {theme['table_fg']};
            gridline-color: {theme['table_grid']};
            border: 1px solid {theme['table_grid']};
        }}
        QTableWidget::item {{
            background-color: {theme['table_bg']};
            color: {theme['table_fg']};
            border: 1px solid {theme['table_grid']};
        }}
        QTableWidget::item:selected {{
            background-color: {theme['table_selection']};
        }}
        QTableWidget::item:alternate {{
            background-color: {theme['table_alternate']};
        }}
        QHeaderView::section {{
            background-color: {theme['table_alternate']};
            color: {theme['table_fg']};
            border: 1px solid {theme['table_grid']};
            padding: 4px;
        }}
        QTableCornerButton::section {{
            background-color: {theme['table_alternate']};
            border: 1px solid {theme['table_grid']};
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
        
        # Settings
        self.settings = QSettings("CSVViewer", "AppSettings")
        self.recent_files = self.settings.value("recentFiles", []) or []
        self.current_theme_name = self.settings.value("theme", "Django") or "Django"
        self.current_theme = THEMES[self.current_theme_name]
        self.current_file_path = None
        
        # Create widgets before applying theme
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
        
        # Create dock widget example
        self.create_dock_widget()
        
        # Create menus
        self.create_menus()
        
        # Status bar
        self.status_bar = self.statusBar()
        self.status_bar.setAccessibleName("Status Bar")
        self.status_bar.showMessage("Ready")
        
        # Find/Replace dialog
        self.find_dialog = None
        
        # Apply theme
        self.apply_theme(self.current_theme_name)

    def create_dock_widget(self):
        dock = QDockWidget("Information Panel", self)
        dock.setAccessibleName("Information Dock Widget")
        
        dock_content = QTextBrowser()
        dock_content.setAccessibleName("Dock Widget Content")
        dock_content.setHtml("""
        <h3>Welcome to CSV Table Viewer</h3>
        <p>This panel demonstrates a DockWidget component.</p>
        <p>You can drag this panel around or close it.</p>
        """)
        
        dock.setWidget(dock_content)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)

    def apply_theme(self, theme_name):
        self.current_theme_name = theme_name
        self.current_theme = THEMES[theme_name]
        theme = self.current_theme
        
        # Apply theme to table
        self.table.apply_theme(theme)
        
        # Windows 11 specific adjustments
        is_windows_11 = theme_name == "Windows 11"
        button_fg = "black" if is_windows_11 else "white"
        
        style = f"""
        QMainWindow {{
            background-color: {theme['main_bg']};
            color: {theme['main_fg']};
        }}
        QWidget {{
            background-color: {theme['main_bg']};
            color: {theme['main_fg']};
        }}
        QMenuBar {{
            background-color: {theme['menu_bg']};
            color: {theme['main_fg']};
            border: 1px solid {theme['accent']};
        }}
        QMenuBar::item {{
            background-color: transparent;
            padding: 4px 12px;
            color: {theme['main_fg']};
        }}
        QMenuBar::item:selected {{
            background-color: {theme['menu_hover']};
        }}
        QMenu {{
            background-color: {theme['menu_bg']};
            color: {theme['main_fg']};
            border: 1px solid {theme['accent']};
        }}
        QMenu::item {{
            padding: 4px 20px;
            color: {theme['main_fg']};
        }}
        QMenu::item:selected {{
            background-color: {theme['menu_hover']};
        }}
        QScrollBar:vertical {{
            background-color: {theme['scrollbar_bg']};
            width: 15px;
            border: 1px solid {theme['accent']};
        }}
        QScrollBar::handle:vertical {{
            background-color: {theme['scrollbar_handle']};
            min-height: 20px;
            border-radius: 2px;
        }}
        QScrollBar::handle:vertical:hover {{
            background-color: {theme['scrollbar_handle_hover']};
        }}
        QScrollBar:horizontal {{
            background-color: {theme['scrollbar_bg']};
            height: 15px;
            border: 1px solid {theme['accent']};
        }}
        QScrollBar::handle:horizontal {{
            background-color: {theme['scrollbar_handle']};
            min-width: 20px;
            border-radius: 2px;
        }}
        QScrollBar::handle:horizontal:hover {{
            background-color: {theme['scrollbar_handle_hover']};
        }}
        QScrollBar::add-line, QScrollBar::sub-line {{
            background: none;
        }}
        QScrollBar::add-page, QScrollBar::sub-page {{
            background: {theme['scrollbar_bg']};
        }}
        QStatusBar {{
            background-color: {theme['main_bg']};
            color: {theme['main_fg']};
            border-top: 1px solid {theme['accent']};
        }}
        QPushButton {{
            background-color: {theme['button_bg']};
            color: {button_fg};
            border: none;
            padding: 5px 15px;
            border-radius: 3px;
        }}
        QPushButton:hover {{
            background-color: {theme['button_hover']};
        }}
        QLineEdit, QComboBox, QSpinBox {{
            background-color: {theme['input_bg']};
            color: {theme['main_fg']};
            border: 1px solid {theme['accent']};
            padding: 3px;
        }}
        QCheckBox, QRadioButton {{
            color: {theme['main_fg']};
        }}
        QDialog {{
            background-color: {theme['main_bg']};
            color: {theme['main_fg']};
        }}
        QTabWidget::pane {{
            background-color: {theme['main_bg']};
            border: 1px solid {theme['accent']};
        }}
        QTabBar::tab {{
            background-color: {theme['input_bg']};
            color: {theme['main_fg']};
            padding: 5px 10px;
            margin-right: 2px;
        }}
        QTabBar::tab:selected {{
            background-color: {theme['accent']};
            color: white;
        }}
        QTreeWidget, QListWidget {{
            background-color: {theme['input_bg']};
            color: {theme['main_fg']};
            border: 1px solid {theme['accent']};
        }}
        QTreeWidget::item:selected, QListWidget::item:selected {{
            background-color: {theme['accent']};
        }}
        QProgressBar {{
            background-color: {theme['input_bg']};
            border: 1px solid {theme['accent']};
            text-align: center;
            color: {theme['main_fg']};
        }}
        QProgressBar::chunk {{
            background-color: {theme['accent']};
        }}
        QGroupBox {{
            color: {theme['main_fg']};
            border: 1px solid {theme['accent']};
            margin-top: 10px;
            padding-top: 10px;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
        }}
        QDockWidget {{
            background-color: {theme['main_bg']};
            color: {theme['main_fg']};
        }}
        QDockWidget::title {{
            background-color: {theme['main_bg']};
            color: {theme['main_fg']};
            border: 1px solid {theme['accent']};
            padding: 5px;
        }}
        QTextBrowser {{
            background-color: {theme['input_bg']};
            color: {theme['main_fg']};
            border: 1px solid {theme['accent']};
        }}
        QHeaderView::section {{
            background-color: {theme['input_bg']};
            color: {theme['main_fg']};
            border: 1px solid {theme['accent']};
            padding: 4px;
        }}
        """
        
        # Apply stylesheet
        self.setStyleSheet(style)
        
        # Update window frame color (platform-specific)
        if sys.platform == "win32":
            try:
                import ctypes
                from ctypes import wintypes
                
                # Dark title bar for dark themes
                if theme_name == "Django":
                    # Use dark mode
                    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                    hwnd = int(self.winId())
                    value = ctypes.c_int(1)  # TRUE for dark mode
                    ctypes.windll.dwmapi.DwmSetWindowAttribute(
                        hwnd, 
                        DWMWA_USE_IMMERSIVE_DARK_MODE,
                        ctypes.byref(value),
                        ctypes.sizeof(value)
                    )
                else:
                    # Use light mode
                    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                    hwnd = int(self.winId())
                    value = ctypes.c_int(0)  # FALSE for light mode
                    ctypes.windll.dwmapi.DwmSetWindowAttribute(
                        hwnd, 
                        DWMWA_USE_IMMERSIVE_DARK_MODE,
                        ctypes.byref(value),
                        ctypes.sizeof(value)
                    )
            except:
                pass  # Fallback if Windows API is not available
        
        # Save theme preference
        self.settings.setValue("theme", theme_name)

    def create_menus(self):
        menubar = self.menuBar()
        menubar.setAccessibleName("Main Menu Bar")

        # File Menu
        file_menu = menubar.addMenu("&File")
        file_menu.setAccessibleName("File Menu")

        new_action = QAction("&New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_table)

        
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
        file_menu.addMenu(self.recent_menu)
        self.update_recent_files_menu()
        
        file_menu.addSeparator()
        
        save_action = QAction("&Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("Save &As...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_as_file)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()

        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Alt+F4")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit Menu
        edit_menu = menubar.addMenu("&Edit")
        edit_menu.setAccessibleName("Edit Menu")
        
        copy_action = QAction("&Copy", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy_cells)
        edit_menu.addAction(copy_action)

        paste_action = QAction("&Paste", self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.paste_cells)
        edit_menu.addAction(paste_action)
        
        edit_menu.addSeparator()
        
        select_all_action = QAction("Select &All", self)
        select_all_action.setShortcut("Ctrl+A")
        select_all_action.triggered.connect(self.select_all)
        edit_menu.addAction(select_all_action)
        
        edit_menu.addSeparator()
        
        find_action = QAction("&Find...", self)
        find_action.setShortcut("Ctrl+F")
        find_action.triggered.connect(self.show_find_dialog)
        edit_menu.addAction(find_action)
        
        find_next_action = QAction("Find &Next", self)
        find_next_action.setShortcut("F3")
        find_next_action.triggered.connect(self.find_next)
        edit_menu.addAction(find_next_action)
        
        replace_action = QAction("&Replace...", self)
        replace_action.setShortcut("Ctrl+H")
        replace_action.triggered.connect(self.show_find_dialog)
        edit_menu.addAction(replace_action)

        # View Menu
        view_menu = menubar.addMenu("&View")
        view_menu.setAccessibleName("View Menu")
        
        resize_action = QAction("&Resize Columns to Contents", self)
        resize_action.triggered.connect(self.table.resizeColumnsToContents)
        view_menu.addAction(resize_action)
        
        view_menu.addSeparator()
        
        # Theme submenu
        theme_menu = QMenu("&Theme", self)
        theme_menu.setAccessibleName("Theme Menu")
        
        theme_group = QActionGroup(self)
        for theme_name in THEMES.keys():
            theme_action = QAction(theme_name, self)
            theme_action.setCheckable(True)
            theme_action.setChecked(theme_name == self.current_theme_name)
            theme_action.triggered.connect(lambda checked, name=theme_name: self.apply_theme(name))
            theme_group.addAction(theme_action)
            theme_menu.addAction(theme_action)
        
        view_menu.addMenu(theme_menu)

        # Help Menu
        help_menu = menubar.addMenu("&Help")
        help_menu.setAccessibleName("Help Menu")
        
        settings_action = QAction("&Settings", self)
        settings_action.triggered.connect(self.show_settings)
        help_menu.addAction(settings_action)
        
        help_menu.addSeparator()
        
        # Shortcut demonstration
        shortcut_action = QAction("&Keyboard Shortcuts", self)
        shortcut_action.triggered.connect(self.show_shortcuts)
        help_menu.addAction(shortcut_action)
        
        help_menu.addSeparator()
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        # Create custom shortcuts
        self.create_shortcuts()

    def create_shortcuts(self):
        # Additional custom shortcuts
        shortcut1 = QShortcut("Ctrl+Shift+F", self)
        shortcut1.setObjectName("Advanced Find Shortcut")
        shortcut1.activated.connect(lambda: self.statusBar().showMessage("Advanced Find (Ctrl+Shift+F) pressed"))
        
        shortcut2 = QShortcut("F5", self)
        shortcut2.setObjectName("Refresh Shortcut")
        shortcut2.activated.connect(lambda: self.statusBar().showMessage("Refresh (F5) pressed"))

    def show_shortcuts(self):
        shortcuts_text = """
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
        <tr><td><b>Ctrl+Shift+F</b></td><td>Advanced find (demo)</td></tr>
        <tr><td><b>F5</b></td><td>Refresh (demo)</td></tr>
        </table>
        """
        msg = QMessageBox()
        msg.setWindowTitle("Keyboard Shortcuts")
        msg.setTextFormat(Qt.RichText)
        msg.setText(shortcuts_text)
        msg.exec_()

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
                        item.setText(line.split('\t')[0])

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
        about_text = f"""
        <h3>CSV Table Viewer</h3>
        <p>An accessible, automatable table UI for large CSV files.</p>
        <p>Built with PyQt5.</p>
        <p><b>Current Theme:</b> {self.current_theme_name}</p>
        <h4>Features:</h4>
        <ul>
        <li>Full accessibility support for UI automation</li>
        <li>Multiple themes (Django and Windows 11)</li>
        <li>Find and replace functionality</li>
        <li>Recent files tracking</li>
        <li>Multiple window support</li>
        <li>Comprehensive UI component demonstrations</li>
        </ul>
        """
        msg = QMessageBox()
        msg.setWindowTitle("About CSV Table Viewer")
        msg.setTextFormat(Qt.RichText)
        msg.setText(about_text)
        msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for better theming
    
    # Create input dialog demonstration
    # text, ok = QInputDialog.getText(None, "Welcome", "Enter your name (optional):", 
    #                                QLineEdit.Normal, "")
    # if ok and text:
    #     print(f"Welcome, {text}!")
    
    window = MainWindow()
    dialog = SettingsDialog()
    dialog.show()
    window.show()
    sys.exit(app.exec_())