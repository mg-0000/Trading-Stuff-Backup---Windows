#### This file contains functions and classes to calculate the technical indicators, for both backtesting purposes with continuous data and for tick-by-tick data stream ####
# As of now, I am making functions only for a continuous data for backtesting only. I will add functions for tick-by-tick data stream later.

#### Moving Average (MA) class ####
class MA:
    def __init__(self, period, data):
        self.period = period
        self.data = data
        self.name = 'MA'
        self.values = self.calculate_MA()
        
    def calculate_MA(self):
        return self.data.rolling(window=self.period).mean()
    
    def get_values(self):
        return self.values
    
    def get_name(self):
        return self.name
    

#### Bias class ####
class Bias:
    def __init__(self, period, data):
        self.period = period
        self.data = data
        self.name = 'Bias'
        self.values = self.calculate_Bias()
        
    def calculate_Bias(self):
        ma = MA(self.period, self.data)
        return (self.data - ma.get_values()) / ma.get_values()
    
    def get_values(self):
        return self.values
    
    def get_name(self):
        return self.name