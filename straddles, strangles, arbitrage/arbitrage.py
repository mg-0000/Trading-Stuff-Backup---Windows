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

#print(option_chain_put)
arbitrage_opps = []



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
#call_data.drop(columns = ["index", "product_type", "exchange_code"], inplace=True)
call_data.reset_index(inplace=True)

call_dist_from_spot = call_data[:]["spot_price"].astype(float) - (call_data[:]["strike_price"].astype(float) + call_data[:]["ltp"].astype(float))
call_data["Dist From Spot"] = call_dist_from_spot

call_data.sort_values(by=["Dist From Spot"], inplace=True, ignore_index=True, ascending=False)



put_data = pd.DataFrame(option_chain_put["Success"])
put_data = put_data[put_data["ltp"]!=0.0]
put_data = put_data[put_data["chnge_oi"]!=0.0]
put_data = put_data[put_data["strike_price"]<=int((spot+temp_2*diffs))]
put_data.reset_index(inplace=True)

put_dist_from_spot = - put_data[:]["spot_price"].astype(float) + (put_data[:]["strike_price"].astype(float) - put_data[:]["ltp"].astype(float))
put_data["Dist From Spot"] = put_dist_from_spot

put_data.sort_values(by=["Dist From Spot"], inplace=True, ignore_index=True, ascending=False)

spot = call_data.loc[0]["spot_price"]

arbitrage_opps = []

for i in range(len(call_data)):
    effective_call_price = call_data.loc[i]["strike_price"] + call_data.loc[i]["ltp"]
    for j in range(len(put_data)):
        effective_put_price = put_data.loc[j]["strike_price"] - put_data.loc[j]["ltp"]
        arb_diff = effective_put_price - effective_call_price
        cost = call_data.loc[i]["ltp"] + put_data.loc[j]["ltp"]
        arbitrage_opps.append([call_data.loc[i]["strike_price"], call_data.loc[i]["open_interest"], call_data.loc[i]["chnge_oi"], call_data.loc[i]["ltp"], put_data.loc[j]["strike_price"], put_data.loc[j]["open_interest"], put_data.loc[j]["chnge_oi"], put_data.loc[j]["ltp"], cost, cost*lot_size, arb_diff, float(arb_diff)/float(spot) * 100.0, arb_diff/cost])

df = pd.DataFrame(arbitrage_opps, columns=["Call Strike", "OI of Call", "Change_oi in Call", "Call ltp", "Put Strike", "OIPut", "Change_oi in Put", "Put ltp", "Cost", "Cost Per Lot", "Arbitrage Diff", "Arbitrage percent in Spot", "Arbitrage percent in Cost"])
df = df[df["Change_oi in Call"]!=0.0]
df = df[df["Change_oi in Put"]!=0.0]

df.sort_values(by=["Arbitrage Diff"], inplace=True, ignore_index=True, ascending=False)
temp_df = df.head(100)
temp_df.sort_values(by=["Cost"], inplace=True, ignore_index=True, ascending=True)

df.to_csv('temp.csv')

print("Spot Price = ", spot)
print(df.head(60))
print(temp_df.head(60))