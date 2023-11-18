from datetime import datetime, timedelta

print('here')

def get_weekday_dates(start_date, end_date, interval = 1):

    print('here')
    # Initialize an empty list to store the result
    result = []

    # Convert the input strings to datetime objects
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    # Define a timedelta of one day
    one_day = timedelta(days=interval)

    # Iterate through the dates and add weekdays to the result
    current_date = start_date
    while current_date <= end_date:
        # Check if the current date is a weekday (0 = Monday, 6 = Sunday)
        
        if current_date.weekday() < 5:  # Monday to Friday
            result.append(current_date.strftime("%Y-%m-%d"))

        # Move to the next day
        current_date += one_day

    return result

def get_expiry_dates(dates, first_expiry):
    expiries = []
    first_expiry = datetime.strptime(first_expiry, "%Y-%m-%d")

    
    
    for date in dates:
        date = datetime.strptime(date, "%Y-%m-%d")

        # to correct for the expiry change to wednesday from thursday
        if(first_expiry==datetime.strptime("2023-09-07", "%Y-%m-%d")):
            first_expiry -= timedelta(days=1)

        # to correct the expiry holiday on 29th June
        if(first_expiry==datetime.strptime("2023-06-29", "%Y-%m-%d")):
            first_expiry -= timedelta(days=1)
        if(first_expiry==datetime.strptime("2023-07-05", "%Y-%m-%d")):
            first_expiry += timedelta(days=1)

        # to correct the expiry holiday on 30th March
        if(first_expiry==datetime.strptime("2023-03-30", "%Y-%m-%d")):
            first_expiry -= timedelta(days=1)
        if(first_expiry==datetime.strptime("2023-04-05", "%Y-%m-%d")):
            first_expiry += timedelta(days=1)

        # to correct the expiry holiday on 26th January
        if(first_expiry==datetime.strptime("2023-01-26", "%Y-%m-%d")):
            first_expiry -= timedelta(days=1)
        if(first_expiry==datetime.strptime("2023-02-01", "%Y-%m-%d")):
            first_expiry += timedelta(days=1)

        # to account for the change in first_expiry, if any
        if(len(expiries)>0):
            expiries.pop()
            expiries.append(first_expiry.strftime("%Y-%m-%d"))

        if(date<=first_expiry):
            expiries.append(first_expiry.strftime("%Y-%m-%d"))
        else:
            first_expiry = first_expiry + timedelta(days=7)
            expiries.append(first_expiry.strftime("%Y-%m-%d"))
    return expiries


# # Example usage
# start_date = "2023-09-11"
# end_date = "2023-09-21"
# weekday_dates = get_weekday_dates(start_date, end_date)
# print(weekday_dates)
# expiry_dates = get_expiry_dates(weekday_dates, "2023-09-13")
# print(expiry_dates)
