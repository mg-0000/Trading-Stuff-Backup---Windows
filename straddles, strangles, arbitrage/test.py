import pandas as pd
from breeze_connect import BreezeConnect 

print("here1")
# Initialize SDK
breeze = BreezeConnect(api_key="650G7Z51z645540%&15~b93v5*4M!574")

# Obtain your session key from https://api.icicidirect.com/apiuser/login?api_key=YOUR_API_KEY
# Incase your api-key has special characters(like +,=,!) then encode the api key before using in the url as shown below.
#import urllib
#print("https://api.icicidirect.com/apiuser/login?api_key="+urllib.parse.quote_plus("your_api_key"))

# Generate Session
breeze.generate_session(api_secret="6r1j471F_02Cw3371I38Ex045c42218F", session_token="14621711")

breeze2 = BreezeConnect(api_key="650G7Z51z645540%&15~b93v5*4M!574")

# Obtain your session key from https://api.icicidirect.com/apiuser/login?api_key=YOUR_API_KEY
# Incase your api-key has special characters(like +,=,!) then encode the api key before using in the url as shown below.
#import urllib
#print("https://api.icicidirect.com/apiuser/login?api_key="+urllib.parse.quote_plus("your_api_key"))

# Generate Session
breeze2.generate_session(api_secret="6r1j471F_02Cw3371I38Ex045c42218F", session_token="14621711")
breeze.ws_connect()
breeze2.ws_connect()

def on_ticks(ticks):
    print("HERE")
    print(ticks)

breeze.on_ticks = on_ticks
breeze2.on_ticks = on_ticks

#breeze.subscribe_feeds(exchange_code="NSE", stock_code="CNXBAN", get_exchange_quotes=True, get_market_depth=False,interval="1second")
#breeze.subscribe_feeds(stock_code="CNXBAN",exchange_code="NFO", product_type="options", expiry_date="06-June-2023", strike_price="45100", right="call", get_exchange_quotes=True, get_market_depth=False, interval="1minute")
breeze.subscribe_feeds(stock_token="1.1!500780",interval="1second")
breeze2.subscribe_feeds(stock_token="1.1!500780", interval="1second")