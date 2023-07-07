import pandas as pd
import numpy as np
from pprint import pprint
from colorama import Fore, Style

initial_capital = 100000  # Capitale iniziale


def backtest(csv_file, individual , leverage=1, commission_rate=0.9999):
    
    take_profit = individual['Take_Profit']
    stop_loss = individual['Stop_Loss']
    long_ma = individual['Long_MA']
    short_ma = individual['Short_MA']

    # Leggi i dati CSV utilizzando Pandas
    df = pd.read_csv(csv_file,sep='\t')

    # Calcola le medie mobili
    df['Long_MA'] = df['Close'].rolling(long_ma).mean()
    df['Short_MA'] = df['Close'].rolling(short_ma).mean()
    
    # Inizializza le variabili per il backtest
    capital = 100000  # Capitale iniziale
    position_size = capital #df.iloc[0]['Close']  # Dimensione posizione iniziale in base al capitale
    position_value = position_size * df.iloc[0]['Close']  # Valore posizione iniziale
    in_position = False  # Indica se si è in una posizione aperta
    trade_history = []  # Storico delle operazioni
    equity_histoy = []
    # Esegui il backtest
    for i in range(1, len(df)):
        prev_row = df.iloc[i - 1]
        curr_row = df.iloc[i]
        
        # Condizioni per aprire una posizione lunga
        if not in_position and curr_row['Short_MA'] > curr_row['Long_MA']:
            entry_price = curr_row['Close']
            position_size = capital * leverage / entry_price  # Calcola la dimensione della posizione in base alla leva
            position_value = position_size * entry_price  # Calcola il valore della posizione
            stop_loss_price = entry_price - entry_price * stop_loss
            take_profit_price = entry_price + entry_price * take_profit
            capital -= position_value * commission_rate  # Sottrai la commissione dalla capitale
            in_position = True
            trade_history.append(('BL', curr_row['Datetime'], entry_price))
        
        # Condizioni per chiudere una posizione lunga
        elif in_position and (curr_row['Close'] < stop_loss_price or curr_row['Close'] > take_profit_price):
            exit_price = curr_row['Close']
            capital += position_value * leverage * (exit_price - entry_price)  # Calcola il profitto o la perdita della posizione in base alla leva
            capital -= position_value * commission_rate  # Sottrai la commissione dalla capitale
            position_size = capital / exit_price  # Aggiorna la dimensione della posizione in base al capitale
            position_value = position_size * exit_price  # Aggiorna il valore della posizione
            in_position = False
            trade_history.append(('SL', curr_row['Datetime'], exit_price))
        if initial_capital*0.8 > capital:
            print('Burned')
            return capital, trade_history, equity_histoy
        
        equity_histoy.append(capital)
    # Calcola il capitale finale
    capital += position_value * leverage  # Aggiungi il valore della posizione finale al capitale
    return capital, trade_history, equity_histoy

from tqdm import tqdm  
import numpy as np

def generate_initial_population(num_strategies):
    strategies = []
    for _ in range(num_strategies):
        tp = np.random.uniform(0.01, 0.025)  # Take Profit tra 1% e 10%
        sl = np.random.uniform(0.01, 0.025)  # Stop Loss tra 1% e 10%
        long_ma = np.random.randint(5, 220)  # Media mobile lunga tra 10 e 50 periodi
        short_ma = np.random.randint(1, 50)  # Media mobile corta tra 5 e 20 periodi
        strategies.append({'Take_Profit': tp, 'Stop_Loss': sl, 'Long_MA': long_ma, 'Short_MA': short_ma})
    return strategies

def mutate(strategy, mutation_rate):
    mutated_strategy = strategy.copy()
    for key in mutated_strategy:
        if np.random.uniform(0, 1) < mutation_rate:
            if key == 'Take_Profit' or key == 'Stop_Loss':
                mutated_strategy[key] = np.random.uniform(0.01, 0.2)
            else:
                mutated_strategy[key] = np.random.randint(1, 250)
    return mutated_strategy

def crossover(strategy1, strategy2):
    crossover_point = np.random.randint(1, len(strategy1) - 1)
    new_strategy = {}
    for i, key in enumerate(strategy1):
        if i < crossover_point:
            new_strategy[key] = strategy1[key]
        else:
            new_strategy[key] = strategy2[key]
    return new_strategy

def select_parents(population, num_parents):
    # Ordina la popolazione in base al parametro 'fitness' in ordine decrescente
    sorted_population = sorted(population, key=lambda x: x['fitness'], reverse=True)
    
    # Seleziona i primi num_parents/2 elementi come genitori
    parents = sorted_population[:num_parents // 2]
    
    return parents

def repopulate(parents, num_offsprings, mutation_rate):
    offsprings = []
    num_parents = len(parents)
    for _ in range(num_offsprings):
        parent1 = parents[np.random.randint(0, num_parents)]
        parent2 = parents[np.random.randint(0, num_parents)]
        offspring = crossover(parent1, parent2)
        offspring = mutate(offspring, mutation_rate)
        capital, trade_history, equity_histoy = backtest('/home/minerva/Documents/PorsennaTrading/database/crypto/BTCUSD/BTCUSD_5m.csv',individual)
        offspring['fitness'] = capital
        offsprings.append(offspring)
        print(capital,len(trade_history))
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
    capital, trade_history, equity_histoy = backtest('/home/minerva/Documents/PorsennaTrading/database/forex/AUDGBP/AUDGBP_5m.csv',individual)
    print(capital,len(trade_history))
    population[idx]['fitness'] = capital
    
    #plt.plot(equity_histoy)
    #plt.show()

for generation in range(generations):
    parents = select_parents(population, num_parents)
    offsprings = repopulate(parents, num_offsprings, mutation_rate)
    
# best
print(offsprings)
