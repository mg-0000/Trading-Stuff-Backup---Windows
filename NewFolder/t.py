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
    
sum = 0
no_profitable = 0
no_lossy = 0
avg_profitable = 0
avg_lossy = 0
for i in range(5000,50000):
    # print(df.iloc[-i]['Real Buy Time'], df.iloc[-i]['Real Sell Time'], df.iloc[-i]['PnL'])
    if(i%10000==0):
        print(sum, i)
    sum += df.iloc[-i]['PnL']
    if(df.iloc[-i]['PnL'] > 0):
        no_profitable += 1
        avg_profitable += df.iloc[-i]['PnL']
    else:
        no_lossy += 1
        avg_lossy += df.iloc[-i]['PnL']
# print(get_half_hour_interval('11:40:00'))
print(sum, no_profitable, avg_profitable/no_profitable, no_lossy, avg_lossy/no_lossy, no_profitable+no_lossy)