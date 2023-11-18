import numpy as np
import math

def get_derivative_value(current, previous, interval):
    # print(int(float(current) - float(previous)))
    return math.degrees(math.atan((float(current) - float(previous))/(interval)))

class get_derivative:
    def __init__(self, lookback_period, der_interval) -> None:
        self.price_history = []     # will contain the price history to decide the derivatives
        self.derivatives_history = []   # will contain the derivatives history to decide the order
        self.lookback_period = lookback_period  # return an order if the last lookback_period ders are the same
        self.price = 0  
        self.der_interval = der_interval    # the derivative is taken at t, t-der_interval

    def update_price_history(self, price):
        self.price = price
        if(len(self.price_history)<self.der_interval):
            self.price_history.append(price)
        else:
            self.price_history.pop(0)
            self.price_history.append(price)
        return price

    def update_der_history(self):
        # self.update_price_history(price)    # update the price_history list
        der = get_derivative_value(self.price_history[-1], self.price_history[0], self.der_interval)  # get the derivative
        # update the derivatives_history list
        if(len(self.derivatives_history)<self.lookback_period):
            self.derivatives_history.append(der)
        else:
            self.derivatives_history.pop(0)
            self.derivatives_history.append(der)
        return der

    def update(self, price):
        # update the price_history list
        self.update_price_history(price)

        # update the derivatives_history list
        self.update_der_history()

        return self.derivatives_history

def get_order(derivatives_history, buy_trigger, exit_trigger):
    # check if the all the derivatives in the derivatives_history list are above the trigger
    if(all(x>buy_trigger for x in derivatives_history)):
        return "buy"    # enter long position
    elif(all(x<-buy_trigger for x in derivatives_history)):
        return "sell"   # enter short position
    elif(all(x<exit_trigger for x in derivatives_history)):
        return "exit"   # exit long position
    else:
        return 0    