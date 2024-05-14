import os

from PyQt5 import QtWidgets
import sys

from tabs.dataGenerateTab.DataGenerateTab import DataGenerateTab
from tabs.GlobalExceptionHandler import GlobalExceptionHandler
from tabs.modelTrainingTab.ModelTrainingTab import ModelTrainingTab
from ui.UI_MainWindow import Ui_MainWindow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_USE_CUDNN'] = '1'
class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.generatorTab = DataGenerateTab(self.ui)
        self.ui.trainingTab = ModelTrainingTab(self.ui)
        self.ui.globalExceptionHandlerPlainTextEdit.setReadOnly(True)



app = QtWidgets.QApplication([])
application = MyWindow()
global_handler = GlobalExceptionHandler(application.ui)
application.show()
sys.exit(app.exec())
