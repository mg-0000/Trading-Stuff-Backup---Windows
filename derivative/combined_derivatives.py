import pandas as pd
from breeze_connect import BreezeConnect 

import math
import json
import time


import sys
import os
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '/home/mgoel/Documents/quant_algos/breeze')
import historical_data

def get_derivative(current, previous, interval):
    # print(int(float(current) - float(previous)))
    return math.degrees(math.atan((float(current) - float(previous))/(interval)))

class StopLoss:

    def __init__(self, sl = 0.25):
        self.sl = sl

        self.current_price = 0
        self.current_high = 0
        
        return

    def check(self, current_price):
        self.current_price = float(current_price)
        if(self.current_price < self.sl*self.current_high):
            return 1    #stoploss hit
        elif(self.current_price > self.current_high):
            self.current_high = self.current_price
            return 0    #new high
        else:
            return 0    #stoploss not hit

class delta_strategy:
    def __init__(self, trig, right="put") -> None:
        self.price = 0
        self.trig = trig
        self.profit = []
        self.holding = "none"
        self.net_pl = 0
        self.last_buy_price = 0
        self.right = right
        self.no_of_trades = 0
        self.stoploss = StopLoss(0.9)
        pass

    def set_price(self, price):
        self.price = float(price)
        return

    def check_for_buy(self, derivative):
        if(derivative > self.trig):
            return "buy"
        elif(derivative < -1*self.trig):
            return "sell"
        else:
            return "hold"
        return "hold"

    def update_profit(self, order):
        result = {}
        if(order=="buy" and self.holding=="none"):
            self.last_buy_price = self.price
            self.holding = "buy"
            result["trig"] = self.trig
            result["order"]='buy'
            result["price"]= self.price
            result["current holding"]= self.holding
        elif(order=="sell" and self.holding=="buy"):
            self.net_pl += self.price - self.last_buy_price
            self.holding = "none"
            self.no_of_trades += 1
            result["trig"] = self.trig
            result["order"]= 'sell'
            result["price"]= self.price
            result["current holding"]= self.holding
            result["current profit"] = self.net_pl
            # if(self.trig==85 and self.right=="put"):
            #     print(result)
        else:
            result["trig"] = self.trig
            result["order"]= 'none'
            result["price"]= self.price
            result["current holding"]= self.holding
            return 0
        self.profit.append(result)

        return 1

    def check_stoploss(self):
        if(self.holding=="buy"):
            if(self.stoploss.check(self.price)==1):
                self.update_profit("sell")
                return "sell"
            else:
                return "hold"
        else:
            return "hold"

    def upload_data_to_file(self, name):
        #upload the self.profits array to a json file
        with open(name, 'w') as f:
            json.dump(self.profit, f)

#define the objects, with trigs 0.6,0.50.7,0.8,0.9  
strat1_call = delta_strategy(20, "call")
strat2_call = delta_strategy(30, "call")
strat3_call = delta_strategy(40, "call")
strat4_call = delta_strategy(50, "call")
strat5_call = delta_strategy(55, "call")
strat6_call = delta_strategy(60, "call")
strat7_call = delta_strategy(65, "call")
strat8_call = delta_strategy(70, "call")
strat9_call = delta_strategy(75, "call")

strat1_put = delta_strategy(20)
strat2_put = delta_strategy(30)
strat3_put = delta_strategy(40)
strat4_put = delta_strategy(50)
strat5_put = delta_strategy(55)
strat6_put = delta_strategy(60)
strat7_put = delta_strategy(65)
strat8_put = delta_strategy(70)
strat9_put = delta_strategy(75)

def get_derivative_lookback(current, lookback, looks, index):
    if(len(looks)<lookback):
        looks.append(current)
        return 0
    else:
        looks[index[0]] = current
        # print(looks)
        if(index[0] != len(looks) - 1):
            der = get_derivative(current, looks[index[0]+1], lookback)
            # print(current - looks[index+1], ' ', der)
            index[0]+=1
        else:
            der = get_derivative(current, looks[0], lookback)
            # print(current - looks[0], ' ', der)
            index[0] = 0
        return der

calls = []
puts = []
index_call = [0]
index_put = [0]
# Callback to receive ticks.
def on_ticks(ticks_call, ticks_put, lookback):
    #define the current and last prices
    current = float(ticks_call)
    other = float(ticks_put)
    # if(prev1==-1):
    #     prev1 = current
    #     return
    # if(prev2==-1):
    #     prev2 = prev1
    #     return

    # calculate the derivatives
    # derivative = get_derivative(current, prev2, 2)
    # prev1 = current
    # prev2 = prev1

    derivative = get_derivative_lookback(current, lookback, calls, index_call)
    derivative_put = get_derivative_lookback(other, lookback, puts, index_put)
    # print(index_call[0], ' ', index_put[0])

    # print(int(derivative), " : ", int(derivative_put))

    strat1_call.set_price(current)
    strat2_call.set_price(current)
    strat3_call.set_price(current)
    strat4_call.set_price(current)
    strat5_call.set_price(current)
    strat6_call.set_price(current)
    strat7_call.set_price(current)
    strat8_call.set_price(current)
    strat9_call.set_price(current)
    
    strat1_put.set_price(other)
    strat2_put.set_price(other)
    strat3_put.set_price(other)
    strat4_put.set_price(other)
    strat5_put.set_price(other)
    strat6_put.set_price(other)
    strat7_put.set_price(other)
    strat8_put.set_price(other)
    strat9_put.set_price(other)

    strat1_call.check_stoploss()
    strat2_call.check_stoploss()
    strat3_call.check_stoploss()
    strat4_call.check_stoploss()
    strat5_call.check_stoploss()
    strat6_call.check_stoploss()
    strat7_call.check_stoploss()
    strat8_call.check_stoploss()
    strat9_call.check_stoploss()

    strat1_put.check_stoploss()
    strat2_put.check_stoploss()
    strat3_put.check_stoploss()
    strat4_put.check_stoploss()
    strat5_put.check_stoploss()
    strat6_put.check_stoploss()
    strat7_put.check_stoploss()
    strat8_put.check_stoploss()
    strat9_put.check_stoploss()

    st1 = (strat1_call.check_for_buy(derivative))
    st2 = (strat2_call.check_for_buy(derivative))
    st3 = (strat3_call.check_for_buy(derivative))
    st4 = (strat4_call.check_for_buy(derivative))
    st5 = (strat5_call.check_for_buy(derivative))
    st6 = (strat6_call.check_for_buy(derivative))
    st7 = (strat7_call.check_for_buy(derivative))
    st8 = (strat8_call.check_for_buy(derivative))
    st9 = (strat9_call.check_for_buy(derivative))

    st1_put = (strat1_put.check_for_buy(derivative_put))
    st2_put = (strat2_put.check_for_buy(derivative_put))
    st3_put = (strat3_put.check_for_buy(derivative_put))
    st4_put = (strat4_put.check_for_buy(derivative_put))
    st5_put = (strat5_put.check_for_buy(derivative_put))
    st6_put = (strat6_put.check_for_buy(derivative_put))
    st7_put = (strat7_put.check_for_buy(derivative_put))
    st8_put = (strat8_put.check_for_buy(derivative_put))
    st9_put = (strat9_put.check_for_buy(derivative_put))

    if((st1=="buy" and st1_put=="sell") or (st1=="sell" and st1_put=="buy")):
        strat1_call.update_profit(st1)
        strat1_put.update_profit(st1_put)
    if((st2=="buy" and st2_put=="sell") or (st2=="sell" and st2_put=="buy")):
        strat2_call.update_profit(st2)
        strat2_put.update_profit(st2_put)
    if((st3=="buy" and st3_put=="sell") or (st3=="sell" and st3_put=="buy")):
        strat3_call.update_profit(st3)
        strat3_put.update_profit(st3_put)
    if((st4=="buy" and st4_put=="sell") or (st4=="sell" and st4_put=="buy")):
        strat4_call.update_profit(st4)
        strat4_put.update_profit(st4_put)
    if((st5=="buy" and st5_put=="sell") or (st5=="sell" and st5_put=="buy")):
        strat5_call.update_profit(st5)
        strat5_put.update_profit(st5_put)
    if((st6=="buy" and st6_put=="sell") or (st6=="sell" and st6_put=="buy")):
        strat6_call.update_profit(st6)
        strat6_put.update_profit(st6_put)
    if((st7=="buy" and st7_put=="sell") or (st7=="sell" and st7_put=="buy")):
        strat7_call.update_profit(st7)
        strat7_put.update_profit(st7_put)
    if((st8=="buy" and st8_put=="sell") or (st8=="sell" and st8_put=="buy")):
        strat8_call.update_profit(st8)
        strat8_put.update_profit(st8_put)
    if((st9=="buy" and st9_put=="sell") or (st9=="sell" and st9_put=="buy")):
        strat9_call.update_profit(st9)
        strat9_put.update_profit(st9_put)


def test(ticks):
    print("Ticks:", ticks)

def get_path(stock, expiry, right, strike, date, time_interval):
    return '/home/mgoel/Documents/quant_algos/Data/'+ stock + '_options_' + expiry + '_' + right + str(strike) + '_' + time_interval + str(date) + 'T09:30:00.csv'

def get_data(stock, expiry, right, strike, date, time_interval):
    path = get_path(stock, expiry, right, strike, date, time_interval)
    if(os.path.isfile(path)==False):
        historical_data.get_option_historical_data(start_date = str(date) + "T09:30:00.000Z", end_date = str(date) + "T15:30:00.000Z", expiry = expiry + "T07:00:00.000Z", strike = str(strike), stock_code=stock, time_interval=time_interval, right=right)
    return path

def get_price(stock, expiry, right, strike, date, time_interval, lookback):
    path = get_data(stock, expiry, right, strike, date, time_interval)
    df = pd.read_csv(path)

    if(right=="call"):
        path = get_data(stock, expiry, "put", strike, date, time_interval)
        df2 = pd.read_csv(path)
    else:
        path = get_data(stock, expiry, "call", strike, date, time_interval)
        df2 = pd.read_csv(path)

    for i in range(min(len(df), len(df2))):
         #print(df.iloc[i]['close'],' ', df2.iloc[i]['close'])
        on_ticks(df.iloc[i]['close'], df2.iloc[i]['close'], lookback)
    
    strat1_call.upload_data_to_file("strat1_call.json")
    strat2_call.upload_data_to_file("strat2_call.json")
    strat3_call.upload_data_to_file("strat3_call.json")
    strat4_call.upload_data_to_file("strat4_call.json")
    strat5_call.upload_data_to_file("strat5_call.json")
    strat6_call.upload_data_to_file("strat6_call.json")
    strat7_call.upload_data_to_file("strat7_call.json")
    strat8_call.upload_data_to_file("strat8_call.json")

    print("strat1 call",strat1_call.net_pl, " strat1 put", " no of trades ", strat1_call.no_of_trades, strat1_put.net_pl, " no of trades ", strat1_put.no_of_trades)
    print("strat2 call",strat2_call.net_pl, " strat2 put", " no of trades ", strat2_call.no_of_trades, strat2_put.net_pl, " no of trades ", strat2_put.no_of_trades)
    print("strat3 call",strat3_call.net_pl, " strat3 put", " no of trades ", strat3_call.no_of_trades, strat3_put.net_pl, " no of trades ", strat3_put.no_of_trades)
    print("strat4 call",strat4_call.net_pl, " strat4 put", " no of trades ", strat4_call.no_of_trades, strat4_put.net_pl, " no of trades ", strat4_put.no_of_trades)
    print("strat5 call",strat5_call.net_pl, " strat5 put", " no of trades ", strat5_call.no_of_trades, strat5_put.net_pl, " no of trades ", strat5_put.no_of_trades)
    print("strat6 call",strat6_call.net_pl, " strat6 put", " no of trades ", strat6_call.no_of_trades, strat6_put.net_pl, " no of trades ", strat6_put.no_of_trades)
    print("strat7 call",strat7_call.net_pl, " strat7 put", " no of trades ", strat7_call.no_of_trades, strat7_put.net_pl, " no of trades ", strat7_put.no_of_trades)
    print("strat8 call",strat8_call.net_pl, " strat8 put", " no of trades ", strat8_call.no_of_trades, strat8_put.net_pl, " no of trades ", strat8_put.no_of_trades)
    print("strat9 call",strat9_call.net_pl, " strat9 put", " no of trades ", strat9_call.no_of_trades, strat9_put.net_pl, " no of trades ", strat9_put.no_of_trades)

    

'''
stock = 'CNXBAN'
expiry = '2021-09-30'
right = 'call'
strike = 38000
date = '2021-09-30'
time_interval = '1minute'
'''

def get_spot_price(stock, expiry, right, date, time_interval, lookback = 10):
    path = '/home/mgoel/Documents/quant_algos/Data/' + stock + '_1day' + str(date) + 'T09:30:00.csv'
    if(os.path.isfile(path)==False):
        historical_data.get_equity_historical_data(start_date = str(date) + "T09:30:00.000Z", end_date = str(date) + "T15:30:00.000Z", stock_code=stock, time_interval="1day")
    df = pd.read_csv(path)
    spot = float(df.iloc[0]['open'])

    # spot =  44800

    if(spot%100>=50):
        spot = (spot//100 + 1)*100
    else:
        spot = (spot//100)*100

    print(spot)

    get_price(stock = stock, expiry = expiry, right = right, strike = spot, date = date, time_interval = time_interval, lookback = lookback)

get_spot_price(stock = 'CNXBAN', expiry = '2023-08-24', right = 'call', date = '2023-08-23', time_interval = '1second', lookback = 20)