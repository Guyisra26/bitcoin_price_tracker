import logging
import os


class LoggerFactory:
    LOG_DIR = "logs"
    LOG_LEVELS = {
        "INFO": "log_info.txt",
        "WARNING": "log_warning.txt",
        "ERROR": "log_error.txt",
    }

    @staticmethod
    def create_logger(name: str = "btc_logger") -> logging.Logger:
        os.makedirs(LoggerFactory.LOG_DIR, exist_ok=True)
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        if logger.hasHandlers():
            logger.handlers.clear()

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        for level_name, filename in LoggerFactory.LOG_LEVELS.items():
            file_handler = logging.FileHandler(
                os.path.join(LoggerFactory.LOG_DIR, filename)
            )
            file_handler.setFormatter(formatter)
            file_handler.setLevel(getattr(logging, level_name))

            file_handler.addFilter(
                lambda record, lvl=level_name: record.levelname == lvl
            )
            logger.addHandler(file_handler)

        return logger
