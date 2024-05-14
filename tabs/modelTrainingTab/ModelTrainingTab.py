import os

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QMessageBox

from ProgressDialog import ProgressDialog
from ui.UI_MainWindow import Ui_MainWindow
from tabs.modelTrainingTab.TrainingUtils import ModelTrainingProcessingThread

class ModelTrainingTab(QtWidgets.QWidget):
    def __init__(self, main_window_ui: Ui_MainWindow):
        super().__init__()
        self.ui = main_window_ui
        self.ui.tabWidget.currentChanged.connect(self.onTabChanged)
        self.ui.datasetListUpdateButton.clicked.connect(self.updateDatasetList)
        self.ui.modelStartTrainingButton.clicked.connect(self.showConfirmationDialog)

        self.listModel = QStringListModel()
        self.ui.datasetListView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.ui.datasetListView.setModel(self.listModel)
        self.ui.datasetListView.selectionModel().selectionChanged.connect(self.onSelectionChanged)

        self.datasetFolderPath = None


    def onTabChanged(self, index):
        if index == 1:
            self.updateDatasetList()

    def onSelectionChanged(self):
        self.datasetFolderPath = os.path.join(os.getcwd(),self.ui.datasetListView.currentIndex().data())


    def updateDatasetList(self):
        rootDirectory = os.getcwd()
        datasetFolders = [folder for folder in os.listdir(rootDirectory) if
                           os.path.isdir(os.path.join(rootDirectory, folder)) and folder.startswith("Dataset")]
        self.listModel.setStringList(datasetFolders)
        self.ui.datasetListView.setModel(self.listModel)

    def showConfirmationDialog(self):
        self.setDisabled(True)

        reply = QMessageBox.question(self, 'Подтверждение действия обучение модели',
                                     'Вы уверены, что хотите осуществить обучение модели?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            if  self.datasetFolderPath :
                thread = ModelTrainingProcessingThread(self.datasetFolderPath)
                dialog = ProgressDialog()

                thread.updateProgress.connect(dialog.updateProgress)
                thread.start()
                dialog.exec_()
                thread.stop()

                if (thread.status):
                    QMessageBox.information(self, 'Подтверждение', 'Модель готова')
                else:
                    QMessageBox.warning(self, 'Ошибка', 'Модель не обучилась')
            else:
                QMessageBox.warning(self, 'Ошибка', 'Вы не указали датасет')

        self.setEnabled(True)