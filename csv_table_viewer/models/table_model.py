"""
Qt Table Model adapter for CSV data
"""

from typing import Any, Optional
from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex
from PyQt5.QtGui import QColor

from .csv_model import CSVModel


class TableModel(QAbstractTableModel):
    """Qt table model adapter for CSVModel"""
    
    def __init__(self, csv_model: CSVModel, parent=None):
        super().__init__(parent)
        self._csv_model = csv_model
        self._csv_model.attach(self._on_data_changed)   
    
    def _on_data_changed(self) -> None:
        """Handle data changes from CSV model"""
        self.beginResetModel()
        self.endResetModel()
    
    # QAbstractTableModel implementation
    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Get number of rows"""
        if parent.isValid():
            return 0
        return self._csv_model.get_row_count()
    
    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Get number of columns"""
        if parent.isValid():
            return 0
        return self._csv_model.get_column_count()
    
    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        """Get data for a specific cell"""
        if not index.isValid():
            return None
        
        row, col = index.row(), index.column()

        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            return self._csv_model.get_cell(row, col)
        
        elif role == Qt.ItemDataRole.AccessibleTextRole:
            return f"Cell_{row+1}_{col+1}"

        return None

    def setData(self, index: QModelIndex, value: Any, role: int = Qt.ItemDataRole.EditRole) -> bool:
        """Set data for a specific cell"""
        if not index.isValid() or role != Qt.ItemDataRole.EditRole:
            return False
        
        row, col = index.row(), index.column()
        self._csv_model.set_cell(row, col, str(value))
        self.dataChanged.emit(index, index, [role])
        return True


    def headerData(self, section: int, orientation: Qt.Orientation,
                   role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        """Get header data"""
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return f"Column {section + 1}"
            else:
                return f"Row {section + 1}"

        elif role == Qt.ItemDataRole.AccessibleTextRole:
            if orientation == Qt.Orientation.Horizontal:
                return f"Column Header {section + 1}"
            else:
                return f"Row Header {section + 1}"
        
        return None
    
    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        """
        This method tells the view what is allowed for each cell.
        This is the key to enabling editing.
        """
        if not index.isValid():
            return Qt.ItemFlags()        # No flags for invalid index
        # selected, enabled, and edited.
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable