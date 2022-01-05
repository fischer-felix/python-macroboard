from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QSystemTrayIcon, QMenu, QAction, QColorDialog
from PyQt5.QtGui import QIcon

import sys

from random import randint


class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window % d" % randint(0,100))
        layout.addWidget(self.label)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.w = AnotherWindow()

        tray = QSystemTrayIcon()
        tray.setIcon(QIcon('bug.png'))
        tray.setVisible(True)

        menu = QMenu()
        option1 = QAction("Hex")
        option2 = QAction("RGB")
        menu.addAction(option1)
        menu.addAction(option2)

        tray.setContextMenu(menu)

        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.toggle_window)
        self.setCentralWidget(self.button)


    def toggle_window(self, checked):
        if self.w.isVisible():
            self.w.hide()

        else:
            self.w.show()



app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
