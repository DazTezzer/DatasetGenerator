import os
import torch
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QStringListModel, Qt
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
        self.ui.cudaStatusLabel.setText("Проверка доступности видеокарты")
        self.ui.cudaStatusLabel.setTextFormat(Qt.RichText)
        self.ui.standardSettingsButton.clicked.connect(self.setStandartSettings)
        self.updateDatasetList()
        self.updateCUDAStatus()

    def setStandartSettings(self):
        self.ui.cfgLineEdit.setText("yolov5s.yaml")
        self.ui.imgszLineEdit.setText("512")
        self.ui.batchSizeLineEdit.setText("16")
        self.ui.epochsLineEdit.setText("10")
        self.ui.weightsLineEdit.setText("yolov5s.pt")

    def updateCUDAStatus(self):
        text = ""
        if torch.cuda.is_available():
            text = '<span>Видеокарта может быть использована для обучения модели</span>' + f'<br>Доступные CUDA устройства:<span style="color: rgb(0, 230, 0);"> {torch.cuda.get_device_name(0)}</span>'
        else:
            text = '<span style="color: rgb(250, 55, 55);">К сожалению, видеокарта не может быть использована для обучения модели </span>'
        self.ui.cudaStatusLabel.setText(text)
    def onTabChanged(self, index):
        if index == 1:
            self.updateDatasetList()
            self.updateCUDAStatus()



    def onSelectionChanged(self):
        datasetsFolderPath = os.path.join(os.getcwd(),"Datasets")
        self.datasetFolderPath = os.path.join(datasetsFolderPath,self.ui.datasetListView.currentIndex().data())


    def updateDatasetList(self):
        datasetsDirectory = os.path.join(os.getcwd(),"Datasets")
        if os.path.exists(datasetsDirectory) and os.path.isdir(datasetsDirectory):
            datasetFolders = [folder for folder in os.listdir(datasetsDirectory) if
                              os.path.isdir(os.path.join(datasetsDirectory, folder))]
            self.listModel.setStringList(datasetFolders)
            self.ui.datasetListView.setModel(self.listModel)


    def showConfirmationDialog(self):
        self.setDisabled(True)

        reply = QMessageBox.question(self, 'Подтверждение действия обучение модели',
                                     'Вы уверены, что хотите осуществить обучение модели?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            if  self.datasetFolderPath :
                thread = ModelTrainingProcessingThread(self.datasetFolderPath,self.ui.cfgLineEdit.text(),self.ui.imgszLineEdit.text(),self.ui.batchSizeLineEdit.text(),self.ui.epochsLineEdit.text(),self.ui.weightsLineEdit.text())
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