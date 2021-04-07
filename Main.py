# Module Imports - System
from threading import Thread
import pprint
import datetime
import time
import json
import subprocess
import os
# Module Imports - pip install *
import pyautogui
import requests
import schedule

# Function -> getTimeTable
def getTimeTable(sessionID):
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

# Function -> sign in to zoom if not already signed in
def signINtoZOOM():
    signin_btn = pyautogui.locateCenterOnScreen('./Assets/signin.png')
    pyautogui.moveTo(signin_btn)
    pyautogui.click()
    time.sleep(1)
    pyautogui.write(email)
    pyautogui.press('tab')
    pyautogui.write(password)
    pyautogui.press('tab',presses=3)
    pyautogui.press('enter')

# Function -> sign in to zoom meetings

def OpenZoom():
  subprocess.call("C:/Users/prakh/AppData/Roaming/Zoom/bin/Zoom.exe")

def SignIn(meetID, meetPassword):
    thrd = Thread(target=OpenZoom)
    thrd.start()
    time.sleep(5)
    try:
        x,y = pyautogui.locateCenterOnScreen('./Assets/join1.png')
    except Exception as e:
        signINtoZOOM()
    time.sleep(2)
    pyautogui.keyDown('alt')
    pyautogui.press(' ')
    pyautogui.press('x')
    pyautogui.keyUp('alt')
    pyautogui.moveTo(800, 460)
    pyautogui.click()
    time.sleep(2)
    pyautogui.write(meetID)
    media_btn = pyautogui.locateAllOnScreen('./Assets/cb.png')
    for btn in media_btn:
        pyautogui.moveTo(btn)
        pyautogui.click()
    pyautogui.press('tab')
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.write(meetPassword)
    pyautogui.press('enter')


# Code to remove all old datadump files
date = datetime.date.today()
dumpRemoveList = [i for i in os.listdir(os.getcwd()) if ".json" in i]
dumpRemoveList.remove("config.json")
if len(dumpRemoveList) > 0:
    if f"datadump{date}.json" in dumpRemoveList:
        dumpRemoveList.remove(f"datadump{date}.json")
    for i in dumpRemoveList:
        os.remove(i)

# Config
with open(f"config.json") as f:
    configFile = json.load(f)
sessionID = configFile["sessionID"]
email = configFile["email"]
password = configFile["password"]

# Get Time Table
if not os.path.exists(f"datadump{date}.json"):
    getTimeTable(sessionID)

# Schedule meeting
with open(f"datadump{date}.json", 'r') as f:
    y = json.load(f)
x = []
for i in y:
    a, b = i['TimeFrom'].split("-")[0].strip(" ").split(" ")
    time_ = a
    link = i["JoinUrl"]
    x.append((time_, link))
x.sort()
for time_, link in x:
    meetID, meetPasswd = link[18::].split("?pwd=")
    schedule.every().day.at(time_).do(SignIn, meetID, meetPasswd)


pprint.pprint(schedule.jobs)

while True:
    schedule.run_pending()
    time.sleep(1)
