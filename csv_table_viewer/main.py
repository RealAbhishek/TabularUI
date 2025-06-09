#!/usr/bin/env python3
"""
CSV Table Viewer Application
Main entry point
"""

import sys
import logging
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from views.main_window import MainWindow
from core.settings import AppSettings
from utils.platform_utils import configure_platform_specific

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main application entry point"""
    try:
        # Create Qt application
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        
        # Set application metadata
        app.setOrganizationName("CSVViewer")
        app.setApplicationName("CSV Table Viewer")
        app.setApplicationDisplayName("CSV Table Viewer")
        
        # High DPI support
        app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
        app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
        
        # Configure platform-specific settings
        configure_platform_specific()
        
        # Initialize application settings
        settings = AppSettings.instance()
        settings.load()
        
        # Create and show main window
        window = MainWindow()
        window.show()
        
        logger.info("Application started successfully")
        
        # Run event loop
        return app.exec_()
        
    except Exception as e:
        logger.error(f"Application failed to start: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())