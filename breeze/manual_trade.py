from breeze_import import breeze
from place_order import place_order
from datetime import datetime
import threading
import time

# global variables
current_price = 0
limit_rate_calculated = 0
stop_threads = 0

def on_ticks(ticks):
    global current_price, stop_threads, stock,sltp_expiry, expiry, strike, right

    if stop_threads:
        breeze.unsubscribe_feeds(exchange_code="NFO", stock_code=stock, product_type="options", expiry_date=sltp_expiry, strike_price=str(strike), right=right, interval="1second")
        return

    current_price = ticks['close']

breeze.ws_connect()
breeze.on_ticks = on_ticks

def get_live_data(stock, sltp_expiry, strike, right):
    # expiry = "28-Dec-2023"
    # strike = "47700"
    # right = "call"
    print(stock, sltp_expiry, strike, right)
    breeze.subscribe_feeds(exchange_code="NFO", stock_code=stock, product_type="options", expiry_date=sltp_expiry, strike_price=str(strike), right=right, interval="1second")

def get_limit_price(strike, sltp_expiry, sltp_stock, stoploss, right):
    while True:
        global current_price, limit_rate_calculated, stop_threads
        if(stop_threads):
            break
        fresh_order_limit = current_price
        limit_calculated = breeze.limit_calculator(strike_price = str(strike),                                    
                    product_type = "optionplus",                 
                    expiry_date  = sltp_expiry,
                    underlying = sltp_stock,
                    exchange_code = "NFO",
                    order_flow = "sell",
                    stop_loss_trigger = str(stoploss),
                    option_type = right,
                    source_flag = "P",
                    limit_rate = "",
                    order_reference = "",
                    available_quantity = "",
                    market_type = "market",
                    fresh_order_limit = str(fresh_order_limit))
            
        limit_rate_calculated = limit_calculated["Success"]["limit_rate"]
        time.sleep(1)

print(breeze.get_funds())

validity_date="2023-12-28T06:00:00.000Z"

while(True):
    print("Enter 1 for NIFTYBANK and 2 for NIFTY50 ")
    choice = int(input())
    if(choice == 1):
        stock = "CNXBAN"
        sltp_stock = stock
        quantity = 15   # One lot
        expiry = "2023-12-28T16:00:00.000Z"
        sltp_expiry = "28-Dec-2023"
    elif(choice == 2):
        stock = "NIFTY"
        sltp_stock = "NIFTY"
        quantity = 50   # One lot
        expiry = "2023-12-28T16:00:00.000Z"
        sltp_expiry = "28-Dec-2023"
    else:
        print("Wrong Choice")
        continue

    print("Enter 1 for buy and 2 for selling last order ")
    buy_or_sell = int(input())
    if(buy_or_sell == 1):
        action = "buy"
    elif(buy_or_sell == 2):
        action = "sell"
    else:
        print("Wrong Choice")
        continue

    if(action=="buy"):
        print("Enter the strike price ")
        strike = int(input())

        print("Enter 1 for Call and 2 for Put ")
        choice = int(input())
        if(choice == 1):
            right = "call"
        elif(choice == 2):
            right = "put"
        else:
            print("Wrong Choice")
            continue

        # Threading
        t1 = None
        t1 = threading.Thread(target=get_live_data, args=(stock, sltp_expiry, strike, right))
        t1.start()

        print("Enter stoploss price ")
        stoploss = int(input())

        # Threading
        t2 = None
        t2 = threading.Thread(target=get_limit_price, args=(strike, sltp_expiry, sltp_stock, stoploss, right))
        t2.start()

        print("Place Order? (y/n)")
        if(input()!='y'):
            continue

        order_time = datetime.now()
        fresh_order = (breeze.place_order(stock_code=str(stock),
                        exchange_code="NFO",
                        product="optionplus",
                        action=str(action),
                        order_type="market",    ##
                        stoploss=str(stoploss),    # Stoploss trigger price    180
                        quantity=str(quantity),     # Stoploss trigger price    15
                        price=str(limit_rate_calculated),   # Stoploss limit price  171
                        validity="day",
                        validity_date=str(validity_date),
                        disclosed_quantity="0",
                        expiry_date=str(expiry),
                        right=str(right),
                        strike_price=str(strike),
                        order_type_fresh = "market",
                        order_rate_fresh = "",
                        user_remark="Placing Order"))
        print(fresh_order)
        fresh_order_id = fresh_order["Success"]["order_id"]
        detail = breeze.get_order_detail('NFO',fresh_order_id)
        cover_order_id = detail['Success'][0]['parent_order_id']
        print("Order should be placed at ", order_time)
        print("Buy order details:", detail )

        stop_threads = 1

    else:
        order_time = datetime.now()
        fresh_order = breeze.modify_order(order_id=cover_order_id,
                    exchange_code="NFO",
                    order_type="market",
                    stoploss="0",
                    quantity=str(quantity),
                    price="0",
                    validity="Day",
                    disclosed_quantity="0",
                    validity_date=validity_date)
        fresh_order_id = fresh_order["Success"]["order_id"]
        detail = breeze.get_order_detail('NFO',fresh_order_id)
        # cover_order_id = detail['Success'][0]['parent_order_id']
        # detail = breeze.get_order_detail('NFO',cover_order_id)
        print(fresh_order)
        print("Order should be placed at ", order_time)
        print("Sell order details:", detail )
           
    