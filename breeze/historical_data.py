from breeze_connect import BreezeConnect 
import datetime
import pandas as pd
import numpy as np
import time

#the 'interval' will be in the format of breeze itself
#make sure start and end are datetime objects
def divide(start, end, interval):
    dt_start = datetime.datetime(int(start[:4]), int(start[5:7]), int(start[8:10]), hour=int(start[11:13]), minute=int(start[14:16]), second=int(start[17:19]))
    dt_end = datetime.datetime(int(end[:4]), int(end[5:7]), int(end[8:10]), hour=int(end[11:13]), minute=int(end[14:16]), second=int(end[17:19]))
    if(interval == "1second"):
        #return_list is of the format [[start1,end1],[start2,end2]]
        return_list = []
        num = dt_end - dt_start
        # print(num.total_seconds())
        if(num.total_seconds()<=1000):
            return([[start,end]])
        intervals = int(num.total_seconds()//1000 + 1)
        for i in range(intervals - 1):
            temp_start = dt_start + datetime.timedelta(seconds=(i*1000 ))
            temp_end = temp_start +  datetime.timedelta(seconds=999)
            return_list.append([temp_start.isoformat()+".000Z", temp_end.isoformat()+".000Z"])
        last_end = datetime.datetime(int(str(return_list[len(return_list) - 1][1])[:4]), int(str(return_list[len(return_list) - 1][1])[5:7]), int(str(return_list[len(return_list) - 1][1])[8:10]), hour=int(str(return_list[len(return_list) - 1][1])[11:13]), minute=int(str(return_list[len(return_list) - 1][1])[14:16]), second=int(str(return_list[len(return_list) - 1][1])[17:19]))
        temp = last_end + datetime.timedelta(seconds=1)
        return_list.append([temp.isoformat()+".000Z", end])
        return return_list

# Initialize SDK
breeze = BreezeConnect(api_key="650G7Z51z645540%&15~b93v5*4M!574")

# Obtain your session key from https://api.icicidirect.com/apiuser/login?api_key=YOUR_API_KEY
# Incase your api-key has special characters(like +,=,!) then encode the api key before using in the url as shown below.
#import urllib
#print("https://api.icicidirect.com/apiuser/login?api_key="+urllib.parse.quote_plus("your_api_key"))

# Generate Session
breeze.generate_session(api_secret="8505G11&242r661%P4$035n8191s25V4", session_token="23728819")

# Connect to websocket(it will connect to tick-by-tick data server)
#breeze.ws_connect()

# Callback to receive ticks.
#def on_ticks(ticks):
#    print("Ticks: {}".format(ticks))

# Assign the callbacks.
#breeze.on_ticks = on_ticks

# subscribe stocks feeds
#breeze.subscribe_feeds(exchange_code="NFO", stock_code="ZEEENT", product_type="options", expiry_date="31-Mar-2022", strike_price="350", right="Call", get_exchange_quotes=True, get_market_depth=False)

# initializing input variables like expiry date and strike price

def get_option_historical_data(start_date, end_date, expiry, strike, stock_code='NIFTY', time_interval="1minute", right = "call"):

    #start_date = "2023-05-12T07:00:00.000Z"
    #
    #end_date = "2023-05-12T18:00:00.000Z"
    #
    #time_interval = "1second"
    #
    #
    #expiry = "2023-05-25T07:00:00.000Z"
    #
    #stock_code = "NIFTY"
    #
    exchange_code = "NFO"
    #
    product_type = "options"
    #
    #right = "call"
    #
    #strike = 18200


    #save directory
    # csv_path = "/home/mgoel/Documents/quant_algos/Data/" + stock_code + "_" + product_type + "_" + expiry[:10] + "_" + right + str(strike) + "_" + time_interval + start_date[:19] + ".csv"
    csv_path = "Data/" + stock_code + "_" + product_type + "_" + expiry[:4] + '_' + expiry[5:7] + '_' + expiry[8:10] + "_" + right + str(strike) + "_" + time_interval + start_date[:4] + '_' + start_date[5:7] + '_'  + start_date[8:10] + ".csv"

    #pass the intervals through divide func 
    if(time_interval=="1second"):
        put_data_list = []
        sub_intervals = divide(start_date, end_date, "1second")
        for intervals in sub_intervals:
            # print("Extracting data of interval number ", sub_intervals.index(intervals))
            data =  breeze.get_historical_data_v2(interval = time_interval,

                                from_date = intervals[0],

                                to_date = intervals[1],

                                stock_code = stock_code,

                                exchange_code = exchange_code,

                                product_type = product_type,

                                expiry_date = expiry,

                                right = right,

                                strike_price = strike)
            put_data_list.append(pd.DataFrame(data["Success"]))
        put_data = pd.concat(put_data_list)

    else:
        # downloading historical data for put option contract 

        data1 = breeze.get_historical_data(interval = time_interval,

                                    from_date = start_date,

                                    to_date = end_date,

                                    stock_code = stock_code,

                                    exchange_code = exchange_code,

                                    product_type = product_type,

                                    expiry_date = expiry,

                                    right = right,

                                    strike_price = strike)

        if(data1["Error"]=='Limit exceed: API call per minute:Try after some time'):
            time.sleep(60)
            data1 = breeze.get_historical_data(interval = time_interval,
                                    from_date = start_date,
                                    to_date = end_date,
                                    stock_code = stock_code,
                                    exchange_code = exchange_code,
                                    product_type = product_type,
                                    expiry_date = expiry,
                                    right = right,
                                    strike_price = strike)
        put_data = pd.DataFrame(data1["Success"])

    if(len(put_data)==0):
        print("No data")
        return "No data"

    put_data.to_csv(index=False)

    put_data.to_csv(csv_path)

    #print(put_data.shape)
    #print(csv_path)

    return(put_data)

def get_equity_historical_data(start_date, end_date, stock_code, time_interval = "1minute"):

    #start_date = "2023-05-12T07:00:00.000Z"
    #
    #end_date = "2023-05-12T18:00:00.000Z"
    
    exchange_code = "NSE"

    product_type = "cash"


    #save directory
    csv_path = "Data/" + stock_code + "_" + time_interval + start_date[:4] + '_' + start_date[5:7] + '_'  + start_date[8:10] + ".csv"

    if(time_interval=="1second"):
        put_data_list = []
        sub_intervals = divide(start_date, end_date, "1second")
        for intervals in sub_intervals:
            # print("Extracting data of interval number ", sub_intervals.index(intervals))
            data = breeze.get_historical_data_v2(interval=time_interval,
                            from_date= intervals[0],
                            to_date= intervals[1],
                            stock_code=stock_code,
                            exchange_code=exchange_code,
                            product_type=product_type)
            put_data_list.append(pd.DataFrame(data["Success"]))
        put_data = pd.concat(put_data_list)

    else:
        data1 = breeze.get_historical_data(interval=time_interval,
                            from_date= start_date,
                            to_date= end_date,
                            stock_code=stock_code,
                            exchange_code=exchange_code,
                            product_type=product_type)
        put_data = pd.DataFrame(data1["Success"])
    
    put_data.to_csv(index=False)

    put_data.to_csv(csv_path)

    # print(put_data.shape)
    # print(csv_path)

    return(put_data)

#for date in [11,12,15,16,17,18,19,22,23,24]:
#    for strike in range(45100, 46100, 100):
#        get_option_historical_data(start_date = "2023-05-" + str(date) + "T07:00:00.000Z", end_date = "2023-05-" + str(date) + "T18:00:00.000Z", expiry = "2023-05-25T07:00:00.000Z", strike = strike, stock_code="CNXBAN", time_interval="1minute")

# date = "2023-02-22"
# expiry = "2023-04-15"
#get_option_historical_data(start_date = "2023-09-21T07:00:00.000Z", end_date = "2023-09-22T18:00:00.000Z", expiry = "2023-09-27T07:00:00.000Z", strike = 44800, stock_code="CNXBAN", time_interval="1minute")
#get_equity_historical_data(start_date = "2023-09-21T07:00:00.000Z", end_date = "2023-09-22T18:00:00.000Z", stock_code="CNXBAN", time_interval="1minute")
#get_option_historical_data(start_date = (date) + "T07:00:00.000Z", end_date = (date) + "T18:00:00.000Z", expiry = expiry + "T07:00:00.000Z", strike = 41000, stock_code="CNXBAN", time_interval="1minute", right="call")