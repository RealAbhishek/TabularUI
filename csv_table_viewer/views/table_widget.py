"""
CSV table widget
"""

import logging
from typing import Optional
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QKeyEvent

from core import INITIAL_NEW_ROWS, INITIAL_NEW_COLS, ThemeManager

from models import CSVModel
from utils import set_accessible_name

logger = logging.getLogger(__name__)


class CsvTableWidget(QTableWidget):
    """Table widget for displaying CSV data"""
    
    def __init__(self, csv_model: CSVModel, parent=None):
        super().__init__(parent)
        self._csv_model = csv_model
        self._current_theme = None
        
        # Setup table
        self._setup_table()
        
        # Connect to model
        self._csv_model.attach(self._on_model_changed)
    
    def _setup_table(self):
        """Setup table properties"""
        set_accessible_name(self, "CSV Data Table")
        
        # Table settings
        self.setAlternatingRowColors(True)
        self.setEditTriggers(
            QTableWidget.DoubleClicked | QTableWidget.SelectedClicked
        )
        self.setSelectionBehavior(QTableWidget.SelectItems)
        self.setSelectionMode(QTableWidget.ExtendedSelection)
        self.setCornerButtonEnabled(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setTabKeyNavigation(True)
        self.setShowGrid(True)
        
        # Disable internal scrollbars (using external ones)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)
        self.setVerticalScrollMode(QTableWidget.ScrollPerPixel)
    
    def _on_model_changed(self):
        """Handle model data changes"""
        self._update_from_model()
    
    def _update_from_model(self):
        """Update table from model data"""
        data = self._csv_model.get_data()
        
        if not data:
            self.clear()
            self.setRowCount(0)
            self.setColumnCount(0)
            return
        
        # Set table dimensions
        self.setRowCount(len(data))
        self.setColumnCount(len(data[0]) if data else 0)
        
        # Set headers
        self.setHorizontalHeaderLabels(
            [f"Column {i + 1}" for i in range(self.columnCount())]
        )
        self.setVerticalHeaderLabels(
            [f"Row {i + 1}" for i in range(self.rowCount())]
        )
        
        # Populate table
        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                # item.setFlags(
                #     Qt.ItemFlags.ItemIsSelectable | Qt.ItemFlags.ItemIsEnabled | Qt.ItemFlags.ItemIsEditable
                # )
                item.setData(Qt.ItemDataRole.AccessibleTextRole, f"Cell_{row_idx+1}_{col_idx+1}")
                self.setItem(row_idx, col_idx, item)
        
        # Resize columns
        self.resizeColumnsToContents()
    
    def update_theme(self):
        """Update table theme"""
        if self._current_theme:
            theme = ThemeManager.create_theme(self._current_theme)
        if theme:
            self._apply_table_theme(theme)
    
    def _apply_table_theme(self, theme):
        """Apply theme to table"""
        colors = theme.get_colors()
        
        style = f"""
        QTableWidget {{
            background-color: {colors['table_bg']};
            color: {colors['table_fg']};
            gridline-color: {colors['table_grid']};
            border: 1px solid {colors['table_grid']};
        }}
        QTableWidget::item {{
            background-color: {colors['table_bg']};
            color: {colors['table_fg']};
            border: 1px solid {colors['table_grid']};
        }}
        QTableWidget::item:selected {{
            background-color: {colors['table_selection']};
        }}
        QTableWidget::item:alternate {{
            background-color: {colors['table_alternate']};
        }}
        QHeaderView::section {{
            background-color: {colors['table_alternate']};
            color: {colors['table_fg']};
            border: 1px solid {colors['table_grid']};
            padding: 4px;
        }}
        QTableCornerButton::section {{
            background-color: {colors['table_alternate']};
            border: 1px solid {colors['table_grid']};
        }}
        """
        
        self.setStyleSheet(style)
    
    def set_theme(self, theme_name: str):
        """Set the current theme"""
        self._current_theme = theme_name
        self.update_theme()
    
    # Override item change to update model
    def itemChanged(self, item: QTableWidgetItem):
        """Handle item changes"""
        if item:
            row = item.row()
            col = item.column()
            value = item.text()
            
            # Update model
            self._csv_model.set_cell(row, col, value)