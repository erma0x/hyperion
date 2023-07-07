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
 
[ ] report pdf

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