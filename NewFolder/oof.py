###    BACKTESTING CODE   ###
# Should accept the strategy as a function which takes in the df as an input and returns the orders list
# The orders list should be of the form [[pnl, buy_time, sell_time],...] for each trade every day

# imports
import numpy as np
import pandas as pd
import math
from datetime import datetime, timedelta
import os
import sys
sys.path.insert(1, '../breeze')
import historical_data

def update_history(history, current_price):
    for i in range(len(history) - 1):
      history[i] = history[i + 1]
    history[-1] = current_price
    return history

class fixed_strike_strategy_class:
    # Initiaization
    weights = []
    total_orders = 0
    time = 0
    order_qty = 0
    net_pnl = 0
    avg_array = []
    history = []
    my_orders = {}
    orders_list = []    # [order pnl, order buy time, order sell time]

    #### Hyperparameters ####
    max_order_qty = 1
    target_margin = 1.1
    stoploss_margin = 0.9
    c_std = 4
    ##########################

    def __init__(self, strike, date, expiry, action) -> None:
        # Initialisation
        temp = np.arange(-30,0,2)
        temp = temp/15    ##  This can be a parameter
        temp = np.flip(temp)
        temp = np.exp(temp)
        self.weights = temp
        print(self.weights)

        self.strike = strike
        self.date = date
        self.expiry = expiry
        self.action = action

        pass

    def buy_condition(self, curr_price, history, order_qty):
      if curr_price > np.ma.average(np.array(history), weights = self.weights) + self.c_std*np.std(np.array(history)) and curr_price <= 1.1*history[-1] and order_qty < self.max_order_qty:
        return True
      else:
        return False
        
    def update_target_sl(self, order, curr_price_time, pnl, order_qty):
        # new_target = 0
        # new_stoploss = 0
        old_target = order[1]
        old_stoploss = order[2]
        flag = order[4]

        if flag:
          if curr_price_time[0] > old_target:
            print(f'Order bought at {order[0]} has been executed at {curr_price_time[0]} and premium gained: {curr_price_time[0] - order[0]}')
            pnl += curr_price_time[0] - order[0]
            self.orders_list.append([curr_price_time[0] - order[0], order[3], curr_price_time[1], order[5], curr_price_time[2]])  # [order pnl, order buy time, order sell time, real buy time, real sell time]
            flag = False
            order_qty -= 1
            return [order[0],old_target, old_stoploss, order[3], flag, order[5], curr_price_time[2]], pnl, order_qty


          if curr_price_time[0] < old_stoploss:
            if old_stoploss - order[0] > 0:
              print(f'Order at {order[0]} has been executed at {curr_price_time[0]} and premium gained: {curr_price_time[0] - order[0]}')
              # pass
            else:
              print(f'Order at {order[0]} has been executed at {curr_price_time[0]} and premium lost: {curr_price_time[0] - order[0]}')
              # pass

            pnl += curr_price_time[0] - order[0]
            self.orders_list.append([curr_price_time[0] - order[0], order[3], curr_price_time[1], order[5], curr_price_time[2]])
            flag = False
            order_qty -= 1
            return [order[0],old_target, old_stoploss, order[3], flag, order[5], curr_price_time[2]], pnl, order_qty

          decay_factor = (5/100)*math.exp(-(curr_price_time[1] - order[3])/20) # Linearly vary between 0.1% to 1% between 1 sec to 30 sec (in %)

          if curr_price_time[1] - order[3] < 20 and curr_price_time[0]*(1+5*decay_factor) > old_target and flag == True:
            decay_factor = (1/100)*math.exp(-(curr_price_time[1] - order[3])/5) # Linearly vary between 0.1% to 1% between 1 sec to 30 sec (in %)
            new_target = (1+decay_factor)*old_target
            new_stoploss = (1-decay_factor)*curr_price_time[0]
            # return [order[0],new_target, new_stoploss, curr_price_time[1], flag], pnl, order_qty
          elif curr_price_time[1] - order[3] < 20 and curr_price_time[0]*(1+5*decay_factor) < old_target and flag == True:
            decay_factor = (1/100)*math.exp(-(curr_price_time[1] - order[3])/5) # Linearly vary between 0.1% to 1% between 1 sec to 30 sec (in %)
            new_target = (1-decay_factor)*old_target
            new_stoploss = (1+decay_factor)*old_stoploss
            if new_stoploss > curr_price_time[0]:
              new_stoploss = (1-decay_factor)*curr_price_time[0]
            # return [order[0],new_target, new_stoploss, curr_price_time[1], flag], pnl, order_qty
          else:
            new_target = old_target
            new_stoploss = old_stoploss

          return [order[0],new_target, new_stoploss, order[3], flag, order[5], order[6]], pnl, order_qty
    
    def on_ticks(self, ticks):
      curr_price = float(ticks['close'])
      real_time = ticks['datetime'][-8:]
      time += 1

      if(time<=15):
          self.history.append(curr_price)
          return
      
      if self.buy_condition(curr_price, self.history, self.order_qty):
        strike_price_order = curr_price
        target = self.target_margin*curr_price
        stoploss = self.stoploss_margin*curr_price
        self.order_qty += 1
        self.total_orders += 1
        self.my_orders[curr_price] = [strike_price_order, target, stoploss, time, True, real_time, 0] # Values {order_price, target, SL, order_time, active_order_flag, buy_real_time, real_sell_time}

      order_copy = self.my_orders.copy()
      if len(self.my_orders)>0:
        for i in self.my_orders.keys():
          if order_copy[i][4]:
            order_copy[i], self.net_pnl, self.order_qty = self.update_target_sl(self.my_orders[i],[curr_price,time, real_time], self.net_pnl, self.order_qty)
            if len(self.my_orders) == 0:
              break
      self.my_orders = order_copy.copy()
      self.history = update_history(self.history, curr_price)

    def square_off_all(self, curr_price, time, real_time):
      for i in self.my_orders.keys():
        if self.my_orders[i][4]:
          self.my_orders[i][4] = False
          self.orders_list.append([self.my_orders[i][0] - curr_price, self.my_orders[i][3], time, self.my_orders[i][5], real_time])
          self.net_pnl += self.my_orders[i][0] - curr_price
          self.order_qty -= 1   # Selling
          # del self.my_orders[i]

    # def start_data_stream(self):
    #   path = 'Data/CNXBAN' + '_options_' + self.expiry[:4] + '_' + self.expiry[5:7] + '_' + self.expiry[8:10] + '_' + self.action + str(int(self.strike)) + '_1second' + self.date[:4] + '_' + self.date[5:7] + '_' + self.date[8:10] + '.csv'
    #   if(os.path.isfile(path)==False):
    #     historical_data.get_option_historical_data(start_date = str(self.date) + "T09:30:00.000Z", end_date = str(self.date) + "T15:30:00.000Z", stock_code="CNXBAN", expiry=self.expiry, strike=str(int(self.strike)), right=self.action, time_interval="1second")
    #     if(os.path.isfile(path)==False):
    #       self.expiry = (datetime.strptime(self.expiry, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
    #       historical_data.get_option_historical_data(start_date = str(self.date) + "T09:30:00.000Z", end_date = str(self.date) + "T15:30:00.000Z", stock_code="CNXBAN", expiry=self.expiry, strike=str(int(self.strike)), right=self.action, time_interval="1second")
    #       if(os.path.isfile(path)==False):
    #         self.expiry = (datetime.strptime(self.expiry, "%Y-%m-%d") - timedelta(days=2)).strftime("%Y-%m-%d")
    #         historical_data.get_option_historical_data(start_date = str(self.date) + "T09:30:00.000Z", end_date = str(self.date) + "T15:30:00.000Z", stock_code="CNXBAN", expiry=self.expiry, strike=str(int(self.strike)), right=self.action, time_interval="1second")
    #         if(os.path.isfile(path)==False):
    #           print("No data for call for expiry", self.expiry, "and date", self.date, "and strike", str(int(self.strike)))
    #           return
    #   df = pd.read_csv(path)
    #   for idx, data in df.iterrows():
    #     self.on_ticks(df.iloc[idx])
    #   eod = df.iloc[-1]['datetime'][-8:]
    #   self.square_off_all(float(df.iloc[-1]['close']), self.time, eod)
    #   print("Done for strike", self.strike, "and date", self.date, "and expiry", self.expiry)
    #   print("Total orders placed:", self.total_orders, "and net pnl:", self.net_pnl)
    #   return self.orders_list

    def get_orders_list(self):
      return self.orders_list
    


## Now define the actual backtesting function which runs the strategy class object
