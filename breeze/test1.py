import datetime
import time

#d = datetime.time(hour=18, minute=38)
#now = datetime.datetime.now()
#current_time = now.strftime("%H:%M:%S")
now = time.localtime()
print(type(now))
t = time.strptime("18:43:00", "%H:%M:%S")
print(t)
print(type(t))
if(t[3]==now[3]):
    print("equal")