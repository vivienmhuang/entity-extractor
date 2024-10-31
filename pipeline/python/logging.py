# /*************************************************************************************************
# Imports 
# *************************************************************************************************/
import logging
import sys
from datetime import datetime

# /*************************************************************************************************
# Importing scripts
# *************************************************************************************************/
class Logger:
    """
    A wrapper class for Python's built-in logging module that provides simplified logging functionality.
    
    This class sets up a logger with console output and a consistent format for log messages.
    It includes methods for different logging levels (info, error, warning, debug) and
    automatically handles formatter creation and handler setup.

    Attributes:
        logger (logging.Logger): The underlying logger instance from the logging module.
    """
    def __init__(self, name):
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers to avoid duplicates
        self.logger.handlers.clear()
        
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
    
    def info(self, message):
        self.logger.info(message)
    
    def error(self, message):
        self.logger.error(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def debug(self, message):
        self.logger.debug(message)