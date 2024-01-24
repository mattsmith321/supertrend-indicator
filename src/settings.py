from decouple import config
# from decouple import Csv

# logging
# Can be DEBUG, INFO, WARNING, ERROR, CRITICAL, etc.
LOGGING_LEVEL = config('LOGGING_LEVEL')

DATA_SOURCE_NAME = config('DATA_SOURCE_NAME')
DATA_SOURCE_API_KEY_ENV_VAR = config('DATA_SOURCE_API_KEY_ENV_VAR')
DATA_SOURCE_TARGET_COLUMN = config('DATA_SOURCE_TARGET_COLUMN')

# # application
# DATA_DIR = config('DATA_DIR')
# OUTPUT_DIR = config('OUTPUT_DIR')

# INITIAL_BALANCE_AMOUNT = config('INITIAL_BALANCE_AMOUNT', cast=int)

# TARGET_COLUMN_NAME = config('TARGET_COLUMN_NAME')
# RETURN_COLUMN_NAME = config('RETURN_COLUMN_NAME')

# DATA_SOURCES = config('DATA_SOURCES', cast=Csv())
# DATA_SOURCE_ALPHAVANTAGE = config('DATA_SOURCE_ALPHAVANTAGE', cast=Csv(post_process=tuple))
# DATA_SOURCE_EODHD = config('DATA_SOURCE_EODHD', cast=Csv(post_process=tuple))
# DATA_SOURCE_PORTFOLIOVISUALIZER = config('DATA_SOURCE_PORTFOLIOVISUALIZER', cast=Csv(post_process=tuple))
# DATA_SOURCE_TIINGO = config('DATA_SOURCE_TIINGO', cast=Csv(post_process=tuple))
# DATA_SOURCE_YAHOOFINANCE = config('DATA_SOURCE_YAHOOFINANCE', cast=Csv(post_process=tuple))

# # Name of the data source to be used as the baseline data source.
# # This is the data source that will be used to compare the other data
# # sources to see how much they deviate.
# DATA_SOURCE_FOR_BASELINE = config('DATA_SOURCE_FOR_BASELINE')

# DATA_COLUMNS = config('DATA_COLUMNS', cast=Csv())
# DATA_COLUMN_RETURN = config('DATA_COLUMN_RETURN', cast=Csv(post_process=tuple))
# DATA_COLUMN_TOTALRETURN = config('DATA_COLUMN_TOTALRETURN', cast=Csv(post_process=tuple))
# DATA_COLUMN_BALANCE = config('DATA_COLUMN_BALANCE', cast=Csv(post_process=tuple))
# DATA_COLUMN_ABSDEV = config('DATA_COLUMN_ABSDEV', cast=Csv(post_process=tuple))


# # utils

# cache_util
CACHE_DIR = config('CACHE_DIR')
CACHE_FILENAME_FORMAT = config('CACHE_FILENAME_FORMAT')

# # excel_util
# EXCEL_CHART_TITLE_FSTR = config('EXCEL_CHART_TITLE_FSTR')
# EXCEL_CHART_XY_SCALE = config('EXCEL_CHART_XY_SCALE', cast=float)
# EXCEL_COL_WIDTH = config('EXCEL_COL_WIDTH', cast=float)
# EXCEL_START_ROW = config('EXCEL_START_ROW', cast=int)
# EXCEL_TABLE_STYLE = config('EXCEL_TABLE_STYLE')