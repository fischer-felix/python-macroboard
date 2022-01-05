import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider, QPushButton, QVBoxLayout
)
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, pyqtSlot
import os
import re
import macroboard

devlist = os.listdir('/dev/input/by-id/')
r = re.compile('.*kbd')
newdevlist = list(filter(r.match, devlist))
print(newdevlist)


class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run(self):
        macroboard.main()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        button = QPushButton('Run')
        button.clicked.connect(self.on_click)

        self.setCentralWidget(button)


    # def index_changed(self, i):
    #     print(i)

    # def value_changed_str(self, s):
    #     print(s)

    def on_click(self):
        self.thread = QThread()

        self.worker = Worker()

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.thread.deleteLater)

        self.thread.start()




        



app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
    
