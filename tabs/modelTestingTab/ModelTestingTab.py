import os
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QPixmap, QPainter, QColor, QImage, QPen
from PyQt5.QtCore import Qt, QPoint, QStringListModel
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QFileDialog, QMessageBox

from ProgressDialog import ProgressDialog
from tabs.modelTestingTab.TestingUtils import ModelTestingProcessingThread
from ui.UI_MainWindow import Ui_MainWindow

class ModelTestingTab(QtWidgets.QWidget):
    def __init__(self, main_window_ui: Ui_MainWindow):
        super().__init__()
        self.ui = main_window_ui
        self.ui.tabWidget.currentChanged.connect(self.onTabChanged)
        self.modelsListModel = QStringListModel()
        self.testsListModel = QStringListModel()
        self.modelsList()
        self.testsList()
        self.testingImagesFolderPath =None
        self.modelFolderPath = None
        self.testsFolderPath = None
        self.ui.testingImagesFileDialogButton.clicked.connect(
            lambda: setattr(self, 'testingImagesFolderPath', self.openFileDialog()))
        self.ui.testingStartButton.clicked.connect(self.showConfirmationDialog)
        self.ui.modelsListView.selectionModel().selectionChanged.connect(self.modelsOnSelectionChanged)
        self.ui.testingResultsListView.selectionModel().selectionChanged.connect(self.testsOnSelectionChanged)
        self.ui.updateTestingResultsPushButton.clicked.connect(self.testsList)
        self.ui.testingResultsListView.clicked.connect(self.generateTestsResults)

    def onTabChanged(self, index):
        if index == 2:
            self.modelsList()
            self.testsList()

    def generateTestsResults(self):
        if self.testsFolderPath:
            pngCount, jpgCount, jpegCount = self.count_image_types(self.testsFolderPath)
            allImagesCount = pngCount+jpgCount+jpegCount
            filename = os.path.basename(self.testsFolderPath)
            metricsPath = os.path.join(self.testsFolderPath, "metrics")
            f1CurveImage = os.path.join(metricsPath, "F1_curve.png")
            pCurveImage = os.path.join(metricsPath, "P_curve.png")
            prCurveImage = os.path.join(metricsPath, "PR_curve.png")
            rCurveImage = os.path.join(metricsPath, "R_curve.png")
            confusionMatrixImage = os.path.join(metricsPath, "confusion_matrix.png")
            labelsImage =os.path.join(metricsPath, "labels.jpg")
            labelsCorrelogram = os.path.join(metricsPath, "labels_correlogram.jpg")
            resultImage = os.path.join(metricsPath, "results.png")
            testText = f"""
                <h1 style="text-align: center; color: #333;">Отчет тестирования</h1>
                <h3 style="text-align: center; color: #666;">{filename}</h3>
                <br>
                <br>
                <br>
                <br>
                <table style="text-align: center">
                    <tr>
                        <th style="background-color: #f2f2f2; padding: 8px; border: 1px solid #ccc; text-align: center;">Изображения</th>
                        <th style="background-color: #f2f2f2; padding: 8px; border: 1px solid #ccc; text-align: center;">Количество</th>
                        <th style="background-color: #f2f2f2; padding: 8px; border: 1px solid #ccc; text-align: center;">Количество объектов всего</th>
                        <th style="background-color: #f2f2f2; padding: 8px; border: 1px solid #ccc; text-align: center;">Количество правильно найденных объектов</th>
                        <th style="background-color: #f2f2f2; padding: 8px; border: 1px solid #ccc; text-align: center;">Количество неправильно найденных объектов</th>
                        <th style="background-color: #f2f2f2; padding: 8px; border: 1px solid #ccc; text-align: center;">Процентное соотношение</th>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border: 1px solid #ccc; text-align: center;">Всего</td>
                        <td style="padding: 8px; border: 1px solid #ccc; text-align: center;">{allImagesCount}</td>
                        <td style="padding: 8px; border: 1px solid #ccc; text-align: center;">100</td>
                        <td style="padding: 8px; border: 1px solid #ccc; text-align: center;">85</td>
                        <td style="padding: 8px; border: 1px solid #ccc; text-align: center;">15</td>
                        <td style="padding: 8px; border: 1px solid #ccc; text-align: center;">85%</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border: 1px solid #ccc; text-align: center;">PNG</td>
                        <td style="padding: 8px; border: 1px solid #ccc; text-align: center;">{pngCount}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border: 1px solid #ccc; text-align: center;">JPG</td>
                        <td style="padding: 8px; border: 1px solid #ccc; text-align: center;">{jpgCount}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border: 1px solid #ccc; text-align: center;">JPEG</td>
                        <td style="padding: 8px; border: 1px solid #ccc; text-align: center;">{jpegCount}</td>
                    </tr>
                </table>
                <br>
                <br>
                <table style="text-align: center">
                    <tr>
                        <th  text-align: center;"><img src="{f1CurveImage}" class="image" alt="Image 1" width="900" height="600"> </th>
                        <th  text-align: center;"><img src="{pCurveImage}" class="image" alt="Image 2" width="900" height="600"></th>
                    </tr>
                    <tr>
                        <td  text-align: center;"><img src="{prCurveImage}" class="image" alt="Image 3" width="900" height="600"></td>
                        <td  text-align: center;"><img src="{rCurveImage}" class="image" alt="Image 4" width="900" height="600"></td>
                    </tr>
                </table>
                <br>
                <th  text-align: center;"><img src="{confusionMatrixImage}" class="image" alt="Image 1" width="1500" height="1125"> </th>
                <br>
                <table style="text-align: center">
                    <tr>
                        <th  text-align: center;"><img src="{labelsImage}" class="image" alt="Image 1" width="900" height="600"> </th>
                    </tr>
                    <tr>
                        <td  text-align: center;"><img src="{labelsCorrelogram}" class="image" alt="Image 3" width="900" height="600"></td>
                    </tr>
                </table>
                <br>
                <th  text-align: center;"><img src="{resultImage}" class="image" alt="Image 1" width="1500" height="1125"> </th>
            """
            self.ui.testingResultTextEdit.setText(testText)


    def count_image_types(self,directory):
        png_count = 0
        jpg_count = 0
        jpeg_count = 0

        for file in os.listdir(directory):
            if file.lower().endswith('.png'):
                png_count += 1
            elif file.lower().endswith('.jpg'):
                jpg_count += 1
            elif file.lower().endswith('.jpeg'):
                jpeg_count += 1

        return png_count, jpg_count, jpeg_count

    def modelsList(self):
        modelsDirectory = os.path.join(os.getcwd(),"Models")
        modelsFolders = [folder for folder in os.listdir(modelsDirectory) if
                           os.path.isdir(os.path.join(modelsDirectory, folder))]
        self.modelsListModel.setStringList(modelsFolders)
        self.ui.modelsListView.setModel(self.modelsListModel)

    def testsList(self):
        testingsDirectory = os.path.join(os.getcwd(),"Testings")
        if os.path.exists(testingsDirectory) and os.path.isdir(testingsDirectory):
            testsFolders = [folder for folder in os.listdir(testingsDirectory) if
                            os.path.isdir(os.path.join(testingsDirectory, folder))]
            self.testsListModel.setStringList(testsFolders)
            self.ui.testingResultsListView.setModel(self.testsListModel)

    @QtCore.pyqtSlot()
    def openFileDialog(self):
        options = QFileDialog.Options()
        FolderPath = QFileDialog.getExistingDirectory(self, "Выберите папку", options=options)
        if FolderPath:
            self.ui.testingImagesPathLabel.setText("Папка: "+str(FolderPath))
        else:
            self.ui.testingImagesPathLabel.setText("Папка не выбрана")
            return None
        return FolderPath

    def modelsOnSelectionChanged(self):
        modelsFolderPath = os.path.join(os.getcwd(),"Models")
        self.modelFolderPath = os.path.join(modelsFolderPath,self.ui.modelsListView.currentIndex().data())

    def testsOnSelectionChanged(self):
        testsFolderPath = os.path.join(os.getcwd(),"Testings")
        self.testsFolderPath = os.path.join(testsFolderPath,self.ui.testingResultsListView.currentIndex().data())
    def showConfirmationDialog(self):
        self.setDisabled(True)

        reply = QMessageBox.question(self, 'Подтверждение действия тестирование модели',
                                     'Вы уверены, что хотите осуществить тестирование модели?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        print(self.testingImagesFolderPath)
        print(self.modelFolderPath)
        if reply == QMessageBox.Yes:
            if self.testingImagesFolderPath and self.modelFolderPath:
                thread = ModelTestingProcessingThread(self.testingImagesFolderPath,self.modelFolderPath)
                dialog = ProgressDialog()

                thread.updateProgress.connect(dialog.updateProgress)
                thread.start()
                dialog.exec_()
                thread.stop()

                if (thread.status):
                    QMessageBox.information(self, 'Подтверждение', 'Тестирование прошло успешно')
                else:
                    QMessageBox.warning(self, 'Ошибка', 'Тестирование не удалось')
            else:
                QMessageBox.warning(self, 'Ошибка', 'Вы не указали модель или папку с изображениями')

        self.setEnabled(True)
