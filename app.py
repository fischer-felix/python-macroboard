import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider, QPushButton, QVBoxLayout, QHBoxLayout, QToolBar, QAction, QWidget,
    QSystemTrayIcon, qApp, QMenu, QMessageBox
)
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, pyqtSlot, QSize
from PyQt5.QtGui import QIcon, QKeySequence
from evdev import InputDevice, categorize, ecodes
import pyautogui
import os
import re
from time import sleep
import json
import sqlite3


conn = sqlite3.connect('macroboard.db')

conn.execute('''CREATE TABLE IF NOT EXISTS OVERRIDES
       (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
       KEY          TEXT        NOT NULL,
       SHIFT        INT         NOT NULL,
       CTRL         INT         NOT NULL,
       META         INT         NOT NULL,
       ALT          INT         NOT NULL,
       COMMAND      TEXT        NOT NULL);''')

conn.execute('''CREATE TABLE IF NOT EXISTS STATES
         (ID INT PRIMARY KEY     NOT NULL,
         TRAY           INT          NOT NULL,
         DEVICE         TEXT         NOT NULL);''')



devlist = os.listdir('/dev/input/by-id/')   # list input devices and filter out keyboards
r = re.compile('.*kbd')
newdevlist = list(filter(r.match, devlist))
print(newdevlist)



class runReplacement(QThread):                      # Start worker for backend task (listening for keyboard input & replacing it)

    def __init__(self, device):
        QThread.__init__(self)
        self.device = device
        print(self.device)

        self.dev = InputDevice('/dev/input/by-id/' + self.device)
        print(self.dev)

        self.dev.grab()

    def __del__(self):
        self.wait()

    def run(self):

        c = sqlite3.connect('macroboard.db')

        for event in self.dev.read_loop():
            if event.type == ecodes.EV_KEY:

                key = categorize(event)

                if key.keystate == key.key_down:

                    print(key.keycode)

                    symbol = str.removeprefix(key.keycode, 'KEY_')
                    print(symbol)

                    if c.execute("SELECT * FROM OVERRIDES WHERE KEY = ?", (symbol,)).fetchone():
                        print("Override exists, using it over default")
                        
                        cursor = c.execute("SELECT * FROM OVERRIDES WHERE KEY = ?", (symbol,))
                        for row in cursor:
                            key_db = row[1]
                            shift_db = row[2]
                            ctrl_db = row[3]
                            meta_db = row[4]
                            alt_db = row[5]
                            command_db = row[6]
                            print(key_db, shift_db, ctrl_db, meta_db, alt_db, command_db)

                            if command_db != '':
                                print("Executing system command")
                                os.system(command_db + " &")
                            else:
                                # pyautogui.keyDown('ctrl')
                                # pyautogui.keyDown('shift')
                                # pyautogui.keyDown('alt')
                                # pyautogui.keyDown('winleft')
                                # pyautogui.press(symbol)
                                # pyautogui.keyUp('ctrl')
                                # pyautogui.keyUp('shift')
                                # pyautogui.keyUp('alt')
                                # pyautogui.keyUp('winleft')

                                if shift_db == 2:
                                    print("holding shift")
                                    pyautogui.keyDown('shift')
                                if ctrl_db == 2:
                                    print("holding ctrl")
                                    pyautogui.keyDown('ctrl')
                                if meta_db == 2:
                                    print("holding meta")
                                    pyautogui.keyDown('winleft')
                                if alt_db == 2:
                                    print("holding alt")
                                    pyautogui.keyDown('alt')
                                if key_db != '':
                                    print("pressing key")
                                    pyautogui.press(symbol)
                                if shift_db == 2:
                                    print("releasing shift")
                                    pyautogui.keyUp('shift')
                                if ctrl_db == 2:
                                    print("releasing ctrl")
                                    pyautogui.keyUp('ctrl')
                                if meta_db == 2:
                                    print("releasing meta")
                                    pyautogui.keyUp('winleft')
                                if alt_db == 2:
                                    print("releasing alt")
                                    pyautogui.keyUp('alt')


                        
                    else:
                        print("No override found, using default modifier keys")
                        pyautogui.keyDown('ctrl')
                        pyautogui.keyDown('shift')
                        pyautogui.keyDown('alt')
                        pyautogui.keyDown('winleft')
                        pyautogui.press(symbol)
                        pyautogui.keyUp('ctrl')
                        pyautogui.keyUp('shift')
                        pyautogui.keyUp('alt')
                        pyautogui.keyUp('winleft')



              



class Card(QVBoxLayout):
    def __init__(self, character, shift, ctrl, meta, alt, command):
        super(Card, self).__init__()

        self.character = ''
        self.modlist = []
        self.command = ''
        

        with open('charlist.txt', 'r') as f:
            self.charlist = json.load(f)

        hlayout1 = QHBoxLayout()
        hlayout2 = QHBoxLayout()


        self.keyselector = QComboBox()           # Create and add widgets to first layout
        self.keyselector.addItems(self.charlist)
        if character != 'default':
            self.keyselector.setCurrentText(character)
        self.keyselector.currentTextChanged.connect(self.character_changed)

        self.checkbox_shift = QCheckBox("Shift")
        if shift != 'default':
            self.checkbox_shift.setCheckState(shift)
        self.checkbox_shift.stateChanged.connect(self.checkbox_shift_changed)

        self.checkbox_ctrl = QCheckBox("Ctrl")
        if ctrl != 'default':
            self.checkbox_ctrl.setCheckState(ctrl)
        self.checkbox_ctrl.stateChanged.connect(self.checkbox_ctrl_changed)

        self.checkbox_meta = QCheckBox("Meta")
        if meta != 'default':
            self.checkbox_meta.setCheckState(meta)
        self.checkbox_meta.stateChanged.connect(self.checkbox_meta_changed)

        self.checkbox_alt = QCheckBox("Alt")
        if alt != 'default':
            self.checkbox_alt.setCheckState(alt)
        self.checkbox_alt.stateChanged.connect(self.checkbox_alt_changed)

        hlayout1.addWidget(self.keyselector)
        hlayout1.addWidget(self.checkbox_shift)
        hlayout1.addWidget(self.checkbox_ctrl)
        hlayout1.addWidget(self.checkbox_meta)
        hlayout1.addWidget(self.checkbox_alt)


        self.addLayout(hlayout1)


        self.commandbox = QLineEdit()
        self.commandbox.setPlaceholderText("Enter command here")
        if command != '':
            self.commandbox.setText(command)
            self.checkbox_shift.setEnabled(False)
            self.checkbox_ctrl.setEnabled(False)
            self.checkbox_meta.setEnabled(False)
            self.checkbox_alt.setEnabled(False)
        self.commandbox.textChanged.connect(self.text_changed)

        savebutton = QPushButton("Save")
        savebutton.clicked.connect(self.save)

        hlayout2.addWidget(QLabel("Custom:"))
        hlayout2.addWidget(self.commandbox)
        hlayout2.addWidget(savebutton)

        self.addLayout(hlayout2)




    def character_changed(self, s):                 # Slots for signals from override configuration
        print(s)
        self.character = s

    def checkbox_shift_changed(self, i):
        print(i)

    def checkbox_ctrl_changed(self, i):
        print(i)

    def checkbox_meta_changed(self, i):                  # winleft is the name for the metakey in the pyautogui library
        print(i)

    def checkbox_alt_changed(self, i):
        print(i)

    def text_changed(self, s):
        print(s)
        if s != '':
            self.checkbox_shift.setEnabled(False)
            self.checkbox_ctrl.setEnabled(False)
            self.checkbox_meta.setEnabled(False)
            self.checkbox_alt.setEnabled(False)
        else:
            self.checkbox_shift.setEnabled(True)
            self.checkbox_ctrl.setEnabled(True)
            self.checkbox_meta.setEnabled(True)
            self.checkbox_alt.setEnabled(True)


    def save(self):

        key = self.keyselector.currentText()

        shift = self.checkbox_shift.checkState()
        ctrl = self.checkbox_ctrl.checkState()
        meta = self.checkbox_meta.checkState()
        alt = self.checkbox_alt.checkState()

        command = self.commandbox.text()

        cursor = conn.execute("SELECT * FROM OVERRIDES")
        for row in cursor:
            key_db = row[1]
            shift_db = row[2]
            ctrl_db = row[3]
            meta_db = row[4]
            alt_db = row[5]
            command_db =  row[6]

        if key_db == key:
            conn.execute("UPDATE OVERRIDES SET SHIFT = ?, CTRL = ?, META = ?, ALT = ?, COMMAND = ? WHERE KEY = ?", (shift, ctrl, meta, alt, command, key))
        else:   
            conn.execute("INSERT INTO OVERRIDES (KEY, SHIFT, CTRL, META, ALT, COMMAND) \
            VALUES (?, ?, ?, ?, ?, ?);", (key, shift, ctrl, meta, alt, command))

        conn.commit()

        print("Saved")

        



        


    

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Macroboard")

        self.vlayout = QVBoxLayout()


        cursor = conn.execute("SELECT * FROM OVERRIDES")
        for row in cursor:
            key = row[1]
            shift = row[2]
            ctrl = row[3]
            meta = row[4]
            alt = row[5]
            command =  row[6]
            print(key, shift, ctrl, meta, alt, command)

            self.vlayout.addLayout(Card(key, shift, ctrl, meta, alt, command))


        self.addcardbutton = QPushButton("Add Override")
        self.addcardbutton.setIcon(QIcon.fromTheme("list-add"))
        self.addcardbutton.clicked.connect(self.add_card)
        self.vlayout.addWidget(self.addcardbutton)


        widget = QWidget()
        widget.setLayout(self.vlayout)
        self.setCentralWidget(widget)


        toolbar = QToolBar("Toolbar")       # Create toolbar
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        self.devselector = QComboBox()           # Create combobox for selecting input device
        self.devselector.addItems(newdevlist)
        self.devselector.currentTextChanged.connect(self.devselector_changed)
        toolbar.addWidget(self.devselector)

        toolbar.addSeparator()

        self.startbutton_action = QAction(QIcon.fromTheme("media-playback-start"), "Start", self)    # Create start button
        self.startbutton_action.triggered.connect(self.on_click)
        self.running = False
        toolbar.addAction(self.startbutton_action)




        self.tray_icon = QSystemTrayIcon(self)                  # Create system tray icon
        self.tray_icon.setIcon(QIcon.fromTheme('input-keyboard-symbolic'))
        self.tray_icon.activated.connect(self.tray_click)

        show_action = QAction("Show", self)
        hide_action = QAction("Hide", self)
        quit_action = QAction("Quit", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(qApp.quit)

        tray_menu = QMenu()
        tray_menu.addAction(self.startbutton_action)
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()



        menu = self.menuBar()                   # Create menu bar

        file_menu = menu.addMenu("&File")
        file_menu.addAction(self.startbutton_action)

        self.tray_enabled_action = QAction("Tray Enabled", self, checkable=True)
        self.tray_enabled_action.setChecked(True)
        file_menu.addAction(self.tray_enabled_action)
        file_menu.addAction(hide_action)
        file_menu.addAction(quit_action)



    def add_card(self):
        print("add card")
        self.vlayout.removeWidget(self.addcardbutton)
        self.vlayout.addLayout(Card('default', 'default', 'default', 'default', 'default', ''))
        self.vlayout.addWidget(self.addcardbutton)

    def devselector_changed(self, s):
        print(s)


    def on_click(self):
        print(self.running)
        if self.running == False:
            self.running = True
            self.startbutton_action.setIcon(QIcon.fromTheme("media-playback-stop"))
            self.startbutton_action.setText("Stop")


            self.replaceThread = runReplacement(self.devselector.currentText())

            self.replaceThread.start()    


        elif self.running == True:
            self.running = False
            self.startbutton_action.setIcon(QIcon.fromTheme("media-playback-start"))
            self.startbutton_action.setText("Start")
            
            self.replaceThread.dev.ungrab()

            self.replaceThread.terminate()


        

    def tray_click(self):
        print("tray click")
        self.show()

    def closeEvent(self, event):
        if self.tray_enabled_action.isChecked():
            self.hide()
            event.ignore()
        else:
            qApp.quit()

        

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()





