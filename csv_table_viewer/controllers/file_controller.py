"""
File operations controller
"""

import logging
from typing import Optional
from pathlib import Path

from core import INITIAL_NEW_ROWS, INITIAL_NEW_COLS
from models import CSVModel

logger = logging.getLogger(__name__)


class FileController:
    """Controller for file operations"""
    
    def __init__(self, csv_model: CSVModel):
        self._csv_model = csv_model
    
    def new_file(self):
        """Create a new file"""
        logger.info("Creating new file")
        self._csv_model.new_document(INITIAL_NEW_ROWS, INITIAL_NEW_COLS)
    
    def open_file(self, file_path: str):
        """Open a file"""
        logger.info(f"Opening file: {file_path}")
        self._csv_model.load_from_file(file_path)
    
    def save_file(self):
        """Save current file"""
        if self._csv_model.has_file:
            logger.info("Saving file")
            self._csv_model.save_to_file()
        else:
            raise ValueError("No file path specified")
    
    def save_file_as(self, file_path: str):
        """Save file with new path"""
        logger.info(f"Saving file as: {file_path}")
        self._csv_model.save_to_file(file_path)
    
    def has_unsaved_changes(self) -> bool:
        """Check if there are unsaved changes"""
        return self._csv_model.is_modified
    
    def get_current_file_path(self) -> Optional[Path]:
        """Get current file path"""
        return self._csv_model.file_path