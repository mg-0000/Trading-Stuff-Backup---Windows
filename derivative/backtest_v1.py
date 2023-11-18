import sys
sys.path.insert(1, 'C:/Users/mridu/Documents/Trading Stuff/derivative')
import backtest

# buy_trigs = [10, 20, 30, 40, 50, 60, 70, 80, 90]
# exit_trigs = [-10, -10, -10, -10, -10, -10, -10, -10, -10]
# exit_trigs = [-10, -20, -30, -40, -50, -60, -70, -80, -90]
# exit_trigs = [10, 10, 10, 10, 10, 10, 10, 10, 10]
buy_trigs = [50]
exit_trigs = [-10]
derivatives_lookback_period = 2   # number of derivatives to consider
derivatives_interval = 4    # interval between two derivatives

averaging_lookback = 15
averaging_sigma_1 = 5.
averaging_sigma_2 = 5.

stock = "CNXBAN"
expiry = "2023-09-13"
date = "2023-09-13"

averaging_method = "bilateral"

print(len(buy_trigs), len(exit_trigs))

params = [stock, expiry, date, "1second", averaging_method, [buy_trigs, exit_trigs, derivatives_lookback_period, derivatives_interval, averaging_lookback, averaging_sigma_1, averaging_sigma_2]]

print(params)

b1 = backtest.backtest(params[0], params[1], params[2], params[3], params[4], params[5])
b1.backtest()
res = b1.get_results()
print(res)
b1.print_results()