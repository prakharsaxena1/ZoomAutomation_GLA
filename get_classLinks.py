import json
import requests
import config
import datetime
import os

def convert24Hours(number, x):
    if x == "AM":
        return number+":00"
    return str(int(number) + 12)+":00"


Previous_Date = (datetime.datetime.today() -datetime.timedelta(days=1)).strftime('%Y-%m-%d')
date = datetime.date.today()
if os.path.exists(f"datadump{Previous_Date}.json"):
    os.remove(f"datadump{Previous_Date}.json")

sessionID = config.sessionID
GYOC = {"ASP.NET_SessionId": sessionID}
data = {"text": date}
url = "https://glauniversity.in:8085/MyAccount/DutyDetails"
r = requests.post(url, data=data, cookies=GYOC)

try:
    with open(f"datadump{date}.json", 'w') as f:
        f.write(r.text)
except json.decoder.JSONDecodeError as e:
    print("SessionID has expired, will need a new one in order to continue")
    exit()
with open(f"datadump{date}.json") as f:
    y = json.load(f)
# For distribution
for i in y:
    print(i['TimeFrom']+"   "+i['SubName']+"   "+i['JoinUrl'] + "\n")
