import base64 
import socketio
from breeze_import import breeze, api_key, api_secret, session_token
from get_session_key import get_key
from get_stock_token import get_token

#Get User ID and Session Token
session_key = get_key(sessiontoken=session_token, appkey=api_key)
#e.g session_key = "QUYyOTUzMTM6NjY5ODc5NzY="

user_id, session_token = base64.b64decode(session_key.encode('ascii')).decode('ascii').split(":")
#e.g Decoded value - AF296713:66987976, after split user_id = AF295313, session_token = 6698797

# Python Socket IO Client
sio = socketio.Client()
auth = {"user": user_id, "token": session_token}
sio.connect("https://breezeapi.icicidirect.com/", socketio_path='ohlcvstream', headers={"User-Agent":"python-socketio[client]/socket"}, 
                auth=auth, transports="websocket", wait_timeout=3)

# Script Code of Stock or Instrument  e.g 4.1!1594, 1.1!500209 , 13.1!5023, 6.1!247457. 
script_code = ["4.1!" + str(get_token("17-Jan-2024", 48100, "PE")) ] #Subscribe more than one stock at a time

#Channel name i.e 1SEC,1MIN,5MIN,30MIN
channel_name = "1SEC"

#CallBack functions to receive feeds
def on_ticks(ticks):
       print(ticks)
       close = ticks[8]

#Connect to receive feeds
sio.emit('join', script_code)
sio.on(channel_name, on_ticks)

#Unwatch from the stock
sio.emit("leave", script_code)

#Disconnect from the server
sio.emit("disconnect", "transport close")

