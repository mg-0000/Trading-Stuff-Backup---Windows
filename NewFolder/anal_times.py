import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Raw file with only 25 per side loss limit
csv_file = "orders_lists_5.csv"
df = pd.read_csv(csv_file)

pos_list_times = []
neg_list_times = []
pos_sell_times = []
neg_sell_times = []
profitable_hold_times = []
lossy_hold_times = []
avg_buy_pnls = {}
avg_sell_pnls = {}
no_buy_pnls = {}
no_sell_pnls = {}
other_pos_times = {}
other_neg_times = {}
sum_times = {}
avg_pnl_wrt_hold_time = {}
no_avg_pnl_wrt_hold_time = {}

def get_half_hour_interval(time):
    time = datetime.strptime(time, '%H:%M:%S')
    half_hour = (time.replace(minute=0, second=0) + timedelta(minutes=30))
    return half_hour

def get_hold_time(order):
    buy_time = datetime.strptime(order['Real Buy Time'], '%H:%M:%S')
    sell_time = datetime.strptime(order['Real Sell Time'], '%H:%M:%S')
    return (sell_time - buy_time).total_seconds()

def get_closest_time(time):
    if int(time[-5:-3])<15:
      closest_time = str(int(time[:2])) + ":00:00"
    elif int(time[-5:-3])>=15 and int(time[-5:-3])<45 :
      closest_time = str(int(time[:2])) + ":30:00" 
    else:
      if int(time[:2])<9:
        closest_time = "0" + str(int(time[:2])+1) + ":00:00"
      else:
        closest_time = str(int(time[:2])+1) + ":00:00"
    return closest_time
    
i = 0
tmp = 0
sum = 0
for idx, row_data in df.iterrows():
    sum += row_data['PnL']
    i+=1
    # if(i<len(df) - 1000):
    #     continue
    
    if(get_hold_time(row_data) not in avg_pnl_wrt_hold_time):
        avg_pnl_wrt_hold_time[get_hold_time(row_data)] = 0
        no_avg_pnl_wrt_hold_time[get_hold_time(row_data)] = 0
    avg_pnl_wrt_hold_time[get_hold_time(row_data)] += row_data['PnL']
    no_avg_pnl_wrt_hold_time[get_hold_time(row_data)] += 1

    if(row_data['PnL'] > 0):
        profitable_hold_times.append(get_hold_time(row_data))
        if(get_closest_time(row_data['Real Buy Time']) not in other_pos_times):
            other_pos_times[get_closest_time(row_data['Real Buy Time'])] = 0
        if(get_closest_time(row_data['Real Buy Time']) not in sum_times):
            sum_times[get_closest_time(row_data['Real Buy Time'])] = 0
        other_pos_times[get_closest_time(row_data['Real Buy Time'])] += 1
    else:
        lossy_hold_times.append(get_hold_time(row_data))
        if(get_closest_time(row_data['Real Buy Time']) not in other_neg_times):
            other_neg_times[get_closest_time(row_data['Real Buy Time'])] = 0
        if(get_closest_time(row_data['Real Buy Time']) not in sum_times):
            sum_times[get_closest_time(row_data['Real Buy Time'])] = 0
        other_neg_times[get_closest_time(row_data['Real Buy Time'])] += 1
    
    sum_times[get_closest_time(row_data['Real Buy Time'])] += 1

    if(get_closest_time(row_data['Real Buy Time']) not in avg_buy_pnls):
        avg_buy_pnls[get_closest_time(row_data['Real Buy Time'])] = 0
        no_buy_pnls[get_closest_time(row_data['Real Buy Time'])] = 0
    if(get_closest_time(row_data['Real Sell Time']) not in avg_sell_pnls):
        avg_sell_pnls[get_closest_time(row_data['Real Sell Time'])] = 0
        no_sell_pnls[get_closest_time(row_data['Real Sell Time'])] = 0
    avg_buy_pnls[get_closest_time(row_data['Real Buy Time'])] += row_data['PnL']
    avg_sell_pnls[get_closest_time(row_data['Real Sell Time'])] += row_data['PnL']
    no_buy_pnls[get_closest_time(row_data['Real Buy Time'])] += 1
    no_sell_pnls[get_closest_time(row_data['Real Sell Time'])] += 1
    # print(row_data['Real Buy Time'], row_data['Real Sell Time'], row_data['PnL'])

for key in other_pos_times:
    other_pos_times[key] /= (sum_times[key])*0.01
for key in other_neg_times:
    other_neg_times[key] /= (sum_times[key])*0.01

for key in avg_buy_pnls:
    avg_buy_pnls[key] /= no_buy_pnls[key]
for key in avg_sell_pnls:
    avg_sell_pnls[key] /= no_sell_pnls[key]

# for key in avg_pnl_wrt_hold_time:
#     avg_pnl_wrt_hold_time[key] /= no_avg_pnl_wrt_hold_time[key]
    
print(sum, len(df))
# print(avg_buy_pnls)
# print(avg_sell_pnls)

plt.bar(list(other_pos_times.keys()), other_pos_times.values(), width=0.8, color='blue')
plt.title("Percentage of Profitable Trades by Buy Time")
plt.xlabel("Buy Time")
plt.ylabel("Number of Trades")
plt.show()

plt.bar(list(other_neg_times.keys()), other_neg_times.values(), width=0.8, color='red')
plt.title("Percentage of Lossy Trades by Buy Time")
plt.xlabel("Buy Time")
plt.ylabel("Number of Trades")
plt.show()

colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightskyblue'] * (len(avg_buy_pnls) // 4 + 1)

plt.bar(list(avg_buy_pnls.keys()), avg_buy_pnls.values(), width=0.8, color=colors[:len(avg_buy_pnls)])
plt.title("Average PnL by Buy Time")
plt.xlabel("Buy Time")
plt.ylabel("Average PnL")
plt.show()

# plt.bar(list(avg_sell_pnls.keys()), avg_sell_pnls.values(), width=timedelta(minutes=50), color=colors[:len(avg_sell_pnls)])
# plt.title("Average PnL by Sell Time")
# plt.xlabel("Sell Time")
# plt.ylabel("Average PnL")
# plt.show()

plt.hist(profitable_hold_times, bins=500, alpha=0.5, color='blue', label='Profitable Trades')
plt.hist(lossy_hold_times, bins=1000, alpha=0.5, color='red', label='Lossy Trades')
plt.legend(loc='upper right')
plt.title("Distribution of Trade Hold Times")
plt.xlabel("Hold Times")
plt.ylabel("Frequency")
plt.xlim(0, 35)
plt.show()

plt.bar(list(avg_pnl_wrt_hold_time.keys()), avg_pnl_wrt_hold_time.values(), width=0.8, color='blue')
plt.title("Average PnL by Hold Time")
plt.xlabel("Hold Time")
plt.ylabel("Average PnL")
plt.xlim(0,50)
# plt.ylim(-5,15)
plt.show()