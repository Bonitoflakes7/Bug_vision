import pyautogui
import time

print("Move your mouse to TOP-LEFT of the region...")
time.sleep(5)
x1, y1 = pyautogui.position()
print("Top-left corner:", x1, y1)

print("Now move to BOTTOM-RIGHT...")
time.sleep(5)
x2, y2 = pyautogui.position()
print("Bottom-right corner:", x2, y2)
