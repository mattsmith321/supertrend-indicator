# Built-in imports
import logging
import os
import pandas as pd

# Application-specific imports
import settings

# module-level (or global-level) variables/constants
logger = logging.getLogger(__name__)

class CacheUtil:
    CACHE_DIR = settings.CACHE_DIR
    CACHE_FILENAME_FORMAT = settings.CACHE_FILENAME_FORMAT

    @classmethod
    def cache_filename(cls, ticker, data_source):
        return cls.CACHE_FILENAME_FORMAT.format(ticker=ticker, data_source=data_source)

    @classmethod
    def cache_path(cls, filename):
        return os.path.join(cls.CACHE_DIR, filename)

    @classmethod
    def is_cached(cls, filename):
        logger.debug(f"load_from_cache(): {filename}")
        return os.path.exists(cls.cache_path(filename))

    @classmethod
    def load_from_cache(cls, filename):
        logger.debug(f"load_from_cache(): {filename}")
        return pd.read_csv(cls.cache_path(filename), index_col=0, parse_dates=True)

    @classmethod
    def save_to_cache(cls, data, filename):
        logger.debug(f"save_to_cache(): {filename}")
        if not os.path.exists(cls.CACHE_DIR):
            os.makedirs(cls.CACHE_DIR)
        data.to_csv(cls.cache_path(filename))

