#the broker code

#strategy.main(close) returns "buy" or "sell"

import os
#import test_strategy as strategy
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
from pylab import rcParams
rcParams['figure.figsize'] = 10, 6
#import dateparse
import io
import numpy as np

def main(path_long, lot_size = 50, lookback = 14, max_investment = 5000, brokerage = 55, allow_short = True, sl = True, stoploss = 5, target_orders=False):

    # max_investment = 5000
    #brokerage = 30
    #allow_short = False
    #ticker_symbol = "ADANIENT.NS"
    #path = '/home/mgoel/Documents/quant_algos/Broker_simulation/Data/'+ticker_symbol+'.csv'
    #no_of_ticks = 20

    if(os.path.exists(path_long.strip())==False):
        print("Data file does not exist")
        print(path_long)
        exit()

    data_long = pd.read_csv(path_long)

    #stoploss
    global stoploss_buy_prices, stoploss_sell_prices
    stoploss_buy_prices = []
    stoploss_sell_prices = []
    def sl_check(price):
        global stoploss_sell_prices, stoploss_buy_prices

        for stop_loss in stoploss_buy_prices:
            if(price<stop_loss):
                sell_order(price)
                stoploss_buy_prices.remove(stop_loss)
        for stop_loss in stoploss_sell_prices:
            if(price>stop_loss):
                buy_order(price)
                stoploss_sell_prices.remove(stop_loss)


    #buy variables
    global no_of_buys 
    global total_buy 

    no_of_buys = 0
    total_buy = 0
    #buy order
    def buy_order(price):
        global no_of_buys, total_buy, stoploss_buy_prices
        if((total_buy + price - total_sells)>max_investment):
            return
        no_of_buys+=1
        total_buy+=price
        stoploss_buy_prices.append(price*(100-stoploss)/100)


    #buy variables
    global no_of_sells, total_sells
    no_of_sells = 0
    total_sells = 0
    #buy order
    def sell_order(price):
        global no_of_sells, total_sells, stoploss_sell_prices
        if((total_sells + price - brokerage - total_buy)>max_investment):
            return
        if(allow_short==False and no_of_sells>=no_of_buys):
            return
        no_of_sells+=1
        total_sells+=price - brokerage
        stoploss_sell_prices.append(price*(100+stoploss)/100)

    def buy_target(price):
        global no_of_buys, total_buy, stoploss_buy_prices
        global stoploss_sell_prices
        if(no_of_buys<=no_of_sells):
            if(total_buy + price*(no_of_sells - no_of_buys + 1) - total_sells > max_investment):
                return
            total_buy += price*(no_of_sells - no_of_buys + 1)
            no_of_buys += no_of_sells - no_of_buys + 1  
        stoploss_sell_prices = []
        stoploss_buy_prices=[price*(100-stoploss)/100]

    def sell_target(price):
        global stoploss_buy_prices
        global no_of_sells, total_sells, stoploss_sell_prices
        if(no_of_buys>=no_of_sells):
            total_sells += price*(no_of_buys - no_of_sells + 1)
            no_of_sells += no_of_buys - no_of_sells + 1
            
        stoploss_buy_prices = []
        stoploss_sell_prices=[price*(100+stoploss)/100]

    strategy_return = "none"
    pnl = []
    net_profit = []
    profit_variance = []
    for n in range(len(data_long)):
        close_long = data_long.loc[n]['close'] * lot_size
        #close *= lot_size
        strategy_return = strategy.main(close_long, lookback)
        if(sl==True):
            sl_check(price=close_long)
        if(strategy_return=="buy"):
            if(target_orders):
                buy_target(close_long)
            else:
                buy_order(close_long)
        elif(strategy_return=="sell"):
            if(target_orders):
                sell_target(close_long)
            else:
                sell_order(close_long)
        pnl.append(total_sells-total_buy)
        net_profit.append(total_sells-total_buy + ((no_of_buys - no_of_sells )*close_long) )
        profit_variance.append(np.std(net_profit))


    y_axis_1 = pd.Series(pnl, index = data_long.loc[:]['datetime'].values)
    y_axis_2 = pd.Series(net_profit, index = data_long.loc[:]['datetime'].values)
    y_axis_3 = data_long.loc[:]['close']
    y_axis_3.index = data_long.loc[:]['datetime'].values
    #plt.figure(1)
    #plt.plot(y_axis_1,color='blue', label="Booked profits")

    plt.figure(2)
    plt.plot(y_axis_2, color='green', label = "Net profits")
    
    plt.figure(3)
    plt.plot(y_axis_3, color='black', label = "Price")

    print("Maximum investment = ", -min(pnl))
    print("Current_holdings = ",no_of_buys - no_of_sells )
    print("Net profit = ", net_profit[-1])
    print("Number of buys = ", no_of_buys)
    print("Number of sells = ", no_of_sells)
    print("Profit by holding ", no_of_buys - no_of_sells, "shares = ", lot_size*((no_of_buys - no_of_sells)*(float(data_long.loc[len(data_long) - 1]['close']) - float(data_long.loc[0]['close']))))
    print("Profits without brokerage = ", net_profit[-1] + (no_of_sells*brokerage))
    print("Standard Deviation of profit = ", profit_variance[-1])
    plt.legend(loc='upper left', fontsize=8)
    plt.show()