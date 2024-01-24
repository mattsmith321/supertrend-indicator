# Package-specific imports
import argparse
import logging
import numpy as np
import pandas as pd
from math import floor
from colorama import just_fix_windows_console
from termcolor import colored as cl

# Application-specific imports
import settings
from data_sources.data_source_factory import DataSourceFactory
from utils.logging_util import LoggingUtil
from utils.supertrend_util import SupertrendUtil

# setting up the logger
logger = logging.getLogger(__name__)


def main():
    # Setup logging
    LoggingUtil.setup_logging()

    # Call the method to get the list of tickers
    tickers = get_tickers()

    data_source = get_data_source()

    for ticker in tickers:
        logger.info(f'Fetching data for {ticker} from {data_source}')
        df_ticker_data = data_source.get_data(ticker)
        calculate_supertrend(ticker, df_ticker_data)


def get_tickers():
    """
    Parse tickers from the command line arguments.

    Returns:
        list: A list of tickers obtained from the command line.
    """
    parser = argparse.ArgumentParser(description='Process some tickers.')
    parser.add_argument('tickers', type=str, help='Space-separated list of tickers e.g. "AAPL VFINX"')
    args = parser.parse_args()
    tickers = args.tickers.split(' ')

    logger.info(f'Parsed these tickers from the command line: {tickers}')

    return tickers

def get_data_source():
    """
    Get the data source based on the settings.

    Returns:
        BaseDataSource: An instance of the data source class.
    """
    data_source_factory = DataSourceFactory()
    data_source = data_source_factory.create_data_source()
    return data_source

def calculate_supertrend(ticker, df):
    stu = SupertrendUtil()

    df['st'], df['s_upt'], df['st_dt'] = stu.get_indicators(df['high'], df['low'], df['close'], 10, 3)

    df = df[1:]

    buy_price, sell_price, st_signal = stu.get_signals(df['close'], df['st'])

    position = []
    for i in range(len(st_signal)):
        if st_signal[i] > 1:
            position.append(0)
        else:
            position.append(1)
            
    for i in range(len(df['close'])):
        if st_signal[i] == 1:
            position[i] = 1
        elif st_signal[i] == -1:
            position[i] = 0
        else:
            position[i] = position[i-1]
            
    close_price = df['close']
    st = df['st']
    st_signal = pd.DataFrame(st_signal).rename(columns = {0:'st_signal'}).set_index(df.index)
    position = pd.DataFrame(position).rename(columns = {0:'st_position'}).set_index(df.index)

    frames = [close_price, st, st_signal, position]
    strategy = pd.concat(frames, join = 'inner', axis = 1)

    tsla_ret = pd.DataFrame(np.diff(df['close'])).rename(columns = {0:'returns'})
    st_strategy_ret = []

    for i in range(len(tsla_ret)):
        returns = tsla_ret['returns'].iloc[i] * strategy['st_position'].iloc[i]
        st_strategy_ret.append(returns)
        
    st_strategy_ret_df = pd.DataFrame(st_strategy_ret).rename(columns = {0:'st_returns'})
    investment_value = 10000
    number_of_stocks = floor(investment_value/df['close'].iloc[-1])
    st_investment_ret = []

    for i in range(len(st_strategy_ret_df['st_returns'])):
        returns = number_of_stocks*st_strategy_ret_df['st_returns'][i]
        st_investment_ret.append(returns)

    st_investment_ret_df = pd.DataFrame(st_investment_ret).rename(columns = {0:'investment_returns'})
    total_investment_ret = round(sum(st_investment_ret_df['investment_returns']), 2)
    profit_percentage = (total_investment_ret/investment_value)*100

    # use Colorama to make Termcolor work on Windows too
    just_fix_windows_console()

    print(cl(f'Supertrend results for {ticker}', attrs = ['bold']))
    print(cl(f'* Profit gained from the strategy by investing $10k : ${total_investment_ret:,.0f}', attrs = ['bold']))
    print(cl(f'* Profit percentage of the strategy : {profit_percentage:,.1f}%', attrs = ['bold']))


if __name__ == "__main__":
    main()