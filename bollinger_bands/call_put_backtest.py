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

#import strategy
import modified_strategy as strategy

def main(path_long, path_short, lot_size = 50, lookback = 14, max_investment = 5000, brokerage = 55, allow_short = True, sl = True, stoploss = 5, target_orders=False, std_mult = 1):

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
    global total_buys, total_sells
    global total_buys_no_broker, total_sells_no_broker

    no_of_buys = 0
    no_of_sells = 0
    total_buys = 0
    total_sells = 0
    total_buys_no_broker = 0
    total_sells_no_broker = 0

    def long(long_price, short_price):
        global no_of_buys, no_of_sells, total_buys, total_sells, stoploss_buy_prices, stoploss_sell_prices, total_sells_no_broker, total_buys_no_broker

        if(no_of_buys>no_of_sells):
            return
        elif(no_of_buys<no_of_sells):
            no_of_buys += 2
            total_buys += long_price
            total_buys_no_broker += long_price
            total_sells += short_price - brokerage
            total_sells_no_broker += short_price
        elif(no_of_buys==no_of_sells):
            no_of_buys += 1
            total_buys += long_price
            total_buys_no_broker += long_price
        stoploss_buy_prices = [long_price*(100-stoploss)/100]
        stoploss_sell_prices = []

    def short(long_price, short_price):
        global no_of_buys, no_of_sells, total_buys, total_sells, stoploss_buy_prices, stoploss_sell_prices, total_sells_no_broker, total_buys_no_broker

        if(no_of_sells>no_of_buys):
            return
        elif(no_of_sells<no_of_buys):
            no_of_sells += 2
            total_buys += short_price
            total_sells += long_price - brokerage
            total_buys_no_broker += short_price
            total_sells_no_broker += long_price
        elif(no_of_buys==no_of_sells):
            no_of_sells += 1
            total_buys += short_price
            total_buys_no_broker += short_price
        stoploss_sell_prices = [short_price*(100-stoploss)/100]
        stoploss_buy_prices = []

    def buy(long_price, short_price):   #you are squaring off the short, or selling the short_price stock
        global no_of_buys, no_of_sells, total_buys, total_sells, stoploss_buy_prices, stoploss_sell_prices, total_sells_no_broker, total_buys_no_broker

        if(no_of_sells>no_of_buys):
            no_of_buys += 1
            total_sells += short_price - brokerage
            total_sells_no_broker += short_price
        stoploss_sell_prices = []
    
    def sell(long_price, short_price):   #you are squaring off the long, or selling the long_price stock
        global no_of_buys, no_of_sells, total_buys, total_sells, stoploss_buy_prices, stoploss_sell_prices, total_sells_no_broker, total_buys_no_broker

        if(no_of_buys>no_of_sells):
            no_of_sells += 1
            total_sells += long_price - brokerage
            total_sells_no_broker += long_price
        stoploss_buy_prices = []

    def stoploss_check(long_price, short_price):
        global no_of_buys, no_of_sells, total_buys, total_sells, stoploss_buy_prices, stoploss_sell_prices

        if(len(stoploss_buy_prices)>0):
            if(long_price<stoploss_buy_prices[0]):
                print("stoploss selling " + str(long_price) + "/" + str(short_price))
                sell(long_price, short_price)
        if(len(stoploss_sell_prices)>0):
            if(short_price<stoploss_sell_prices[0]):
                print("stoploss buying " + str(long_price) + "/" + str(short_price))
                buy(long_price, short_price)
    

    long_signals = ["none", "none", "none", "none", "none"]
    short_signals = ["none", "none", "none", "none", "none"]
    index = 0

    strategy_return = "none"
    pnl = []
    net_profit = []
    profit_variance = []
    net_profit_no_broker = []

    strategy_long = strategy.strategy()
    strategy_short = strategy.strategy()

    for n in range(len(data_long)):
        close_long = data_long.loc[n]['close'] * lot_size
        close_short = data_short.loc[n]['close'] * lot_size

        long_strategy_return = strategy_long.main(close_long, lookback, std_mult)
        short_strategy_return = strategy_short.main(close_short, lookback, std_mult)

        if(sl==True):
            stoploss_check(close_long, close_short)

        long_signals[index] = long_strategy_return
        short_signals[index] = short_strategy_return
        index += 1
        if(index==3):
            index = 0

        if("buy" in long_signals and "sell" in short_signals):
            #square off shorts and buy long, i.e. sqayre off puts and buy call
            print("buy " + str(close_long) + "/" + str(close_short))
            buy(close_long, close_short)
        elif("sell" in long_signals and "buy" in short_signals):
            #square off long and buy short, i.e squre off calls and buy put
            print("sell " + str(close_long) + "/" + str(close_short))
            sell(close_long, close_short)
        elif("long" in long_signals and "short" in short_signals):
            #square off long and buy short, i.e squre off calls and buy put
            print("sell " + str(close_long) + "/" + str(close_short))
            long(close_long, close_short)
        elif("short" in long_signals and "long" in short_signals):
            #square off long and buy short, i.e squre off calls and buy put
            print("sell " + str(close_long) + "/" + str(close_short))
            long(close_long, close_short)

        #if(long_strategy_return=="buy"):
        #    print("buying")
        #    buy(close_long, close_short)
        #if(long_strategy_return=="sell"):
        #    print("selling")
        #    sell(close_long, close_short)
        #if(long_strategy_return=="short"):
        #    print("shorting")
        #    short(close_long, close_short)
        #if(long_strategy_return=="long"):
        #    print("longing")
        #    long(close_long, close_short)

        pnl.append(total_sells-total_buys)
        if(no_of_buys>no_of_sells):
            net_profit.append(total_sells-total_buys + ((no_of_buys - no_of_sells )*close_long))
        else:
            net_profit.append(total_sells-total_buys + ((no_of_sells - no_of_buys )*close_short))
        profit_variance.append(np.std(net_profit))

    ref_no = abs(no_of_buys - no_of_sells)
    if(no_of_buys>no_of_sells):
        ref_pro = float(data_long.loc[len(data_long) - 1]['close']) * ref_no
        net_profit_no_broker.append(total_sells_no_broker-total_buys_no_broker + ((no_of_buys - no_of_sells )*close_long))
    else:
        ref_pro = float(data_short.loc[len(data_long) - 1]['close']) * ref_no
        net_profit_no_broker.append(total_sells_no_broker-total_buys_no_broker + ((no_of_sells - no_of_buys )*close_short))

    #y_axis_1 = pd.Series(pnl, index = data_long.loc[:]['datetime'].values)
    y_axis_2 = pd.Series(net_profit, index = data_long.loc[:]['datetime'].values)
    #y_axis_3 = data_long.loc[:]['close']
    #y_axis_3.index = data_long.loc[:]['datetime'].values
    #plt.figure(1)
    #plt.plot(y_axis_1,color='blue', label="Booked profits")

    plt.figure(2)
    plt.plot(y_axis_2, color='green', label = "Net profits")
    
    #plt.figure(3)
    #plt.plot(y_axis_3, color='black', label = "Price")

    print("Long open price = ", data_long.loc[0]["close"] * lot_size)
    print("Short open price = ", data_short.loc[0]["close"] * lot_size)
    print("Long close price = ", data_long.loc[len(data_long) - 1]["close"] * lot_size)
    print("Short close price = ", data_short.loc[len(data_long) - 1]["close"] * lot_size)

    print("Maximum investment = ", -min(pnl))
    print("Current_holdings = ",no_of_buys - no_of_sells )
    print("Net profit = ", net_profit[-1])
    print("Number of buys = ", no_of_buys)
    print("Number of sells = ", no_of_sells)
    print("Profit by holding ", ref_no, "shares = ", ref_pro)
    print("Profits without brokerage = ", net_profit_no_broker[-1])
    print("Standard Deviation of profit = ", profit_variance[-1])
    plt.legend(loc='upper left', fontsize=8)
    #plt.show()

no_of_strikes = 5

def get_strike(date):

    banknifty_path = "/home/mgoel/Documents/quant_algos/Data/CNXBAN_1minute" + str(date) + "T09:15:00.csv"
    if(os.path.isfile(banknifty_path)==False):
        print("extracting data")
        historical_data.get_equity_historical_data(start_date = str(date) + "T09:15:00.000Z", end_date = str(date) + "T15:30:00.000Z", stock_code="CNXBAN", time_interval="1minute")
    if(os.path.isfile(banknifty_path)==False):
        print("No bank_nifty data")
        print(banknifty_path)
        exit(0)
    bank_nifty_data = pd.read_csv(banknifty_path)

    strikes_call = []
    strikes_put = []
    bank_nifty_strikes = []

    bank_nifty = (bank_nifty_data.loc[bank_nifty_data['datetime'] == date + ' 09:15:00']['close'].values[0])
    if(bank_nifty%100>=50):
        bank_nifty = (bank_nifty//100 + 1)*100
    else:
        bank_nifty = (bank_nifty//100)*100
    bank_nifty_strikes.append(bank_nifty)
    for i in range(no_of_strikes + 1):
        strikes_call.append(int(bank_nifty) + i*100) 
        strikes_put.append(int(bank_nifty) - i*100) 
        
    print(strikes_call)
    print(strikes_put)
    return strikes_call, strikes_put
            

i = 0
date = "05"
calls, puts = get_strike("2023-06-" + date)
strike_call = calls[no_of_strikes-1]
strike_put = puts[no_of_strikes-1]
expiry = "2023-06-08"
path_call = '/home/mgoel/Documents/quant_algos/Data/CNXBAN_options_' + expiry + '_call' + str(strike_call) + '_1minute' + expiry[:-2] + str(date) + 'T09:15:00.csv'
path_put = '/home/mgoel/Documents/quant_algos/Data/CNXBAN_options_' + expiry + '_put' + str(strike_put) + '_1minute' + expiry[:-2] + str(date) + 'T09:15:00.csv'

if(os.path.isfile(path_call)==False):
        historical_data.get_option_historical_data(start_date = expiry[:-2] + str(date) + "T09:15:00.000Z", end_date = expiry[:-2] + str(date) + "T15:30:00.000Z", expiry = expiry + "T07:00:00.000Z", strike = strike_call, stock_code="CNXBAN", time_interval="1minute", right="call")

if(os.path.isfile(path_put)==False):
        historical_data.get_option_historical_data(start_date = expiry[:-2] + str(date) + "T09:15:00.000Z", end_date = expiry[:-2] + str(date) + "T13:30:00.000Z", expiry = expiry + "T07:00:00.000Z", strike = strike_put, stock_code="CNXBAN", time_interval="1minute", right="put")

main(path_call, path_put, lot_size=25, lookback=12, max_investment=2000, brokerage=35, allow_short=False, sl=True, stoploss=10, target_orders=True, std_mult=2)