import sys
sys.path.insert(1, 'C:/Users/mridu/Documents/Trading Stuff/breeze')
from breeze_import import breeze
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

date = "2023-12-04"
expiry = "2023-12-06"
strike = 45700
right = "call"

# tmp = get_option_historical_data(start_date = (date) + "T09:15:00.000Z", end_date = (date) + "T15:30:00.000Z", expiry = expiry + "T09:15:00.000Z", strike = strike, stock_code="CNXBAN", time_interval="1second", right=right)
data = get_equity_historical_data(start_date=(date) + "T09:15:00.000Z", end_date=(date) + "T15:30:00.000Z", stock_code="CNXBAN", time_interval="1minute")
print(data)
print(data.iloc[data.index[data['datetime']=="2023-12-04 09:14:00"][0]: data.index[data['datetime']=="2023-12-04 09:30:00"][0]]['close'])

open_close = float(data[data['datetime']==date+" 09:00:00"]['open'].values) - float(data[data['datetime']==date+" 09:15:00"]['open'].values)
print(open_close)
# print(tmp)