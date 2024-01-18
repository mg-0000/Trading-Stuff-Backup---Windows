import http.client
import json

def get_key(sessiontoken, appkey):
    conn = http.client.HTTPSConnection("api.icicidirect.com")
    # payload = "{\r\n    \"SessionToken\": \"30135814\",\r\n    \"AppKey\": \"650G7Z51z645540%&15~b93v5*4M!574\"\r\n}"
    payload = {
        "SessionToken": str(sessiontoken),
        "AppKey": str(appkey)
    }
    payload = json.dumps(payload)
    headers = {
                "Content-Type": "application/json"
            }
    conn.request("GET", "/breezeapi/api/v1/customerdetails", payload, headers)
    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    data = json.loads(data)
    # print(data)
    key = data["Success"]["session_token"]
    print(key)
    return key

# get_key("30249576", "650G7Z51z645540%&15~b93v5*4M!574")