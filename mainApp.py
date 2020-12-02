import pprint
import json
import os
import time
import requests
import schedule
import config

if not os.path.exists("tt.py"):
    f = open("tt.py",'w')
    f.close()

def convert24Hours(number, x):
    if x == "AM":
        return number+":00"
    return str(int(number) + 12)+":00"

def getTimeTable():
    fortt = """
import subprocess\nimport time\nimport pyautogui\nimport schedule\nfrom pynput.keyboard import Controller, Key\n
def SignIn(meetID, meetPassword):
    subprocess.call(["C:/Users/prakh/AppData/Roaming/Zoom/bin/Zoom.exe"])
    time.sleep(10)
    join_btn = pyautogui.locateCenterOnScreen('join1.png')
    pyautogui.moveTo(join_btn)
    pyautogui.click()
    time.sleep(2)
    pyautogui.write(meetID)
    media_btn = pyautogui.locateAllOnScreen('cb.png')
    for btn in media_btn:
        pyautogui.moveTo(btn)
        pyautogui.click()
    keyboard = Controller()
    keyboard.press(Key.tab)
    keyboard.release(Key.tab)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    pyautogui.moveTo(join_btn)
    pyautogui.click()
    time.sleep(2)
    pyautogui.write(meetPassword)
    pyautogui.press('enter')
    """
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
    schList = []
    meetingID, password, time_ = "", "", ""
    for i in y:
        a, b = i['TimeFrom'].split("-")[0].strip(" ").split(" ")
        time_ = convert24Hours(a[0:a.index(":")], b)
        meetingID, password = i["JoinUrl"][18::].split("?pwd=")
        message = f'schedule.every().day.at("{time_}").do(SignIn,"{meetingID}","{password}")'
        schList.append(message)
    with open("tt.py", 'w') as f:
        f.write(fortt)
        f.write("\ndef setSch4tt():\n")
        for i in schList:
            f.write("\t"+i+"\n")
getTimeTable()
from tt import setSch4tt
setSch4tt()
pprint.pprint(schedule.jobs)
while True:
    schedule.run_pending()
    time.sleep(1)
