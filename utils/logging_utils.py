"""
Logging utilities for Theo-AI.
"""
import os
import logging
from pathlib import Path

def setup_logger(name: str, log_file: str, level=logging.INFO):
    """
    Set up a logger with file and console handlers.
    
    Args:
        name: Name of the logger.
        log_file: Path to the log file.
        level: Logging level.
        
    Returns:
        A configured logger instance.
    """
    # Ensure the logs directory exists
    Path("logs").mkdir(exist_ok=True)
    
    # Configure logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Add file handler
    file_handler = logging.FileHandler(f"logs/{log_file}")
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    
    # Add console handler
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger 