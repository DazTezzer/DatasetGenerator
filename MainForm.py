from PyQt5 import QtWidgets, QtGui, QtCore
import sys

from DataGenerateTab import DataGenerateTab
from ui.UI_MainWindow import Ui_MainWindow


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.generatorTab = DataGenerateTab(self.ui)


app = QtWidgets.QApplication([])
application = MyWindow()
application.show()
sys.exit(app.exec())
