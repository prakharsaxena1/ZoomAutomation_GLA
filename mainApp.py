# chrome://settings/cookies/detail?site=glauniversity.in&search=cookies
# C:\Users\prakh\AppData\Local\Google\Chrome\User Data\Default
# Session ID:  pysl2rgq2odca1vk0d4z3yvo

import time
import datetime
import requests
import json
import subprocess
from pynput.keyboard import Key, Controller
import schedule
import pyautogui
import os


def convert24Hours(number, x):
    number = number[0:2]
    if x == "AM":
        return number
    return int(number) + 12


def tabenter():
    keyboard = Controller()
    keyboard.press(Key.tab)
    keyboard.release(Key.tab)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)


def SignIn(meetID, meetPassword):
    subprocess.call(["C:/Users/prakh/AppData/Roaming/Zoom/bin/Zoom.exe"])
    time.sleep(10)
    # Big join button
    join_btn = pyautogui.locateCenterOnScreen('join1.png')
    pyautogui.moveTo(join_btn)
    pyautogui.click()
    # Meeting ID
    time.sleep(2)
    pyautogui.write(meetID)
    # Disables: camera and mic
    media_btn = pyautogui.locateAllOnScreen('cb.png')
    for btn in media_btn:
        pyautogui.moveTo(btn)
        pyautogui.click()
    tabenter()
    pyautogui.moveTo(join_btn)
    pyautogui.click()
    time.sleep(2)
    # Types the password and hits enter
    pyautogui.write(meetPassword)
    pyautogui.press('enter')


def getTimeTable():
    sessionID = "pysl2rgq2odca1vk0d4z3yvo"  # For testing purposes
    # sessionID = input("Enter session ID:  ")
    date = "2020-12-1"  # For testing purposes
    # date = input("Enter date(FORMAT: YYYY-MM-D,no preceeding zeros):  ")
    GYOC = {"ASP.NET_SessionId": sessionID}
    data = {"text": date}
    url = "https://glauniversity.in:8085/MyAccount/DutyDetails"
    r = requests.post(url, data=data, cookies=GYOC)
    y = json.loads(r.text)
    X = []
    for i in y:
        number, x = i["TimeFrom"].split(" - ")[0].split(" ")
        timed = convert24Hours(number, x)
        meetingID, password = i["JoinUrl"][18::].split("?pwd=")
        X.append([str(timed), meetingID, password])
    X.sort()
    timetable = open("timetable.txt", 'w')
    for i in X:
        timetable.write(str(i).replace("'", "").replace("]", "").replace("[", "")+"\n")
    timetable.write("end, end, end")
    timetable.close()
    print("Timetable loaded")


def getIDPasswd(now):
    meetID = ""
    meetPasswd = ""
    f = open("timetable.txt", 'r')
    for i in f.readlines():
        j = i.split(",")
        if j[0] == "end":
            f.close()
            os.remove("timetable.txt")
            print("Exiting App...")
            exit()
        elif int(j[0]) < int(now):
            continue
        else:
            meetID, meetPasswd = j[1].strip(" "), j[2].strip("\n").strip(" ")
            break
    return (meetID, meetPasswd)

if not os.path.exists("timetable.txt"):
    getTimeTable()

now = 12  # For testing purposes
# now = datetime.datetime.now().strftime("%H")
meetID, meetPasswd = getIDPasswd(now)
print(meetID, meetPasswd)

