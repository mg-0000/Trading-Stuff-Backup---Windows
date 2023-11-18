from breeze_connect import BreezeConnect 
import datetime
import strategy
import time

# Initialize SDK
breeze = BreezeConnect(api_key="650G7Z51z645540%&15~b93v5*4M!574")

# Obtain your session key from https://api.icicidirect.com/apiuser/login?api_key=YOUR_API_KEY
# Incase your api-key has special characters(like +,=,!) then encode the api key before using in the url as shown below.

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

#strategy params
lookback = 12

#order params
stoploss = 25   #percent
quantity = 1    #maximum exposure
if(stock=="NIFTY"):
    lot = 50
elif(stock=="CNXBAN"):
    lot = 25

target_orders = True

#square off time
square_off = time.strptime("15:25:00", "%H:%M:%S")

def initialise():
    global no_of_buys, no_of_sells
    no_of_buys = 0
    no_of_sells = 0

initialise()

# Callback to receive ticks.
def on_ticks(ticks):
    global no_of_buys, no_of_sells

    new_buys = 0
    new_sells = 0

    #squaring off
    now = time.localtime()
    if(square_off[3]==now[3] and square_off[4]==now[4]):
        print("Squaring off")
        if(no_of_sells>no_of_buys):
            new_buys = no_of_sells - no_of_buys
            no_of_buys += new_buys
            print("Buy order placed for ", new_buys, "lots when squaring off for the day")
            order = breeze.place_order(stock_code=stock,
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
            if(order["Success"]==None):
                no_of_buys -= new_buys
        elif(no_of_sells>no_of_buys):
            new_sells = no_of_buys - no_of_sells
            no_of_sells += new_buys
            print("Buy order placed for ", new_sells, "lots when squaring off for the day")
            order = breeze.place_order(stock_code=stock,
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
            if(order["Success"]==None):
                no_of_sells -= new_sells
        return


    close = ticks['close']
    signal = strategy(close, lookback)
    if(signal=="buy"):
        if(no_of_buys<=no_of_sells and target_orders==True):
            new_buys = no_of_sells - no_of_buys + quantity 
        elif(target_orders==False):
            new_buys = 1
        else:
            new_buys = 0
        if(new_buys>0):
            no_of_buys += new_buys
            sl = close*(100 - stoploss)/100
            print("Buy order placed for ", new_buys, "lots")
            order = breeze.place_order(stock_code=stock,
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
            if(order["Success"]==None):
                no_of_buys -= new_buys

    elif(signal=="sell"):
        if(no_of_buys<=no_of_sells and target_orders==True):
            new_sells = no_of_buys - no_of_sells + quantity 
        elif(target_orders==False):
            new_sells = 1
        else:
            new_sells = 0
        if(new_sells>0):
            no_of_sells += new_sells
            sl = close*(100 + stoploss)/100
            print("Sell order placed for ", new_sells, "lots")
            order = breeze.place_order(stock_code=stock,
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
            if(order["Success"]==None):
                no_of_buys -= new_buys
    print("Ticks: {}".format(ticks))

# Assign the callbacks.
breeze.on_ticks = on_ticks

#breeze.subscribe_feeds(exchange_code='NFO', stock_code=stock,interval=interval, product_type="options", expiry_date=expiry, strike_price=strike, right=right, get_exchange_quotes=True, get_market_depth=False)