import time
import pyautogui

loc1 = 320,564
loc2 = 356,564
loc3 = 392,564
loc4 = 426,564
loc5 = 462,564
loc6 = 500,564
loc7 = 536,564
time.sleep(3.5)
t=  0.25
def click(loc,sleep):
    if sleep < 0:
        sleep = 0.1  # Set to 0 to avoid the error
    pyautogui.moveTo(loc)
    pyautogui.press("q")
    time.sleep(sleep)

click(loc=loc7,sleep=t*2-0.2)
click(loc=loc6,sleep=t*2-0.2)
click(loc=loc5,sleep=t-0.2)
click(loc=loc4,sleep=t*3-0.2)
click(loc=loc4,sleep=t*2-0.2)
click(loc=loc3,sleep=t*2-0.2)
click(loc=loc2,sleep=t-0.2)
click(loc=loc1,sleep=t*3-0.2)
click(loc=loc4,sleep=t-0.2)
click(loc=loc5,sleep=t*3-0.2)
click(loc=loc5,sleep=t-0.2)
click(loc=loc6,sleep=t*3-0.2)
click(loc=loc6,sleep=t-0.2)
click(loc=loc7,sleep=t*3-0.2)
click(loc=loc7,sleep=t-0.2)
click(loc=loc7,sleep=t-0.2)
click(loc=loc6,sleep=t-0.2)
click(loc=loc5,sleep=t-0.2)
click(loc=loc4,sleep=t*2-0.2)
click(loc=loc4,sleep=t-0.2)
click(loc=loc4,sleep=t-0.2)
click(loc=loc3,sleep=t-0.2)
click(loc=loc2,sleep=t-0.2)
click(loc=loc1,sleep=t-0.2)
click(loc=loc3,sleep=t-0.2)
click(loc=loc5,sleep=t-0.2)
click(loc=loc7,sleep=t-0.2)




