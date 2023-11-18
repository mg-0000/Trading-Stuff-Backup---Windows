# import os
# #import test_strategy as strategy
# import pandas as pd
# import matplotlib.pyplot as plt
# plt.style.use('fivethirtyeight')
# from pylab import rcParams
# rcParams['figure.figsize'] = 10, 6
# #import dateparse
# import tailer
# import io

import moving_average_main as strategy
import sys
sys.path.append( '/home/mgoel/Documents/quant_algos/Broker_simulation/')
from broker import main


main('ADANIENT.NS')