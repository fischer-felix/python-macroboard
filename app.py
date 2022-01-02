import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider, QPushButton, QVBoxLayout, QHBoxLayout, QToolBar, QAction, QWidget
)
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, pyqtSlot, QSize
from PyQt5.QtGui import QIcon, QKeySequence
import os
import re
import macroboard
import overrides




devlist = os.listdir('/dev/input/by-id/')   # list input devices and filter out keyboards
r = re.compile('.*kbd')
newdevlist = list(filter(r.match, devlist))
print(newdevlist)




class Worker(QObject):                      # Start worker for backend task (listening for keyboard input & replacing it)
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run(self):
        macroboard.main()




class Card(QVBoxLayout):
    def __init__(self):
        super(Card, self).__init__()

        hlayout1 = QHBoxLayout()
        hlayout2 = QHBoxLayout()


        keyselector = QComboBox()           # Create and add widgets to first layout
        keyselector.addItems(["a", "b", "c"])
        keyselector.currentTextChanged.connect(self.character_changed)

        checkbox_shift = QCheckBox("Shift")
        checkbox_shift.stateChanged.connect(self.checkbox_shift_changed)

        checkbox_ctrl = QCheckBox("Ctrl")
        checkbox_ctrl.stateChanged.connect(self.checkbox_ctrl_changed)

        checkbox_meta = QCheckBox("Meta")
        checkbox_meta.stateChanged.connect(self.checkbox_meta_changed)

        checkbox_alt = QCheckBox("Alt")
        checkbox_alt.stateChanged.connect(self.checkbox_alt_changed)

        hlayout1.addWidget(keyselector)
        hlayout1.addWidget(checkbox_shift)
        hlayout1.addWidget(checkbox_ctrl)
        hlayout1.addWidget(checkbox_meta)
        hlayout1.addWidget(checkbox_alt)


        self.addLayout(hlayout1)


        commandbox = QLineEdit()
        commandbox.setPlaceholderText("Enter command here")
        commandbox.textChanged.connect(self.text_changed)

        savebutton = QPushButton("Save")
        savebutton.clicked.connect(self.save)

        hlayout2.addWidget(QLabel("Custom:"))
        hlayout2.addWidget(commandbox)
        hlayout2.addWidget(savebutton)

        self.addLayout(hlayout2)

    def character_changed(self, s):                 # Slots for signals from override configuration
        print(s)
        with open('overrides.py', "a+") as f:
                    f.seek(0)
                    data = f.read(100)
                    if len(data) > 0:
                        f.write("\n\n")
                    elif len(data) == 0:
                        f.write('import pyautogui\n\n')
                    f.write("def " + s + "():\n")
                    f.write("    pyautogui.keyDown('" + 'ctrl' + "')\n")
                    f.write("    pyautogui.keyDown('" + '' + "')\n")
                    f.write("    pyautogui.keyDown('" + 'alt' + "')\n")
                    f.write("    pyautogui.press('" + s + "')\n")
                    f.write("    pyautogui.keyUp('" + 'alt' + "')\n")
                    f.write("    pyautogui.keyUp('" + '' + "')\n")
                    f.write("    pyautogui.keyUp('" + 'ctrl' + "')\n")

    def checkbox_shift_changed(self, i):
        print(i)

    def checkbox_ctrl_changed(self, i):
        print(i)

    def checkbox_meta_changed(self, i):
        print(i)

    def checkbox_alt_changed(self, i):
        print(i)

    def text_changed(self, s):
        print(s)

    def save(self):
        print("save")
        


    

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Macroboard")

        self.vlayout = QVBoxLayout()

        

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

        devselector = QComboBox()           # Create combobox for selecting input device
        devselector.addItems(newdevlist)
        devselector.currentTextChanged.connect(self.devselector_changed)
        toolbar.addWidget(devselector)

        toolbar.addSeparator()

        self.startbutton_action = QAction(QIcon.fromTheme("media-playback-start"), "Start", self)    # Create start button
        self.startbutton_action.triggered.connect(self.on_click)
        self.running = False
        toolbar.addAction(self.startbutton_action)

        menu = self.menuBar()

        file_menu = menu.addMenu("&File")
        file_menu.addAction(self.startbutton_action)


    def add_card(self):
        print("add card")
        self.vlayout.removeWidget(self.addcardbutton)
        self.vlayout.addLayout(Card())
        self.vlayout.addWidget(self.addcardbutton)

    def devselector_changed(self, s):
        print(s)

    def on_click(self):
        print(self.running)
        if self.running == False:
            self.running = True
            self.startbutton_action.setIcon(QIcon.fromTheme("media-playback-stop"))
            self.startbutton_action.setText("Stop")

        elif self.running == True:
            self.running = False
            self.startbutton_action.setIcon(QIcon.fromTheme("media-playback-start"))
            self.startbutton_action.setText("Start")

        

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()





