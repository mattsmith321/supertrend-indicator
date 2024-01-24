import pandas as pd
from tiingo import TiingoClient

from .base_data_source import BaseDataSource

class TiingoDataSource(BaseDataSource):
    def __init__(self, name, api_key):
        self.name = name
        tiingo_config = {'session': True, 'api_key': api_key}
        self.tiingo_client = TiingoClient(tiingo_config)

    def _fetch_data_from_source(self, ticker) -> pd.DataFrame:
        """
        Fetch historical stock data for a given ticker symbol within a date range.

        Args:
            ticker (str): The stock ticker symbol (e.g., "AAPL").

        Returns:
            list: A list of historical stock data points (e.g., OHLC prices) as dictionaries.
        """
        # TODO: Replace hardcoded startDate and endDate with parameters
        df = self.tiingo_client.get_dataframe(ticker,
                                    fmt='json',
                                    startDate='1950-01-01',
                                    endDate='2024-12-31',
                                    frequency='daily')

        return df

class TiingoDataFetchError(Exception):
    pass
