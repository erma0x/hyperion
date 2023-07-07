
import numpy as np
import pandas as pd
import yfinance as yf
from tqdm import tqdm
import datetime
from pprint import pprint
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from os import listdir
from os.path import isfile, join
import os
import sys
import random as rnd
import glob


from genetic_algorithm import generate_random_configuration
from plotter import plot_equity, plot_logs_returns, plot_operations, plot_signals, plot_long_vs_short_trades, plot_and_save

def get_df_from_pair_and_timeframe(configurations):
    
    market=configurations['market']
    pair=configurations['ticker']
    timeframe=configurations['interval']

    asset_path = sys.path[0].replace('hiperion_strategy_explorer/hyperion','databases/')+market+'/'+pair + '_' + timeframe + '*.csv'
    print(f'ASSET PATH {asset_path}')
    data = pd.read_csv(filepath_or_buffer=asset_path,sep='\t')
    data.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    data = data.sort_values('Date', ascending=True)
    data = data.set_index(data.Date)
    return data


def backtest(configurations, df, capital=100_000, leverage=20):

    pair = configurations['ticker']
    timeframe = configurations['interval']

    dates = []
    for i in range(10):
        date = datetime.date.today() - datetime.timedelta(days=i * 6)
        dates.append(date)
    
    dates = dates[::-1]

    WINNING_TRADES = 0
    LOSING_TRADES = 0
    SUM_WINNING_TRADES = 0
    SUM_LOSING_TRADES = 0
    SHORT_TRADES = 0
    LONG_TRADES = 0
    WINNING_TRADES_LONG = 0
    WINNING_TRADES_SHORT = 0

    initial_capital = capital
    open_operation = False
    open_long = False
    open_short = False
    buffer_period = 2 

    take_profit = configurations['tp']
    stop_loss = configurations['sl']
    trailing_stop_buffer = configurations['trailing_stop']
    WINDOW_SHORT = configurations['ma_short']
    WINDOW_LONG = configurations['ma_long']
    position_size = configurations['postion_size']
    
    df['OL'] = None
    df['OS'] = None
    df['CL'] = None
    df['CS'] = None
    df['equity'] = 100_000

    for idx in tqdm(range(WINDOW_LONG, len(df.index))):
    
        Date = df.index[idx]
        High = df['High'].iloc[idx]
        Low = df['Low'].iloc[idx]
        Close = df['Close'].iloc[idx]
        ma_short = pd.Series(df['Close']).rolling(window=WINDOW_SHORT).mean()
        ma_long = pd.Series(df['Close']).rolling(window=WINDOW_LONG).mean()
        
        df.loc[df.index[idx], 'equity'] = capital

        if not open_operation:
            # OPEN LONG OPERATION           
            if ma_short.iloc[idx] > ma_long.iloc[idx]:
                open_price = Close
                open_operation = True
                open_long = True
                df.loc[df.index[idx], 'OL'] = Close
                df.loc[df.index[idx], 'equity'] = capital
        
            # OPEN SHORT OPERATION           
            elif ma_short.iloc[idx] < ma_long.iloc[idx]:
                open_price = Close
                open_operation = True
                open_short = True
                df.loc[df.index[idx], 'OS'] = Close
                df.loc[df.index[idx], 'equity'] = capital

        # CLOSE LONG OPERATION                    
        if open_operation == True and open_long == True: 
            profit_gain = (Close - open_price) * capital * position_size * leverage  # LONG OPERATIONs
            real_TP = take_profit * capital * position_size * leverage
            real_SL = -stop_loss * capital * position_size * leverage
            trailing_stop = (Close - trailing_stop_buffer) * capital * leverage

            df.loc[df.index[idx], 'equity'] = capital + profit_gain

            if profit_gain < real_SL:  # CLOSE 
                capital += profit_gain
                LOSING_TRADES += 1
                SUM_LOSING_TRADES += profit_gain
                LONG_TRADES += 1
                df.loc[df.index[idx], 'CL'] = Close
                df.loc[df.index[idx], 'equity'] = capital
                open_operation = False
                open_long = False

            if profit_gain > real_TP:
                capital += profit_gain
                WINNING_TRADES_LONG += 1
                SUM_WINNING_TRADES += profit_gain
                LONG_TRADES += 1
                df.loc[df.index[idx], 'CL'] = Close
                df.loc[df.index[idx], 'equity'] = capital
                open_operation = False
                open_long = False
            
            if profit_gain > trailing_stop:
                open_price = trailing_stop  # Attiva il trailing stop

        # CLOSE SHORT OPERATION                    
        if open_operation == True and open_short == True: 
            profit_gain = (open_price - Close) * capital * position_size * leverage  # LONG OPERATIONs
            real_TP = take_profit * capital * position_size * leverage
            real_SL = -stop_loss * capital * position_size * leverage
            trailing_stop = (Close + trailing_stop_buffer) * capital * leverage

            df.loc[df.index[idx], 'equity'] = capital + profit_gain

            if profit_gain < real_SL: 
                capital += profit_gain
                LOSING_TRADES += 1
                SUM_LOSING_TRADES += profit_gain
                SHORT_TRADES += 1
                df.loc[df.index[idx], 'CS'] = Close
                df.loc[df.index[idx], 'equity'] = capital
                open_operation = False
                open_short = False

            if profit_gain > real_TP:
                capital += profit_gain
                WINNING_TRADES_SHORT += 1
                SUM_WINNING_TRADES += profit_gain
                SHORT_TRADES += 1
                df.loc[df.index[idx], 'CS'] = Close
                df.loc[df.index[idx], 'equity'] = capital
                open_operation = False
                open_short = False

            if profit_gain > trailing_stop:
                open_price = trailing_stop  # Attiva il trailing stop

        if capital < initial_capital*0.8:
            return df

    return df


def calculate_max_drawdown(series):
    if series.size > 0: 
        cum_max = cum_max = np.maximum.accumulate(series)    
        drawdown = (series - cum_max) / cum_max    
        max_drawdown = np.min(drawdown)
        return max_drawdown
    else:
        return None
    
def calculate_sortino_ratio(equity):
    if equity.size > 0:
        returns = (equity[1:] - equity[:-1]) / equity[:-1] * 100
        avg_return = returns.mean()
        target_return = 0
        downside_deviation = np.sqrt((returns[returns < target_return] - target_return)**2).sum() / len(returns)
        sortino_ratio = (avg_return - target_return) / downside_deviation
        return round(sortino_ratio,4)
    else:
        return None
    
def get_full_performances(df, performances):
    configs = {}
    
    if df['equity'].any():
        configs['final_equity'] = round( df['equity'].iloc[-1] ,2)
    else:
        configs['final_equity'] = 100_000

    if performances:
        max_drowdown = calculate_max_drawdown(df['equity'])
        sortino_ratio = calculate_sortino_ratio(df['equity'])
        
        winning_trades = performances['WINNING_TRADES']
        losing_trades = performances['LOSING_TRADES']
        tot_trades = winning_trades  + losing_trades
        sum_winning_trades = performances['SUM_WINNING_TRADES']
        sum_losing_trades = performances['SUM_LOSING_TRADES']

        configs['WINNING_TRADES_LONG'] = performances['WINNING_TRADES_LONG']
        configs['WINNING_TRADES_SHORT'] = performances['WINNING_TRADES_SHORT']

        configs['LONG_TRADES'] = performances['LONG_TRADES']
        configs['SHORT_TRADES'] = performances['SHORT_TRADES']
        configs['sortino_ratio'] = sortino_ratio
        configs['winning_trades'] = performances['WINNING_TRADES']
        configs['losing_trades'] = performances['LOSING_TRADES']
        configs['tot_trades'] = tot_trades
        configs['sum_winning_trades'] = performances['SUM_WINNING_TRADES']
        configs['sum_losing_trades'] = performances['SUM_LOSING_TRADES']
        
        if winning_trades > 0:
            average_winning_trade = sum_winning_trades/winning_trades
        else:
            average_winning_trade = 0

        if losing_trades > 0:
            average_losing_trade = sum_losing_trades/losing_trades
        else:
            average_losing_trade = 0

        if sum_losing_trades<0 and sum_winning_trades>0:
            profit_factor =  sum_winning_trades/sum_losing_trades
        else:
            profit_factor = -1
        
        if tot_trades > 0:
            win_rateo = (winning_trades/tot_trades)*100
            average_trade_net_profit = ( sum_losing_trades + sum_winning_trades ) / tot_trades
        
        else:
            win_rateo, average_trade_net_profit = -1, -1

        configs['win_rateo'] = round(win_rateo,2)
        configs['profit_factor'] = round(profit_factor,2)
        configs['max_drowdown'] = max_drowdown
        configs['average_winning_trade'] = round(average_winning_trade,2)
        configs['average_losing_trade'] = round(average_losing_trade,2)
        configs['average_trade_net_profit']= round(average_trade_net_profit,2)
        configs['total_net_profit'] = round( configs['final_equity'] - df['equity'].iloc[0] , 2 )        
        configs['final_equity'] = df['equity'].iloc[-1]
        configs['percentage_gain'] = round(( configs['final_equity'] / df['equity'].iloc[0]) *100 )

    return configs

def save_strategy(path, configurations):
    with open(path, 'w') as f:
        json.dump(configurations, f)


def load_strategy(path):
    with open(path, 'r') as f:
        configuration = json.load(f)
        return configuration


class RandomFileExecution:
    avaiable_pairs = []

    def __init__(self) -> None:
        self.database_path = self.get_databases_path()
        self.pair = 'UUS'
        self.timeframe = '30m'
        self.market = 'forex'

    def __repr__(self) -> str:
        
        return """
        1. take db path
        2. choose random market
        3. choose random pair
        4. choose random timeframe
        5. return the random filepath.csv
        """

    def get_avaiable_timeframe(self,pair) -> str:
        path_to_check = self.database_path+'/'+self.market+'/'+pair
        onlyfiles = [f for f in listdir(path_to_check) if isfile(join(path_to_check, f))]
        self.avaiable_timeframes = [f.split('_')[1] for f in onlyfiles]

    def get_databases_path(self) -> str:
        return sys.path[0].replace('hyperion_strategy_explorer/hyperion','database/')

    def get_random_asset(self):
        path_market_databases = self.database_path+self.market+'/'
        #print(path_market_databases)
        list_avaiable_pairs = os.listdir(path_market_databases)
        #print(list_avaiable_pairs)
        self.pair = rnd.choice(list_avaiable_pairs)
        #print(self.pair)
        random_asset_path = rnd.choice(glob.glob(self.database_path+self.market+'/'+self.pair+'/*.csv'))
        #print(random_asset_path)
        return random_asset_path

    def run(self):
        return self.get_random_asset()
    



def plot_operations(df,configs):
    # configs plot
    plt.figure(figsize=(20, 15), dpi=180)
    plt.grid()
    
    # price
    plt.plot(df.index,df['Close'])
    
    # Moving Averages
    WINDOW_LONG=configs['ma_long']
    WINDOW_SHORT=configs['ma_short']
    ma_short = pd.Series(df['Close']).rolling(window=WINDOW_SHORT).mean()
    ma_long = pd.Series(df['Close']).rolling(window=WINDOW_LONG).mean()
    plt.plot(df.index,ma_long)
    plt.plot(df.index,ma_short)
    
    # Long op
    plt.scatter(df.index, df['OL'], color='green', label='buy_long',marker='^',alpha=1,s=300 )
    plt.scatter(df.index, df['CL'], color='red', label='sell_long' ,marker='v',alpha=1,s=300 )

    # Short op
    plt.scatter(df.index, df['OS'], color='blue', label='buy_short',marker='^',alpha=1 ,s=300)
    plt.scatter(df.index, df['CS'], color='orange', label='sell_short' ,marker='v',alpha=1,s=300 )
    
    plt.title(f"backtest { configs['ticker'].replace('=X','') } {configs['interval']} from {df.index[0]} to {df.index[-1]}")
    plt.xticks([])
    
    plt.show()


if __name__ == "__main__":
        
    initial_capital = 100_000
    generation_size = 20

    # INITIAL GENERATION
    for i in range(generation_size):
        configs = generate_random_configuration()
        random_taker = RandomFileExecution()
        random_asset_path = random_taker.run()
        print(random_asset_path)
        try:
            data = pd.read_csv(filepath_or_buffer=random_asset_path,sep='\t')
            data.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
            data = data.sort_values('Date', ascending=True)
            data = data.set_index(data.Date) 
            del data['Date']

            # PERFORMANCES
            df = backtest( configurations = configs, df = data, capital = initial_capital)
            
            print(df.tail(1))
            if df['equity'].iloc[-1]>initial_capital:
                print(configs)

        except IndexError:
            print(f'file not found in {random_asset_path}')
