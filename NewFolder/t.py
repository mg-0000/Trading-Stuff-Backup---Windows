import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Raw file with only 25 per side loss limit
csv_file = "orders_lists_2.csv"
df = pd.read_csv(csv_file)
print(df.shape, len(df))

def get_half_hour_interval(time):
    time = datetime.strptime(time, '%H:%M:%S')
    half_hour = (time.replace(minute=0, second=0) + timedelta(minutes=30))
    return half_hour

def get_closest_time(time):
    if int(time[-5:-3])<15:
      closest_time = str(int(time[:2])) + ":00:00"
    elif int(time[-5:-3])>=15 and int(time[-5:-3])<45 :
      closest_time = str(int(time[:2])) + ":30:00" 
    else:
      if int(time[:2])<10:
        closest_time = "0" + str(int(time[:2])+1) + ":00:00"
      else:
        closest_time = str(int(time[:2])+1) + ":00:00"
    return closest_time
    
sum = 0
no_profitable = 0
no_lossy = 0
avg_profitable = 0
avg_lossy = 0
for i in range(0,len(df)):
    # print(df.iloc[-i]['Real Buy Time'], df.iloc[-i]['Real Sell Time'], df.iloc[-i]['PnL'])
    if(i%500==0):
        print(sum, i)
    sum += df.iloc[-i]['PnL']
    if(df.iloc[-i]['PnL'] > 0):
        no_profitable += 1
        avg_profitable += df.iloc[-i]['PnL']
    else:
        no_lossy += 1
        avg_lossy += df.iloc[-i]['PnL']
# print(get_closest_time('11:40:00'))
print(sum, no_profitable, avg_profitable/no_profitable, no_lossy, avg_lossy/no_lossy, no_profitable+no_lossy)