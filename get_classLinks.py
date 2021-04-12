import json
import requests
import datetime
import os

date = datetime.date.today()
dumpRemoveList = [i for i in os.listdir(os.getcwd()) if ".json" in i]
dumpRemoveList.remove("config.json")
if len(dumpRemoveList) > 0:
    if f"datadump{date}.json" in dumpRemoveList:
        dumpRemoveList.remove(f"datadump{date}.json")
    for i in dumpRemoveList:
        os.remove(i)

if not os.path.exists(f"datadump{date}.json"):
    with open("config.json",'r') as f:
        sessionID = f["sessionID"]
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

input("Press enter to exit")
