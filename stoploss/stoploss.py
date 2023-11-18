class StopLoss:

    def __init__(self, sl = 0.25):
        self.sl = sl

        self.current_price = 0
        self.current_high = 0
        
        return

    def check(self, current_price):
        self.current_price = float(current_price)
        if(self.current_price < self.sl*self.current_high):
            return 1    #stoploss hit
        elif(self.current_price > self.current_high):
            self.current_high = self.current_price
            return 0    #new high
        else:
            return 0    #stoploss not hit