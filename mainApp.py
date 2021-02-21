import datetime
import pprint
import json
import time
import requests
import schedule
import pyautogui
import subprocess
import os


date = datetime.date.today()
dumpRemoveList = [i for i in os.listdir(os.getcwd()) if ".json" in i]
if len(dumpRemoveList)>0:
    if f"datadump{date}.json" in dumpRemoveList:
        dumpRemoveList.remove(f"datadump{date}.json")
    for i in dumpRemoveList:
            os.remove(i)

def convert24Hours(number, x):
    if x == "AM" or number=="12":
        return number+":00"
    return str(int(number) + 12)+":00"

def SignIn(meetID, meetPassword):
    subprocess.call(["C:/Users/prakh/AppData/Roaming/Zoom/bin/Zoom.exe"])
    time.sleep(7)
    join_btn = pyautogui.locateCenterOnScreen('Assets/join1.png')
    pyautogui.moveTo(join_btn)
    pyautogui.click()
    time.sleep(2)
    pyautogui.write(meetID)
    media_btn = pyautogui.locateAllOnScreen('Assets/cb.png')
    for btn in media_btn:
        pyautogui.moveTo(btn)
        pyautogui.click()
    pyautogui.press('tab')
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.write(meetPassword)
    pyautogui.press('enter')

def getTimeTable():
    if not os.path.exists(f"datadump{date}.json"):
        sessionID = "lctdl05oxs11kshconv50s45"  # Your session ID here
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
    x = []
    for i in y:
        a, b = i['TimeFrom'].split("-")[0].strip(" ").split(" ")
        time_=a
        link = i["JoinUrl"]
        x.append((time_, link))
    x.sort()
    for time_, link in x:
        meetID, meetPasswd = link[18::].split("?pwd=")
        schedule.every().day.at(time_+":00").do(SignIn, meetID, meetPasswd)

try:
    getTimeTable()
except Exception as e:
    print("Some error occurred")

pprint.pprint(schedule.jobs)
while True:
    schedule.run_pending()
    time.sleep(1)
