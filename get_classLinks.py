import json
import requests
import config


def convert24Hours(number, x):
    if x == "AM":
        return number+":00"
    return str(int(number) + 12)+":00"


sessionID = config.sessionID
date = "2020-12-2"
GYOC = {"ASP.NET_SessionId": sessionID}
data = {"text": date}
url = "https://glauniversity.in:8085/MyAccount/DutyDetails"
r = requests.post(url, data=data, cookies=GYOC)
y = json.loads(r.text)
x=[]
# For distribution
for i in y:
    print(i['TimeFrom']+"   "+i['SubName']+"   "+i['JoinUrl'] + "\n")
