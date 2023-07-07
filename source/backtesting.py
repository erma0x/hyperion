import pandas as pd

def backtest_strategy(data, capital=100000, leverage=10, transaction_cost=0.005):
    """
    Performs backtesting of a trading strategy using historical data.

    Arguments:
    - data: pandas DataFrame containing historical data.
    - capital: Initial capital for backtesting (default: 100,000).
    - leverage: Leverage to use for positions (default: 10).
    - transaction_cost: Transaction cost in percentage (default: 0.005).

    Returns:
    - capital: Final capital after backtesting.
    - trade_history: List of trades executed during backtesting.
    """

    position_size = capital * leverage / data.iloc[0]['Close']  # Initial position size based on capital and leverage
    position_value = position_size * data.iloc[0]['Close']  # Initial position value
    in_position = False  # Indicates whether in an open position
    trade_history = []  # Trade history

    for i in range(1, len(data)):
        curr_row = data.iloc[i]
        open_long_signal = data['open_long_signal'].iloc[i]
        close_long_signal = data['close_long_signal'].iloc[i]
        open_short_signal = data['open_short_signal'].iloc[i]
        close_short_signal = data['close_short_signal'].iloc[i]

        if open_long_signal and not in_position:
            entry_price = curr_row['open_long']
            position_size = capital * leverage / entry_price  # Calculates position size based on capital and leverage
            position_value = position_size * entry_price  # Calculates position value
            capital -= position_value * transaction_cost  # Deducts transaction costs from capital
            in_position = True
            trade_history.append(('Buy', curr_row['Date'], entry_price))

        elif close_long_signal and in_position:
            exit_price = curr_row['close_long']
            capital += position_value * leverage * (exit_price - entry_price)  # Calculates the profit or loss of the position based on leverage
            capital -= position_value * transaction_cost  # Deducts transaction costs from capital
            position_size = capital / exit_price  # Updates position size based on capital
            position_value = position_size * exit_price  # Updates position value
            in_position = False
            trade_history.append(('Sell', curr_row['Date'], exit_price))

        elif open_short_signal and in_position:
            exit_price = curr_row['open_short']
            capital += position_value * leverage * (exit_price - entry_price)  # Calculates the profit or loss of the position based on leverage
            capital -= position_value * transaction_cost  # Deducts transaction costs from capital
            position_size = capital / exit_price  # Updates position size based on capital
            position_value = position_size * exit_price  # Updates position value
            in_position = False
            trade_history.append(('Open Short', curr_row['Date'], exit_price))

        elif close_short_signal and in_position:
            exit_price = curr_row['close_short']
            capital += position_value * leverage * (exit_price - entry_price)  # Calculates the profit or loss of the position based on leverage
            capital -= position_value * transaction_cost  # Deducts transaction costs from capital
            position_size = capital / exit_price  # Updates position size based on capital
            position_value = position_size * exit_price  # Updates position value
            in_position = False
            trade_history.append(('Sell', curr_row['Date'], exit_price))

        # Calculate final capital
        capital += position_value * leverage  # Adds the value of the final position to the capital

    return capital, trade_history


def calculate_trading_signal(data):
    """
    Calculates trading signals based on moving averages.

    Arguments:
    - data: pandas DataFrame containing the data.

    Returns:
    - data: Updated DataFrame with trading signals.

    """

    signals = pd.DataFrame()
    signals['signal'] = 0
    short_ma = 10
    long_ma = 30

    # Calculate moving averages
    signals['long_ma'] = data['Close'].rolling(long_ma).mean()
    signals['short_ma'] = data['Close'].rolling(short_ma).mean()

    # Generate trading signals (Long)
    data['open_long_signal'] = data['Close'] < signals['short_ma']
    data['open_short_signal'] = data['Close'] < signals['short_ma']
    data['close_long_signal'] = data['Close'] < signals['short_ma']
    data['close_short_signal'] = data['Close'] < signals['short_ma']

    return data
