"""
Logging configuration for Flask application
Provides structured logging for debugging and monitoring
"""

import logging
import logging.handlers
import os
from datetime import datetime


class LoggerSetup:
    """Setup logging configuration for the Flask app"""

    @staticmethod
    def setup_logging(app, log_level=logging.INFO):
        """
        Configure logging for Flask application

        Args:
            app: Flask application instance
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """

        # Create logs directory if it doesn't exist
        log_dir = os.path.join(os.path.dirname(__file__), 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Remove default Flask logger
        for handler in app.logger.handlers[:]:
            app.logger.removeHandler(handler)

        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        simple_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Console Handler (INFO level and above)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)

        # File Handler for all logs (DEBUG level and above)
        log_file = os.path.join(log_dir, 'app.log')
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(detailed_formatter)

        # Rotating File Handler for error logs
        error_log_file = os.path.join(log_dir, 'errors.log')
        error_handler = logging.handlers.RotatingFileHandler(
            error_log_file,
            maxBytes=10485760,  # 10MB
            backupCount=5
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_formatter)

        # Add handlers to app logger
        app.logger.addHandler(console_handler)
        app.logger.addHandler(file_handler)
        app.logger.addHandler(error_handler)
        app.logger.setLevel(log_level)

        # Log startup message
        app.logger.info("=" * 60)
        app.logger.info("Flask Application Started")
        app.logger.info(f"Environment: {app.config.get('ENV', 'unknown')}")
        app.logger.info(f"Debug Mode: {app.debug}")
        app.logger.info(f"Log Level: {logging.getLevelName(log_level)}")
        app.logger.info("=" * 60)

        return app.logger


def get_logger(name):
    """
    Get logger instance with the given name

    Args:
        name: Logger name (usually __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)
