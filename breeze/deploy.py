from breeze_connect import BreezeConnect 

import strategy.main as strategy

# Initialize SDK
breeze = BreezeConnect(api_key="650G7Z51z645540%&15~b93v5*4M!574")

# Obtain your session key from https://api.icicidirect.com/apiuser/login?api_key=YOUR_API_KEY
# Incase your api-key has special characters(like +,=,!) then encode the api key before using in the url as shown below.
#import urllib
#print("https://api.icicidirect.com/apiuser/login?api_key="+urllib.parse.quote_plus("your_api_key"))

# Generate Session
breeze.generate_session(api_secret="59q0120c8ps19960605758a3557759C6", session_token="10842907")

# Connect to websocket(it will connect to tick-by-tick data server)
breeze.ws_connect()

#live data params
stock = "CNXBAN"
interval = "1minute"
expiry = "25-May-2023"
strike = "44500"
right = "call"

#order params
stoploss = 25   #percent
quantity = 1    #maximum exposure
if(stock=="NIFTY"):
    lot = 50
elif(stock=="CNXBAN"):
    lot = 25

target_orders = True

def initialise():
    global no_of_buys, no_of_sells
    no_of_buys = 0
    no_of_sells = 0

# Callback to receive ticks.
def on_ticks(ticks):
    global no_of_buys, no_of_sells
    close = ticks['close']
    signal = strategy(close)
    if(signal=="buy"):
        if(no_of_buys<=no_of_sells):
            if(target_orders):
                new_buys = no_of_sells - no_of_buys + quantity 
            else:
                new_buys = 1
            no_of_buys += new_buys
            sl = close*(100 - stoploss)/100
            print("Buy order placed for ", new_buys, "lots")
            breeze.place_order(stock_code=stock,
                exchange_code="NFO",
                product="options",
                action="buy",
                order_type="market",
                stoploss=sl,
                quantity=new_buys*lot,
                price="",
                validity="ioc",
                expiry_date=expiry,
                right=right,
                strike_price=strike
            )
    elif(signal=="sell"):
        if(no_of_buys<=no_of_sells):
            if(target_orders):
                new_sells = no_of_buys - no_of_sells + quantity 
            else:
                new_sells = 1
            no_of_sells += new_sells
            sl = close*(100 + stoploss)/100
            print("Sell order placed for ", new_sells, "lots")
            breeze.place_order(stock_code=stock,
                exchange_code="NFO",
                product="options",
                action="sell",
                order_type="market",
                stoploss=sl,
                quantity=new_sells*lot,
                price="",
                validity="ioc",
                expiry_date=expiry,
                right=right,
                strike_price=strike
            )
    print("Ticks: {}".format(ticks))

# Assign the callbacks.
breeze.on_ticks = on_ticks

def get_live_option_data(stock, interval, expiry, strike, right):
    # subscribe stocks feeds
    breeze.subscribe_feeds(exchange_code='NFO', stock_code=stock,interval=interval, product_type="options", expiry_date=expiry, strike_price=strike, right=right, get_exchange_quotes=True, get_market_depth=False)

initialise()

#get_live_option_data(stock="CNXBAN", interval="1second", expiry="25-May-2023", strike="44500", right="Call"), 