import pandas as pd
from breeze_connect import BreezeConnect 
import time

initial_call_strike = 45100
initial_call_premium = 100

initial_put_strike = 45600
initial_put_premium = 100

initial_spot = 45301

stock = "CNXBAN"
expiry = "06-Jun-2023"
expiry_format = "2023-07-06"

today_date="2023-07-05T06:00:00.000Z",

brokerage_and_margin = 0

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

print("here1")
# Initialize SDK
breeze = BreezeConnect(api_key="650G7Z51z645540%&15~b93v5*4M!574")

# Obtain your session key from https://api.icicidirect.com/apiuser/login?api_key=YOUR_API_KEY
# Incase your api-key has special characters(like +,=,!) then encode the api key before using in the url as shown below.
#import urllib
#print("https://api.icicidirect.com/apiuser/login?api_key="+urllib.parse.quote_plus("your_api_key"))

# Generate Session
breeze.generate_session(api_secret="6r1j471F_02Cw3371I38Ex045c42218F", session_token="14621711")

# Connect to websocket(it will connect to tick-by-tick data server)
breeze.ws_connect()

print("here2")

breeze2 = BreezeConnect(api_key="650G7Z51z645540%&15~b93v5*4M!574")

# Obtain your session key from https://api.icicidirect.com/apiuser/login?api_key=YOUR_API_KEY
# Incase your api-key has special characters(like +,=,!) then encode the api key before using in the url as shown below.
#import urllib
#print("https://api.icicidirect.com/apiuser/login?api_key="+urllib.parse.quote_plus("your_api_key"))

# Generate Session
breeze2.generate_session(api_secret="6r1j471F_02Cw3371I38Ex045c42218F", session_token="14621711")

# Connect to websocket(it will connect to tick-by-tick data server)
breeze2.ws_connect()

print("here3")

breeze3 = BreezeConnect(api_key="650G7Z51z645540%&15~b93v5*4M!574")

# Obtain your session key from https://api.icicidirect.com/apiuser/login?api_key=YOUR_API_KEY
# Incase your api-key has special characters(like +,=,!) then encode the api key before using in the url as shown below.
#import urllib
#print("https://api.icicidirect.com/apiuser/login?api_key="+urllib.parse.quote_plus("your_api_key"))

# Generate Session
breeze3.generate_session(api_secret="6r1j471F_02Cw3371I38Ex045c42218F", session_token="14621711")

# Connect to websocket(it will connect to tick-by-tick data server)
breeze3.ws_connect()

spot = initial_spot
current_target_put_strike = int(spot/diffs)*diffs + 2*diffs
current_target_call_strike = int(spot/diffs)*diffs - 1*diffs
put_price = initial_put_premium
call_price = initial_call_premium

check_for_put = True
check_for_call = True

temp = 2

def locking_in(right, strike, limit_price):
    if(right=="put"):
        initial_strike = initial_put_strike
    else:
        initial_strike = initial_call_strike

    #breeze.place_order(stock_code=stock,
    #                   exchange_code="NFO",
    #                   action="sell",
    #                   order_type="market",
    #                   stoploss="",
    #                   quantity=str(lot_size),
    #                   validity="ioc",
    #                   expiry_date=expiry,
    #                   right=right,
    #                   strike_price=initial_strike)
#
    #breeze.place_order(stock_code=stock,
    #                   exchange_code="NFO",
    #                   action="buy",
    #                   order_type="limit",
    #                   stoploss="",
    #                   quantity=str(lot_size),
    #                   price=str(limit_price),
    #                   validity="day",
    #                   validity_date=today_date,
    #                   expiry_date=expiry,
    #                   right=right,
    #                   strike_price=strike)
    print("Stuff")

# Callback to receive ticks.
def on_ticks(ticks):
    # spot = ticks['spot_price']
    spot = ticks['ltp']

    global temp

    #spot = (breeze.get_quotes(stock_code="CNXBAN",
    #                exchange_code="NSE",
    #                product_type="cash"))
    spot = spot["Success"][0]["spot_price"]
    if(spot - int(spot/diffs)>50):
        temp = 3
    current_target_put_strike = int(spot/diffs)*diffs + temp*diffs
    current_target_call_strike = int(spot/diffs)*diffs - temp*diffs

    if(spot > initial_spot):
        check_for_put = True
        check_for_call = False
    elif(spot <= initial_spot):
        check_for_put = False
        check_for_call = True
    print("Ticks: {}".format(ticks))

def on_ticks2(ticks):
    global put_price
    put_price = ticks['ltp']
def on_ticks3(ticks):
    global call_price
    call_price = ticks['ltp']

    #checks
    if(spot > initial_spot):    #check for put
        if((current_target_put_strike - put_price) - (initial_call_strike + initial_call_premium) >= initial_put_premium ):
            print("PUT Strike: ", current_target_put_strike, "Price: ", put_price)
            print("In Profit: ", (current_target_put_strike - put_price) - (initial_call_strike + initial_call_premium) - (initial_put_premium))
            if((current_target_put_strike - put_price) - (initial_call_strike + initial_call_premium) >= initial_put_premium  + brokerage_and_margin):
                print("Locking in profit: ", (current_target_put_strike - put_price) - (initial_call_strike + initial_call_premium) - (initial_put_premium) - brokerage_and_margin)
                locking_in("put", current_target_put_strike, put_price)
    elif(spot < initial_spot):
        if((initial_put_strike - initial_put_premium) - (current_target_call_strike + call_price) >= initial_call_premium):
            print("PUT Strike: ", current_target_put_strike, "Price: ", put_price)
            print("In Profit: ", (initial_put_strike - initial_put_premium) - (current_target_call_strike + call_price) - initial_call_premium)
            if((initial_put_strike - initial_put_premium) - (current_target_call_strike + call_price) >= initial_call_premium + brokerage_and_margin):
                print("Locking in profit: ", (initial_put_strike - initial_put_premium) - (current_target_call_strike + call_price) - initial_call_premium - brokerage_and_margin)
                locking_in("put", current_target_put_strike, put_price)





# Assign the callbacks.
breeze.on_ticks = on_ticks
breeze2.on_ticks = on_ticks2
breeze3.on_ticks = on_ticks3

breeze.subscribe_feeds(exchange_code="NSE", stock_code=stock, get_exchange_quotes=True, get_market_depth=False, interval="1second")
breeze2.subscribe_feeds(exchange_code="NFO", stock_code=stock, product_type="options", expiry_date=expiry, strike_price=current_target_put_strike, right="put", get_exchange_quotes=True, get_market_depth=False, interval="1second")
breeze2.subscribe_feeds(exchange_code="NFO", stock_code=stock, product_type="options", expiry_date=expiry, strike_price=current_target_call_strike, right="call", get_exchange_quotes=True, get_market_depth=False, interval="1second")