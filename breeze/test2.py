import base64 
import socketio
from datetime import datetime
from get_stock_token import get_token

#Get User ID and Session Token
session_key = "SESSION_TOKEN_FROM_CUSTOMER_DETAILS_API"
session_key = "QUczNDE0ODQ6NzczNjQ2MzM="
#e.g session_key = "QUYyOTUzMTM6NjY5ODc5NzY="

user_id, session_token = base64.b64decode(session_key.encode('ascii')).decode('ascii').split(":")
#e.g Decoded value - AF296713:66987976, after split user_id = AF295313, session_token = 6698797

# Python Socket IO Client
sio = socketio.Client()
auth = {"user": user_id, "token": session_token}
sio.connect("https://breezeapi.icicidirect.com/", socketio_path='ohlcvstream', headers={"User-Agent":"python-socketio[client]/socket"}, 
                auth=auth, transports="websocket", wait_timeout=3)

# Script Code of Stock or Instrument  e.g 4.1!1594, 1.1!500209 , 13.1!5023, 6.1!247457. 
script_code = ["4.1!1594"] #Subscribe more than one stock at a time
script_code = "4.1!" + str(get_token("28-Dec-2023", 48000, "CE")) 

#Channel name i.e 1SEC,1MIN,5MIN,30MIN
channel_name = "1SEC"

#CallBack functions to receive feeds
def on_ticks(ticks):
       print("here3")
       now = datetime.now()
       print(ticks, now)

#Connect to receive feeds
print('here2')
sio.emit('join', script_code)
sio.on(channel_name, on_ticks)

#Unwatch from the stock
# sio.emit("leave", script_code)

#Disconnect from the server
# sio.emit("disconnect", "transport close")
