import pyautogui
import time

time.time()
x=0
time.sleep(4)
def forage():
    pyautogui.press("5")
    pyautogui.rightClick()
    pyautogui.rightClick()
    pyautogui.keyDown("a")
    time.sleep(.001)
    pyautogui.keyUp("a")
    pyautogui.rightClick()

    pyautogui.rightClick()
    pyautogui.keyDown("d")
    time.sleep(.001)
    pyautogui.keyUp("d")
    
    pyautogui.press("3")
    pyautogui.rightClick()
    pyautogui.press("2")
    time.sleep(0.05)
    pyautogui.click()
    time.sleep(.2)
    global x
    x +=1
i = True
while i is True:
    forage()
    print(f"{x} trees broken")