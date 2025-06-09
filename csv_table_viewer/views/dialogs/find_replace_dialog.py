"""
Find and Replace dialog
"""

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QCheckBox, QGroupBox
)

from utils import set_accessible_name


class FindReplaceDialog(QDialog):
    """Find and Replace dialog"""
    
    # Signals
    find_requested = pyqtSignal(str, bool, bool, bool)  # text, case, whole, next
    find_next_requested = pyqtSignal()
    find_all_requested = pyqtSignal(str, bool, bool)
    replace_requested = pyqtSignal(str, str, bool, bool)
    replace_all_requested = pyqtSignal(str, str, bool, bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup dialog UI"""
        self.setWindowTitle("Find and Replace")
        set_accessible_name(self, "Find and Replace Dialog")
        self.setFixedSize(450, 300)
        
        layout = QVBoxLayout()
        
        # Find section
        find_group = QGroupBox("Find")
        find_layout = QHBoxLayout()
        
        find_label = QLabel("Find:")
        set_accessible_name(find_label, "Find Label")
        
        self._find_input = QLineEdit()
        set_accessible_name(self._find_input, "Find Text Input")
        
        find_layout.addWidget(find_label)
        find_layout.addWidget(self._find_input)
        find_group.setLayout(find_layout)
        
        # Replace section
        replace_group = QGroupBox("Replace")
        replace_layout = QHBoxLayout()
        
        replace_label = QLabel("Replace:")
        set_accessible_name(replace_label, "Replace Label")
        
        self._replace_input = QLineEdit()
        set_accessible_name(self._replace_input, "Replace Text Input")
        
        replace_layout.addWidget(replace_label)
        replace_layout.addWidget(self._replace_input)
        replace_group.setLayout(replace_layout)
        
        # Options
        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout()
        
        self._case_sensitive = QCheckBox("Case sensitive")
        set_accessible_name(self._case_sensitive, "Case Sensitive Checkbox")
        
        self._whole_words = QCheckBox("Whole words only")
        set_accessible_name(self._whole_words, "Whole Words Checkbox")
        
        options_layout.addWidget(self._case_sensitive)
        options_layout.addWidget(self._whole_words)
        options_group.setLayout(options_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self._find_btn = QPushButton("Find")
        set_accessible_name(self._find_btn, "Find Button")
        self._find_btn.clicked.connect(self._on_find)
        
        self._find_next_btn = QPushButton("Find Next")
        set_accessible_name(self._find_next_btn, "Find Next Button")
        self._find_next_btn.clicked.connect(self._on_find_next)
        
        self._find_all_btn = QPushButton("Find All")
        set_accessible_name(self._find_all_btn, "Find All Button")
        self._find_all_btn.clicked.connect(self._on_find_all)
        
        self._replace_btn = QPushButton("Replace")
        set_accessible_name(self._replace_btn, "Replace Button")
        self._replace_btn.clicked.connect(self._on_replace)
        
        self._replace_all_btn = QPushButton("Replace All")
        set_accessible_name(self._replace_all_btn, "Replace All Button")
        self._replace_all_btn.clicked.connect(self._on_replace_all)
        
        self._close_btn = QPushButton("Close")
        set_accessible_name(self._close_btn, "Close Button")
        self._close_btn.clicked.connect(self._close)
        
        button_layout.addWidget(self._find_btn)
        button_layout.addWidget(self._find_next_btn)
        button_layout.addWidget(self._find_all_btn)
        button_layout.addWidget(self._replace_btn)
        button_layout.addWidget(self._replace_all_btn)
        button_layout.addWidget(self._close_btn)
        
        # Add to main layout
        layout.addWidget(find_group)
        layout.addWidget(replace_group)
        layout.addWidget(options_group)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Set initial focus
        self._find_input.setFocus()
    
    def show_replace_options(self):
        """Show replace options"""
        self._replace_input.setFocus()
    
    def get_find_text(self) -> str:
        """Get find text"""
        return self._find_input.text()
    
    def get_replace_text(self) -> str:
        """Get replace text"""
        return self._replace_input.text()
    
    def is_case_sensitive(self) -> bool:
        """Check if case sensitive"""
        return self._case_sensitive.isChecked()
    
    def is_whole_words(self) -> bool:
        """Check if whole words only"""
        return self._whole_words.isChecked()
    
    # Slots
    def _on_find(self):
        """Handle find button"""
        text = self.get_find_text()
        if text:
            self.find_requested.emit(
                text,
                self.is_case_sensitive(),
                self.is_whole_words(),
                False
            )
    
    def _on_find_next(self):
        """Handle find next button"""
        self.find_next_requested.emit()
    
    def _on_find_all(self):
        """Handle find all button"""
        text = self.get_find_text()
        if text:
            self.find_all_requested.emit(
                text,
                self.is_case_sensitive(),
                self.is_whole_words()
            )
    
    def _on_replace(self):
        """Handle replace button"""
        find_text = self.get_find_text()
        replace_text = self.get_replace_text()
        if find_text:
            self.replace_requested.emit(
                find_text,
                replace_text,
                self.is_case_sensitive(),
                self.is_whole_words()
            )
    
    def _on_replace_all(self):
        """Handle replace all button"""
        find_text = self.get_find_text()
        replace_text = self.get_replace_text()
        if find_text:
            self.replace_all_requested.emit(
                find_text,
                replace_text,
                self.is_case_sensitive(),
                self.is_whole_words()
            )

    def _close(self):
        """Close the dialog"""
        self.reject()
        self.close()