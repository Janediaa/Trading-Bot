"""Logging configuration module."""

import logging
import logging.handlers
from pathlib import Path
from typing import Optional


class LoggerSetup:
    """Setup and manage application logging."""

    _loggers: dict = {}
    LOG_DIR = Path(__file__).parent.parent / "logs"
    LOG_FILE = LOG_DIR / "trading_bot.log"
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    @classmethod
    def setup_log_directory(cls) -> None:
        """Create logs directory if it doesn't exist."""
        cls.LOG_DIR.mkdir(exist_ok=True)

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """
        Get or create a logger with rotating file handler.

        Args:
            name: Logger name (typically __name__).

        Returns:
            logging.Logger: Configured logger instance.
        """
        if name in cls._loggers:
            return cls._loggers[name]

        cls.setup_log_directory()

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        # Remove existing handlers to avoid duplicates
        if logger.handlers:
            logger.handlers.clear()

        # Rotating file handler
        file_handler = logging.handlers.RotatingFileHandler(
            cls.LOG_FILE,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5,
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(cls.LOG_FORMAT, cls.DATE_FORMAT)
        file_handler.setFormatter(file_formatter)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(cls.LOG_FORMAT, cls.DATE_FORMAT)
        console_handler.setFormatter(console_formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        cls._loggers[name] = logger
        return logger
