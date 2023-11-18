import numpy as np
import math

class gaussian_mean:
    def __init__(self, sigma = 5, length = 50) -> None:
        self.sigma = sigma
        self.length = length
        self.history = []
        self.history_index = 0
    
    def get_gaussian_weights(self, l, sigma):
        weights = []
        for i in range(1,l+1):
            weights.append(math.exp(-(i*i)/(2*sigma)))
        weights = [weight/sum(weights) for weight in weights]
        return weights

    def update_history(self, price):
        if(len(self.history)<self.length):
            self.history.append(price)
        else:
            self.history.pop(0)
            self.history.append(price)

    def get_mean(self, price):
        self.update_history(price)
        # print(self.history)
        if(len(self.history)<self.length):
            return self.history[-1]
        else:
            weights = self.get_gaussian_weights(self.length, self.sigma)
            weights = np.flip(weights)
            return np.average(self.history, weights=weights)