import numpy as np
import math

def get_gaussian_weughts(l, sigma):
    weights = []
    for i in range(1,l+1):
        weights.append(math.exp(-(i*i)/(2*sigma)))
    return weights

def get_intensity_weights(I, sigma):
    weights = []
    for i in I:
        weights.append(math.exp(-(i*i)/(2*sigma)))
    return weights

class bilateral_mean:

    def get_gaussian_weights(self, l, sigma):
        weights = []
        for i in range(1,l+1):
            weights.append(math.exp(-(i*i)/(2*sigma)))
        return weights

    def get_intensity_weights(self, I, sigma):
        weights = []
        for i in I:
            weights.append(math.exp(-(i*i)/(2*sigma)))
        return weights

    def __init__(self, sigma_temporal = 5, sigma_intensity = 5, length = 50) -> None:
        self.sigma_temporal = 5
        self.sigma_intensity = 5
        self.length = 50
        self.history = []
        self.history_index = 0

    def update_history(self, price):
        if(len(self.history)<self.length):
            self.history.append(price)
        else:
            self.history.pop(0)
            # print(len(self.history))
            self.history.append(price)

    def get_mean(self, price):
        self.update_history(price)
        if(len(self.history)<self.length):
            return self.history[-1]
        else:
            weights_temporal = self.get_gaussian_weights(self.length, self.sigma_temporal)
            weights_temporal = np.flip(weights_temporal)
            intensity_history = [x - self.history[-1] for x in self.history]
            weights_intensity = self.get_intensity_weights(intensity_history, self.sigma_intensity)
            weights_intensity = np.flip(weights_intensity)
            temp = np.multiply(weights_intensity, weights_temporal)
            temp = np.multiply(self.history, temp)/sum(temp)
            # return np.average(self.history, np.multiply(weights_intensity, weights_temporal))
            return sum(temp)