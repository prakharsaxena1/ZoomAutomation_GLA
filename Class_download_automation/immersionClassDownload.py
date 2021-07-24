# IMPORTS
from datetime import date, timedelta
import os
import requests
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
import pyautogui

# Constants
sessionID = input("Enter sessionID: ")
todayDate = date.today()
url = "https://glauniversity.in:8085/MyAccount/PREPDutyDetails"
GYOC = {"ASP.NET_SessionId": sessionID}
dateList =[]
allList = []


# linksFile
if not os.path.exists("reclinks.txt"):
    open("reclinks.txt", 'w').close()
else:
    os.remove("./reclinks.txt")

# Folder
if not os.path.exists("dump"):
    os.mkdir("dump")



monthMap = {
    "01": "JAN",
    "02": "FEB",
    "03": "MAR",
    "04": "APR",
    "05": "MAY",
    "06": "JUN",
    "07": "JUL",
    "08": "AUG",
    "09": "SEP",
    "10": "OCT",
    "11": "NOV",
    "12": "DEC"
}
# Functions
def getUpperChar(s):
    m=''
    for i in s:
        if i.isupper():
            m+=i
    return m

def downloadAll():
    partCount = 1
    with open("./reclinks.txt") as f:
        for i in f.readlines():
            if i !="\n":
                isplit = i.strip("\n").split("*")
                if isplit[2] != "":
                    sub=getUpperChar(isplit[0])
                    if sub=="S":
                        sub="SQL"
                    elif sub=="ADSAA":
                        sub="ADSA"
                    downloadName = f"{sub} {isplit[1].split('.')[0]} {monthMap[isplit[1].split('.')[1]]}"
                    isplit2 = isplit[2].split(",")
                    if len(isplit2) > 1:
                        for j in isplit2:
                            temp = downloadName + " part " + str(partCount)
                            allList.append([temp, j])
                            partCount+=1
                    else:
                        allList.append([downloadName, isplit[2]])
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": "./dump/",
        "download.prompt_for_download": True
    })
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="./chromedriver.exe")
    for i in allList:
        driver.get(i[1])
        time.sleep(5)
        a = driver.find_element_by_class_name("download-btn")
        a.click()
        time.sleep(7)
        print("Downloading: ",i[0])
        pyautogui.write(i[0])
        pyautogui.press('enter')
        time.sleep(5)

# Main
def getData():
    fromDate = int(input("How many days ago from today: "))
    for i in range(fromDate,0,-1):
        dateList.append(todayDate - timedelta(i))
    dateList.append(todayDate)
    for i in dateList:
        data = {"text": i}
        r = requests.post(url, data=data, cookies=GYOC)
        try:
            x = r.json()
        except requests.RequestException as e2:
            print(e2)
        with open("reclinks.txt", 'a') as file:
            for i in x:
                if i['SubName'] == None:
                    break
                else:
                    file.write(f"\n{i['SubName']}*{i['ScheduleDate']}*{i['Recording']}\n")
    downloadAll()

getData()
