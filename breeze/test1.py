from breeze_import import breeze
from datetime import datetime
import http.client
import json
import hashlib
import requests
import pytz

#checksum computation
#time_stamp & checksum generation for request-headers
appkey = "650G7Z51z645540%&15~b93v5*4M!574"
secret_key = "409755400@8P#xT7009=x6~O58977333"
session_token = 'QUczNDE0ODQ6NzczNjQ2MzM='

now = datetime.now()

payload = json.dumps({})
time_stamp = datetime.utcnow().isoformat()[:19] + '.000Z'
checksum = hashlib.sha256((time_stamp+payload+secret_key).encode("utf-8")).hexdigest()

headers = {
    'Content-Type': 'application/json',
    'X-Checksum': 'token ' + checksum,
    'X-Timestamp': time_stamp,
    'X-AppKey': appkey,
    'X-SessionToken': session_token
}

tmp = requests.get('https://api.icicidirect.com/breezeapi/api/v1/funds', headers=headers, data=payload)
print(now, datetime.now())
# print(tmp.json())