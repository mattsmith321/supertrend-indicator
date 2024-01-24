# Package-specific imports
import logging

# Application-specific imports
import settings

logger = logging.getLogger(__name__)

class LoggingUtil:

    # Map string levels to their respective logging constants
    LOGGING_LEVEL_MAP = {
        'CRITICAL': logging.CRITICAL,
        'ERROR': logging.ERROR,
        'WARNING': logging.WARNING,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG
    }

    @classmethod
    def setup_logging(cls):
        logging_level = cls.LOGGING_LEVEL_MAP.get(settings.LOGGING_LEVEL, logging.INFO)  # Default to INFO if not found
        logging.basicConfig(level=logging_level)
