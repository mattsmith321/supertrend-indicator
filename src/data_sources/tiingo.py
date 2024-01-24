import pandas as pd

from decouple import config
from tiingo import TiingoClient

import settings
from .base_data_source import BaseDataSource


class Tiingo(BaseDataSource):

    def _fetch_data_from_source(self) -> pd.DataFrame:
        tiingo_config = {'session': True, 'api_key': config(self.data_source.api_key)}
        tiingo_client = TiingoClient(tiingo_config)
        df = tiingo_client.get_dataframe(self.ticker,
                                         fmt='json',
                                         startDate='1950-01-01',
                                         endDate='2024-12-31',
                                         frequency='daily')
        # Keep only the adjusted close column
        df = pd.DataFrame({settings.TARGET_COLUMN_NAME: df[self.data_source.source_column_name]})
        # Rename the index and remove any timezone information
        df = df.rename_axis('date').tz_localize(None)
        return df
