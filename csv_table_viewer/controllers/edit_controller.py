"""
Edit operations controller
"""

import re
import logging
from typing import Optional, Tuple, List
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QApplication

from models import CSVModel

logger = logging.getLogger(__name__)


class EditController:
    """Controller for edit operations"""
    
    def __init__(self, csv_model: CSVModel):
        self._csv_model = csv_model
        self._last_search_pos = (0, 0)
    
    def copy_cells(self, table: QTableWidget) -> int:
        """Copy selected cells to clipboard"""
        selected_items = table.selectedItems()
        if not selected_items:
            return 0
        
        # Get selection bounds
        rows = sorted(set(item.row() for item in selected_items))
        cols = sorted(set(item.column() for item in selected_items))
        
        # Build clipboard text
        clipboard_text = []
        for row in rows:
            row_text = []
            for col in cols:
                item = table.item(row, col)
                if item and item.isSelected():
                    row_text.append(item.text())
                else:
                    row_text.append("")
            clipboard_text.append("\t".join(row_text))
        
        # Copy to clipboard
        clipboard = QApplication.clipboard()
        if clipboard:
            clipboard.setText("\n".join(clipboard_text))
        
        logger.info(f"Copied {len(selected_items)} cells")
        return len(selected_items)
    
    def paste_cells(self, table: QTableWidget) -> int:
        """Paste cells from clipboard"""
        clipboard = QApplication.clipboard()
        if not clipboard:
            return 0
        text = clipboard.text()
        
        if not text:
            return 0
        
        current_item = table.currentItem()
        if not current_item:
            return 0
        
        start_row = current_item.row()
        start_col = current_item.column()
        
        # Parse clipboard text
        lines = text.strip().split('\n')
        count = 0
        
        for i, line in enumerate(lines):
            if start_row + i >= table.rowCount():
                break
            
            cells = line.split('\t')
            for j, cell_text in enumerate(cells):
                if start_col + j >= table.columnCount():
                    break
                
                item = table.item(start_row + i, start_col + j)
                if item:
                    item.setText(cell_text)
                    count += 1
        
        logger.info(f"Pasted {count} cells")
        return count
    
    def find_text(self, table: QTableWidget, text: str, 
                  case_sensitive: bool, whole_words: bool,
                  find_next: bool = False) -> Optional[Tuple[int, int]]:
        """Find text in table"""
        if not text:
            return None
        
        # Prepare search pattern
        pattern = text
        if whole_words:
            pattern = r'\b' + re.escape(text) + r'\b'
        else:
            pattern = re.escape(text)
        
        flags = 0 if case_sensitive else re.IGNORECASE
        
        # Determine start position
        if find_next:
            start_row, start_col = self._last_search_pos
            start_col += 1  # Start from next cell
        else:
            start_row, start_col = 0, 0
        
        # Search from current position
        for row in range(start_row, table.rowCount()):
            col_start = start_col if row == start_row else 0
            for col in range(col_start, table.columnCount()):
                item = table.item(row, col)
                if item and re.search(pattern, item.text(), flags):
                    table.setCurrentCell(row, col)
                    self._last_search_pos = (row, col)
                    return (row, col)
        
        # Wrap around search
        if find_next and (start_row > 0 or start_col > 0):
            for row in range(0, start_row + 1):
                col_end = start_col if row == start_row else table.columnCount()
                for col in range(0, col_end):
                    item = table.item(row, col)
                    if item and re.search(pattern, item.text(), flags):
                        table.setCurrentCell(row, col)
                        self._last_search_pos = (row, col)
                        return (row, col)
        
        return None
    
    def find_all(self, table: QTableWidget, text: str,
                 case_sensitive: bool, whole_words: bool) -> int:
        """Find all occurrences of text"""
        if not text:
            return 0
        
        # Prepare search pattern
        pattern = text
        if whole_words:
            pattern = r'\b' + re.escape(text) + r'\b'
        else:
            pattern = re.escape(text)
        
        flags = 0 if case_sensitive else re.IGNORECASE
        
        # Clear selection
        table.clearSelection()
        
        # Search all cells
        count = 0
        for row in range(table.rowCount()):
            for col in range(table.columnCount()):
                item = table.item(row, col)
                if item and re.search(pattern, item.text(), flags):
                    item.setSelected(True)
                    count += 1
        
        logger.info(f"Found {count} occurrences")
        return count
    
    def replace_current(self, table: QTableWidget, find_text: str,
                       replace_text: str, case_sensitive: bool,
                       whole_words: bool) -> bool:
        """Replace current occurrence"""
        current_item = table.currentItem()
        if not current_item or not current_item.isSelected():
            return False
        
        # Prepare search pattern
        pattern = find_text
        if whole_words:
            pattern = r'\b' + re.escape(find_text) + r'\b'
        else:
            pattern = re.escape(find_text)
        
        flags = 0 if case_sensitive else re.IGNORECASE
        
        # Check if current item matches
        if re.search(pattern, current_item.text(), flags):
            new_text = re.sub(pattern, replace_text, current_item.text(), flags=flags)
            current_item.setText(new_text)
            return True
        
        return False
    
    def replace_all(self, table: QTableWidget, find_text: str,
                   replace_text: str, case_sensitive: bool,
                   whole_words: bool) -> int:
        """Replace all occurrences"""
        if not find_text:
            return 0
        
        # Prepare search pattern
        pattern = find_text
        if whole_words:
            pattern = r'\b' + re.escape(find_text) + r'\b'
        else:
            pattern = re.escape(find_text)
        
        flags = 0 if case_sensitive else re.IGNORECASE
        
        # Replace in all cells
        count = 0
        for row in range(table.rowCount()):
            for col in range(table.columnCount()):
                item = table.item(row, col)
                if item and re.search(pattern, item.text(), flags):
                    new_text = re.sub(pattern, replace_text, item.text(), flags=flags)
                    item.setText(new_text)
                    count += 1
        
        logger.info(f"Replaced {count} occurrences")
        return count