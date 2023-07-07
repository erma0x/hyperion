import pandas as pd

def backtest_strategy(data, capital = 100000, leverage=10, transaction_cost=0.005):

    position_size = capital * leverage / data.iloc[0]['Close']  # Dimensione posizione iniziale in base al capitale e alla leva
    position_value = position_size * data.iloc[0]['Close']  # Valore posizione iniziale
    in_position = False  # Indica se si è in una posizione aperta
    trade_history = []  # Storico delle operazioni
    
    for i in range(1, len(data)):

        curr_row = data.iloc[i]
        open_long_signal = data['open_long_signal'].iloc[i]
        close_long_signal = data['close_long_signal'].iloc[i]
        open_short_signal = data['open_short_signal'].iloc[i]
        close_short_signal = data['close_short_signal'].iloc[i]

        if open_long_signal and not in_position:
            entry_price = curr_row['open_long']
            position_size = capital * leverage / entry_price  # Calcola la dimensione della posizione in base al capitale e alla leva
            position_value = position_size * entry_price  # Calcola il valore della posizione
            capital -= position_value * transaction_cost  # Sottrai i costi di transazione dal capitale
            in_position = True
            trade_history.append(('Buy', curr_row['Date'], entry_price))
        
        elif close_long_signal and in_position:
            exit_price = curr_row['close_long']
            capital += position_value * leverage * (exit_price - entry_price)  # Calcola il profitto o la perdita della posizione in base alla leva
            capital -= position_value * transaction_cost  # Sottrai i costi di transazione dal capitale
            position_size = capital / exit_price  # Aggiorna la dimensione della posizione in base al capitale
            position_value = position_size * exit_price  # Aggiorna il valore della posizione
            in_position = False
            trade_history.append(('Sell', curr_row['Date'], exit_price))

        elif open_short_signal and in_position:
            exit_price = curr_row['open_short']
            capital += position_value * leverage * (exit_price - entry_price)  # Calcola il profitto o la perdita della posizione in base alla leva
            capital -= position_value * transaction_cost  # Sottrai i costi di transazione dal capitale
            position_size = capital / exit_price  # Aggiorna la dimensione della posizione in base al capitale
            position_value = position_size * exit_price  # Aggiorna il valore della posizione
            in_position = False
            trade_history.append(('Open Short', curr_row['Date'], exit_price))
    
        elif close_short_signal and in_position:
            exit_price = curr_row['close_short']
            capital += position_value * leverage * (exit_price - entry_price)  # Calcola il profitto o la perdita della posizione in base alla leva
            capital -= position_value * transaction_cost  # Sottrai i costi di transazione dal capitale
            position_size = capital / exit_price  # Aggiorna la dimensione della posizione in base al capitale
            position_value = position_size * exit_price  # Aggiorna il valore della posizione
            in_position = False
            trade_history.append(('Sell', curr_row['Date'], exit_price))
    
        # Calcola il capitale finale
        capital += position_value * leverage  # Aggiungi il valore della posizione finale al capitale
        
    return capital, trade_history 

def calculate_trading_signal(data):
    signals = pd.DataFrame()
    signals['signal'] = 0
    short_ma = 10
    long_ma = 30

    # Calcola le medie mobili
    signals['long_ma'] = data['Close'].rolling(long_ma).mean()
    signals['short_ma'] = data['Close'].rolling(short_ma).mean()
    
    
    # Genera i segnali di trading Long
    data['open_long_signal'] = data['Close'] < signals['short_ma']

    data['open_short_signal'] = data['Close'] < signals['short_ma']

    data['close_long_signal'] = data['Close'] < signals['short_ma']

    data['close_short_signal'] = data['Close'] < signals['short_ma']

    return data