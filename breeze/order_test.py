from breeze_import import breeze

# from breeze_connect import BreezeConnect 

# # Initialize SDK
# breeze = BreezeConnect(api_key="650G7Z51z645540%&15~b93v5*4M!574")

# # Obtain your session key from https://api.icicidirect.com/apiuser/login?api_key=YOUR_API_KEY
# # Incase your api-key has special characters(like +,=,!) then encode the api key before using in the url as shown below.
# #import urllib
# #print("https://api.icicidirect.com/apiuser/login?api_key="+urllib.parse.quote_plus("your_api_key"))

# # Generate Session
# breeze.generate_session(api_secret="409755400@8P#xT7009=x6~O58977333", session_token="26676922")

# # Connect to websocket(it will connect to tick-by-tick data server)
# breeze.ws_connect()

print(breeze.get_funds())

validity_date="2023-11-22T15:00:00.000Z",

a=15

breeze.limit_calculator(strike_price = str(st),                                    
    product_type = "optionplus",                 
    expiry_date  = "06-JUL-2023",
    underlying = "NIFTY",
    exchange_code = "NFO",
    order_flow = "Buy",
    stop_loss_trigger = "200.00",
    option_type = "Call",
    source_flag = "P",
    limit_rate = "",
    order_reference = "",
    available_quantity = "",
    market_type = "limit",
    fresh_order_limit = "177.70")

# print("Placing order")
# print(breeze.place_order(stock_code="CNXBAN",
#                     exchange_code="NFO",
#                     product="options",
#                     action="buy",
#                     order_type="limit",
#                     stoploss="170",
#                     quantity=str(a),
#                     price="170",
#                     validity="day",
#                     validity_date="2023-11-22T06:00:00.000Z",
#                     disclosed_quantity="0",
#                     expiry_date="2023-11-22T16:00:00.000Z",
#                     right="call",
#                     strike_price="43600"))
# a = 15
# print(breeze.place_order(stock_code="CNXBAN",
#                     exchange_code="NFO",
#                     product="optionplus",
#                     action="buy",
#                     order_type="limit",
#                     stoploss="160",
#                     quantity=str(a),
#                     price="100",
#                     validity="vtc",
#                     validity_date="2023-11-22T06:00:00.000Z",
#                     disclosed_quantity="0",
#                     expiry_date="2023-11-22T06:00:00.000Z",
#                     right="call",
#                     strike_price="46600",
#                     order_type_fresh = "market",
#                     order_rate_fresh = "",
#                     user_remark="Test"))
