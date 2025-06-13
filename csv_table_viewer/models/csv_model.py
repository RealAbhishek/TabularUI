"""
CSV data model
"""

import csv
import logging
from typing import List, Optional, Callable
from pathlib import Path

logger = logging.getLogger(__name__)


class CSVModel:
    """Model for handling CSV data"""
    
    def __init__(self):
        self._data: List[List[str]] = []
        self._file_path: Optional[Path] = None
        self._modified: bool = False
        self._observers: List[Callable] = []
    
    # Observer pattern implementation
    def attach(self, observer: Callable) -> None:
        """Attach an observer to be notified of data changes"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Callable) -> None:
        """Detach an observer"""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def _notify_observers(self) -> None:
        """Notify all observers of data changes"""
        for observer in self._observers:
            try:
                observer()
            except Exception as e:
                logger.error(f"Error notifying observer: {e}")
    
    # Data management
    def load_from_file(self, file_path: str) -> None:
        """Load CSV data from file"""
        try:
            path = Path(file_path)
            with path.open('r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                self._data = list(reader)
            
            self._file_path = path
            self._modified = False
            logger.info(f"Loaded CSV from: {file_path}")
            self._notify_observers()
            
        except Exception as e:
            logger.error(f"Failed to load CSV: {e}")
            raise
    
    def save_to_file(self, file_path: Optional[str] = None) -> None:
        """Save CSV data to file"""
        try:
            path = Path(file_path) if file_path else self._file_path
            if not path:
                raise ValueError("No file path specified")
            
            with path.open('w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(self._data)
            
            self._file_path = path
            self._modified = False
            logger.info(f"Saved CSV to: {path}")
            
        except Exception as e:
            logger.error(f"Failed to save CSV: {e}")
            raise
    
    def new_document(self, rows: int, cols: int) -> None:
        """Create a new empty document"""
        self._data = [[f"Cell_{r + 1}_{c + 1}" for c in range(cols)] for r in range(rows)]
        self._file_path = None
        self._modified = False
        logger.info(f"Created new document: {rows}x{cols}")
        self._notify_observers()
    
    # Data access
    def get_data(self) -> List[List[str]]:
        """Get all data"""
        return self._data
    
    def get_cell(self, row: int, col: int) -> str:
        """Get value of a specific cell"""
        if 0 <= row < len(self._data) and 0 <= col < len(self._data[row]):
            return self._data[row][col]
        return ""
    
    def set_cell(self, row: int, col: int, value: str) -> None:
        """Set value of a specific cell"""
        if 0 <= row < len(self._data) and 0 <= col < len(self._data[row]):
            if self._data[row][col] != value:
                self._data[row][col] = value
                self._modified = True
                # self._notify_observers()
    
    def get_row_count(self) -> int:
        """Get number of rows"""
        return len(self._data)
    
    def get_column_count(self) -> int:
        """Get number of columns"""
        return len(self._data[0]) if self._data else 0
    
    # Properties
    @property
    def file_path(self) -> Optional[Path]:
        """Get current file path"""
        return self._file_path
    
    @property
    def is_modified(self) -> bool:
        """Check if data has been modified"""
        return self._modified
    
    @property
    def has_file(self) -> bool:
        """Check if model is associated with a file"""
        return self._file_path is not None
    
    def clear(self) -> None:
        """Clear all data"""
        self._data = []
        self._file_path = None
        self._modified = False
        self._notify_observers()