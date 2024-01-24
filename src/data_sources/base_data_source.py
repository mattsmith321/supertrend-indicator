import logging
import pandas as pd

from abc import ABC

import settings
from utils.cache_util import CacheUtil

# module-level (or global-level) variables/constants
logger = logging.getLogger(__name__)

class BaseDataSource(ABC):
    DATA_SOURCE_TARGET_COLUMN = settings.DATA_SOURCE_TARGET_COLUMN

    def __init__(self, data_source):
        """
        Initialize the data source with a specific ticker.

        Args:
            ticker (str): The ticker symbol for the data source.
        """
        self.data_source = data_source

    def _fetch_data(self, ticker) -> pd.DataFrame:
        """
        Retrieve data for the given ticker symbol. This method first checks if 
        the data is available in the cache. If it is, the cached data is returned. 
        Otherwise, it fetches the data from the data source by calling the 
        subclass-specific _fetch_data_from_source method, caches it, and then returns it.

        This method is intended to be used internally within the class and its 
        subclasses, and it abstracts away the caching logic to avoid repetition 
        in each data source subclass.

        Returns:
            pd.DataFrame: A pandas DataFrame containing the data for the specified ticker. 
                          The data is either retrieved from the cache or directly from 
                          the data source.
        """
        cache_filename = CacheUtil.cache_filename(ticker, self.name)
        logger.debug(f"Loading {cache_filename}")

        # Check if data is cached
        if CacheUtil.is_cached(cache_filename):
            logger.debug(f"Loading {ticker} for {self.name} from cache")
            return CacheUtil.load_from_cache(cache_filename)

        # If not cached, fetch data from source
        logger.debug(f"Fetching data from server")
        df = self._fetch_data_from_source(ticker)

        # Cache the fetched data
        CacheUtil.save_to_cache(df, cache_filename)

        return df
    
    def get_data(self, ticker) -> pd.DataFrame:
        """
        Aggregate and return the data on a monthly basis. This method should
        work for any data source, and it should not be implemented by subclasses.

        Returns:
            DataFrame: A pandas DataFrame containing the monthly aggregated data.
        """
        df = self._fetch_data(ticker)

        # Keep only the target column
        # df = pd.DataFrame(df[self.DATA_SOURCE_TARGET_COLUMN])

        # Remove any time-related data from the index so that we end up with yyyy-mm-dd
        df.index = pd.to_datetime(df.index).tz_localize(None)

        return df
    
