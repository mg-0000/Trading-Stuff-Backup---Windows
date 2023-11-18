import pandas as pd
from breeze_connect import BreezeConnect 

import math
import json
import time
import datetime


import sys
import os
sys.path.insert(1, 'C:/Users/mridu/Documents/Trading Stuff/breeze')
import historical_data
sys.path.insert(1, 'C:/Users/mridu/Documents/Trading Stuff/Averaging')
sys.path.insert(1, 'C:/Users/mridu/Documents/Trading Stuff/derivative')
sys.path.insert(1, 'C:/Users/mridu/Documents/Trading Stuff/stoploss')
sys.path.insert(1, 'C:/Users/mridu/Documents/Trading Stuff/pnl_book')
from book_v1 import pnl_book
from stoploss import StopLoss
from gaussian import gaussian_mean
from bilateral import bilateral_mean
import derivative_v1 as derivative
        
class backtest:
    # params = [buy_trigs[], exit_trigs[], der_lookback_period, der_interval, averaging_lookback, averaging_sigma1, averaging_sigma2]
    def __init__(self, stock, expiry, date, time_interval, averaging_method, *params) -> None:
        self.stock = stock
        self.expiry = expiry
        self.date = date
        self.time_interval = time_interval
        self.params = params[0]
        self.spot = get_spot_price(self.stock, self.date)

        # derivatives
        self.buy_trigs = self.params[0]
        self.exit_trigs = self.params[1]
        self.der_lookback_period = self.params[2]
        self.der_interval = self.params[3]
        self.call_derivative_onject = derivative.get_derivative(self.der_lookback_period, self.der_interval)
        self.put_derivative_onject = derivative.get_derivative(self.der_lookback_period, self.der_interval)

        # pnl book
        self.calls_book = []
        self.puts_book = []
        for i in range(len(self.params[0])):
            self.calls_book.append(pnl_book("calls"))
            self.puts_book.append(pnl_book("puts"))

        # print(self.params)

        if(averaging_method=="gaussian"):
            self.Call_Averaging = gaussian_mean(self.params[5], self.params[4])
            self.Put_Averaging = gaussian_mean(self.params[5], self.params[4])
        elif(averaging_method=="bilateral"):
            self.Call_Averaging = bilateral_mean(self.params[5], self.params[6], self.params[4])
            self.Put_Averaging = bilateral_mean(self.params[5], self.params[6], self.params[4])
    
    def get_price(self):
        # get the call data
        path_call = get_data(self.stock, self.expiry, "call", self.spot, self.date, self.time_interval)
        df_call = pd.read_csv(path_call)

        # get the put data
        path_put = get_data(self.stock, self.expiry, "put", self.spot, self.date, self.time_interval)
        df_put = pd.read_csv(path_put)

        # return the dataframes
        return [df_call, df_put]

    def on_ticks(self, call_price, put_price):
        # apply the averaging
        averaged_call_price = self.Call_Averaging.get_mean(call_price)
        averaged_put_price = self.Put_Averaging.get_mean(put_price)

        # print(call_price, averaged_call_price)

        call_derivatives = self.call_derivative_onject.update(averaged_call_price)
        put_derivatives = self.put_derivative_onject.update(averaged_put_price)

        # print(call_price, averaged_call_price, self.call_derivative_onject.price_history)

        for i in range(len(self.buy_trigs)):
            # get the orders
            call_order = (derivative.get_order(call_derivatives, self.buy_trigs[i], self.exit_trigs[i]))
            put_order = (derivative.get_order(put_derivatives, self.buy_trigs[i], self.exit_trigs[i]))

            # update the pnl book prices
            self.calls_book[i].update_price(averaged_call_price)
            self.puts_book[i].update_price(averaged_put_price)

            # update the profits
            self.calls_book[i].update_profit(call_order, put_order)
            self.puts_book[i].update_profit(put_order, call_order)

    def backtest(self):
        [df_call, df_put] = self.get_price()
        for i in range(min(len(df_call), len(df_put))):
            self.on_ticks(df_call.iloc[i]['close'], df_put.iloc[i]['close'])
        
    def print_results(self):
        print("Buy Trig | Exit Trig | calls[net pl, no of trades, last holding, holding pnl] | puts[net pl, no of trades, last holding,  holding pnl]]")
        for i in range(len(self.buy_trigs)):
            call_result = self.calls_book[i].get_current_status()
            put_result = self.puts_book[i].get_current_status()

            print(self.buy_trigs[i], '|', self.exit_trigs[i], '|', call_result, '|', put_result)

    def get_results(self):
        calls_results = []
        puts_results = []
        for i in range(len(self.buy_trigs)):
            calls_results.append(self.calls_book[i].get_current_status())
            puts_results.append(self.puts_book[i].get_current_status())
        return [calls_results, puts_results]

def get_path(stock, expiry, right, strike, date, time_interval):
    return 'Data/'+ stock + '_options_' + expiry[:4] + '_' + expiry[5:7] + '_' + expiry[8:10] + '_' + right + str(strike) + '_' + time_interval + date[:4] + '_' + date[5:7] + '_' + date[8:10] + '.csv'

def get_data(stock, expiry, right, strike, date, time_interval):
    path = get_path(stock, expiry, right, strike, date, time_interval)
    # print(path)
    if(os.path.isfile(path)==False):
        historical_data.get_option_historical_data(start_date = str(date) + "T09:30:00.000Z", end_date = str(date) + "T15:30:00.000Z", expiry = expiry + "T07:00:00.000Z", strike = str(strike), stock_code=stock, time_interval=time_interval, right=right)
    return path

def get_spot_price(stock, date):
    path = 'Data/' + stock + '_1day' + date[:4] + '_' + date[5:7] + '_' + date[8:10] + '.csv'
    # print(path)
    next_date = (datetime.datetime.strptime(date, "%Y-%m-%d") + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    if(os.path.isfile(path)==False):
        historical_data.get_equity_historical_data(start_date = str(date) + "T09:30:00.000Z", end_date = str(next_date) + "T15:30:00.000Z", stock_code=stock, time_interval="1day")
    df = pd.read_csv(path)
    spot = float(df.iloc[0]['open'])

    # spot =  44800

    if(spot%100>=50):
        spot = (spot//100 + 1)*100
    else:
        spot = (spot//100)*100

    # print(spot)
    return spot