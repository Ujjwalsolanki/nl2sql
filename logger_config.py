# logger_config.py

import logging
import os

def setup_logging(
    log_file: str = "nl2sql_app.log",
    log_level: str = "INFO",
    console_output: bool = True
) -> logging.Logger:
    """
    Configures and returns a logger for the application.

    Args:
        log_file (str): The name of the file to which logs will be written.
                        If None, no file handler is added.
        log_level (str): The minimum logging level to capture (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').
        console_output (bool): Whether to also output logs to the console.

    Returns:
        logging.Logger: The configured logger instance.
    """
    # Create a logger
    logger = logging.getLogger("nl2sql_app")
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Prevent duplicate handlers if called multiple times
    if not logger.handlers:
        # Define a common formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )

        # Add console handler if requested
        if console_output:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        # Add file handler if log_file is provided
        if log_file:
            # Ensure the logs directory exists
            log_dir = "logs"
            os.makedirs(log_dir, exist_ok=True)
            file_path = os.path.join(log_dir, log_file)

            file_handler = logging.FileHandler(file_path)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    print(f"Logging configured. Level: {log_level.upper()}. Logs will be saved to '{os.path.join('logs', log_file)}' and/or console.")
    return logger