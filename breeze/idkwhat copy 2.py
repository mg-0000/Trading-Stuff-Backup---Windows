# Main thread:
# - Use websocket to get live data 
# - run the update_target_sl function
#
# Thread 1:
# - Place new orders
#
# Thread 2:
# - Get the limit-rates based on the fixed stoploss using the live data


### Yet to do
# Threadify the on_ticks function

import datetime
import numpy as np
import pandas as pd
import requests
import json
import hashlib
import base64 
import socketio
from datetime import datetime
import threading
import math
import time as tp
from decimal import Decimal

from breeze_import import api_key_2 as api_key
from breeze_import import api_secret_2 as api_secret
from breeze_import import session_token_2 as session_token
from breeze_import import breeze_2 as breeze
from get_session_key import get_key
from get_stock_token import get_token

todays_date_format1 = "16-Jan-2024"
strike = 48100
right_format1 = "CE"  #"PE" for put
right_format2 = "call"
sltp_expiry = "17-Jan-2024"
expiry = "2024-01-17T16:00:00.000Z"
sltp_stock = "CNXBAN"
stock = "CNXBAN"
validity_date = "2024-01-10T16:00:00.000Z"

# Initialisation

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
avg_array = []
history = []
my_orders = {}
curr_price = 0
limit_rate_calculated = 0
stop_threads = False

#### Hyperparameters ####

max_order_qty = 1
target_margin = 1.1
stoploss_margin = 0.9
c_std = 5

##########################

websocket_session_key = get_key(session_token, api_key)

payload = json.dumps({})
time_stamp = datetime.utcnow().isoformat()[:19] + '.000Z'
checksum = hashlib.sha256((time_stamp+payload+api_secret).encode("utf-8")).hexdigest()
headers = {
    'Content-Type': 'application/json',
    'X-Checksum': 'token ' + checksum,
    'X-Timestamp': time_stamp,
    'X-AppKey': api_key,
    'X-SessionToken': session_token
}

tmp = requests.get('https://api.icicidirect.com/breezeapi/api/v1/funds', headers=headers, data=payload)

user_id, temp_session_token = base64.b64decode(websocket_session_key.encode('ascii')).decode('ascii').split(":")
sio = socketio.Client()
script_code = "4.1!" + str(get_token(sltp_expiry, int(strike), right_format1)) 
# script_code = "4.1!1594" #Subscribe more than one stock at a time
channel_name = 'stock'
print("Script Code:", script_code)
auth = {"user": user_id, "token": temp_session_token} 
sio.connect("https://livestream.icicidirect.com", headers={"User-Agent":"python-socketio[client]/socket"}, 
                auth=auth, transports="websocket", wait_timeout=3)
tux_to_user_value = dict()

print(breeze.get_funds())

def parse_data_simple(data):
    if data and type(data) == list and len(data) > 0 and type(data[0]) == str and "!" not in data[0]:
        order_dict = {}
        order_dict["messageTime"] = data[8] 
        return 0, order_dict    # The '0' is for 'dont proceed'
    data_dict = {"last": data[2]}
    data_dict["close"] = data[22]
    data_dict["ltt"] = datetime.fromtimestamp(
                data[21]).strftime('%c')
    return 1, data_dict   # The '1' is for 'proceed'

def round_nearest(n):
  tmp = n*10 - int(n*10)
  # tmp = int(n*100)
  # print(tmp,round(n,1))
  if(tmp < 0.25):
    return round(round(n,1),2)
  elif(tmp < 0.5):
    return round(round(n,1) + 0.05,2)
  elif(tmp < 0.75):
    return round(round(n,1) - 0.05,2)
  else:
    return round(n,1) 

def get_limit_rate(sltp):
  if(sltp>= 60.05):
     temp = 0.95*sltp
  elif(sltp>= 30.05):
     temp = 0.82*sltp
  elif(sltp>= 20.05):
     temp = 0.8*sltp
  elif(sltp>= 15.05):
     temp = 0.6*sltp
  elif(sltp>= 10.05):
     temp = 0.4*sltp
  else:
     temp = 0
  return round_nearest(temp)

def update_history(history, current_price):
  for i in range(len(history) - 1):
    history[i] = history[i + 1]
  history[-1] = current_price
  return history

def update_thread():
  global my_orders, net_pnl, order_qty
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

def update_target_sl(order, curr_price_time, pnl, order_qty):
  # new_target = 0
  # new_stoploss = 0
  old_target = order[1]
  old_stoploss = order[2]
  flag = order[4]

  if flag:
    if curr_price_time[0] > old_target:
      # Place sell order
      order_time = datetime.now()
      try:
        fresh_order = breeze.modify_order(order_id=order[6],
                  exchange_code="NFO",
                  order_type="market",
                  stoploss="0",
                  quantity=str(15),
                  price="0",
                  validity="Day",
                  disclosed_quantity="0",
                  validity_date=validity_date)
      except Exception as error:
        # handle the exception
        print("An exception occurred while selling:", error)
      fresh_order_id = fresh_order["Success"]["order_id"]
      # detail = breeze.get_order_detail('NFO',fresh_order_id)
      print(f'Order bought at {order[0]} has been executed at {curr_price_time[0]} and premium gained: {curr_price_time[0] - order[0]}')
      pnl += curr_price_time[0] - order[0]
      flag = False
      order_qty -= 1
      return [order[0],old_target, old_stoploss, order[3], flag, order[5], order[6], fresh_order_id], pnl, order_qty


    if curr_price_time[0] < old_stoploss:
      # Place sell order
      order_time = datetime.now()
      try:
        fresh_order = breeze.modify_order(order_id=order[6],
                  exchange_code="NFO",
                  order_type="market",
                  stoploss="0",
                  quantity=str(15),
                  price="0",
                  validity="Day",
                  disclosed_quantity="0",
                  validity_date=validity_date)
      except Exception as error:
        # handle the exception
        print("An exception occurred while selling:", error)
      fresh_order_id = fresh_order["Success"]["order_id"]
      # detail = breeze.get_order_detail('NFO',fresh_order_id)
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
      return [order[0],old_target, old_stoploss, order[3], flag, order[5], order[6], fresh_order_id], pnl, order_qty

    decay_factor = (5/100)*math.exp(-(curr_price_time[1] - order[3])/10) # Linearly vary between 0.1% to 1% between 1 sec to 30 sec (in %)

    if curr_price_time[1] - order[3] < 10 and curr_price_time[0]*(1+5*decay_factor) > old_target and flag == True:
    # if curr_price_time[0]*(1+5*decay_factor) > old_target and flag == True:
      decay_factor = (5/100)*math.exp(-(curr_price_time[1] - order[3])/10) # Linearly vary between 0.1% to 1% between 1 sec to 30 sec (in %)
      new_target = (1+decay_factor)*old_target
      new_stoploss = (1-decay_factor)*curr_price_time[0]
      print(f'Updated Order from Old:[TGT:{old_target} and SL:[{old_stoploss}] to'+ \
      f' NEW:[TGT:{new_target} and SL:[{new_stoploss}]')
      # return [order[0],new_target, new_stoploss, curr_price_time[1], flag, order[5], order[6]], pnl, order_qty
    elif curr_price_time[1] - order[3] < 10 and curr_price_time[0]*(1+5*decay_factor) < old_target and flag == True:
    # elif curr_price_time[0]*(1+5*decay_factor) < old_target and flag == True:
      decay_factor = (5/100)*math.exp(-(curr_price_time[1] - order[3])/10) # Linearly vary between 0.1% to 1% between 1 sec to 30 sec (in %)
      new_target = (1-decay_factor)*old_target
      new_stoploss = (1+decay_factor)*old_stoploss
      if new_stoploss > curr_price_time[0]:
        new_stoploss = (1-decay_factor)*curr_price_time[0]
      print(f'Updated Order from Old:[TGT:{old_target} and SL:[{old_stoploss}] to'+ \
      f' NEW:[TGT:{new_target} and SL:[{new_stoploss}]')
      # return [order[0],new_target, new_stoploss, curr_price_time[1], flag, order[5], order[6]], pnl, order_qty
    else:
      new_target = old_target
      new_stoploss = old_stoploss
      print('Order Unchanged')

    return [order[0],new_target, new_stoploss, order[3], flag, order[5], order[6]], pnl, order_qty

def start_websocket():
  print("Getting live data")
  sio.emit('join', script_code)
  sio.on(channel_name, on_ticks)

def stop_websocket():
  stop_threads = True
  print("Time's up!")
  # Print the pnl and orders and stuff
  print("Net pnl:", net_pnl)
  print("Orders", my_orders)
  print("total orders:", total_orders)   
  sio.emit("leave", script_code)
  sio.emit("disconnect", "transport close")

# CallBack functions to receive feeds
def on_ticks(ticks):
    global sio
    global curr_price
    global time
    global history
    global order_qty
    global total_orders
    global my_orders
    global net_pnl
    global stop_threads
    global limit_rate_calculated

    now = datetime.now()
    if(now.hour == 15 and now.minute >= 24):
        stop_websocket()
        return

    # print("here")
    # print(ticks)
    go_ahead, ticks = parse_data_simple(ticks)
    if(go_ahead==0):
       print("No go!", ticks)
       return
    curr_price = float(ticks['last'])
    sltp_price = round_nearest(stoploss_margin*curr_price)
    limit_rate_calculated = get_limit_rate(sltp = sltp_price) 
    time += 1
    # print("Current Price :", str(curr_price), "and the limit rate is", limit_rate_calculated, "and the sltp is", sltp_price)
    print("Price: ", curr_price, int(ticks['ltt'][-7:-5]) - int(now.second))

    # If too much delay in live data
    if(int(now.second)!=0 and int(now.second)!=1 and int(now.second)!=59 and int(now.second)!=58 and int(ticks['ltt'][-7:-5]) - int(now.second) <= -3):
        # stop_threads = True
        # print("Delay in live data, restarting websocket", ticks['ltt'], now)
        # sio.emit("leave", script_code)
        # sio.emit("disconnect", "transport close")
        # sio.emit('join', script_code)
        # sio.on(channel_name, on_ticks)
        stop_websocket()
        tp.sleep(1)
        start_websocket()
        # return
    
    if(time<=15):
        history.append(curr_price)
        print("Initial", len(history), "ticks")
        return
    
    # Check for a new buy order
    if curr_price > np.ma.average(np.array(history), weights = weights) + c_std*np.std(np.array(history)) and order_qty < max_order_qty:
        # Place buy order
        fresh_order = (breeze.place_order(stock_code=str(stock),
                        exchange_code="NFO",
                        product="optionplus",
                        action="buy",
                        order_type="market",    ##
                        stoploss=str(sltp_price),
                        quantity=str(15),     # Stoploss trigger price
                        price=str(limit_rate_calculated),   # Stoploss limit price
                        validity="day",
                        validity_date=str(validity_date),
                        disclosed_quantity="0",
                        expiry_date=str(expiry),
                        right=str(right_format2),
                        strike_price=str(strike),
                        order_type_fresh = "market",
                        order_rate_fresh = "",
                        user_remark="Placing Order"))
        print('buy call at ',curr_price,'with target ', target_margin*curr_price,'and stoploss',sltp_price,'at time',time)
        if(fresh_order["Error"]!='None'):
            strike_price_order = curr_price
            target = target_margin*curr_price
            stoploss = stoploss_margin*curr_price
            try:
                fresh_order_id = fresh_order["Success"]["order_id"]
            except:
                print(fresh_order, limit_rate_calculated)
                return
            detail = breeze.get_order_detail('NFO',fresh_order_id)
            cover_order_id = detail['Success'][0]['parent_order_id']
            my_orders[curr_price] = [strike_price_order, target, stoploss, time, True, fresh_order_id, cover_order_id]
            order_qty += 1
            total_orders += 1
            ###
            # order_copy = my_orders.copy()
            # if(len(my_orders)>0):
            #   for i in my_orders.keys():
            #     if order_copy[i][4]:
            #       order_copy[i][3] = time
            # my_orders = order_copy.copy()
            ###
        else:
           print(fresh_order, limit_rate_calculated)

    # Threads for updateing the target and stoploss
    # order_copy = my_orders.copy()
    # if len(my_orders)>0:
    #     for i in my_orders.keys():
    #         if order_copy[i][4]:
    #             order_copy[i], net_pnl, order_qty = update_target_sl(my_orders[i],[curr_price,time], net_pnl, order_qty)
    #             if order_copy[i][3] == False:
    #                 del my_orders[i]
    #             if len(my_orders) == 0:
    #                 break
    # my_orders = order_copy.copy()
           
    tq = threading.Thread(target=update_thread)
    tq.start()

    # Update history
    history = update_history(history, curr_price)

    # print(ticks, now)

# print("here")
start_websocket()
# print("here")
#Unwatch from the stock
# sio.emit("leave", script_code)
#Disconnect from the server
# sio.emit("disconnect", "transport close")