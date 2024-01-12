from breeze_import import breeze 
import datetime

if(datetime.datetime.now()>=datetime.datetime(2023,12,13,15,6)):
    print("done")
else:
    print("not done")

# Connect to websocket(it will connect to tick-by-tick data server)
breeze.ws_connect()

# Callback to receive ticks.
def on_ticks(ticks):
    print("Ticks: {}".format(ticks))
    #  'datetime': '2023-12-13 14:58:58
    # if ticks['datetime'== '2023-12-13 14:58:58]
    return ticks['close']



# Assign the callbacks.
breeze.on_ticks = on_ticks

def get_live_option_data(stock, interval, expiry, strike, right):
    # subscribe stocks feeds
    breeze.subscribe_feeds(exchange_code='NFO', stock_code=stock,interval=interval, product_type="options", expiry_date=expiry, strike_price=strike, right=right, get_exchange_quotes=True, get_market_depth=False)

get_live_option_data('CNXBAN', '1second', '13-Dec-2023', '46700', 'Call')