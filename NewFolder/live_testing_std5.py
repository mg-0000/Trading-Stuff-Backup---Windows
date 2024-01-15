import pandas as pd
import numpy as np
import math
from datetime import datetime, timedelta
import pytz
import sys
import os
sys.path.insert(1, '../breeze')
sys.path.insert(1, '../support')
from dates import *
import historical_data

def get_metrics(file):
  # Initialisation

  global weights, total_orders, time, order_qty, net_pnl, new_pnl, avg_array, history, my_orders

  temp = np.arange(-30,0,2)
  temp = temp/15    ##  This can be a parameter
  temp = np.flip(temp)
  temp = np.exp(temp)
  weights = temp
  # print(weights)

  total_orders = 0
  time = 0
  order_qty = 0
  net_pnl = 0
  new_pnl = 0
  avg_array = []
  history = []
  my_orders = {}

  def update_target_sl(order, curr_price_time, pnl, order_qty):
    # new_target = 0
    # new_stoploss = 0
    old_target = order[1]
    old_stoploss = order[2]
    flag = order[4]

    global new_pnl, total_orders

    if curr_price_time[1] - order[3] < 10 and flag == True and (curr_price_time[0] <= old_stoploss or curr_price_time[0] >= old_target):
      flag = False
      return [order[0],old_target, old_stoploss, order[3], flag], pnl, order_qty
    elif curr_price_time[1] - order[3] == 10 and flag == True and (curr_price_time[0] < 1.02*order[0] and curr_price_time[0] > 0.98*order[0]):
      flag = False
      return [order[0],old_target, old_stoploss, order[3], flag], pnl, order_qty
    elif curr_price_time[1] - order[3] == 10 and flag == True and (curr_price_time[0] > old_stoploss and curr_price_time[0] < old_target):
      flag = True
      order_qty += 1
      total_orders += 1
      order[0] = curr_price_time[0] 

    if flag:
      if curr_price_time[0] > old_target:
        if(curr_price_time[1] - order[3] > 10):
          # print("After time, target hit")
          new_pnl += curr_price_time[0] - order[0]
        print(f'Order bought at {order[0]} has been executed at {curr_price_time[0]} and premium gained: {curr_price_time[0] - order[0]}')
        pnl += curr_price_time[0] - order[0]
        flag = False
        order_qty -= 1
        return [order[0],old_target, old_stoploss, order[3], flag], pnl, order_qty


      if curr_price_time[0] < old_stoploss:
        if(curr_price_time[1] - order[3] > 10):
          new_pnl += curr_price_time[0] - order[0]
          # print("After time, stoploss hit")
        # print(str(curr_price_time)+'L')
        if old_stoploss - order[0] > 0:
          print(f'Order at {order[0]} has been executed at {curr_price_time[0]} and premium gained: {curr_price_time[0] - order[0]}')
          # pass
        else:
          print(f'Order at {order[0]} has been executed at {curr_price_time[0]} and premium lost: {curr_price_time[0] - order[0]}')
          # pass

        pnl += curr_price_time[0] - order[0]
        flag = False
        order_qty -= 1
        return [order[0],old_target, old_stoploss, order[3], flag], pnl, order_qty

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
        # print('Order Unchanged')

      return [order[0],new_target, new_stoploss, order[3], flag], pnl, order_qty

  def update_history(history, current_price):
    for i in range(len(history) - 1):
      history[i] = history[i + 1]
    history[-1] = current_price
    return history
  
  def on_ticks(ticks):
    global time
    global history
    global order_qty
    global total_orders
    global my_orders
    global net_pnl
    global avg_array

    curr_price = float(ticks['close'])
    # print("Price = ", curr_price)

    time += 1
    # print("Current Price :"+ str(curr_price))
    if(time<=15):
      history.append(curr_price)
      # print("Initial", len(history), "ticks")
      return

    if curr_price > np.ma.average(np.array(history), weights = weights) + c_std*np.std(np.array(history)) and curr_price <= 1.1*history[-1] and order_qty < max_order_qty:
      # print('buy call at ',curr_price,'with target ', target_margin*curr_price,'and stoploss',stoploss_margin*curr_price,'at time',time)
      strike_price_order = curr_price
      target = target_margin*curr_price
      stoploss = stoploss_margin*curr_price
      my_orders[curr_price] = [strike_price_order, target, stoploss, time, True, False] # Values {order_price, target, SL, order_time, active_order_flag, buy_trigger_flag}
      # order_qty += 1
      # total_orders += 1
      ###
      # order_copy = my_orders.copy()
      # if(len(my_orders)>0):
      #   for i in my_orders.keys():
      #     if order_copy[i][4]:
      #       order_copy[i][3] = time
      # my_orders = order_copy.copy()
      ###

    order_copy = my_orders.copy()
    if len(my_orders)>0:
      for i in my_orders.keys():
        if order_copy[i][4]:
          order_copy[i], net_pnl, order_qty = update_target_sl(my_orders[i],[curr_price,time], net_pnl, order_qty)
          if order_copy[i][3] == False:
            del my_orders[i]
          if len(my_orders) == 0:
            break
    my_orders = order_copy.copy()
    history = update_history(history, curr_price)

  #### Hyperparameters ####

  max_order_qty = 1
  target_margin = 1.1
  stoploss_margin = 0.9
  c_std = 4

  ##########################

  df_calls = pd.read_csv(file)

  for idx, data in df_calls.iterrows():
    on_ticks(df_calls.iloc[idx])

  # Square off at EOD
  eod_price = float(df_calls.iloc[-1]['close'])
  for order_key in my_orders.keys():
    if my_orders[order_key][4]:
      net_pnl += eod_price - my_orders[order_key][0]
      my_orders[order_key][4] = False

  # avg_array = np.array(avg_array)
  # print(my_orders)
  print("Total Orders placed:", total_orders)
  print(f'Net PnL:',net_pnl)
  # print(f'New PnL:', new_pnl)

  return total_orders, net_pnl

# ---- All Files ---- #
import os

## New strike price
def get_spot_price(stock, date):
  path = 'Data/' + stock + '_30minute' + date[:4] + '_' + date[5:7] + '_' + date[8:10] + '.csv'
  # print(path)
  next_date = (datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
  if(os.path.isfile(path)==False):
      historical_data.get_equity_historical_data(start_date = str(date) + "T09:30:00.000Z", end_date = str(date) + "T15:30:00.000Z", stock_code=stock, time_interval="30minute")
      if(os.path.isfile(path)==False):
          print("No data for date", date)
          return 0
  df = pd.read_csv(path)
  # spot = float(df.iloc[:]['open'].mean())
  spot = float(df.iloc[0]['open'])

  # spot =  44800

  if(spot%100>=50):
      spot = (spot//100 + 1)*100
  else:
      spot = (spot//100)*100

  # print(spot)
  return spot

return_list = []

start_dates = '2024-01-09'
end_dates = '2024-01-15'
first_expiry = '2024-01-10'

weekday_dates = get_weekday_dates(start_dates, end_dates)
expiry_dates = get_expiry_dates(weekday_dates, first_expiry)

print(weekday_dates)

for i in range(len(weekday_dates)):
  date = weekday_dates[i]
  expiry = expiry_dates[i]
  mean_spot = get_spot_price("CNXBAN", date)
  if(mean_spot==0):
    continue
  path = 'Data/CNXBAN' + '_options_' + expiry[:4] + '_' + expiry[5:7] + '_' + expiry[8:10] + '_call' + str(int(mean_spot)) + '_1second' + date[:4] + '_' + date[5:7] + '_' + date[8:10] + '.csv'
  if(os.path.isfile(path)==False):
    historical_data.get_option_historical_data(start_date = str(date) + "T09:30:00.000Z", end_date = str(date) + "T15:30:00.000Z", stock_code="CNXBAN", expiry=expiry, strike=str(int(mean_spot)), right="call", time_interval="1second")
    path = 'Data/CNXBAN' + '_options_' + expiry[:4] + '_' + expiry[5:7] + '_' + expiry[8:10] + '_call' + str(int(mean_spot)) + '_1second' + date[:4] + '_' + date[5:7] + '_' + date[8:10] + '.csv'
    if(os.path.isfile(path)==False):
      expiry = (datetime.strptime(expiry, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
      historical_data.get_option_historical_data(start_date = str(date) + "T09:30:00.000Z", end_date = str(date) + "T15:30:00.000Z", stock_code="CNXBAN", expiry=expiry, strike=str(int(mean_spot)), right="call", time_interval="1second")
      path = 'Data/CNXBAN' + '_options_' + expiry[:4] + '_' + expiry[5:7] + '_' + expiry[8:10] + '_call' + str(int(mean_spot)) + '_1second' + date[:4] + '_' + date[5:7] + '_' + date[8:10] + '.csv'
      if(os.path.isfile(path)==False):
        expiry = (datetime.strptime(expiry, "%Y-%m-%d") - timedelta(days=2)).strftime("%Y-%m-%d")
        historical_data.get_option_historical_data(start_date = str(date) + "T09:30:00.000Z", end_date = str(date) + "T15:30:00.000Z", stock_code="CNXBAN", expiry=expiry, strike=str(int(mean_spot)), right="call", time_interval="1second")
        path = 'Data/CNXBAN' + '_options_' + expiry[:4] + '_' + expiry[5:7] + '_' + expiry[8:10] + '_call' + str(int(mean_spot)) + '_1second' + date[:4] + '_' + date[5:7] + '_' + date[8:10] + '.csv'
        if(os.path.isfile(path)==False):
          print("No data for call for expiry", expiry, "and date", date, "and strike", str(int(mean_spot)))
          continue
  orders, pnl = get_metrics(path)
  return_list.append(["Call", date,orders, pnl])
  print("For CALL Expiry:", expiry, "Date:", date, "Orders:", orders, "PnL:", pnl)

  path = 'Data/CNXBAN' + '_options_' + expiry[:4] + '_' + expiry[5:7] + '_' + expiry[8:10] + '_put' + str(int(mean_spot)) + '_1second' + date[:4] + '_' + date[5:7] + '_' + date[8:10] + '.csv'
  if(os.path.isfile(path)==False):
    historical_data.get_option_historical_data(start_date = str(date) + "T09:30:00.000Z", end_date = str(date) + "T15:30:00.000Z", stock_code="CNXBAN", expiry=expiry, strike=str(int(mean_spot)), right="put", time_interval="1second")
    path = 'Data/CNXBAN' + '_options_' + expiry[:4] + '_' + expiry[5:7] + '_' + expiry[8:10] + '_put' + str(int(mean_spot)) + '_1second' + date[:4] + '_' + date[5:7] + '_' + date[8:10] + '.csv'
    if(os.path.isfile(path)==False):
      expiry = (datetime.strptime(expiry, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
      historical_data.get_option_historical_data(start_date = str(date) + "T09:30:00.000Z", end_date = str(date) + "T15:30:00.000Z", stock_code="CNXBAN", expiry=expiry, strike=str(int(mean_spot)), right="put", time_interval="1second")
      path = 'Data/CNXBAN' + '_options_' + expiry[:4] + '_' + expiry[5:7] + '_' + expiry[8:10] + '_put' + str(int(mean_spot)) + '_1second' + date[:4] + '_' + date[5:7] + '_' + date[8:10] + '.csv'
      if(os.path.isfile(path)==False):
        expiry = (datetime.strptime(expiry, "%Y-%m-%d") - timedelta(days=2)).strftime("%Y-%m-%d")
        historical_data.get_option_historical_data(start_date = str(date) + "T09:30:00.000Z", end_date = str(date) + "T15:30:00.000Z", stock_code="CNXBAN", expiry=expiry, strike=str(int(mean_spot)), right="put", time_interval="1second")
        path = 'Data/CNXBAN' + '_options_' + expiry[:4] + '_' + expiry[5:7] + '_' + expiry[8:10] + '_put' + str(int(mean_spot)) + '_1second' + date[:4] + '_' + date[5:7] + '_' + date[8:10] + '.csv'
        if(os.path.isfile(path)==False):
          print("No data for put for expiry", expiry, "and date", date, " and strike", str(int(mean_spot)))
          continue
  orders, pnl = get_metrics(path)
  return_list.append(["Put", date, orders, pnl])
  print("For PUT Expiry:", expiry, "Date:", date, "Orders:", orders, "PnL:", pnl)

  # Save return_list to a file output.txt
  with open('output.txt', 'w') as f:
    for item in return_list:
      f.write("%s," % item)

print("return_list =", return_list)