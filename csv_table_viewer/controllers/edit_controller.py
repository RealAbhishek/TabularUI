"""
Edit operations controller
"""

import re
import logging
from typing import Optional, Tuple, List
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import QItemSelectionModel

from models import CSVModel

logger = logging.getLogger(__name__)


class EditController:
    """Controller for edit operations"""
    
    def __init__(self, csv_model: CSVModel):
        self._csv_model = csv_model
        self._last_search_pos = (0, 0)
    
    def copy_cells(self, table: QTableView) -> int:
        """Copy selected cells to clipboard using QTableView's selection model."""
        selection_model = table.selectionModel()
        if not selection_model.hasSelection():
            return 0
        
        indexes = selection_model.selectedIndexes()
        if not indexes:
            return 0

        min_row = min(index.row() for index in indexes)
        max_row = max(index.row() for index in indexes)
        min_col = min(index.column() for index in indexes)
        max_col = max(index.column() for index in indexes)

        clipboard_text = []
        for row in range(min_row, max_row + 1):
            row_text = []
            for col in range(min_col, max_col + 1):
                index = table.model().index(row, col)
                if index in indexes:
                    # Use the model to get data
                    cell_data = table.model().data(index) or ""
                    row_text.append(cell_data)
                else:
                    row_text.append("")
            clipboard_text.append("\t".join(row_text))

        QApplication.clipboard().setText("\n".join(clipboard_text))
        
        logger.info(f"Copied {len(indexes)} cells")
        return len(indexes)
    
    def paste_cells(self, table: QTableView) -> int:
        """Paste cells from clipboard into a QTableView."""
        clipboard = QApplication.clipboard()
        if not clipboard:
            return 0
        
        text = clipboard.text()
        if not text:
            return 0
        
        start_index = table.currentIndex()
        if not start_index.isValid():
            return 0
        
        start_row = start_index.row()
        start_col = start_index.column()
        model = table.model()

        lines = text.strip().split('\n')
        count = 0
        
        for i, line in enumerate(lines):
            row = start_row + i
            if row >= model.rowCount():
                break
            
            cells = line.split('\t')
            for j, cell_text in enumerate(cells):
                col = start_col + j
                if col >= model.columnCount():
                    break
                
                target_index = model.index(row, col)
                model.setData(target_index, cell_text)
                count += 1
        
        logger.info(f"Pasted {count} cells")
        return count
    
    def find_text(self, table: QTableView, text: str, 
                  case_sensitive: bool, whole_words: bool,
                  find_next: bool = False) -> Optional[Tuple[int, int]]:
        """Find text in the model associated with a QTableView."""
        if not text:
            return None
        
        model = table.model()
        
        pattern = re.escape(text)
        if whole_words:
            pattern = r'\b' + pattern + r'\b'
        
        flags = 0 if case_sensitive else re.IGNORECASE
        
        start_row, start_col = (0, 0)
        if find_next:
            start_row, start_col = self._last_search_pos
            start_col += 1
        
        # Search from start position to the end
        for row in range(start_row, model.rowCount()):
            col_start = start_col if row == start_row else 0
            for col in range(col_start, model.columnCount()):
                index = model.index(row, col)
                cell_data = model.data(index) or ""
                if re.search(pattern, cell_data, flags):
                    table.setCurrentIndex(index)
                    self._last_search_pos = (row, col)
                    return (row, col)

        # Wrap-around search from the beginning to the start position
        if find_next:
            for row in range(0, start_row + 1):
                col_end = start_col if row == start_row else model.columnCount()
                for col in range(0, col_end):
                    index = model.index(row, col)
                    cell_data = model.data(index) or ""
                    if re.search(pattern, cell_data, flags):
                        table.setCurrentIndex(index)
                        self._last_search_pos = (row, col)
                        return (row, col)
        
        return None
    
    def find_all(self, table: QTableView, text: str,
                 case_sensitive: bool, whole_words: bool) -> int:
        """Find all occurrences and select them in the QTableView."""
        if not text:
            return 0
        
        model = table.model()
        selection_model = table.selectionModel()
        
        pattern = re.escape(text)
        if whole_words:
            pattern = r'\b' + pattern + r'\b'
        
        flags = 0 if case_sensitive else re.IGNORECASE
        
        selection_model.clear()
        
        count = 0
        for row in range(model.rowCount()):
            for col in range(model.columnCount()):
                index = model.index(row, col)
                cell_data = model.data(index) or ""
                if re.search(pattern, cell_data, flags):
                    # Select the matching cell
                    selection_model.select(index, QItemSelectionModel.Select)
                    count += 1
        
        logger.info(f"Found {count} occurrences")
        return count

    def replace_all(self, table: QTableView, find_text: str,
                   replace_text: str, case_sensitive: bool,
                   whole_words: bool) -> int:
        """Replace all occurrences in the model."""
        if not find_text:
            return 0
        
        model = table.model()
        
        pattern = re.escape(find_text)
        if whole_words:
            pattern = r'\b' + pattern + r'\b'
        
        flags = 0 if case_sensitive else re.IGNORECASE
        
        count = 0
        for row in range(model.rowCount()):
            for col in range(model.columnCount()):
                index = model.index(row, col)
                cell_data = model.data(index) or ""
                if re.search(pattern, cell_data, flags):
                    new_text = re.sub(pattern, replace_text, cell_data, flags=flags)
                    model.setData(index, new_text)
                    count += 1
        
        logger.info(f"Replaced {count} occurrences")
        return count