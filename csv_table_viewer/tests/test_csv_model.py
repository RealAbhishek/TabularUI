"""
Tests for CSV model
"""

import unittest
import tempfile
import os
from pathlib import Path

from models import CSVModel


class TestCSVModel(unittest.TestCase):
    """Test cases for CSVModel"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.model = CSVModel()
        self.temp_file = None
    
    def tearDown(self):
        """Clean up test fixtures"""
        if self.temp_file and os.path.exists(self.temp_file):
            os.unlink(self.temp_file)
    
    def test_new_document(self):
        """Test creating new document"""
        self.model.new_document(5, 3)
        
        self.assertEqual(self.model.get_row_count(), 5)
        self.assertEqual(self.model.get_column_count(), 3)
        self.assertFalse(self.model.is_modified)
        self.assertFalse(self.model.has_file)
    
    def test_set_get_cell(self):
        """Test setting and getting cell values"""
        self.model.new_document(3, 3)
        
        # Set cell value
        self.model.set_cell(1, 1, "test")
        self.assertEqual(self.model.get_cell(1, 1), "test")
        self.assertTrue(self.model.is_modified)
        
        # Out of bounds
        self.assertEqual(self.model.get_cell(10, 10), "")
    
    def test_save_load_file(self):
        """Test saving and loading files"""
        # Create test data
        self.model.new_document(3, 2)
        self.model.set_cell(0, 0, "A1")
        self.model.set_cell(0, 1, "B1")
        self.model.set_cell(1, 0, "A2")
        self.model.set_cell(1, 1, "B2")
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            self.temp_file = f.name
        
        self.model.save_to_file(self.temp_file)
        self.assertFalse(self.model.is_modified)
        
        # Load from file
        new_model = CSVModel()
        new_model.load_from_file(self.temp_file)
        
        # Verify data
        self.assertEqual(new_model.get_cell(0, 0), "A1")
        self.assertEqual(new_model.get_cell(0, 1), "B1")
        self.assertEqual(new_model.get_cell(1, 0), "A2")
        self.assertEqual(new_model.get_cell(1, 1), "B2")
    
    def test_observer_pattern(self):
        """Test observer notification"""
        notified = []
        
        def observer():
            notified.append(True)
        
        self.model.attach(observer)
        
        # Should notify on new document
        self.model.new_document(2, 2)
        self.assertEqual(len(notified), 1)
        
        # Should notify on cell change
        self.model.set_cell(0, 0, "test")
        self.assertEqual(len(notified), 2)
        
        # Detach observer
        self.model.detach(observer)
        self.model.set_cell(1, 1, "test2")
        self.assertEqual(len(notified), 2)  # No new notification


if __name__ == '__main__':
    unittest.main()