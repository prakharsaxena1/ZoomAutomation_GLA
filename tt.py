
import subprocess
import time
import pyautogui
import schedule

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
    
def setSch4tt():
	schedule.every().day.at("10:00").do(SignIn,"95252998034","aHFFTnZwaTgwb1RmYkxGQWhVbTUrQT09")
	schedule.every().day.at("14:00").do(SignIn,"94407499085","SGs5WXNOUmRoZElXL0VQNU5RbzBQZz09")
	schedule.every().day.at("15:00").do(SignIn,"98591665353","bG9RL3dSSDAyaU1DdUx6bG02VnM4UT09")
	schedule.every().day.at("13:00").do(SignIn,"95116198894","MDhLNkhscVA5UVA0dnhSQy9aZFdsdz09")
	schedule.every().day.at("08:00").do(SignIn,"95109570696","a08rWnlOTWx2R3ZhVUdGbG5kWERRQT09")
	schedule.every().day.at("11:00").do(SignIn,"96645802879","cytlcEdCUnl3TkdjNG5yOEkycHAvUT09")
