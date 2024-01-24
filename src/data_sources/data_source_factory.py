from decouple import config

import settings

from .tiingo_data_source import TiingoDataSource


class DataSourceFactory:
    # Constants for data source settings
    DATA_SOURCE_NAME = settings.DATA_SOURCE_NAME
    DATA_SOURCE_API_KEY_ENV_VAR = settings.DATA_SOURCE_API_KEY_ENV_VAR

    def __init__(self):
        self.data_sources = {
            'Tiingo': TiingoDataSource
        }

    def create_data_source(self):
        if self.DATA_SOURCE_NAME not in self.data_sources:
            raise ValueError(f"Invalid data provider: {self.DATA_SOURCE_NAME}")

        data_source_class = self.data_sources[self.DATA_SOURCE_NAME]
        api_key = config(self.DATA_SOURCE_API_KEY_ENV_VAR)
        return data_source_class(self.DATA_SOURCE_NAME, api_key)
