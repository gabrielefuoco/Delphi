import logging
import sys
from pathlib import Path

# Adapted from src/utils/logger.py

def setup_logger(name="ThesisFlowManager"):
    """Configures the application logger."""
    # Log to a file in the skill directory or temp?
    # For CLI, stdout is usually enough, but let's keep file logging if verbose
    
    # Let's log to .agent/logs if possible, or just stderr
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stderr)
        ]
    )
    
    logger = logging.getLogger(name)
    return logger

def get_logger(name="ThesisFlowManager"):
    return logging.getLogger(name)
