import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider
)
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("My App")
        widget = QDoubleSpinBox()
        widget.setMinimum(-10)
        widget.setMaximum(3)
        widget.setPrefix("$")
        widget.setSuffix("c")
        widget.setSingleStep(3)
        widget.valueChanged.connect(self.value_changed)
        widget.textChanged.connect(self.value_changed_str)
        self.setCentralWidget(widget)
    def value_changed(self, i):
        print(i)
    def value_changed_str(self, s):
        print(s)
app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
    
