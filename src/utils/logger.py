import os
import logging
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOGS_DIR = os.path.join(BASE_DIR, "logs")

# Create logs directory if it doesn't exist
os.makedirs(LOGS_DIR, exist_ok=True)

def setup_logger(name: str, log_file: str = None, level: int = logging.INFO) -> logging.Logger:
    """Set up and configure a logger."""
    logger = logging.getLogger(name)
    
    if logger.handlers:  # Return existing logger if already configured
        return logger
        
    logger.setLevel(level)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        log_path = os.path.join(LOGS_DIR, log_file)
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger
