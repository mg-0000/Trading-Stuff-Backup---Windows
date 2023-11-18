#build the bollinger bands strategy

import numpy as np
import pandas as pd

price_list = []

#bool variables to define where the price is currently
overbought = False
underbought = False
last_replace = 0

def main(price, lookback = 12):
    global price_list, overbought, underbought, last_replace

    if(len(price_list) < lookback):
        price_list = np.append(price_list, [price], axis=0)
        return "none"
    
    price_list = np.array(price_list)
    price_list[last_replace] = price
    last_replace+=1
    if(last_replace==lookback):
        last_replace = 0
        
    mean = np.mean(price_list)
    std = np.std(price_list)
    std *= 2
    if(overbought==False and price>(mean + std)):
        overbought = True
    if(underbought==False and price<(mean - std)):
        underbought = True
    
    #send the signals
    if(overbought==True and price<(mean + std)):
        overbought = False
        return "buy"
    if(underbought==True and price>(mean - std)):
        underbought = False
        return "sell"