import sys
import csv
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QAction, QTableWidget, QTableWidgetItem, 
    QGridLayout, QWidget, QMessageBox, QScrollBar
)

# Constants for the new empty table
INITIAL_NEW_ROWS = 50
INITIAL_NEW_COLS = 20

class CsvTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlternatingRowColors(True)
        self.setEditTriggers(QTableWidget.DoubleClicked | QTableWidget.SelectedClicked)
        self.setSelectionBehavior(QTableWidget.SelectItems)
        self.setSelectionMode(QTableWidget.SingleSelection)
        self.setCornerButtonEnabled(True)
        # Enable keyboard navigation and accessibility features
        self.setFocusPolicy(Qt.StrongFocus)
        self.setTabKeyNavigation(True)

        self.setShowGrid(True)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Ensure scroll per pixel is set for smooth control by external scrollbars
        self.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)
        self.setVerticalScrollMode(QTableWidget.ScrollPerPixel)

    def new_table(self):
        """Create a new empty table with predefined dimensions."""
        self.clear() # Clears everything including headers and items
        self.setRowCount(INITIAL_NEW_ROWS)
        self.setColumnCount(INITIAL_NEW_COLS)

        # Set numbered headers
        self.setHorizontalHeaderLabels([str(i + 1) for i in range(INITIAL_NEW_COLS)])
        self.setVerticalHeaderLabels([str(i + 1) for i in range(INITIAL_NEW_ROWS)])

        # Populate with empty, editable items
        for r in range(INITIAL_NEW_ROWS):
            for c in range(INITIAL_NEW_COLS):
                item = QTableWidgetItem("") # Empty item
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)
                accessible_name = f"cell_{r}_{c}"
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
                self.clear_table_contents() # Clear if CSV is empty
                return
            self.setRowCount(len(data))
            self.setColumnCount(len(data[0]))

            for row_idx, row_data in enumerate(data):
                for col_idx, value in enumerate(row_data):
                    item = QTableWidgetItem(value)
                    accessible_name = f"cell_{row_idx}_{col_idx}"
                    item.setData(Qt.AccessibleTextRole, accessible_name)
                    item.setFlags(item.flags() | Qt.ItemIsEditable) # Make cells editable
                    self.setItem(row_idx, col_idx, item)
            
            self.setHorizontalHeaderLabels([str(i+1) for i in range(self.columnCount())])
            self.setVerticalHeaderLabels([str(i+1) for i in range(self.rowCount())])
            self.resizeColumnsToContents() # Optional: adjust column widths


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CSV Table Viewer")
        self.resize(1200, 800)

        self.table = CsvTableWidget(self)

        self.h_scrollbar = QScrollBar(Qt.Horizontal)
        self.h_scrollbar.setObjectName("HorizontalScrollBar")
        self.h_scrollbar.setAccessibleName("Horizontal Scroll Bar")
        self.v_scrollbar = QScrollBar(Qt.Vertical)
        self.v_scrollbar.setObjectName("VerticalScrollBar")
        self.v_scrollbar.setAccessibleName("Vertical Scroll Bar")

        # Connect external scrollbars to the table's internal scrollbars
        # Horizontal scrollbar
        self.h_scrollbar.valueChanged.connect(self.table.horizontalScrollBar().setValue)
        self.table.horizontalScrollBar().valueChanged.connect(self.h_scrollbar.setValue)
        self.table.horizontalScrollBar().rangeChanged.connect(self.h_scrollbar.setRange)

        # Vertical scrollbar
        self.v_scrollbar.valueChanged.connect(self.table.verticalScrollBar().setValue)
        self.table.verticalScrollBar().valueChanged.connect(self.v_scrollbar.setValue)
        self.table.verticalScrollBar().rangeChanged.connect(self.v_scrollbar.setRange)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(0) # No space between widgets
        grid_layout.addWidget(self.table, 0, 0)
        grid_layout.addWidget(self.v_scrollbar, 0, 1)
        grid_layout.addWidget(self.h_scrollbar, 1, 0)


        grid_layout.addWidget(self.table, 0, 0)          # Table in cell (0,0)
        grid_layout.addWidget(self.v_scrollbar, 0, 1)    # Vertical scrollbar in cell (0,1)
        grid_layout.addWidget(self.h_scrollbar, 1, 0)    # Horizontal scrollbar in cell (1,0)

        grid_layout.setContentsMargins(10, 10, 10, 10)

        # Optional: Add a corner widget (e.g., QSizeGrip or just a plain QWidget)
        # If you use QTableWidget.setCornerButtonEnabled(False) in CsvTableWidget
        # or if you want a custom widget in the corner.
        # For simplicity, we can add a plain QWidget to fill the space.
        corner_widget = QWidget() 
        # Make corner widget non-distracting, or use QSizeGrip(self) for resizing
        corner_widget.setFixedSize(self.v_scrollbar.sizeHint().width(), self.h_scrollbar.sizeHint().height())
        grid_layout.addWidget(corner_widget, 1, 1) # Corner widget in cell (1,1)


        # Set row and column stretch factors so the table expands
        grid_layout.setRowStretch(0, 1)    # Row 0 (table and v_scrollbar) takes all vertical stretch
        grid_layout.setRowStretch(1, 0)    # Row 1 (h_scrollbar and corner) does not stretch vertically
        grid_layout.setColumnStretch(0, 1) # Column 0 (table and h_scrollbar) takes all horizontal stretch
        grid_layout.setColumnStretch(1, 0) # Column 1 (v_scrollbar and corner) does not stretch horizontally
        

        container = QWidget()
        container.setLayout(grid_layout)
        self.setCentralWidget(container)
        self.create_menus()
        self.statusBar().showMessage("Ready")


    def create_menus(self):
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu("&File")

        new_action = QAction("&New", self)
        new_action.triggered.connect(lambda: self.table.clearContents())
        new_action.triggered.connect(self.new_table)
        file_menu.addAction(new_action)

        open_action = QAction("&Open CSV...", self)
        open_action.triggered.connect(self.open_csv)
        file_menu.addAction(open_action)

        exit_action = QAction("E&xit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit Menu
        edit_menu = menubar.addMenu("&Edit")
        copy_action = QAction("&Copy", self)
        copy_action.triggered.connect(self.copy_cell)
        edit_menu.addAction(copy_action)

        paste_action = QAction("&Paste", self)
        paste_action.triggered.connect(self.paste_cell)
        edit_menu.addAction(paste_action)

        # View Menu
        view_menu = menubar.addMenu("&View")
        resize_action = QAction("&Resize Columns to Contents", self)
        resize_action.triggered.connect(self.table.resizeColumnsToContents)
        view_menu.addAction(resize_action)

        # Help Menu
        help_menu = menubar.addMenu("&Help")
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def new_table(self):
        self.table.new_table()
        self.statusBar().showMessage("New table created with default size.")

    def open_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if file_path:
            try:
                self.table.load_csv(file_path)
                self.statusBar().showMessage(f"Loaded: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load CSV:\n{e}")

    def copy_cell(self):
        item = self.table.currentItem()
        if item:
            QApplication.clipboard().setText(item.text())

    def paste_cell(self):
        item = self.table.currentItem()
        if item:
            item.setText(QApplication.clipboard().text())

    def show_about(self):
        QMessageBox.about(self, "About CSV Table Viewer",
                          "CSV Table Viewer\nAccessible, automatable table UI for large CSV files.\n"
                          "Built with PyQt5.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())