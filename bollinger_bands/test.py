#import strategy_seconds as strategy
#import strategy
#import strategy_modified as strategy

import modified_strategy as strategy

import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '/home/mgoel/Documents/quant_algos/breeze')
import historical_data

#the broker code

#strategy.main(close) returns "buy" or "sell"

import os
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
from pylab import rcParams
rcParams['figure.figsize'] = 10, 6
import io
import numpy as np
import datetime


#strategy: inverse, and std (std *= 1)
#main: pcsame, pcopp, normal

def main_pcsame(path_long, path_short, lot_size = 50, lookback = 14, max_investment = 5000, brokerage = 35, allow_short = True, sl = True, stoploss = 5, target_orders=False, std_mult = 1):

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
        global no_of_buys, no_of_sells, total_buys, total_sells, stoploss_buy_prices, stoploss_sell_prices, total_buys_no_broker, total_sells_no_broker

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
                sell(long_price, short_price)
        if(len(stoploss_sell_prices)>0):
            if(short_price<stoploss_sell_prices[0]):
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

    for n in range(min(len(data_long), len(data_short))):
        close_long = data_long.loc[n]['close'] * lot_size
        close_short = data_short.loc[n]['close'] * lot_size

        long_strategy_return = strategy_long.main(close_long, lookback, std_mult = std_mult)
        short_strategy_return = strategy_short.main(close_short, lookback, std_mult = std_mult)

        if(sl==True):
            stoploss_check(close_long, close_short)

        long_signals[index] = long_strategy_return
        short_signals[index] = short_strategy_return
        index += 1
        if(index==5):
            index = 0

        if("buy" in long_signals and "buy" in short_signals):
            #square off shorts and buy long, i.e. sqayre off puts and buy call
            buy(close_long, close_short)
        elif("sell" in long_signals and "sell" in short_signals):
            sell(close_long, close_short)
        elif("long" in long_signals and "long" in short_signals):
            long(close_long, close_short)
        elif("short" in long_signals and "short" in short_signals):
            long(close_long, close_short)

        #if(long_strategy_return=="buy"):
        #    buy(close_long, close_short)
        #if(long_strategy_return=="short"):
        #    sell(close_long, close_short)

        pnl.append(total_sells-total_buys)
        if(no_of_buys>no_of_sells):
            net_profit.append(total_sells-total_buys + ((no_of_buys - no_of_sells )*close_long))
            net_profit_no_broker.append(total_sells_no_broker-total_buys_no_broker + ((no_of_buys - no_of_sells )*close_long))
        else:
            net_profit.append(total_sells-total_buys + ((no_of_sells - no_of_buys )*close_short))
            net_profit_no_broker.append(total_sells_no_broker-total_buys_no_broker + ((no_of_sells - no_of_buys )*close_short))
        profit_variance.append(np.std(net_profit))


    return -min(pnl), net_profit[-1], net_profit_no_broker[-1]

def main_pcopp(path_long, path_short, lot_size = 50, lookback = 14, max_investment = 5000, brokerage = 55, allow_short = True, sl = True, stoploss = 5, target_orders=False, std_mult = 1):

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

    


    return -min(pnl), net_profit[-1], net_profit_no_broker[-1]

def main_normal(path_long, path_short, lot_size = 50, lookback = 14, max_investment = 5000, brokerage = 35, allow_short = True, sl = True, stoploss = 5, target_orders=False, std_mult = 1):

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
        global no_of_buys, no_of_sells, total_buys, total_sells, stoploss_buy_prices, stoploss_sell_prices, total_buys_no_broker, total_sells_no_broker

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
                sell(long_price, short_price)
        if(len(stoploss_sell_prices)>0):
            if(short_price<stoploss_sell_prices[0]):
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

    for n in range(min(len(data_long), len(data_short))):
        close_long = data_long.loc[n]['close'] * lot_size
        close_short = data_short.loc[n]['close'] * lot_size

        long_strategy_return = strategy_long.main(close_long, lookback, std_mult = std_mult)
        short_strategy_return = strategy_short.main(close_short, lookback, std_mult = std_mult)

        if(sl==True):
            stoploss_check(close_long, close_short)

        long_signals[index] = long_strategy_return
        short_signals[index] = short_strategy_return
        index += 1
        if(index==5):
            index = 0

        #if("buy" in long_signals and "buy" in short_signals):
        #    #square off shorts and buy long, i.e. sqayre off puts and buy call
        #    buy(close_long, close_short)
        #elif("sell" in long_signals and "sell" in short_signals):
        #    #square off long and buy short, i.e squre off calls and buy put
        #    sell(close_long, close_short)

        if(long_strategy_return=="buy"):
            buy(close_long, close_short)
        if(long_strategy_return=="sell"):
            sell(close_long, close_short)
        if(long_strategy_return=="short"):
            short(close_long, close_short)
        if(long_strategy_return=="long"):
            long(close_long, close_short)

        pnl.append(total_sells-total_buys)
        if(no_of_buys>no_of_sells):
            net_profit.append(total_sells-total_buys + ((no_of_buys - no_of_sells )*close_long))
            net_profit_no_broker.append(total_sells_no_broker-total_buys_no_broker + ((no_of_buys - no_of_sells )*close_long))
        else:
            net_profit.append(total_sells-total_buys + ((no_of_sells - no_of_buys )*close_short))
            net_profit_no_broker.append(total_sells_no_broker-total_buys_no_broker + ((no_of_sells - no_of_buys )*close_short))
        profit_variance.append(np.std(net_profit))


    return -min(pnl), net_profit[-1], net_profit_no_broker[-1]



#df_averages = []
expiries = []
expiries.append(datetime.date(year=2023, month=5, day=25))
expiries.append(datetime.date(year=2023, month=5, day=18))
expiries.append(datetime.date(year=2023, month=5, day=11))
expiries.append(datetime.date(year=2023, month=5, day=4))
expiries.append(datetime.date(year=2023, month=4, day=27))
expiries.append(datetime.date(year=2023, month=4, day=20))
expiries.append(datetime.date(year=2023, month=4, day=13))
expiries.append(datetime.date(year=2023, month=4, day=6))
expiries.append(datetime.date(year=2023, month=2, day=23))
expiries.append(datetime.date(year=2023, month=2, day=16))
expiries.append(datetime.date(year=2023, month=2, day=9))
expiries.append(datetime.date(year=2023, month=2, day=2))
expiries.append(datetime.date(year=2023, month=1, day=25))
expiries.append(datetime.date(year=2023, month=1, day=19))
expiries.append(datetime.date(year=2023, month=1, day=12))
expiries.append(datetime.date(year=2023, month=1, day=5))

no_of_strikes = 5
std_mults = [1]
#expiries = [datetime.date(year=2023, month=2, day=23), datetime.date(year=2023, month=2, day=23), datetime.date(year=2023, month=2, day=23), datetime.date(year=2023, month=2, day=23), datetime.date(year=2023, month=2, day=23), datetime.date(year=2023, month=2, day=16), datetime.date(year=2023, month=2, day=9), datetime.date(year=2023, month=2, day=2), datetime.date(year=2023, month=1, day=25), datetime.date(year=2023, month=1, day=19), datetime.date(year=2023, month=1, day=12), datetime.date(year=2023, month=1, day=5)]
#expiries = [datetime.date(year=2023, month=5, day=4)]
for std_mult in std_mults:
    name = "_" + str(std_mult) + "std"
    for expiry in expiries:
        #expiry = datetime.date(year=2023, month=5, day=11)
        dates = []
        no_of_days = 5
        i = 0
        while(i < no_of_days):
            d = (expiry - datetime.timedelta(i + 1))
            if(d.isoweekday()==6 or d.isoweekday()==7 or (d.month==5 and d.day==1) or (d.month==4 and d.day==22) or (d.month==4 and d.day==14) or (d.month==4 and d.day==7) or (d.month==4 and d.day==4) or (d.month==3 and d.day==30) or (d.month==3 and d.day==7) or (d.month==1 and d.day==26)):
                no_of_days += 1
                i += 1
                continue
            else:
                dates.append(str(d))
            i += 1
        dates.reverse()  
        print(dates)  

        #dates = [22,23,24, 25, 26]
        #dates = [15,16,17,18,19,22,23,24]

        banknifty_path = "/home/mgoel/Documents/quant_algos/Data/CNXBAN_1minute" + str(dates[0]) + "T09:15:00.csv"
        if(os.path.isfile(banknifty_path)==False):
            print("extracting data")
            historical_data.get_equity_historical_data(start_date = str(dates[0]) + "T09:15:00.000Z", end_date = str(dates[-1]) + "T15:30:00.000Z", stock_code="CNXBAN", time_interval="1minute")
        if(os.path.isfile(banknifty_path)==False):
            print("No bank_nifty data")
            exit(0)
        bank_nifty_data = pd.read_csv(banknifty_path)

        strikes_call = []
        strikes_put = []
        bank_nifty_strikes = []

        for date in dates:
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
            

        dire = '/home/mgoel/Documents/quant_algos/bollinger_bands/tests_modified/' + str(expiry) + '/'
        if(os.path.isdir(dire)==False):
            os.mkdir(dire)

#        strikes_profit_callput = []
#        strikes_profit_putcall = []
#        strikes_profit_brk_callput = []
#        strikes_profit_brk_putcall = []
#        strikes_inv_callput = []
#        strikes_inv_putcall = []
#        for i in range(no_of_strikes + 1):
#            strikes_profit_callput.append(0)
#            strikes_profit_putcall.append(0)
#            strikes_profit_brk_callput.append(0)
#            strikes_profit_brk_putcall.append(0)
#            strikes_inv_callput.append(0)
#            strikes_inv_putcall.append(0)   
#
#        df = []
#        for j in range(len(dates)):
#            for i in range(no_of_strikes + 1):
#                strike_call = strikes_call[j*(no_of_strikes + 1) + i]
#                strike_put = strikes_put[j*(no_of_strikes + 1) + i]
#                date = dates[j]
#                bank_nifty_strike = strikes_call[j*(no_of_strikes + 1)]
#                path_call = '/home/mgoel/Documents/quant_algos/Data/CNXBAN_options_' + str(expiry) + '_call' + str(strike_call) + '_1minute' + (date) + 'T07:00:00.csv'
#                path_put = '/home/mgoel/Documents/quant_algos/Data/CNXBAN_options_' + str(expiry) + '_put' + str(strike_put) + '_1minute' + (date) + 'T07:00:00.csv'
#
#                if(os.path.isfile(path_call)==False):
#                    print("extracting data")
#                    historical_data.get_option_historical_data(start_date = (date) + "T07:00:00.000Z", end_date = (date) + "T18:00:00.000Z", expiry = str(expiry) + "T07:00:00.000Z", strike = strike_call, stock_code="CNXBAN", time_interval="1minute", right="call")
#                if(os.path.isfile(path_call)==False):
#                    continue
#
#                if(os.path.isfile(path_put)==False):
#                    print("extracting data")
#                    historical_data.get_option_historical_data(start_date = (date) + "T07:00:00.000Z", end_date = (date) + "T18:00:00.000Z", expiry = str(expiry) + "T07:00:00.000Z", strike = strike_put, stock_code="CNXBAN", time_interval="1minute", right="put")
#                if(os.path.isfile(path_put)==False):
#                    continue
#
#                with open(path_call, "rb") as file:
#                    # Go to the end of the file before the last break-line
#                    file.seek(2) 
#                    # Keep reading backward until you find the next break-line
#                    while file.read(1) != b'\n':
#                        file.seek(2, os.SEEK_CUR) 
#                    first_line_call = file.readline().decode()
#
#                    # Go to the end of the file before the last break-line
#                    file.seek(-2, os.SEEK_END) 
#                    # Keep reading backward until you find the next break-line
#                    while file.read(1) != b'\n':
#                        file.seek(-2, os.SEEK_CUR) 
#                    last_line_call = file.readline().decode()
#                first_line_call = first_line_call.split(',')
#                last_line_call = last_line_call.split(',')
#
#                with open(path_put, "rb") as file:
#                    # Go to the end of the file before the last break-line
#                    file.seek(2) 
#                    # Keep reading backward until you find the next break-line
#                    while file.read(1) != b'\n':
#                        file.seek(2, os.SEEK_CUR) 
#                    first_line_put = file.readline().decode()
#
#                    # Go to the end of the file before the last break-line
#                    file.seek(-2, os.SEEK_END) 
#                    # Keep reading backward until you find the next break-line
#                    while file.read(1) != b'\n':
#                        file.seek(-2, os.SEEK_CUR) 
#                    last_line_put = file.readline().decode()
#                first_line_put = first_line_put.split(',')
#                last_line_put = last_line_put.split(',')
#
#                inv_1, pr_1, prbr_1 = main_pcsame(path_call, path_put, lookback=12, max_investment=5000, lot_size=25, sl=True, stoploss=25, target_orders = True, brokerage=35, allow_short=False, std_mult=std_mult)
#                inv_2, pr_2, prbr_2 = main_pcsame(path_put, path_call, lookback=12, max_investment=5000, lot_size=25, sl=True, stoploss=25, target_orders = True, brokerage=35, allow_short=False, std_mult = std_mult)
#                #print([strike_call, first_line_call[11], last_line_call[11], strike_put, first_line_put[11], last_line_put[11], inv_1, pr_1, prbr_1, inv_2, pr_2, prbr_2])
#                df.append([date, abs(bank_nifty_strike - strike_call), strike_call, first_line_call[11], last_line_call[11], strike_put, first_line_put[11], last_line_put[11], inv_1, inv_2, pr_1, pr_2, prbr_1, prbr_2])
#                strikes_profit_callput[i] += pr_1
#                strikes_profit_brk_callput[i] += prbr_1
#                strikes_profit_putcall[i] += pr_2
#                strikes_profit_brk_putcall[i] += prbr_2
#                strikes_inv_callput[i] += inv_1/no_of_days
#                strikes_inv_putcall[i] += inv_2/no_of_days
#
#        for i in range(no_of_strikes + 1):
#            df.append([0, i*100, 0, 0, 0, 0, 0, 0, strikes_inv_callput[i], strikes_inv_putcall[i], strikes_profit_callput[i], strikes_profit_putcall[i], strikes_profit_brk_callput[i], strikes_profit_brk_putcall[i]])
#            #df_averages.append(["putcall same", str(expiry), i*100, strikes_profit_callput[i], strikes_profit_putcall[i]])
#
#        
#        df = pd.DataFrame(df, columns=["Date", "Difference from banknifty", "Call strike", "Call open", "Call close", "Put strike", "Put open", "Put close", "Investment callput", "Investment putcall", "Profit callput", "Profit putcall", "Profits-brokerage callput", "Profits-brokerage putcall"])
#        #dire = '/home/mgoel/Documents/quant_algos/bollinger_bands/tests/' + str(expiry) + '/'
#        #if(os.path.isdir(dire)==False):
#        #    os.mkdir(dire)
#        df.to_csv(dire + 'pcsame' + name + str(expiry) + '.csv')


        strikes_profit_callput = []
        strikes_profit_putcall = []
        strikes_profit_brk_callput = []
        strikes_profit_brk_putcall = []
        strikes_inv_callput = []
        strikes_inv_putcall = []
        for i in range(no_of_strikes + 1):
            strikes_profit_callput.append(0)
            strikes_profit_putcall.append(0)
            strikes_profit_brk_callput.append(0)
            strikes_profit_brk_putcall.append(0)
            strikes_inv_callput.append(0)
            strikes_inv_putcall.append(0)

        df = []
        for j in range(len(dates)):
            for i in range(no_of_strikes + 1):
                strike_call = strikes_call[j*(no_of_strikes + 1) + i]
                strike_put = strikes_put[j*(no_of_strikes + 1) + i]
                date = dates[j]
                bank_nifty_strike = strikes_call[j*(no_of_strikes + 1)]
                path_call = '/home/mgoel/Documents/quant_algos/Data/CNXBAN_options_' + str(expiry) + '_call' + str(strike_call) + '_1minute' + (date) + 'T09:15:00.csv'
                path_put = '/home/mgoel/Documents/quant_algos/Data/CNXBAN_options_' + str(expiry) + '_put' + str(strike_put) + '_1minute' + (date) + 'T09:15:00.csv'

                if(os.path.isfile(path_call)==False):
                    print("extracting data")
                    historical_data.get_option_historical_data(start_date = (date) + "T09:15:00.000Z", end_date = (date) + "T15:30:00.000Z", expiry = str(expiry) + "T07:00:00.000Z", strike = strike_call, stock_code="CNXBAN", time_interval="1minute", right="call")
                if(os.path.isfile(path_call)==False):
                    continue

                if(os.path.isfile(path_put)==False):
                    print("extracting data")
                    historical_data.get_option_historical_data(start_date = (date) + "T09:15:00.000Z", end_date = (date) + "T15:30:00.000Z", expiry = str(expiry) + "T07:00:00.000Z", strike = strike_put, stock_code="CNXBAN", time_interval="1minute", right="put")
                if(os.path.isfile(path_put)==False):
                    continue

                with open(path_call, "rb") as file:
                    # Go to the end of the file before the last break-line
                    file.seek(2) 
                    # Keep reading backward until you find the next break-line
                    while file.read(1) != b'\n':
                        file.seek(2, os.SEEK_CUR) 
                    first_line_call = file.readline().decode()

                    # Go to the end of the file before the last break-line
                    file.seek(-2, os.SEEK_END) 
                    # Keep reading backward until you find the next break-line
                    while file.read(1) != b'\n':
                        file.seek(-2, os.SEEK_CUR) 
                    last_line_call = file.readline().decode()
                first_line_call = first_line_call.split(',')
                last_line_call = last_line_call.split(',')

                with open(path_put, "rb") as file:
                    # Go to the end of the file before the last break-line
                    file.seek(2) 
                    # Keep reading backward until you find the next break-line
                    while file.read(1) != b'\n':
                        file.seek(2, os.SEEK_CUR) 
                    first_line_put = file.readline().decode()

                    # Go to the end of the file before the last break-line
                    file.seek(-2, os.SEEK_END) 
                    # Keep reading backward until you find the next break-line
                    while file.read(1) != b'\n':
                        file.seek(-2, os.SEEK_CUR) 
                    last_line_put = file.readline().decode()
                first_line_put = first_line_put.split(',')
                last_line_put = last_line_put.split(',')

                inv_1, pr_1, prbr_1 = main_pcopp(path_call, path_put, lookback=12, max_investment=5000, lot_size=25, sl=True, stoploss=25, target_orders = True, brokerage=35, allow_short=False, std_mult = std_mult)
                inv_2, pr_2, prbr_2 = main_pcopp(path_put, path_call, lookback=12, max_investment=5000, lot_size=25, sl=True, stoploss=25, target_orders = True, brokerage=35, allow_short=False, std_mult = std_mult)
                #print([strike_call, first_line_call[11], last_line_call[11], strike_put, first_line_put[11], last_line_put[11], inv_1, pr_1, prbr_1, inv_2, pr_2, prbr_2])
                df.append([date, abs(bank_nifty_strike - strike_call), strike_call, first_line_call[11], last_line_call[11], strike_put, first_line_put[11], last_line_put[11], inv_1, inv_2, pr_1, pr_2, prbr_1, prbr_2])
                strikes_profit_callput[i] += pr_1
                strikes_profit_brk_callput[i] += prbr_1
                strikes_profit_putcall[i] += pr_2
                strikes_profit_brk_putcall[i] += prbr_2
                strikes_inv_callput[i] += inv_1/no_of_days
                strikes_inv_putcall[i] += inv_2/no_of_days

        for i in range(no_of_strikes + 1):
            df.append([0, i*100, 0, 0, 0, 0, 0, 0, strikes_inv_callput[i], strikes_inv_putcall[i], strikes_profit_callput[i], strikes_profit_putcall[i], strikes_profit_brk_callput[i], strikes_profit_brk_putcall[i]])
            #df_averages.append(["putcall opposites", str(expiry), i*100, strikes_profit_callput[i], strikes_profit_putcall[i]])

        df = pd.DataFrame(df, columns=["Date", "Difference from banknifty", "Call strike", "Call open", "Call close", "Put strike", "Put open", "Put close", "Investment callput", "Investment putcall", "Profit callput", "Profit putcall", "Profits-brokerage callput", "Profits-brokerage putcall"])
        df.to_csv(dire + 'pcopp' + name + str(expiry) + '.csv')

#        strikes_profit_callput = []
#        strikes_profit_putcall = []
#        strikes_profit_brk_callput = []
#        strikes_profit_brk_putcall = []
#        strikes_inv_callput = []
#        strikes_inv_putcall = []
#        for i in range(no_of_strikes + 1):
#            strikes_profit_callput.append(0)
#            strikes_profit_putcall.append(0)
#            strikes_profit_brk_callput.append(0)
#            strikes_profit_brk_putcall.append(0)
#            strikes_inv_callput.append(0)
#            strikes_inv_putcall.append(0)
#
#        df = []
#        for j in range(len(dates)):
#            for i in range(no_of_strikes + 1):
#                strike_call = strikes_call[j*(no_of_strikes + 1) + i]
#                strike_put = strikes_put[j*(no_of_strikes + 1) + i]
#                date = dates[j]
#                bank_nifty_strike = strikes_call[j*(no_of_strikes + 1)]
#                path_call = '/home/mgoel/Documents/quant_algos/Data/CNXBAN_options_' + str(expiry) + '_call' + str(strike_call) + '_1minute' + (date) + 'T07:00:00.csv'
#                path_put = '/home/mgoel/Documents/quant_algos/Data/CNXBAN_options_' + str(expiry) + '_put' + str(strike_put) + '_1minute' + (date) + 'T07:00:00.csv'
#
#                if(os.path.isfile(path_call)==False):
#                    print("extracting data")
#                    historical_data.get_option_historical_data(start_date = (date) + "T07:00:00.000Z", end_date = (date) + "T18:00:00.000Z", expiry = str(expiry) + "T07:00:00.000Z", strike = strike_call, stock_code="CNXBAN", time_interval="1minute", right="call")
#                if(os.path.isfile(path_call)==False):
#                    continue
#
#                if(os.path.isfile(path_put)==False):
#                    print("extracting data")
#                    historical_data.get_option_historical_data(start_date = (date) + "T07:00:00.000Z", end_date = (date) + "T18:00:00.000Z", expiry = str(expiry) + "T07:00:00.000Z", strike = strike_put, stock_code="CNXBAN", time_interval="1minute", right="put")
#                if(os.path.isfile(path_put)==False):
#                    continue
#
#                with open(path_call, "rb") as file:
#                    # Go to the end of the file before the last break-line
#                    file.seek(2) 
#                    # Keep reading backward until you find the next break-line
#                    while file.read(1) != b'\n':
#                        file.seek(2, os.SEEK_CUR) 
#                    first_line_call = file.readline().decode()
#
#                    # Go to the end of the file before the last break-line
#                    file.seek(-2, os.SEEK_END) 
#                    # Keep reading backward until you find the next break-line
#                    while file.read(1) != b'\n':
#                        file.seek(-2, os.SEEK_CUR) 
#                    last_line_call = file.readline().decode()
#                first_line_call = first_line_call.split(',')
#                last_line_call = last_line_call.split(',')
#
#                with open(path_put, "rb") as file:
#                    # Go to the end of the file before the last break-line
#                    file.seek(2) 
#                    # Keep reading backward until you find the next break-line
#                    while file.read(1) != b'\n':
#                        file.seek(2, os.SEEK_CUR) 
#                    first_line_put = file.readline().decode()
#
#                    # Go to the end of the file before the last break-line
#                    file.seek(-2, os.SEEK_END) 
#                    # Keep reading backward until you find the next break-line
#                    while file.read(1) != b'\n':
#                        file.seek(-2, os.SEEK_CUR) 
#                    last_line_put = file.readline().decode()
#                first_line_put = first_line_put.split(',')
#                last_line_put = last_line_put.split(',')
#
#                inv_1, pr_1, prbr_1 = main_normal(path_call, path_put, lookback=12, max_investment=5000, lot_size=25, sl=True, stoploss=25, target_orders = True, brokerage=35, allow_short=False, std_mult = std_mult)
#                inv_2, pr_2, prbr_2 = main_normal(path_put, path_call, lookback=12, max_investment=5000, lot_size=25, sl=True, stoploss=25, target_orders = True, brokerage=35, allow_short=False, std_mult = std_mult)
#                #print([strike_call, first_line_call[11], last_line_call[11], strike_put, first_line_put[11], last_line_put[11], inv_1, pr_1, prbr_1, inv_2, pr_2, prbr_2])
#                df.append([date, abs(bank_nifty_strike - strike_call), strike_call, first_line_call[11], last_line_call[11], strike_put, first_line_put[11], last_line_put[11], inv_1, inv_2, pr_1, pr_2, prbr_1, prbr_2])
#                strikes_profit_callput[i] += pr_1
#                strikes_profit_brk_callput[i] += prbr_1
#                strikes_profit_putcall[i] += pr_2
#                strikes_profit_brk_putcall[i] += prbr_2
#                strikes_inv_callput[i] += inv_1/no_of_days
#                strikes_inv_putcall[i] += inv_2/no_of_days
#
#        for i in range(no_of_strikes + 1):
#            df.append([0, i*100, 0, 0, 0, 0, 0, 0, strikes_inv_callput[i], strikes_inv_putcall[i], strikes_profit_callput[i], strikes_profit_putcall[i], strikes_profit_brk_callput[i], strikes_profit_brk_putcall[i]])
#            #df_averages.append(["normal", str(expiry), i*100, strikes_profit_callput[i], strikes_profit_putcall[i]])
#
#        df = pd.DataFrame(df, columns=["Date", "Difference from banknifty", "Call strike", "Call open", "Call close", "Put strike", "Put open", "Put close", "Investment callput", "Investment putcall", "Profit callput", "Profit putcall", "Profits-brokerage callput", "Profits-brokerage putcall"])
#        df.to_csv(dire + 'normal' + name + str(expiry) + '.csv')
#
#    #df_averages = pd.DataFrame(df_averages, columns=["type", "expiry", "Strikes", "callput profits", "putcall profits"])
#    #df_averages.to_csv('/home/mgoel/Documents/quant_algos/bollinger_bands/tests_modified/Averages' + name + '.csv')

'''
strikes_70_call = []
strikes_70_put = []
strikes_30_call = []
strikes_30_put = []
strikes_100_call = []
strikes_100_put = []

for date in dates:
    min_diff_70_call = 70000
    strike_70_call = 41000
    min_diff_30_call = 70000
    strike_30_call = 41000
    min_diff_100_call = 70000
    strike_100_call = 41000

    min_diff_70_put = 70000
    strike_70_put = 41000
    min_diff_30_put = 70000
    strike_30_put = 41000
    min_diff_100_put = 70000
    strike_100_put = 41000

    
    for strike in range(41000, 46100, 100):
        path = '/home/mgoel/Documents/quant_algos/Data/CNXBAN_options_' + str(expiry) + '_call' + str(strike) + '_1minute' + (date) + 'T07:00:00.csv'
        if(os.path.isfile(path)==False):
            print("extracting data")
            #historical_data.get_option_historical_data(start_date = (date) + "T07:00:00.000Z", end_date = (date) + "T18:00:00.000Z", expiry = str(expiry) + "T07:00:00.000Z", strike = strike, stock_code="CNXBAN", time_interval="1minute", right="call")
        if(os.path.isfile(path)==False):
            continue
        with open(path, "rb") as file:
            # Go to the end of the file before the last break-line
            file.seek(2) 
            # Keep reading backward until you find the next break-line
            while file.read(1) != b'\n':
                file.seek(2, os.SEEK_CUR) 
            last_line = file.readline().decode()

        last_line = last_line.split(',')

        if(abs(float(last_line[11]) - 70) < min_diff_70_call):
            min_diff_70_call = abs(float(last_line[11]) - 70) 
            strike_70_call = strike
        if(abs(float(last_line[11]) - 30) < min_diff_30_call):
            min_diff_30_call = abs(float(last_line[11]) - 30) 
            strike_30_call = strike
        if(abs(float(last_line[11]) - 100) < min_diff_100_call):
            min_diff_100_call = abs(float(last_line[11]) - 100) 
            strike_100_call = strike

        

        path = '/home/mgoel/Documents/quant_algos/Data/CNXBAN_options_' + str(expiry) + '_put' + str(strike) + '_1minute' + (date) + 'T07:00:00.csv'
        if(os.path.isfile(path)==False):
            print("extracting data")
            #historical_data.get_option_historical_data(start_date = (date) + "T07:00:00.000Z", end_date = (date) + "T18:00:00.000Z", expiry = str(expiry) + "T07:00:00.000Z", strike = strike, stock_code="CNXBAN", time_interval="1minute", right="put")
        if(os.path.isfile(path)==False):
            continue
        with open(path, "rb") as file:
            # Go to the end of the file before the last break-line
            file.seek(2) 
            # Keep reading backward until you find the next break-line
            while file.read(1) != b'\n':
                file.seek(2, os.SEEK_CUR) 
            last_line = file.readline().decode()

        last_line = last_line.split(',')

        if(abs(float(last_line[11]) - 70) < min_diff_70_put):
            min_diff_70_put = abs(float(last_line[11]) - 70) 
            strike_70_put = strike
        if(abs(float(last_line[11]) - 30) < min_diff_30_put):
            min_diff_30_put = abs(float(last_line[11]) - 30) 
            strike_30_put = strike
        if(abs(float(last_line[11]) - 100) < min_diff_100_put):
            min_diff_100_put = abs(float(last_line[11]) - 100) 
            strike_100_put = strike
    
    strikes_70_call.append(strike_70_call)
    strikes_30_call.append(strike_30_call)
    strikes_100_call.append(strike_100_call)

    strikes_70_put.append(strike_70_put)
    strikes_30_put.append(strike_30_put)
    strikes_100_put.append(strike_100_put)

print(strikes_70_call)
print(strikes_30_call)
print(strikes_100_call)
print(strikes_70_put)
print(strikes_30_put)
print(strikes_100_put)
#strikes_70_call = [45000, 44900, 44700, 44500, 44400]
#strikes_70_put = [42500, 42600, 42600, 42600, 42900]
#strikes_70_call = [44700,44600,44900,45100,44800,44700,44600,44500,44400,44100]
#strikes_70_put = [41700, 41700,42100,42500,42500,42900,43000,43300,43500,43500]
df_70 = []
for i in range(len(dates)):
    strike_call = strikes_70_call[i]
    strike_put = strikes_70_put[i]
    date = dates[i]
    path_call = '/home/mgoel/Documents/quant_algos/Data/CNXBAN_options_' + str(expiry) + '_call' + str(strike_call) + '_1minute' + (date) + 'T07:00:00.csv'
    path_put = '/home/mgoel/Documents/quant_algos/Data/CNXBAN_options_' + str(expiry) + '_put' + str(strike_put) + '_1minute' + (date) + 'T07:00:00.csv'
    with open(path_call, "rb") as file:
        # Go to the end of the file before the last break-line
        file.seek(2) 
        # Keep reading backward until you find the next break-line
        while file.read(1) != b'\n':
            file.seek(2, os.SEEK_CUR) 
        first_line_call = file.readline().decode()

        # Go to the end of the file before the last break-line
        file.seek(-2, os.SEEK_END) 
        # Keep reading backward until you find the next break-line
        while file.read(1) != b'\n':
            file.seek(-2, os.SEEK_CUR) 
        last_line_call = file.readline().decode()
    first_line_call = first_line_call.split(',')
    last_line_call = last_line_call.split(',')

    with open(path_put, "rb") as file:
        # Go to the end of the file before the last break-line
        file.seek(2) 
        # Keep reading backward until you find the next break-line
        while file.read(1) != b'\n':
            file.seek(2, os.SEEK_CUR) 
        first_line_put = file.readline().decode()

        # Go to the end of the file before the last break-line
        file.seek(-2, os.SEEK_END) 
        # Keep reading backward until you find the next break-line
        while file.read(1) != b'\n':
            file.seek(-2, os.SEEK_CUR) 
        last_line_put = file.readline().decode()
    first_line_put = first_line_put.split(',')
    last_line_put = last_line_put.split(',')

    inv_1, pr_1, prbr_1 = main(path_call, path_put, lookback=12, max_investment=5000, lot_size=25, sl=True, stoploss=25, target_orders = True, brokerage=35, allow_short=False)
    inv_2, pr_2, prbr_2 = main(path_put, path_call, lookback=12, max_investment=5000, lot_size=25, sl=True, stoploss=25, target_orders = True, brokerage=35, allow_short=False)
    #print([strike_call, first_line_call[11], last_line_call[11], strike_put, first_line_put[11], last_line_put[11], inv_1, pr_1, prbr_1, inv_2, pr_2, prbr_2])
    df_70.append([strike_call, first_line_call[11], last_line_call[11], strike_put, first_line_put[11], last_line_put[11], inv_1, inv_2, pr_1, pr_2, prbr_1, prbr_2])

df = pd.DataFrame(df_70, index = dates, columns=["Call strike", "Call open", "Call close", "Put strike", "Put open", "Put close", "Investment callput", "Investment putcall", "Profit callput", "Profit putcall", "Profits-brokerage callput", "Profits-brokerage putcall"])
df.to_csv('/home/mgoel/Documents/quant_algos/bollinger_bands/tests/tests_70_putcall_' + str(expiry) + '.csv')

#strikes_30_call = [45500, 45300, 45100, 45000, 44700]
#strikes_30_put = [41700, 41900, 42000, 41800, 42100]
#strikes_30_call = [45300,45200,45400,45500,45200,45100,44900,44700,44600,44300]
#strikes_30_put = [40500,40700,41100,41500,41800,42300,42500,42800,43100,43200]

df_70 = []
for i in range(len(dates)):
    strike_call = strikes_30_call[i]
    strike_put = strikes_30_put[i]
    date = dates[i]
    path_call = '/home/mgoel/Documents/quant_algos/Data/CNXBAN_options_' + str(expiry) + '_call' + str(strike_call) + '_1minute' + (date) + 'T07:00:00.csv'
    path_put = '/home/mgoel/Documents/quant_algos/Data/CNXBAN_options_' + str(expiry) + '_put' + str(strike_put) + '_1minute' + (date) + 'T07:00:00.csv'
    with open(path_call, "rb") as file:
        # Go to the end of the file before the last break-line
        file.seek(2) 
        # Keep reading backward until you find the next break-line
        while file.read(1) != b'\n':
            file.seek(2, os.SEEK_CUR) 
        first_line_call = file.readline().decode()

        # Go to the end of the file before the last break-line
        file.seek(-2, os.SEEK_END) 
        # Keep reading backward until you find the next break-line
        while file.read(1) != b'\n':
            file.seek(-2, os.SEEK_CUR) 
        last_line_call = file.readline().decode()
    first_line_call = first_line_call.split(',')
    last_line_call = last_line_call.split(',')

    with open(path_put, "rb") as file:
        # Go to the end of the file before the last break-line
        file.seek(2) 
        # Keep reading backward until you find the next break-line
        while file.read(1) != b'\n':
            file.seek(2, os.SEEK_CUR) 
        first_line_put = file.readline().decode()

        # Go to the end of the file before the last break-line
        file.seek(-2, os.SEEK_END) 
        # Keep reading backward until you find the next break-line
        while file.read(1) != b'\n':
            file.seek(-2, os.SEEK_CUR) 
        last_line_put = file.readline().decode()
    first_line_put = first_line_put.split(',')
    last_line_put = last_line_put.split(',')
    inv_1, pr_1, prbr_1 = main(path_call, path_put, lookback=12, max_investment=5000, lot_size=25, sl=True, stoploss=25, target_orders = True, brokerage=35, allow_short=False)
    inv_2, pr_2, prbr_2 = main(path_put, path_call, lookback=12, max_investment=5000, lot_size=25, sl=True, stoploss=25, target_orders = True, brokerage=35, allow_short=False)
    #print([strike_call, first_line_call[11], last_line_call[11], strike_put, first_line_put[11], last_line_put[11], inv_1, pr_1, prbr_1, inv_2, pr_2, prbr_2])
    df_70.append([strike_call, first_line_call[11], last_line_call[11], strike_put, first_line_put[11], last_line_put[11], inv_1, inv_2, pr_1, pr_2, prbr_1, prbr_2])

df = pd.DataFrame(df_70, index = dates, columns=["Call strike", "Call open", "Call close", "Put strike", "Put open", "Put close", "Investment callput", "Investment putcall", "Profit callput", "Profit putcall", "Profits-brokerage callput", "Profits-brokerage putcall"])
df.to_csv('/home/mgoel/Documents/quant_algos/bollinger_bands/tests/tests_30_putcall_' + str(expiry) + '.csv')

#strikes_100_call = [45500, 45500, 45000, 45000, 44900, 44800, 44700, 44600, 44400, 44200]
#strikes_100_put = [41800, 42100, 42100, 42500, 42500, 42800, 42900, 42800, 42900, 43000]
#strikes_100_call = [44800, 44700, 44600, 44400, 44200]
#strikes_100_put = [42800, 42900, 42800, 42900, 43000]
#strikes_100_call = [44500,44400,44700,44900,44600,44600,44400,44300,44200,44000]
#strikes_100_put = [42000,42100,42400,42800,42800,43200,43200,43500,43600,43600]

df_70 = []
for i in range(len(dates)):
    strike_call = strikes_100_call[i]
    strike_put = strikes_100_put[i]
    date = dates[i]
    path_call = '/home/mgoel/Documents/quant_algos/Data/CNXBAN_options_' + str(expiry) + '_call' + str(strike_call) + '_1minute' + (date) + 'T07:00:00.csv'
    path_put = '/home/mgoel/Documents/quant_algos/Data/CNXBAN_options_' + str(expiry) + '_put' + str(strike_put) + '_1minute' + (date) + 'T07:00:00.csv'
    with open(path_call, "rb") as file:
        # Go to the end of the file before the last break-line
        file.seek(2) 
        # Keep reading backward until you find the next break-line
        while file.read(1) != b'\n':
            file.seek(2, os.SEEK_CUR) 
        first_line_call = file.readline().decode()

        # Go to the end of the file before the last break-line
        file.seek(-2, os.SEEK_END) 
        # Keep reading backward until you find the next break-line
        while file.read(1) != b'\n':
            file.seek(-2, os.SEEK_CUR) 
        last_line_call = file.readline().decode()
    first_line_call = first_line_call.split(',')
    last_line_call = last_line_call.split(',')

    with open(path_put, "rb") as file:
        # Go to the end of the file before the last break-line
        file.seek(2) 
        # Keep reading backward until you find the next break-line
        while file.read(1) != b'\n':
            file.seek(2, os.SEEK_CUR) 
        first_line_put = file.readline().decode()

        # Go to the end of the file before the last break-line
        file.seek(-2, os.SEEK_END) 
        # Keep reading backward until you find the next break-line
        while file.read(1) != b'\n':
            file.seek(-2, os.SEEK_CUR) 
        last_line_put = file.readline().decode()
    first_line_put = first_line_put.split(',')
    last_line_put = last_line_put.split(',')

    inv_1, pr_1, prbr_1 = main(path_call, path_put, lookback=12, max_investment=3000, lot_size=25, sl=True, stoploss=25, target_orders = True, brokerage=35, allow_short=False)
    inv_2, pr_2, prbr_2 = main(path_put, path_call, lookback=12, max_investment=3000, lot_size=25, sl=True, stoploss=25, target_orders = True, brokerage=35, allow_short=False)
    #print([strike_call, first_line_call[11], last_line_call[11], strike_put, first_line_put[11], last_line_put[11], inv_1, pr_1, prbr_1, inv_2, pr_2, prbr_2])
    df_70.append([strike_call, first_line_call[11], last_line_call[11], strike_put, first_line_put[11], last_line_put[11], inv_1, inv_2, pr_1, pr_2, prbr_1, prbr_2])

df = pd.DataFrame(df_70, index = dates, columns=["Call strike", "Call open", "Call close", "Put strike", "Put open", "Put close", "Investment callput", "Investment putcall", "Profit callput", "Profit putcall", "Profits-brokerage callput", "Profits-brokerage putcall"])
df.to_csv('/home/mgoel/Documents/quant_algos/bollinger_bands/tests/tests_100_putcall_' + str(expiry) + '.csv')
'''