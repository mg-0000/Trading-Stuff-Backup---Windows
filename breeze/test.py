from breeze_import import breeze
from datetime import datetime

# t1 = datetime.now()
# fresh_order_limit = breeze.get_quotes(stock_code="CNXBAN",
#                     exchange_code="NFO",
#                     expiry_date='2023-12-28T06:00:00.000Z',
#                     product_type="options",
#                     right='call',
#                     strike_price='47500')
t2 = datetime.now()
limit_calculated = breeze.limit_calculator(strike_price = str(48300),                                    
                product_type = "optionplus",                 
                expiry_date  = '03-Jan-2024',
                underlying = 'CNXBAN',
                exchange_code = "NFO",
                order_flow = "sell",
                stop_loss_trigger = '350',
                option_type = 'Call',
                source_flag = "P",
                limit_rate = "",
                order_reference = "",
                available_quantity = "",
                market_type = "market",
                fresh_order_limit = '400')
t3 = datetime.now()
print(t2,t3)

def on_ticks(ticks):
    now = datetime.now()
    print("Ticks time:", ticks['datetime'], now)

# print(breeze.get_option_chain_quotes(stock_code="CNXBAN",
#                 exchange_code="NFO",
#                 product_type="options",
#                 expiry_date="2023-12-28T06:00:00.000Z",
#                 right="call"))

# breeze.ws_connect()
# breeze.on_ticks = on_ticks

expiry = "28-Dec-2023"
strike = "48000"
right = "call"
# breeze.subscribe_feeds(exchange_code="NFO", stock_code="CNXBAN", product_type="options", expiry_date=expiry, strike_price=str(strike), right=right, interval="1second")
