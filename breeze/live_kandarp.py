from breeze_import import breeze
from place_order import place_order

print(breeze.get_funds())

validity_date="2023-12-13T06:00:00.000Z"

while(True):
    print("Enter 1 for NIFTYBANK and 2 for NIFTY50 ")
    choice = int(input())
    if(choice == 1):
        stock = "CNXBAN"
        sltp_stock = stock
        quantity = 15   # One lot
        expiry = "2023-12-13T16:00:00.000Z"
        sltp_expiry = "13-DEC-2023"
    elif(choice == 2):
        stock = "NIFTY50"
        sltp_stock = "NIFTY"
        quantity = 50   # One lot
        expiry = "2023-12-14T16:00:00.000Z"
        sltp_expiry = "14-DEC-2023"
    else:
        print("Wrong Choice")
        continue

    print("Enter 1 for buy and 2 for selling last order ")
    buy_or_sell = int(input())
    if(buy_or_sell == 1):
        action = "buy"
    elif(buy_or_sell == 2):
        fresh_order_id = fresh_order["Success"]["order_id"]
        detail = breeze.get_order_detail('NFO',fresh_order_id)
        cover_order_id = detail['Success'][0]['parent_order_id']
        action = "sell"
    else:
        print("Wrong Choice")
        continue

    if(action=="buy"):
        print("Enter 1 for Call and 2 for Put ")
        choice = int(input())
        if(choice == 1):
            right = "call"
        elif(choice == 2):
            right = "put"
        else:
            print("Wrong Choice")
            continue

        print("Enter the strike price ")
        strike = int(input())

        if(action == "buy"):
            print("Enter stoploss price ")
            stoploss = int(input())
            if(stoploss==''):
                stoploss = 0
        else:
            stoploss = '0'
    else:
        right = "call"  # doesnt matter
        strike = '0'    # doesnt matter
        stoploss = '0'  # doesnt matter

    # place order
    print("Placing order")
    print(stock, action, stoploss, quantity, right, strike, expiry)
    if(action=="buy"):
        fresh_order = place_order(stock, strike, action, stoploss, quantity, right, expiry, sltp_expiry, sltp_stock, validity_date)
    else:
        fresh_order = place_order(stock, strike, action, stoploss, quantity, right, expiry, sltp_expiry, sltp_stock, validity_date, cover_order_id)
    print(fresh_order)
    
    