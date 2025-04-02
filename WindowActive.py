import pyautogui
import time

pyautogui.FAILSAFE = False

while True:
    pyautogui.press('shift')  # Press the Shift key
    time.sleep(60)            # Wait for 60 seconds before sending the next signal
