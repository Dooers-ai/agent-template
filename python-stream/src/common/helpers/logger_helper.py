import logging

from src.settings import settings


COLORS = {
    "DEBUG": "\033[36m",  # Cyan
    "INFO": "\033[32m",  # Green
    "WARNING": "\033[33m",  # Yellow
    "ERROR": "\033[31m",  # Red
    "CRITICAL": "\033[35m",  # Magenta
    "RESET": "\033[0m",  # Reset
}


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        levelname = record.levelname
        if levelname in COLORS:
            record.levelname = f"{COLORS[levelname]}{levelname}{COLORS['RESET']}"
            record.msg = f"{COLORS[levelname]}{record.msg}{COLORS['RESET']}"
        return super().format(record)


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG if settings.IS_DEVELOPMENT else logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG if settings.IS_DEVELOPMENT else logging.INFO)

formatter = ColoredFormatter(
    "[%(asctime)s] %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
