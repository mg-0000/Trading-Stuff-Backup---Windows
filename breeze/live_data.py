from breeze_import import breeze, api_secret, session_token
import datetime

if(datetime.datetime.now()>=datetime.datetime(2024,1,16,15,20)):
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

breeze.generate_session(api_secret, session_token)
print(breeze.get_funds())
print(breeze.get_customer_details(api_session=session_token))

def get_live_option_data(stock, interval, expiry, strike, right):
    # subscribe stocks feeds
    breeze.subscribe_feeds(exchange_code='NFO', stock_code=stock,interval=interval, product_type="options", expiry_date=expiry, strike_price=strike, right=right, get_exchange_quotes=True, get_market_depth=False)

print('here2')
get_live_option_data('CNXBAN', '1second', '17-Jan-2024', '48100', 'call')
# breeze.subscribe_feeds(exchange_code='NSE', stock_code="ZEEENT",interval="1second", product_type="cash", get_exchange_quotes=True, get_market_depth=False)
# breeze.subscribe_feeds(stock_token="4.1!35512",interval="1second")