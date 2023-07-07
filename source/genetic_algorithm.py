import random as rnd
import json
import os, sys
from pprint import pprint
from colorama import Fore, Style
from pprint import pprint
import os
from os import listdir
from os.path import isfile, join
from source.hyperion import backtest, get_full_performances, save_strategy
from plotter import *

def get_avaiable_pairs(path_to_check):
    if os.path.exists(path_to_check):
        onlyfiles = [f for f in listdir(path_to_check) if isfile(join(path_to_check, f))]
    return onlyfiles

def generate_random_configuration():
    MARKET = 'FOREX' #[],'CRYPTO']
    FOREX_CURRENCIES = ['EUR','CAD','AUD','CHF','JPY','NZD','GBP','MXN']
    CRYPTO_CURRENCIES = ['XRPUSDT', 'DOGEUSDT','BTCUSDT']

    INTERVALS_CRYPTO = ['5m','15m','30m','1h','4h','1d'] 
    INTERVALS = ['5m','15m','30m','60m','90m'] 
    
    LONG_MA = rnd.randint(50,250)
    SHORT_MA = rnd.randint(5,50)
    
    TP = round(rnd.uniform(0.0001,0.1),6)
    SL = round(rnd.uniform(0.0001,0.1),6)
    TS = round(rnd.uniform(0.0001,0.1),6)

    postion_size = round(rnd.uniform(0.01,0.5),6)

    if rnd.random() > 0:
        forex_currency_1 = rnd.choice(FOREX_CURRENCIES)
        forex_currency_2 = rnd.choice(FOREX_CURRENCIES)

        while forex_currency_1 in ('MXN','NZD') and forex_currency_2 in ('MXN','NZD'):
            forex_currency_2 = rnd.choice(FOREX_CURRENCIES)

        while forex_currency_2 == forex_currency_1:
            forex_currency_2 =rnd.choice(FOREX_CURRENCIES)

        interval = rnd.choice(INTERVALS)
        pair = forex_currency_1+forex_currency_2+'=X'

        
    else:
        pair = rnd.choice(CRYPTO_CURRENCIES)
        interval = rnd.choice(INTERVALS_CRYPTO)

    
    configurations = {'market':MARKET,'trailing_stop':TS,'ticker':pair,'postion_size':postion_size,'interval':interval,'tp':TP,'sl':SL,'ma_long':LONG_MA,'ma_short':SHORT_MA}
        
    return configurations






if __name__ == '__main__':

    capital = 100_000
    GENERATION_SIZE = 50


    PRINT_OPERATIONS = False
    #buffer_trailing_stop = 0.0005
    ID = 0


    if not os.path.isdir(sys.path[0]+"/strategies/"):
        os.makedirs(sys.path[0]+"/strategies/")
    
    all_robots = []

    for i in range(GENERATION_SIZE):
        
        try:
            configs = generate_random_configuration()
            equity, performances = backtest( configurations = configs, capital = capital)

            stats = get_full_performances(equity, performances)
            full_strategy = {**configs, **stats} # merge data
            
            all_robots.append(full_strategy)
            if full_strategy['final_equity']>equity[0]:
                print(Fore.GREEN) 
                pprint(full_strategy)
                print(Style.RESET_ALL) 

            else:
                print(Fore.RED) 
                pprint(full_strategy)
                print(Style.RESET_ALL) 

            save_strategy(configurations = full_strategy , name_strategy="{i}_full")
            
            try:
                plot_logs_returns(equity_history=equity)
                plot_long_vs_short_trades(title="Long trades & Short trades",ylabel='number of trades',long_trades=full_strategy['LONG_TRADES'],short_trades=full_strategy['SHORT_TRADES'])
                plot_long_vs_short_trades(title="winning long trades & winning short trades",ylabel='% winning',long_trades=full_strategy['WINNING_TRADES_LONG']/full_strategy['LONG_TRADES'],short_trades=full_strategy['WINNING_TRADES_SHORT']/full_strategy['SHORT_TRADES'])
                plot_equity(equity_history=equity)
            except:
                pass

        except:
           print(f' ERROR -> {configs}')
    
    #EVOLUTION
    configurations = []

    for i in range(GENERATION_SIZE):
        try:
            with open(f'strategies/{i}.txt', 'r') as f:
                configuration = json.load(f)
                configurations.append(configuration) 
        except:
            print('error')

    sorted_list = sorted(tuple(all_robots), key=lambda k: k['total_net_profit'], reverse=True)
    
    print(Fore.YELLOW+"*"*100+" \n\tTop strategies"+Style.RESET_ALL)
    
    for full_strategy in sorted_list[:10]:
        if full_strategy['final_equity']>equity[0]:
            print(Fore.GREEN) 
            pprint(full_strategy)
            print(Style.RESET_ALL) 

        else:
            print(Fore.RED) 
            pprint(full_strategy)
            print(Style.RESET_ALL) 