from breeze_connect import BreezeConnect 
import datetime

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

# Callback to receive ticks.
def on_ticks(ticks):
    print("Ticks: {}".format(ticks))



# Assign the callbacks.
breeze.on_ticks = on_ticks

def get_live_option_data(stock, interval, expiry, strike, right):
    # subscribe stocks feeds
    breeze.subscribe_feeds(exchange_code='NFO', stock_code=stock,interval=interval, product_type="options", expiry_date=expiry, strike_price=strike, right=right, get_exchange_quotes=True, get_market_depth=False)
