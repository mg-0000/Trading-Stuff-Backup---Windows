#build the bollinger bands strategy

import numpy as np
import pandas as pd

class strategy():
    def __init__(self):

        self.price_list = []

        #bool variables to define where the price is currently
        self.overbought = False
        self.underbought = False

        self.last_replace = 0

    def main(self,price, lookback = 12):
        #global price_list, overbought, underbought, last_replace

        if(len(self.price_list) < lookback):
            self.price_list = np.append(self.price_list, [price], axis=0)
            return "none"
        self.price_list = np.array(self.price_list)
        self.price_list[self.last_replace] = price
        self.last_replace+=1
        if(self.last_replace==lookback):
            self.last_replace = 0
        mean = np.mean(self.price_list)
        std = np.std(self.price_list)
        std *= 1
        if(self.overbought==False and price>(mean + std)):
            self.overbought = True
        if(self.underbought==False and price<(mean - std)):
            self.underbought = True
        
        #send the signals
        if(self.overbought==True and price<=(mean + std)):
            self.overbought = False
            return "buy"
        if(self.underbought==True and price>=(mean - std)):
            self.underbought = False
            return "sell"