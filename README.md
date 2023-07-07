# hyperion
genetic algorithm strategy explorer

## Description

The code first defines a backtesting function backtest that takes historical data from a CSV file, along with a trading strategy defined by an individual, and performs the backtest. It calculates moving averages, simulates opening and closing positions based on the strategy's parameters, and tracks the capital, trade history, and equity history during the backtest.

Next, several helper functions are defined. generate_initial_population generates an initial population of trading strategies with random parameters. mutate applies mutation to a trading strategy by randomly modifying its parameters. crossover performs crossover between two trading strategies to create a new strategy. select_parents selects parents from the population based on their fitness. repopulate generates offspring strategies through crossover and mutation.

The code then initializes the population, performs backtesting on each strategy in the population, and assigns a fitness score to each strategy. It iterates over multiple generations, selecting parents, generating offspring, and evaluating their fitness.

Finally, the code prints the offspring strategies, which represent the best strategies found by the genetic algorithm.
