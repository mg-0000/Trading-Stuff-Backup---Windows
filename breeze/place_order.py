from breeze_import import breeze

# Date must be in format "13-DEC-2023"
# Underlying must be "NIFTY", "CNXBAN", "NIFFIN"
def get_sltp(stoploss_price, strike, expiry, underlying, action, order_type, fresh_order_limit, market_type = "limit"):
    
    sltp = stoploss_price
    limit_calculated = breeze.limit_calculator(strike_price = str(strike),                                    
        product_type = "optionplus",                 
        expiry_date  = expiry,
        underlying = underlying,
        exchange_code = "NFO",
        order_flow = action,
        stop_loss_trigger = str(sltp),
        option_type = order_type,
        source_flag = "P",
        limit_rate = "",
        order_reference = "",
        available_quantity = "",
        market_type = market_type,
        fresh_order_limit = str(fresh_order_limit))
    
    while(float(limit_calculated["Success"]["limit_rate"])<stoploss_price):
        sltp = sltp+1
        limit_calculated = breeze.limit_calculator(strike_price = str(strike),                                    
            product_type = "optionplus",                 
            expiry_date  = expiry,
            underlying = underlying,
            exchange_code = "NFO",
            order_flow = action,
            stop_loss_trigger = str(sltp),
            option_type = order_type,
            source_flag = "P",
            limit_rate = "",
            order_reference = "",
            available_quantity = "",
            market_type = market_type,
            fresh_order_limit = str(fresh_order_limit))
    
    if(sltp>fresh_order_limit):
        sltp = fresh_order_limit - 1
        print("Change in StopLoss. New sltp = " + str(sltp))
        limit_calculated = breeze.limit_calculator(strike_price = str(strike),                                    
            product_type = "optionplus",                 
            expiry_date  = expiry,
            underlying = underlying,
            exchange_code = "NFO",
            order_flow = action,
            stop_loss_trigger = str(sltp),
            option_type = order_type,
            source_flag = "P",
            limit_rate = "",
            order_reference = "",
            available_quantity = "",
            market_type = market_type,
            fresh_order_limit = str(fresh_order_limit))
        
    return sltp, limit_calculated["Success"]['limit_rate']

def place_order(stock, strike, action, stoploss, quantity, right, expiry, sltp_expiry, sltp_stock, validity_date, cover_order_id = ''):
    fresh_order_limit = breeze.get_quotes(stock_code=sltp_stock,
                    exchange_code="NFO",
                    expiry_date=expiry,
                    product_type="options",
                    right=right,
                    strike_price=str(strike))
    fresh_order_limit = fresh_order_limit["Success"][0]["ltp"]
    if(action=="buy"):
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
        
        limit_calculated = limit_calculated["Success"]["limit_rate"]
        
        order = (breeze.place_order(stock_code=str(stock),
                        exchange_code="NFO",
                        product="optionplus",
                        action=str(action),
                        order_type="market",    ##
                        stoploss=str(stoploss),
                        quantity=str(quantity),     # Stoploss trigger price
                        price=str(limit_calculated),   # Stoploss limit price
                        validity="day",
                        validity_date=str(validity_date),
                        disclosed_quantity="0",
                        expiry_date=str(expiry),
                        right=str(right),
                        strike_price=str(strike),
                        order_type_fresh = "market",
                        order_rate_fresh = "",
                        user_remark="Placing Order"))

        
        # sltp, limit_calculated = get_sltp(stoploss, strike, sltp_expiry, sltp_stock, "sell", right,fresh_order_limit, "limit")

        # order = (breeze.place_order(stock_code=str(stock),
        #                 exchange_code="NFO",
        #                 product="optionplus",
        #                 action=str(action),
        #                 order_type="limit",    ##
        #                 stoploss=str(sltp),
        #                 quantity=str(quantity),     # Stoploss trigger price
        #                 price=str(limit_calculated),   # Stoploss limit price
        #                 validity="day",
        #                 validity_date=str(validity_date),
        #                 disclosed_quantity="0",
        #                 expiry_date=str(expiry),
        #                 right=str(right),
        #                 strike_price=str(strike),
        #                 order_type_fresh = "market",
        #                 order_rate_fresh = "",
        #                 user_remark="Placing Order"))
        print("Stoploss Limit Calculated = " + str(limit_calculated))
        return order
    elif(action=="sell"):

        order = breeze.modify_order(order_id=cover_order_id,
                    exchange_code="NFO",
                    order_type="market",
                    stoploss="0",
                    quantity=str(quantity),
                    price="0",
                    validity="Day",
                    disclosed_quantity="0",
                    validity_date=validity_date)
        return order
    else:
        return "Invalid"