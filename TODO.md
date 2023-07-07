[ ] obbiettivo finale, un bel backtesting per poter prendere la strategia e metterla in un conto live.
    con FOREX e/o Crypto come Asset, ed utilizzando i Futures per andare Long e Short.
    max DrowDown del 4% in backtest. Con piu position size possibile per maggiori guadagni.
    Dati di almeno 5 anni.
    Backtest e Walk Forward test


WALK FORWARD TEST OPTIMIZATION
    Get all relevant data
    Break data into multiple pieces
    Run an optimisation to find the best parameters on the first piece of data (first in-sample)
    Apply those parameters on the second piece of data (first out-of-sample)
    Run an optimisation to find the best parameters on the next in-sample data
    Apply those parameters on the next out-of-sample data
    Repeat until you’ve covered all the pieces of data
    Collate the performances of all the out-of-sample data

[ ] single strategy evolution
 

[ ] butta giu le basi per un report
    - figure della stessa figsize
    - reformatta l'indice del tempo nel prezzo

[ ] butta giu le basi per un backtest multi market
[ ] prendi e salvati tutti i dati senza scaricarli
[ ] commissioni (sottrai pips dal prezzo nei guadagni ed aggiungilo alle perdite a seconda della coppia)
[ ] report: calcolami i pips medi di guadagno
[ ] multiple experiment directory
[ ] genetic algorithm evolution

[ ] PERFORMANCE METRICs to do
    
    Holding Time average: save in d, h, min, seconds ex 1d,4h,30m   or 35m 
    biggest winner %
    biggest winner $
    biggest loser %
    biggest loser $
    Losing Streak (n trades in loss)
    risk reward  tp/sl
    Sharpe ratio
    Sortino ratio
    Calmar ratio

[ ] visualize short/long?