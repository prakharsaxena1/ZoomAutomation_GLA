from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import datetime
import json
import requests
import os
import time
import pyautogui


def get_data():
    sessionID = "wcmqrkcvvns3vmyloxo11rrl"
    url = "https://glauniversity.in:8085/MyAccount/DutyDetails"
    GYOC = {"ASP.NET_SessionId": sessionID}
    datafile = open("datafile.txt", "w")
    datafile.close()
    fromDate = int(input("How many days ago from today: "))
    todayDate = datetime.date.today()
    if not os.path.exists("data-dump"):
        os.mkdir("data-dump")
    for i in range(fromDate, 0, -1):
        d = datetime.timedelta(days=i)
        date = todayDate - d
        data = {"text": date}
        r = requests.post(url, data=data, cookies=GYOC)
        try:
            with open(f"data-dump/all{date}.json", 'w') as f:
                f.write(r.text)
        except json.decoder.JSONDecodeError as e:
            print("SessionID has expired, will need a new one in order to continue")
            exit()
        with open(f"data-dump/all{date}.json", 'r') as f:
            y = json.load(f)
        with open("datafile.txt", 'a') as file:
            for i in y:
                if i['SubName'] == None:
                    break
                else:
                    file.write(
                        f"{i['SubName']}*{i['ScheduleDate']}*{i['Recording']}\n")
    print("done")

get_data()


subMap = {
    "It Business Continuity & Disaster Recovery": "IT",
    "Air And Noise Pollution Control": "AANP",
    "Digital Forensics": "DF",
    "Gla Coding Foundation League": "GCFL",
    "Advanced Ds & Algorithms": "ADSA",
    "Disaster Management": "DM",
    "Verbal Aptitude": "VA",
    "Quant & Reasoning Aptitude": "Quant",
    "Coding & Programming Aptitude": "CAPA",
    "Group Discussion & Personal Interview": "GDPI"
}
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
allList = []

chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": "/data-dump/",
    "download.prompt_for_download": True
})
chromeDriverPath = "chromedriver.exe"
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="chromedriver.exe")
with open("datafile.txt", 'r') as f:
    for i in f.readlines():
        allList.append(i.split("*"))

for i in allList:
    subName = i[0]
    date = i[1].split(".")[0]
    month = monthMap[i[1].split(".")[1]]
    link = i[2].strip("\n")
    if len(link)<2:
        continue
    else:
        driver.get(link)
        time.sleep(5)
        a = driver.find_element_by_class_name("download-btn")
        a.click()
        time.sleep(8)
        writeThis = subMap[subName].upper() + " " + date +" " + month.upper()
        print("Downloading:",writeThis)
        pyautogui.write(writeThis)
        pyautogui.press('enter')
