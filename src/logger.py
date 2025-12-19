import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(log_file, name="idsips", level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=3)
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
