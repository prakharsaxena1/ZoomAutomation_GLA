import pprint
import json
import os
import time
import requests
import schedule
import config
import pyautogui
import subprocess

if not os.path.exists("tt.py"):
    f = open("tt.py",'w')
    f.close()

def convert24Hours(number, x):
    if x == "AM":
        return number+":00"
    return str(int(number) + 12)+":00"

def SignIn(meetID, meetPassword):
    subprocess.call(["C:/Users/prakh/AppData/Roaming/Zoom/bin/Zoom.exe"])
    time.sleep(10)
    join_btn = pyautogui.locateCenterOnScreen('join1.png')
    pyautogui.moveTo(join_btn)
    time.sleep(1)
    pyautogui.click()
    time.sleep(2)
    pyautogui.write(meetID)
    media_btn = pyautogui.locateAllOnScreen('cb.png')
    for btn in media_btn:
        pyautogui.moveTo(btn)
        pyautogui.click()
    pyautogui.press('tab')
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.write(meetPassword)
    pyautogui.press('enter')
    
def getTimeTable():
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
        meetID, meetPasswd = link[18::].split("?pwd=")
        schedule.every().day.at(time_+":00").do(SignIn,meetID,meetPasswd)

getTimeTable()

pprint.pprint(schedule.jobs)
while True:
    schedule.run_pending()
    time.sleep(1)
