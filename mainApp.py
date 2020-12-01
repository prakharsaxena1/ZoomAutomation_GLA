# chrome://settings/cookies/detail?site=glauniversity.in&search=cookies
# C:\Users\prakh\AppData\Local\Google\Chrome\User Data\Default
# Session ID:  ireedt31vdhs4f2qto13ggk0

import time
import datetime
import requests
import json
import subprocess
from pynput.keyboard import Key, Controller
import pyperclip
import schedule


def hitEnter(keyboard):
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)


def hitPaste(keyboard):
    keyboard.press(Key.ctrl_l)
    keyboard.press('v')
    keyboard.release(Key.ctrl_l)
    keyboard.release('v')


def convert24Hours(number, x):
    number = number[0:2]
    if x == "AM":
        return number
    return int(number) + 12

def checkTime():
    a = str(datetime.datetime.now())
    return a.split(" ")[1][0:2]
    
def SignIn(meetID, meetPassword):
    subprocess.call(["C:/Users/prakh/AppData/Roaming/Zoom/bin/Zoom.exe"])
    time.sleep(10)
    keyboard = Controller()
    pyperclip.copy(meetID)
    for i in range(7):
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
    time.sleep(5)
    hitEnter(keyboard)
    hitPaste(keyboard)
    hitEnter(keyboard)
    pyperclip.copy(meetPassword)
    time.sleep(5)
    hitPaste(keyboard)
    for i in range(2):
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
    hitEnter(keyboard)


sessionID = "ireedt31vdhs4f2qto13ggk0"
# sessionID = input("Enter session ID:  ")
date = "2020-12-1"
# date = input("Enter date(FORMAT: YYYY-MM-D,no preceeding zeros):  ")
GYOC = {"ASP.NET_SessionId": sessionID}
data = {"text": date}
url = "https://glauniversity.in:8085/MyAccount/DutyDetails"
r = requests.post(url, data=data, cookies=GYOC)
y = json.loads(r.text)

X = []
for i in y:
    number, x = i["TimeFrom"].split(" - ")[0].split(" ")
    time = convert24Hours(number, x)
    meetingID, password = i["JoinUrl"][18::].split("?pwd=")
    X.append([str(time), meetingID, password])
X.sort()
timetable = open("timetable.txt", 'w')
for i in X:
    timetable.write(str(i).replace("'", "").replace(
        "]", "").replace("[", "")+"\n")
timetable.write("end, end, end")
timetable.close()

schedule.every().hour.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
