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

validity_date="2023-11-22T06:00:00.000Z"

while(True):
    print("Enter 1 for NIFTYBANK and 2 for NIFTY50 ")
    choice = int(input())
    if(choice == 1):
        stock = "CNXBAN"
        quantity = 15
        expiry = "2023-11-22T16:00:00.000Z"
    elif(choice == 2):
        stock = "NIFTY50"
        quantity = 50
        expiry = "2023-11-23T16:00:00.000Z"
    else:
        print("Wrong Choice")
        continue

    print("Enter 1 for Call and 2 for Put ")
    choice = int(input())
    if(choice == 1):
        right = "call"
    elif(choice == 2):
        right = "put"
    else:
        print("Wrong Choice")
        continue

    print("Enter 1 for buy and 2 for sell ")
    buy_or_sell = int(input())
    if(buy_or_sell == 1):
        action = "buy"
    elif(buy_or_sell == 2):
        action = "sell"
    else:
        print("Wrong Choice")
        continue

    print("Enter the strike price ")
    strike = int(input())

    print("Enter stoploss price ")
    stoploss = int(input())
    if(stoploss==''):
        stoploss = 0

    # place order
    print("Placing order")
    print(stock, action, stoploss, quantity, right, strike, expiry)
    print("2023-11-22T06:00:00.000Z", str(validity_date))

    if(action=="buy"):
        print(breeze.place_order(stock_code=str(stock),
                        exchange_code="NFO",
                        product="optionplus",
                        action=str(action),
                        order_type="limit",
                        stoploss=str(stoploss),
                        quantity=str(quantity),
                        price=str(stoploss),
                        validity="vtc",
                        validity_date=str(validity_date),
                        disclosed_quantity="0",
                        expiry_date=str(expiry),
                        right=str(right),
                        strike_price=str(strike),
                        order_type_fresh = "market",
                        order_rate_fresh = "",
                        user_remark="Placing Order"))
    elif(action=="sell"):
        print(breeze.place_order(stock_code=str(stock),
                    exchange_code="NFO",
                    product="options",
                    action=str(action),
                    order_type="market",
                    stoploss="",
                    quantity=str(quantity),
                    price="",
                    validity="day",
                    validity_date=str(validity_date),
                    disclosed_quantity="0",
                    expiry_date=str(expiry),
                    right=str(right),
                    strike_price=str(strike)))