import pyautogui

def D():
    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('shift')
    pyautogui.keyDown('alt')
    pyautogui.press('D')
    pyautogui.keyUp('alt')
    pyautogui.keyUp('shift')
    pyautogui.keyUp('ctrl')
