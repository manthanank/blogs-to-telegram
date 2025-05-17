"""
Logging utility for the blogs-to-telegram project.
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys
import time
from datetime import datetime

def setup_logger(name="blogs_to_telegram", log_level=logging.INFO, to_console=True, to_file=True):
    """
    Set up a logger with the specified name, log level, and outputs.
    
    Args:
        name (str): The name of the logger
        log_level (int): The logging level (e.g., logging.INFO, logging.DEBUG)
        to_console (bool): Whether to log to the console
        to_file (bool): Whether to log to a file
    
    Returns:
        logging.Logger: The configured logger
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Clear existing handlers
    logger.handlers = []
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Add console handler if requested
    if to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # Add file handler if requested
    if to_file:
        # Create logs directory if it doesn't exist
        logs_dir = Path(__file__).parents[1] / "logs"
        os.makedirs(logs_dir, exist_ok=True)
        
        # Create a rotating file handler
        log_file = logs_dir / f"{name}.log"
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=5 * 1024 * 1024,  # 5 MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def log_execution_time(logger, func_name):
    """
    Decorator to log the execution time of a function.
    
    Args:
        logger (logging.Logger): The logger to use
        func_name (str): The name of the function (for logging)
    
    Returns:
        function: A decorator that logs execution time
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            logger.info(f"Starting {func_name}")
            
            try:
                result = func(*args, **kwargs)
                end_time = time.time()
                execution_time = end_time - start_time
                logger.info(f"Completed {func_name} in {execution_time:.2f} seconds")
                return result
            except Exception as e:
                end_time = time.time()
                execution_time = end_time - start_time
                logger.error(f"Error in {func_name} after {execution_time:.2f} seconds: {e}")
                raise
        
        return wrapper
    
    return decorator
