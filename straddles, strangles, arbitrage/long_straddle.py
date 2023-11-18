import pandas as pd
from breeze_connect import BreezeConnect 
import time

breeze = BreezeConnect(api_key="650G7Z51z645540%&15~b93v5*4M!574")

breeze.generate_session(api_secret="6r1j471F_02Cw3371I38Ex045c42218F", session_token="14621711")

# Connect to websocket(it will connect to tick-by-tick data server)
#breeze.ws_connect()

print("here")


stock = 'CNXBAN'
expiry = '07-06'

option_chain_call = (breeze.get_option_chain_quotes(stock_code=stock,
                    exchange_code="NFO",
                    product_type="options",
                    expiry_date="2023-" + expiry + "T06:00:00.000Z",
                    right="call"))

#time.sleep(60)

option_chain_put = (breeze.get_option_chain_quotes(stock_code=stock,
                    exchange_code="NFO",
                    product_type="options",
                    expiry_date="2023-" + expiry + "T06:00:00.000Z",
                    right="put"))

lot_size = 25
diffs = 100
if(stock == "NIFTY"):
    lot_size = 50
    diffs = 50
elif(stock == "NIFSEL"):
    lot_size = 75
    diffs = 50
elif(stock == "NIFFIN"):
    lot_size = 40
    diffs = 50

#print(option_chain_call)

call_data = pd.DataFrame(option_chain_call["Success"])
spot = float(call_data.loc[0]["spot_price"])
temp = 3
temp_2 = 2
if(spot - int(spot/diffs)*100>50):
    print("here")
    temp = 2
    temp_2 = 3
call_data = call_data[call_data["ltp"]!=0.0]
call_data = call_data[call_data["chnge_oi"]!=0.0]
call_data = call_data[call_data["strike_price"]>=int((spot-temp*diffs))]
call_data.drop(columns = [ "product_type", "exchange_code", "open", "high", "low", "previous_close", 'ltp_percent_change', 'upper_circuit', 'lower_circuit'], inplace=True)
call_data.reset_index(inplace=True)

call_dist_from_spot = call_data[:]["spot_price"].astype(float) - (call_data[:]["strike_price"].astype(float) + call_data[:]["ltp"].astype(float))
call_data["ltp per lot"] = call_data["ltp"]*lot_size
call_data["Dist From Spot"] = call_dist_from_spot
call_data["Dist From Spot as Percentage in Spot"] = (call_data["Dist From Spot"])/float(spot)*100.0
in_profit_calls = call_data[call_data["Dist From Spot"] > 0]
call_data = call_data[call_data["Dist From Spot"] <= 0]

in_profit_calls.sort_values(by=["Dist From Spot"], inplace=True, ignore_index=True, ascending=False)
call_data.sort_values(by=["Dist From Spot"], inplace=True, ignore_index=True, ascending=False)



put_data = pd.DataFrame(option_chain_put["Success"])
put_data = put_data[put_data["ltp"]!=0.0]
put_data = put_data[put_data["chnge_oi"]!=0.0]
put_data = put_data[put_data["strike_price"]<=int((spot+temp_2*diffs))]
put_data.drop(columns = [ "product_type", "exchange_code", "open", "high", "low", "previous_close", 'ltp_percent_change', 'upper_circuit', 'lower_circuit'], inplace=True)
put_data.reset_index(inplace=True)

put_dist_from_spot = - put_data[:]["spot_price"].astype(float) + (put_data[:]["strike_price"].astype(float) - put_data[:]["ltp"].astype(float))
put_data["ltp per lot"] = put_data["ltp"]*lot_size
put_data["Dist From Spot"] = put_dist_from_spot
put_data["Dist From Spot Percentage in Spot"] = (put_data["Dist From Spot"])/float(spot)*100.0
in_profit_puts = put_data[put_data["Dist From Spot"] > 0]
put_data = put_data[put_data["Dist From Spot"] <= 0]
print(call_data.columns)
in_profit_puts.sort_values(by=["Dist From Spot"], inplace=True, ignore_index=True, ascending=False)
put_data.sort_values(by=["Dist From Spot"], inplace=True, ignore_index=True, ascending=False)



print("Spot Price = ", spot)
print("Closest Calls")
print(call_data.head(25))
print("In The Money Calls")
print(in_profit_calls)
print("Closest Puts")
print(put_data.head(25))
print("In The Money Puts")
print(in_profit_puts)

# min_call = -10000
# max_put = 10000
# 
# min_call_ltp = 10000
# max_put_ltp = 10000
# 
# in_profit_call = []
# in_profit_put = []
# 
# opt_call_order = []
# opt_put_order = []
# 
# spot = float(option_chain_call["Success"][0]["spot_price"])
# min_call_strike = spot
# max_put_strike = spot
# 
# for ele in option_chain_call["Success"]:
#     #print(ele)
#     strike = ele["strike_price"]
#     ltp = ele["ltp"]
#     if(ltp == 0.0):
#         continue
# 
#     spot_diff = spot - (strike + ltp) 
#     if(spot_diff > 0):
#         in_profit_call.append([strike, ltp])
#         continue
#     if(spot_diff >= min_call):
#         min_call = spot_diff
#         min_call_strike = strike  
#         min_call_ltp = ltp 
# 
# for ele in option_chain_put["Success"]:
#     #print(ele)
#     strike = ele["strike_price"]
#     ltp = ele["ltp"]
#     if(ltp == 0.0):
#         continue
# 
#     spot_diff = spot - (strike - ltp)
#     if(spot_diff < 0):
#         in_profit_put.append([strike, ltp])
#         continue
#     if(spot_diff <= max_put):
#         max_put = spot_diff
#         max_put_strike = strike  
#         max_put_ltp = ltp
#  
# 
# #print(len(option_chain["Success"]))
# print("Spot = ", spot)
# print("Ideal Call Strike = ", min_call_strike)
# print("Ideal Call Strike ltp = ", min_call_ltp)
# print("Minimum movement for Call profit = ", -min_call)
# print("Ideal Put Strike = ", max_put_strike)
# print("Ideal Put Strike ltp = ", max_put_ltp)
# print("Minimum movement for Put profit = ", -max_put)
# print("InProfit Calls = ", in_profit_call)
# print("InProfit Puts = ", in_profit_put)
