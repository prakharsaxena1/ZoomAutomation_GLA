import webbrowser
import json
import requests
import schedule
import config
import pprint
import time
import pyautogui


def convert24Hours(number, x):
    if x == "AM":
        return number+":00"
    return str(int(number) + 12)+":00"

def joinClass(link):
    webbrowser.open_new_tab(link)
    time.sleep(3)
    pyautogui.press("enter")
def decide():
    sessionID = config.sessionID
    date = "2020-12-2"
    GYOC = {"ASP.NET_SessionId": sessionID}
    data = {"text": date}
    url = "https://glauniversity.in:8085/MyAccount/DutyDetails"
    r = requests.post(url, data=data, cookies=GYOC)
    try:
        y = json.loads(r.text)
    except json.decoder.JSONDecodeError as e:
        print("SessionID has expired, will need a new one in order to continue")
        exit()
    x=[]
    for i in y:
        a, b = i['TimeFrom'].split("-")[0].strip(" ").split(" ")
        time_ = convert24Hours(a[0:a.index(":")], b)
        time_ = time_[0:time_.index(":")]
        link = i["JoinUrl"]
        x.append((time_, link))
    x.sort()
    for time_, link in x:
        schedule.every().day.at(time_+":00").do(joinClass,link)

    pprint.pprint(schedule.jobs)
    while True:
        schedule.run_pending()
        time.sleep(1)

decide()
