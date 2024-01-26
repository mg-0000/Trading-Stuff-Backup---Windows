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
sys.path.insert(1, '../support')
from dates import *
import historical_data
import time
import threading

# def keep_api_active():
#   while True:
#     time.sleep(240)
#     historical_data.breeze.get_funds()
# t1 = threading.Thread(target=keep_api_active)
# t1.start()

def update_history(history, current_price):
    for i in range(len(history) - 1):
      history[i] = history[i + 1]
    history[-1] = current_price
    return history

class fixed_strike_strategy_class:

    # Initialisation
    temp = np.arange(-30,0,2)
    temp = temp/15    ##  This can be a parameter
    temp = np.flip(temp)
    temp = np.exp(temp)
    weights = temp

    #### Hyperparameters ####
    max_order_qty = 1
    target_margin = 1.1
    stoploss_margin = 0.9
    c_std = 5
    max_loss = 100
    ##########################

    def __init__(self, strike, date, expiry, action) -> None:
        
        self.strike = strike
        self.date = date
        self.expiry = expiry
        self.action = action

        self.total_orders = 0
        self.time = 0
        self.order_qty = 0
        self.net_pnl = 0
        self.avg_array = []
        self.history = []
        self.my_orders = {}
        self.orders_list = []  

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
            # if(curr_price_time[1] - order[3]>10):
            print(f'TARGET HIT Order bought at {order[0]} has been executed at {curr_price_time[0]} and premium gained: {curr_price_time[0] - order[0]}')
            pnl += curr_price_time[0] - order[0]
            self.orders_list.append([curr_price_time[0] - order[0], order[3], curr_price_time[1], order[5], curr_price_time[2]])  # [order pnl, order buy time, order sell time, real buy time, real sell time]
            flag = False
            order_qty -= 1
            return [order[0],old_target, old_stoploss, order[3], flag, order[5], curr_price_time[2]], pnl, order_qty


          if curr_price_time[0] < old_stoploss:
            # if old_stoploss - order[0] > 0:
              # if(curr_price_time[1] - order[3]>10):
              # print(f'STOPLOSS HIT Order at {order[0]} has been executed at {curr_price_time[0]} and premium gained: {curr_price_time[0] - order[0]}')
              # pass
            # else:
              # if(curr_price_time[1] - order[3]>10):
              # print(f'STOPLOSS HIT Order at {order[0]} has been executed at {curr_price_time[0]} and premium lost: {curr_price_time[0] - order[0]}')
              # pass

            if order[5]=="09:35:00":
              print("Shouldnt happen", order)

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
      self.time += 1

      if(len(self.history)<=14):
          self.history.append(curr_price)
          return
      
      if self.buy_condition(curr_price, self.history, self.order_qty):
        strike_price_order = curr_price
        target = self.target_margin*curr_price
        stoploss = self.stoploss_margin*curr_price
        self.order_qty += 1
        self.total_orders += 1
        self.my_orders[curr_price] = [strike_price_order, target, stoploss, self.time, True, real_time, 0] # Values {order_price, target, SL, order_time, active_order_flag, buy_real_time, real_sell_time}
        # print("Placing buy order",self.my_orders[curr_price])

      order_copy = self.my_orders.copy()
      if len(self.my_orders)>0:
        for i in self.my_orders.keys():
          if order_copy[i][4]:
            order_copy[i], self.net_pnl, self.order_qty = self.update_target_sl(self.my_orders[i],[curr_price,self.time, real_time], self.net_pnl, self.order_qty)
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
          print("Squaring off at time", real_time, 'for profit', self.my_orders[i][0] - curr_price)
          # del self.my_orders[i]

    def get_orders_list(self):
      return self.orders_list, self.net_pnl, self.total_orders
    
    def get_pnl(self):
      return self.net_pnl
    
    def get_total_orders(self):
      return self.total_orders
    
    def get_open_orders(self):
      return_list = []
      for order_key in self.my_orders.keys():
        if self.my_orders[order_key][4]==True:
          return_list.append(self.my_orders[order_key])
      return return_list
    


## Now define the actual backtesting function which runs the strategy class object
class fixed_date_run_test:
  max_loss = -25

  def __init__(self, date, expiry, stock, action) -> None:
    self.date = date
    self.stock = stock
    self.expiry = expiry
    self.action = action
    self.orders_list = []
    self.fixed_strike_strategy_objects = []
    self.pnl = 0
    self.total_orders = 0

  def get_banknifty_data(self):
    path = 'Data/' + self.stock + '_5minute' + self.date[:4] + '_' + self.date[5:7] + '_' + self.date[8:10] + '.csv'
    if(os.path.isfile(path)==False):
      historical_data.get_equity_historical_data(start_date = str(self.date) + "T09:30:00.000Z", end_date = str(self.date) + "T15:30:00.000Z", stock_code=self.stock, time_interval="5minute")
      if(os.path.isfile(path)==False):
          print("No data for date", self.date)
          return 0
    
    return path
    
  def get_option_data(self, strike, action):
    path = 'Data/CNXBAN' + '_options_' + self.expiry[:4] + '_' + self.expiry[5:7] + '_' + self.expiry[8:10] + '_' + action + str(int(strike)) + '_1second' + self.date[:4] + '_' + self.date[5:7] + '_' + self.date[8:10] + '.csv'
    if(os.path.isfile(path)==False):
      historical_data.get_option_historical_data(start_date = str(self.date) + "T09:30:00.000Z", end_date = str(self.date) + "T15:30:00.000Z", stock_code="CNXBAN", expiry=self.expiry, strike=str(int(strike)), right=action, time_interval="1second")
      if(os.path.isfile(path)==False):
        self.expiry = (datetime.strptime(self.expiry, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
        historical_data.get_option_historical_data(start_date = str(self.date) + "T09:30:00.000Z", end_date = str(self.date) + "T15:30:00.000Z", stock_code="CNXBAN", expiry=self.expiry, strike=str(int(strike)), right=action, time_interval="1second")
        path = 'Data/CNXBAN' + '_options_' + self.expiry[:4] + '_' + self.expiry[5:7] + '_' + self.expiry[8:10] + '_' + action + str(int(strike)) + '_1second' + self.date[:4] + '_' + self.date[5:7] + '_' + self.date[8:10] + '.csv'
        if(os.path.isfile(path)==False):
          self.expiry = (datetime.strptime(self.expiry, "%Y-%m-%d") - timedelta(days=2)).strftime("%Y-%m-%d")
          historical_data.get_option_historical_data(start_date = str(self.date) + "T09:30:00.000Z", end_date = str(self.date) + "T15:30:00.000Z", stock_code="CNXBAN", expiry=self.expiry, strike=str(int(strike)), right=action, time_interval="1second")
          path = 'Data/CNXBAN' + '_options_' + self.expiry[:4] + '_' + self.expiry[5:7] + '_' + self.expiry[8:10] + '_' + action + str(int(strike)) + '_1second' + self.date[:4] + '_' + self.date[5:7] + '_' + self.date[8:10] + '.csv'
          time.sleep(50)
          if(os.path.isfile(path)==False):
            print("No data for call for expiry", self.expiry, "and date", self.date, "and strike", str(int(strike)))
            return 0
    return path
  
  def get_spot(self, time):
    path = self.get_banknifty_data()
    if(path==0):
      return 0
    df = pd.read_csv(path)
    closest_time = time
    # Get closest 30 minute
    if int(time[-5:-3])<15:
      closest_time = str(int(time[:2])) + ":00:00"
    elif int(time[-5:-3])>=15 and int(time[-5:-3])<45 :
      closest_time = str(int(time[:2])) + ":30:00" 
    else:
      if int(time[:2])<10:
        closest_time = "0" + str(int(time[:2])+1) + ":00:00"
      else:
        closest_time = str(int(time[:2])+1) + ":00:00"

    df_indices = df[df['datetime'].str.contains(closest_time)].index[0]

    spot = float(df.iloc[df_indices]['open'])
    if(spot%100>=50):
        spot = (spot//100 + 1)*100
    else:
        spot = (spot//100)*100
    return spot
  
  def get_next_time(self,curr_time):
    if int(curr_time[-5:-3])==00:
      next_time = curr_time[:2] + ":30:00"
    else:
      if int(curr_time[:2]) <9:
        next_time = "0" + str(int(curr_time[:2])+1) + ":00:00"
      else:
        next_time = str(int(curr_time[:2])+1) + ":00:00"
    return next_time
  
  def run_strategy(self):

    time_format = "%H:%M:%S"

    # Initial
    curr_time = "09:35:00"
    next_time = self.get_next_time("09:30:00")
    end_time = "15:24:00"

    spot = self.get_spot(curr_time)
    prev_spot = spot
    if(spot==0):
      print("No data")
      return 0
        
    self.fixed_strike_strategy_objects.append(fixed_strike_strategy_class(spot, self.date, self.expiry, self.action))
    data_path = self.get_option_data(spot, self.action)
    if data_path == 0:
      return 0
    df = pd.read_csv(data_path)

    print("This should be zero ", self.fixed_strike_strategy_objects[-1].net_pnl)

    to_break = False
    now_time = curr_time
    while datetime.strptime(now_time, time_format) < datetime.strptime(end_time, time_format) and to_break==False:

      spot = self.get_spot(curr_time)
      
      if(prev_spot!=spot):

        _, old_pnl, old_tot_orders = self.fixed_strike_strategy_objects[-1].get_orders_list()
        self.fixed_strike_strategy_objects[-1].square_off_all(float(df.iloc[i]['close']), self.fixed_strike_strategy_objects[-1].time, now_time)
        order_list, pnl, tot_orders = self.fixed_strike_strategy_objects[-1].get_orders_list()

        # self.orders_list.extend(order_list) 
        self.pnl += pnl - old_pnl
        self.total_orders += tot_orders - old_tot_orders
        self.fixed_strike_strategy_objects.append(fixed_strike_strategy_class(spot, self.date, self.expiry, self.action))

        print("Profit in this leg:", pnl, "Total profit", self.pnl, "Total orders in this leg:", tot_orders)

        prev_spot = spot

        try:
          data_path = self.get_option_data(spot, self.action)
        except:
          time.sleep(65)
          data_path = self.get_option_data(spot, self.action)
        if data_path == 0:
          break
        df = pd.read_csv(data_path)
      
      while (len(df[df['datetime'].str.contains(curr_time)].index)==0):
        curr_time = (datetime.strptime(curr_time, time_format) + timedelta(minutes=1)).strftime(time_format)
      i = df[df['datetime'].str.contains(curr_time)].index[0]
      
      while datetime.strptime(now_time, time_format) < datetime.strptime(next_time, time_format) and datetime.strptime(now_time, time_format) < datetime.strptime(end_time, time_format):
        
        old_pnl = self.fixed_strike_strategy_objects[-1].get_pnl()
        old_tot_orders = self.fixed_strike_strategy_objects[-1].get_total_orders()
        self.fixed_strike_strategy_objects[-1].on_ticks(df.iloc[i])
        new_pnl = self.fixed_strike_strategy_objects[-1].get_pnl()
        new_tot_orders = self.fixed_strike_strategy_objects[-1].get_total_orders()
        
        self.pnl += new_pnl - old_pnl
        self.total_orders += new_tot_orders - old_tot_orders
        
        now_time = df.iloc[i]['datetime'][-8:]
        
        if(self.pnl<self.max_loss):
          print("Hit Max Loss at pnl", self.pnl, self.max_loss)
          _, old_pnl, old_tot_orders = self.fixed_strike_strategy_objects[-1].get_orders_list()
          self.fixed_strike_strategy_objects[-1].square_off_all(float(df.iloc[i]['close']),self.fixed_strike_strategy_objects[-1].time, now_time)
          order_list, pnl, tot_orders = self.fixed_strike_strategy_objects[-1].get_orders_list()
          self.pnl += pnl - old_pnl
          self.total_orders += tot_orders - old_tot_orders
          print("Hit Max Loss at pnl", self.pnl)
          to_break = True
          break
        
        
        i = i + 1
      
      if(next_time != "15:30:00"):
        curr_time = next_time
        next_time = self.get_next_time(curr_time)
      else:
        curr_time = next_time

    print("Sqaring off at eod. CUrrent pnl is ", self.pnl)
    for strat in self.fixed_strike_strategy_objects:
      _, old_pnl, old_tot_orders = strat.get_orders_list()
      strat.square_off_all(float(df.iloc[i]['close']), strat.time, now_time)
      order_list, pnl, tot_orders = strat.get_orders_list()
      self.orders_list.extend(order_list)
      self.pnl += pnl - old_pnl
      self.total_orders += tot_orders - old_tot_orders
    print("Sqaring off at eod. New pnl is ", self.pnl)
  
  def get_pnl(self):
    return self.pnl
  
  def get_total_orders(self):
    return self.total_orders
  
  def get_orders_list(self):
    # print(self.orders_list)
    return_list = []
    for order in self.orders_list:
      tmp = [self.date, self.action]
      tmp.extend(order)
      return_list.append(tmp)
    return return_list


start_date = "2023-11-23"
end_date = "2024-01-24"
first_expiry = "2023-11-29"

# start_date = "2024-01-11"
# end_date = "2024-01-11"
# first_expiry = "2024-01-17"

weekday_dates = get_weekday_dates(start_date, end_date)
expiry_dates = get_expiry_dates(weekday_dates, first_expiry)
print(weekday_dates)

results = []
orders_dict = {}
orders_lists = []
for i in range(len(weekday_dates)):
  date = weekday_dates[i]
  expiry = expiry_dates[i]

  test = fixed_date_run_test(date, expiry, "CNXBAN", "put")
  test.run_strategy()
  put_pnl = test.get_pnl()
  put_orders = test.get_total_orders()
  results.append(['Put', date, put_orders, put_pnl])
  orders_dict[str(date + " put")] = test.get_orders_list()
  # print(test.get_orders_list())
  # orders_lists.extend(test.get_orders_list())
  orders_lists += test.get_orders_list()
  # print(test.get_orders_list())
  print("Date:", date, " PUT. Orders:", put_orders, "Net Pnl:", put_pnl, len(orders_lists))

  del test

  test2 = fixed_date_run_test(date, expiry, "CNXBAN", "call")
  test2.run_strategy()
  call_pnl = test2.get_pnl()
  call_orders = test2.get_total_orders()
  results.append(['Call', date, call_orders, call_pnl])
  orders_dict[str(date + " call")] = test2.get_orders_list()
  # print(test2.get_orders_list())
  # orders_lists.extend(test2.get_orders_list())
  orders_lists += test2.get_orders_list()
  # print(test2.get_orders_list())
  print("Date:", date, " CALL. Orders:", call_orders, "Net Pnl:", call_pnl, len(orders_lists)) 

  del test2

  output_file = open("live_output_2.txt", "w")
  output_file.write("results = " + str(results) + '\n')
  output_file.close()

  # orders_lists_df = pd.DataFrame(orders_lists, columns = ['Date', 'Type', 'PnL', 'Buy Time', 'Sell Time', 'Real Buy Time', 'Real Sell Time'])
  # orders_lists_df.to_csv("orders_lists_2.csv")

  # time.sleep(50)

# results = pd.DataFrame(results, columns = ['Type', 'Date', 'Orders', 'Net Pnl'])
output_file = open("live_output_2.txt", "w")
output_file.write("results = " + str(results) + '\n')
output_file.close()

orders_lists_df = pd.DataFrame(orders_lists, columns = ['Date', 'Type', 'PnL', 'Buy Time', 'Sell Time', 'Real Buy Time', 'Real Sell Time'])
orders_lists_df.to_csv("orders_lists_2.csv", index=False)

print("results = ", results)