import requests
import json

# For testing purposes sessionID = input("Enter session ID:  ")
sessionID = "Apni daalo sessionID"
date = "2020-12-2"
GYOC = {"ASP.NET_SessionId": sessionID}
data = {"text": date}
url = "https://glauniversity.in:8085/MyAccount/DutyDetails"
r = requests.post(url, data=data, cookies=GYOC)
y = json.loads(r.text)

for i in y:
    print(i['TimeFrom']+"   "+i['SubName']+"   "+i['JoinUrl'] + "\n")


