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

import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '/home/mgoel/Documents/quant_algos/breeze')
import historical_data

import strategy

def main(path_long, path_short, lot_size = 50, lookback = 14, max_investment = 5000, brokerage = 55, allow_short = True, sl = True, stoploss = 5, target_orders=False):

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

    if(os.path.exists(path_short.strip())==False):
        print("Data file does not exist")
        print(path_short)
        exit()

    data_short = pd.read_csv(path_short)

    #stoploss
    global stoploss_buy_prices, stoploss_sell_prices
    stoploss_buy_prices = []
    stoploss_sell_prices = []

    #buy variables
    global no_of_buys, no_of_sells 
    global total_buy, total_sells

    no_of_buys = 0
    no_of_sells = 0
    total_buys = 0
    total_sells = 0

    def buy(long_price, short_price):
        global no_of_buys, no_of_sells, total_buys, total_sells, stoploss_buy_prices, stoploss_sell_prices

        if(no_of_buys>no_of_sells):
            return
        elif(no_of_buys<no_of_sells):
            no_of_buys += 1
            total_buys += long_price
            total_sells += short_price - brokerage
        elif(no_of_buys==no_of_sells):
            no_of_buys += 1
            total_buys += long_price
        stoploss_buy_prices = [long_price*(100-stoploss)/100]
        stoploss_sell_prices = []

    def sell(long_price, short_price):
        global no_of_buys, no_of_sells, total_buys, total_sells, stoploss_buy_prices, stoploss_sell_prices

        if(no_of_sells>no_of_buys):
            return
        elif(no_of_sells<no_of_buys):
            no_of_sells += 1
            total_buys += short_price
            total_sells += long_price - brokerage
        elif(no_of_buys==no_of_sells):
            no_of_buys += 1
            total_buys += short_price
        stoploss_sell_prices = [short_price*(100-stoploss)/100]
        stoploss_buy_prices = []

    def stoploss_check(long_price, short_price):
        global no_of_buys, no_of_sells, total_buy, total_sells, stoploss_buy_prices, stoploss_sell_prices

        if(long_price<stoploss_buy_prices[0]):
            sell(long_price, short_price)
        if(short_price<stoploss_sell_prices[0]):
            buy(long_price, short_price)
    

    long_signals = ["none", "none", "none"]
    short_signals = ["none", "none", "none"]
    index = 0

    strategy_return = "none"
    pnl = []
    net_profit = []
    profit_variance = []
    for n in range(len(data_long)):
        close_long = data_long.loc[n]['close'] * lot_size
        close_short = data_short.loc[n]['close'] * lot_size

        long_strategy_return = strategy.main(close_long, lookback)
        short_strategy_return = strategy.main(close_short, lookback)

        if(sl==True):
            stoploss_check(close_long, close_short)

        long_signals[index] = long_strategy_return
        short_signals[index] = short_strategy_return
        index += 1
        if(index==3):
            index = 0

        if("buy" in long_signals and "buy" in short_signals):
            #square off shorts and buy long, i.e. sqayre off puts and buy call
            buy(close_long, close_short)
        elif("sell" in long_signals and "sell" in short_signals):
            #square off long and buy short, i.e squre off calls and buy put
            sell(close_long, close_short)

        pnl.append(total_sells-total_buy)
        if(no_of_buys>no_of_sells):
            net_profit.append(total_sells-total_buy + ((no_of_buys - no_of_sells )*close_long))
        else:
            net_profit.append(total_sells-total_buy + ((no_of_sells - no_of_buys )*close_short))
        profit_variance.append(np.std(net_profit))

    ref_no = abs(no_of_buys - no_of_sells)
    if(no_of_buys>no_of_sells):
        ref_pro = float(data_long.loc[len(data_long) - 1]['close']) * ref_no
    else:
        ref_pro = float(data_short.loc[len(data_long) - 1]['close']) * ref_no

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
    print("Profit by holding ", ref_no, "shares = ", ref_pro)
    print("Profits without brokerage = ", net_profit[-1] + (no_of_sells*brokerage))
    print("Standard Deviation of profit = ", profit_variance[-1])
    plt.legend(loc='upper left', fontsize=8)
    plt.show()

date = 15
strike_call = 44000
strike_put = 41000
path_call = '/home/mgoel/Documents/quant_algos/Data/CNXBAN_options_2023-05-25_call' + str(strike_call) + '_1minute2023-05-' + str(date) + 'T07:00:00.csv'
path_put = '/home/mgoel/Documents/quant_algos/Data/CNXBAN_options_2023-05-25_put' + str(strike_put) + '_1minute2023-05-' + str(date) + 'T07:00:00.csv'

if(os.path.exists(path_call.strip())==False):
        print("Extracting data")
        historical_data.get_option_historical_data(start_date = "2023-05-" + str(date) + "T07:00:00.000Z", end_date = "2023-05-" + str(date) + "T18:00:00.000Z", expiry = "2023-06-01T07:00:00.000Z", strike = strike_call, stock_code="CNXBAN", time_interval="1minute", right="call")

if(os.path.exists(path_put.strip())==False):
        print("Extracting data")
        historical_data.get_option_historical_data(start_date = "2023-05-" + str(date) + "T07:00:00.000Z", end_date = "2023-05-" + str(date) + "T18:00:00.000Z", expiry = "2023-06-01T07:00:00.000Z", strike = strike_put, stock_code="CNXBAN", time_interval="1minute", right="put")

main(path_call, path_put, lot_size=25, lookback=12, max_investment=4000, brokerage=35, allow_short=False, sl=True, stoploss=25, target_orders=True)