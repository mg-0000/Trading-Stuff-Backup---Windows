import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Raw file with only 25 per side loss limit
csv_file = "orders_lists_2.csv"
df = pd.read_csv(csv_file)

pos_list_times = []
neg_list_times = []
pos_sell_times = []
neg_sell_times = []
avg_buy_pnls = {}
avg_sell_pnls = {}
other_pos_times = {}
other_neg_times = {}

def get_half_hour_interval(time):
    time = datetime.strptime(time, '%H:%M:%S')
    half_hour = (time.replace(minute=0, second=0) + timedelta(minutes=30))
    return half_hour
    
i = 0
tmp = 0
sum = 0
for idx, row_data in df.iterrows():
    sum += row_data['PnL']
    i+=1
    if(i<len(df) - 1000):
        continue
    # if(i>10000):
    #     break
    if(row_data['PnL'] > 0):
        pos_list_times.append(row_data['Real Buy Time'])
        pos_sell_times.append(row_data['Real Sell Time'])

        if(get_half_hour_interval(row_data['Real Buy Time']) not in other_pos_times):
            other_pos_times[get_half_hour_interval(row_data['Real Buy Time'])] = 0
        other_pos_times[get_half_hour_interval(row_data['Real Buy Time'])] += 1
        
    else:
        neg_list_times.append(row_data['Real Buy Time'])
        neg_sell_times.append(row_data['Real Sell Time'])
        if(get_half_hour_interval(row_data['Real Buy Time']) not in other_neg_times):
            other_neg_times[get_half_hour_interval(row_data['Real Buy Time'])] = 0
        other_neg_times[get_half_hour_interval(row_data['Real Buy Time'])] += 1
    
    if(get_half_hour_interval(row_data['Real Buy Time']) not in avg_buy_pnls):
        avg_buy_pnls[get_half_hour_interval(row_data['Real Buy Time'])] = 0
    if(get_half_hour_interval(row_data['Real Sell Time']) not in avg_sell_pnls):
        avg_sell_pnls[get_half_hour_interval(row_data['Real Sell Time'])] = 0
    avg_buy_pnls[get_half_hour_interval(row_data['Real Buy Time'])] += row_data['PnL']
    avg_sell_pnls[get_half_hour_interval(row_data['Real Sell Time'])] += row_data['PnL']
    # print(row_data['Real Buy Time'], row_data['Real Sell Time'], row_data['PnL'])

# plt.hist(pos_list_times, bins=50, alpha=0.5, color='blue', label='Profitable Trades')
# plt.hist(neg_list_times, bins=50, alpha=0.5, color='red', label='Lossy Trades')
# plt.legend(loc='upper right')
# plt.title("Distribution of Trade Buy Times")
# plt.xlabel("Trade Times")
# plt.ylabel("Frequency")
# plt.show()
    
print(sum)
print(avg_buy_pnls)
print(avg_sell_pnls)

# plt.bar(list(other_pos_times.keys()), other_pos_times.values(), width=timedelta(minutes=50), color='blue')
# plt.title("Number of Profitable Trades by Buy Time")
# plt.xlabel("Buy Time")
# plt.ylabel("Number of Trades")
# plt.show()

# plt.bar(list(other_neg_times.keys()), other_neg_times.values(), width=timedelta(minutes=50), color='red')
# plt.title("Number of Lossy Trades by Buy Time")
# plt.xlabel("Buy Time")
# plt.ylabel("Number of Trades")
# plt.show()

colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightskyblue'] * (len(avg_buy_pnls) // 4 + 1)

plt.bar(list(avg_buy_pnls.keys()), avg_buy_pnls.values(), width=timedelta(minutes=50), color=colors[:len(avg_buy_pnls)])
plt.title("Average PnL by Buy Time")
plt.xlabel("Buy Time")
plt.ylabel("Average PnL")
plt.show()

# plt.bar(list(avg_sell_pnls.keys()), avg_sell_pnls.values(), width=timedelta(minutes=50), color=colors[:len(avg_sell_pnls)])
# plt.title("Average PnL by Sell Time")
# plt.xlabel("Sell Time")
# plt.ylabel("Average PnL")
# plt.show()