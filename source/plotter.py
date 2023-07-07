import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def plot_and_save(name_strategy,data,df_signals,equity_history,long_trades,short_trades,winning_long_trades,winning_short_trades):
    # Create PDF
    with PdfPages(f'strategies/{name_strategy}.pdf') as pdf:
        # Create the first plot
        fig1, ax1 = plt.subplots()

        # PRICE
        ax1.plot(data.index, data.Close,alpha=0.9)
        
        # LONG
        ax1.scatter(df_signals.index, df_signals['open_long_signal'], color='green', label='buy',marker='^',alpha=1 )
        ax1.scatter(df_signals.index, df_signals['close_long_signal'], color='red', label='sell' ,marker='v',alpha=1 )
        
        # SHORT
        ax1.scatter(df_signals.index, df_signals['open_short_signal'], color='blue', label='buy',marker='^',alpha=1 )
        ax1.scatter(df_signals.index, df_signals['close_short_signal'], color='purple', label='sell' ,marker='v',alpha=1 )

        ax1.set_title('Trading operations')
        ax1.set_xticks(data.index[::5])
        ax1.set_xticklabels(data.index[::5], rotation=45)
        ax1.set_ylim(min(data.Close)*0.97, max(data.Close)*1.03)
        # Add the first plot to the PDF
        pdf.savefig(fig1)

        # Create the second plot
        fig2, ax2 = plt.subplots()
        fig2.set_figheight(15)
        fig2.set_figwidth(20)
        ax2.plot(equity_history)
        
        #ax2.xlabel('ticks')
        #ax2.ylabel('equity')

        #ax2.title('Backtested trading strategy results')
        
        # Add the second plot to the PDF
        pdf.savefig(fig2)

        # Create the third plot
        fig3, ax3 = plt.subplots()
        x = ['Long Trades','Short Trades'] 
        y = [long_trades, short_trades]
        
        ax3.bar(x, y, width=0.3, color=['green','red'])
        
        #ax3.title('title')
        #ax3.xlabel('Trade Type')
        #ax3.ylabel('ylabel')
        # Add the third plot to the PDF
        pdf.savefig(fig3)

        # Create the fourth plot
        fig4, ax4 = plt.subplots()
        x = ['Long Trades','Short Trades'] 
        y = [winning_long_trades, winning_short_trades]
        ax4.bar(x, y, width=0.3, color=['green','red'])
        
        #ax4.title('% winning trades')
        #ax4.xlabel('Trade Type')
        #ax4.ylabel('% winning trades')
        
        # Add the fourth plot to the PDF
        pdf.savefig(fig4)

    
    
def plot_operations(data):
    
    plt.plot(data.index, data.Close,alpha=0.9)
    
    # LONG
    plt.scatter(data.index, data['open_long_signal'], color='green', label='buy',marker='^',alpha=1 )
    plt.scatter(data.index, data['close_long_signal'], color='red', label='sell' ,marker='v',alpha=1 )
    
    # SHORT
    plt.scatter(data.index, data['open_short_signal'], color='blue', label='buy',marker='^',alpha=1 )
    plt.scatter(data.index, data['close_short_signal'], color='purple', label='sell' ,marker='v',alpha=1 )

    plt.set_title('Trading operations')
    plt.set_xticks(data.index[::5])
    plt.set_xticklabels(data.index[::5], rotation=45)
    plt.set_ylim(min(data.Close)*0.97, max(data.Close)*1.03)

    plt.figure(figsize=(25,20))
    plt.show()
    
def plot_equity(equity_history,name_file):
    
    f, ax1 = plt.subplots(1, 1, sharey=True)
    
    f.set_figheight(15)
    f.set_figwidth(20)

    plt.plot(equity_history)
    
    plt.xlabel('ticks')
    plt.ylabel('equity')

    plt.title('Backtested trading strategy results')
    #plt.show()
    plt.savefig(f'{name_file}_1.png')


def plot_logs_returns(equity_history,name_file):

    log_returns = np.diff(np.log(equity_history))

    fig, ax = plt.subplots()

    pd.Series(log_returns).hist(bins=50, ax=ax)

    #plt.show()
    plt.savefig(f'{name_file}_2.png')

def plot_signals(plot_open_signal,plot_close_signal,name_file):
    f, (ax1, ax2) = plt.subplots(2, 1, sharey=True)
    f.set_figheight(15)
    f.set_figwidth(20)
    
    # OPEN SIGNAL
    ax1.vlines(plot_open_signal,ymin=0,ymax=1,colors='green')
    ax1.set_title('open signal')

    ax1.set_ylim(0, 1)
    ax1.set_xlim(0,max(plot_open_signal)+5)
    x_axis1 = ax1.axes.get_xaxis()
    x_axis1.set_visible(False)
    y_axis1 = ax1.axes.get_yaxis()
    y_axis1.set_visible(False)
    
    # CLOSE SIGNAL
    ax2.vlines(plot_close_signal,ymin=0,ymax=1,colors='red')
    ax2.set_title('close signal')
    x_axis2 = ax2.axes.get_xaxis()    
    x_axis2.set_visible(True)
    y_axis2 = ax2.axes.get_yaxis()
    y_axis2.set_visible(False)
    ax2.set_ylim(0, 1)
    ax2.set_xlim(0,max(plot_open_signal)+5)
    #plt.show()
    plt.savefig(f'{name_file}_3.png')

def plot_long_vs_short_trades(title,ylabel,long_trades,short_trades,name_file):
    x = ['Long Trades','Short Trades'] 
    y = [long_trades, short_trades]
    
    plt.bar(x, y, width=0.3, color=['green','red'])
    plt.title(title)
    plt.xlabel('Trade Type')
    plt.ylabel(ylabel)
    #plt.show()
    plt.savefig(f'{name_file}_4.png')