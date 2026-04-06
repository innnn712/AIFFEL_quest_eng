# app/logger_config.py
"""
Day 3 - 로거 설정
"""
import logging


def setup_logger(name: str) -> logging.Logger:
    """로거를 설정하고 반환합니다."""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger