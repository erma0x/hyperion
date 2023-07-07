import pandas as pd
import numpy as np
from pprint import pprint
from colorama import Fore, Style

initial_capital = 100000  # Initial capital

def backtest(csv_file, individual, leverage=1, commission_rate=0.9999):
    """
    Performs a backtest of a trading strategy using historical data from a CSV file.

    Arguments:
    - csv_file: Path to the CSV file containing historical data.
    - individual: Dictionary representing the parameters of the trading strategy.
    - leverage: Leverage for the trading strategy (default: 1).
    - commission_rate: Commission rate for each trade (default: 0.9999).

    Returns:
    - capital: Final capital after the backtest.
    - trade_history: List of trades executed during the backtest.
    - equity_history: List of equity values during the backtest.
    """
    take_profit = individual['Take_Profit']
    stop_loss = individual['Stop_Loss']
    long_ma = individual['Long_MA']
    short_ma = individual['Short_MA']

    # Read CSV data using Pandas
    df = pd.read_csv(csv_file, sep='\t')

    # Calculate moving averages
    df['Long_MA'] = df['Close'].rolling(long_ma).mean()
    df['Short_MA'] = df['Close'].rolling(short_ma).mean()

    # Initialize variables for backtest
    capital = initial_capital  # Initial capital
    position_size = capital  # Dimension of the initial position based on capital
    position_value = position_size * df.iloc[0]['Close']  # Initial position value
    in_position = False  # Indicates whether in an open position
    trade_history = []  # Trade history
    equity_history = []  # Equity history

    # Perform the backtest
    for i in range(1, len(df)):
        prev_row = df.iloc[i - 1]
        curr_row = df.iloc[i]

        # Conditions for opening a long position
        if not in_position and curr_row['Short_MA'] > curr_row['Long_MA']:
            entry_price = curr_row['Close']
            position_size = capital * leverage / entry_price  # Calculate position size based on leverage
            position_value = position_size * entry_price  # Calculate position value
            stop_loss_price = entry_price - entry_price * stop_loss
            take_profit_price = entry_price + entry_price * take_profit
            capital -= position_value * commission_rate  # Deduct commission from capital
            in_position = True
            trade_history.append(('BL', curr_row['Datetime'], entry_price))

        # Conditions for closing a long position
        elif in_position and (curr_row['Close'] < stop_loss_price or curr_row['Close'] > take_profit_price):
            exit_price = curr_row['Close']
            capital += position_value * leverage * (exit_price - entry_price)  # Calculate profit or loss based on leverage
            capital -= position_value * commission_rate  # Deduct commission from capital
            position_size = capital / exit_price  # Update position size based on capital
            position_value = position_size * exit_price  # Update position value
            in_position = False
            trade_history.append(('SL', curr_row['Datetime'], exit_price))

        if initial_capital * 0.8 > capital:
            print('Burned')
            return capital, trade_history, equity_history

        equity_history.append(capital)

    # Calculate final capital
    capital += position_value * leverage  # Add the value of the final position to the capital
    return capital, trade_history, equity_history

from tqdm import tqdm
import numpy as np

def generate_initial_population(num_strategies):
    """
    Generates an initial population of trading strategies.

    Arguments:
    - num_strategies: Number of strategies to generate.

    Returns:
    - strategies: List of dictionaries representing the generated strategies.
    """
    strategies = []
    for _ in range(num_strategies):
        tp = np.random.uniform(0.01, 0.025)  # Take Profit between 1% and 2.5%
        sl = np.random.uniform(0.01, 0.025)  # Stop Loss between 1% and 2.5%
        long_ma = np.random.randint(5, 220)  # Long moving average between 5 and 220 periods
        short_ma = np.random.randint(1, 50)  # Short moving average between 1 and 50 periods
        strategies.append({'Take_Profit': tp, 'Stop_Loss': sl, 'Long_MA': long_ma, 'Short_MA': short_ma})
    return strategies

def mutate(strategy, mutation_rate):
    """
    Applies mutation to a trading strategy.

    Arguments:
    - strategy: Dictionary representing the trading strategy.
    - mutation_rate: Rate of mutation.

    Returns:
    - mutated_strategy: Dictionary representing the mutated trading strategy.
    """
    mutated_strategy = strategy.copy()
    for key in mutated_strategy:
        if np.random.uniform(0, 1) < mutation_rate:
            if key == 'Take_Profit' or key == 'Stop_Loss':
                mutated_strategy[key] = np.random.uniform(0.01, 0.2)
            else:
                mutated_strategy[key] = np.random.randint(1, 250)
    return mutated_strategy

def crossover(strategy1, strategy2):
    """
    Performs crossover between two trading strategies.

    Arguments:
    - strategy1: First trading strategy.
    - strategy2: Second trading strategy.

    Returns:
    - new_strategy: Dictionary representing the new trading strategy generated by crossover.
    """
    crossover_point = np.random.randint(1, len(strategy1) - 1)
    new_strategy = {}
    for i, key in enumerate(strategy1):
        if i < crossover_point:
            new_strategy[key] = strategy1[key]
        else:
            new_strategy[key] = strategy2[key]
    return new_strategy

def select_parents(population, num_parents):
    """
    Selects parents from the population based on their fitness.

    Arguments:
    - population: List of trading strategies.
    - num_parents: Number of parents to select.

    Returns:
    - parents: List of selected parents.
    """
    # Sort the population based on the 'fitness' parameter in descending order
    sorted_population = sorted(population, key=lambda x: x['fitness'], reverse=True)

    # Select the first num_parents/2 elements as parents
    parents = sorted_population[:num_parents // 2]

    return parents

def repopulate(parents, num_offsprings, mutation_rate):
    """
    Generates offspring strategies through crossover and mutation.

    Arguments:
    - parents: List of parent strategies.
    - num_offsprings: Number of offspring strategies to generate.
    - mutation_rate: Rate of mutation.

    Returns:
    - offsprings: List of generated offspring strategies.
    """
    offsprings = []
    num_parents = len(parents)
    for _ in range(num_offsprings):
        parent1 = parents[np.random.randint(0, num_parents)]
        parent2 = parents[np.random.randint(0, num_parents)]
        offspring = crossover(parent1, parent2)
       offspring = mutate(offspring, mutation_rate)
        capital, trade_history, equity_history = backtest('/home/minerva/Documents/PorsennaTrading/database/crypto/BTCUSD/BTCUSD_5m.csv', individual)
        offspring['fitness'] = capital
        offsprings.append(offspring)
        print(capital, len(trade_history))
        print(offspring)
    
    return offsprings

num_strategies = 10
mutation_rate = 0.1
num_parents = 4
generations = 5
num_offsprings = num_strategies - num_parents

population = generate_initial_population(num_strategies)

import matplotlib.pyplot as plt

for idx, individual in enumerate(population):
    capital, trade_history, equity_history = backtest('/home/minerva/Documents/PorsennaTrading/database/forex/AUDGBP/AUDGBP_5m.csv', individual)
    print(capital, len(trade_history))
    population[idx]['fitness'] = capital

    # plt.plot(equity_history)
    # plt.show()

for generation in range(generations):
    parents = select_parents(population, num_parents)
    offsprings = repopulate(parents, num_offsprings, mutation_rate)

# best
print(offsprings)
