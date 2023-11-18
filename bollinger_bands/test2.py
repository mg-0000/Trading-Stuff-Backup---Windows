import os
import pandas as pd
import numpy as np

import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '/home/mgoel/Documents/quant_algos/breeze')
import historical_data

path = '/home/mgoel/Documents/quant_algos/Data/CNXBAN_options_2023-05-25_call43000_1minute2023-05-11T07:00:00.csv'

df = []

rows = np.arange(15,27)
columns = np.arange(41000, 43100, 100)

for date in range(15,27):
    if(date==20 or date==21):
        strikes = []
        for strike in range(41000,43100,100):
            strikes.append(0)
        df.append(strikes)
        continue
    strikes = []
    for strike in range(41000,43100,100):
        path = '/home/mgoel/Documents/quant_algos/Data/CNXBAN_options_2023-06-01_put' + str(strike) + '_1minute2023-05-' + str(date) + 'T07:00:00.csv'
        if(os.path.isfile(path)==False):
            print("extracting data")
            historical_data.get_option_historical_data(start_date = "2023-05-" + str(date) + "T07:00:00.000Z", end_date = "2023-05-" + str(date) + "T18:00:00.000Z", expiry = "2023-06-01T07:00:00.000Z", strike = strike, stock_code="CNXBAN", time_interval="1minute", right="put")
        if(os.path.isfile(path)==False):
            strikes.append(0)
            continue
        with open(path, "rb") as file:
            # Go to the end of the file before the last break-line
            file.seek(2) 
            # Keep reading backward until you find the next break-line
            while file.read(1) != b'\n':
                file.seek(2, os.SEEK_CUR) 
            last_line = file.readline().decode()

        last_line = last_line.split(',')
        strikes.append(last_line[11])
    df.append(strikes)

df = pd.DataFrame(df, index = rows, columns=columns)
df.to_csv('/home/mgoel/Documents/quant_algos/data_open_puts_1June.csv')