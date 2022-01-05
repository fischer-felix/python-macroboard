from evdev import InputDevice, categorize, ecodes
import evdev
import os
import re
import pyautogui
import overrides

dev = InputDevice('/dev/input/by-id/usb-04d9_1400-event-kbd')


devlist = os.listdir('/dev/input/by-id/')
r = re.compile('.*kbd')
newdevlist = list(filter(r.match, devlist))




#print(dev)
dev.grab()

def main():

    for event in dev.read_loop():

        if event.type == ecodes.EV_KEY:

            key = categorize(event)

            if key.keystate == key.key_down:

                symbol = str.removeprefix(key.keycode, 'KEY_')

                funcname = '_' + symbol

                print(symbol)
                print(funcname)

                if funcname in dir(overrides):

                    print('Override exists, using key combination from overrides.py')

                    overrides.__dict__[funcname]()

                else:

                    print('No override found, using default modifier keys')

                    pyautogui.keyDown('ctrl')

                    pyautogui.keyDown('shift')

                    pyautogui.keyDown('alt')

                    pyautogui.keyDown('winleft')

                    pyautogui.press(symbol)

                    pyautogui.keyUp('ctrl')

                    pyautogui.keyUp('shift')

                    pyautogui.keyUp('alt')

                    pyautogui.keyUp('winleft')


# main()

# with open('overrides.py', "a+") as f:
#                     f.seek(0)
#                     data = f.read(100)
#                     if len(data) > 0:
#                         f.write("\n\n")
#                     elif len(data) == 0:
#                         f.write('import pyautogui\n\n')
#                     f.write("def " + symbol + "():\n")
#                     f.write("    pyautogui.keyDown('" + 'ctrl' + "')\n")
#                     f.write("    pyautogui.keyDown('" + 'shift' + "')\n")
#                     f.write("    pyautogui.keyDown('" + 'alt' + "')\n")
#                     f.write("    pyautogui.press('" + symbol + "')\n")
#                     f.write("    pyautogui.keyUp('" + 'alt' + "')\n")
#                     f.write("    pyautogui.keyUp('" + 'shift' + "')\n")
#                     f.write("    pyautogui.keyUp('" + 'ctrl' + "')\n")