import os
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QPixmap, QPainter, QColor, QImage, QPen
from PyQt5.QtCore import Qt, QPoint, QStringListModel
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QFileDialog, QMessageBox

from ProgressDialog import ProgressDialog
from tabs.dataGenerateTab.ImageUtils import ImageProcessingThread
from ui.UI_MainWindow import Ui_MainWindow
from PIL import Image

class DataGenerateTab(QtWidgets.QWidget):
    def __init__(self, main_window_ui: Ui_MainWindow):
        super().__init__()
        self.ui = main_window_ui

        self.overlay = QPixmap()
        self.overlayItem = QGraphicsPixmapItem(self.overlay)
        self.currentImageName = None

        self.areaFolderPath = None
        self.objectFolderPath = None
        self.overlaysFolderPath = os.path.join(os.getcwd(), "overlays")


        self.scene = QGraphicsScene()
        self.ui.areaGraphicsView.setScene(self.scene)
        self.lastPos = None

        self.ui.areaListView.clicked.connect(lambda: (self.showImage(self.ui.areaListView.currentIndex()), self.ui.saveOverlayButton.setEnabled(True),self.ui.deleteOverlayButton.setEnabled(True)))
        self.ui.objectListView.clicked.connect(lambda: self.ui.saveOverlayButton.setEnabled(False))
        self.ui.objectListView.doubleClicked.connect(lambda: (self.openObjectImage(self.ui.objectListView.currentIndex())))

        self.ui.areaListView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.areaListModel = QStringListModel()
        self.ui.areaListView.setModel(self.areaListModel)

        self.ui.objectListView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.objectListModel = QStringListModel()
        self.ui.objectListView.setModel(self.objectListModel)

        self.ui.saveOverlayButton.setEnabled(False)
        self.ui.deleteOverlayButton.setEnabled(False)

        self.ui.areaFileDialogButton.clicked.connect(lambda: setattr(self, 'areaFolderPath', self.openFileDialog(self.areaListModel)))
        self.ui.objectFileDialogButton.clicked.connect(lambda: setattr(self, 'objectFolderPath', self.openFileDialog(self.objectListModel)))

        self.ui.saveOverlayButton.clicked.connect(self.saveoverlay)
        self.ui.deleteOverlayButton.clicked.connect(self.deleteoverlay)
        self.ui.dataGenerateButton.clicked.connect(self.showConfirmationDialog)
        def drawOnOverlay(event):
            pos = self.ui.areaGraphicsView.mapToScene(event.pos())
            painter = QPainter(self.overlay)
            if event.buttons() == Qt.LeftButton:
                transparentBlack = QColor(0, 0, 255, 10)
                painter.setPen(QPen(transparentBlack, 100, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                if self.lastPos:
                    painter.drawLine(self.lastPos, pos)
                else:
                    painter.drawPoint(pos.toPoint())
            elif event.buttons() == Qt.RightButton:
                painter.setCompositionMode(QPainter.CompositionMode_Clear)
                painter.setPen(QPen(Qt.transparent, 100, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                painter.drawPoint(pos.toPoint())

            self.lastPos = pos
            self.overlayItem.setPixmap(self.overlay)

        def resetLastPos(event):
            self.lastPos = None

        self.ui.areaGraphicsView.mousePressEvent = drawOnOverlay
        self.ui.areaGraphicsView.mouseMoveEvent = drawOnOverlay
        self.ui.areaGraphicsView.mouseReleaseEvent = resetLastPos

    @QtCore.pyqtSlot()
    def openFileDialog(self,ListModel):
        options = QFileDialog.Options()
        FolderPath = QFileDialog.getExistingDirectory(self, "Выберите папку", options=options)
        if FolderPath:
            if (ListModel == self.areaListModel):
                if not (self.checkImageSize(ListModel, FolderPath)):
                    return ""
                else:
                    images = [f for f in os.listdir(FolderPath) if f.lower().endswith(('.png', '.jpeg', '.jpg'))]
                    ListModel.setStringList(images)
            else:
                images = [f for f in os.listdir(FolderPath) if f.lower().endswith(('.png', '.jpeg', '.jpg'))]
                ListModel.setStringList(images)
        return FolderPath

    def checkImageSize(self,ListModel,FolderPath):
        if (ListModel == self.areaListModel):
            images = [f for f in os.listdir(FolderPath) if f.lower().endswith(('.png', '.jpeg', '.jpg'))]
            for image in images:
                imagePath = os.path.join(FolderPath,image)
                img = Image.open(imagePath)
                width, height = img.size
                if (width != 2048 and height != 2048):
                    reply = QMessageBox.warning(self, 'Ошибка',
                                                 'В папке присутствуют изображения, не подходящие по размеру! \nПопробовать преобразовать изображения ?',
                                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        self.resizeImages(images,FolderPath)
                        return 1
                    else:
                        return 0
        return 1
    def resizeImages(self,images,FolderPath):
        for image in images:
            imagePath = os.path.join(FolderPath, image)
            img = Image.open(imagePath)
            resizedImg = img.resize((2048, 2048))
            resizedImg.save(imagePath)



    def showImage(self, index):
        fileName = self.ui.areaListView.currentIndex().data()
        self.currentImageName = fileName
        imagePath = os.path.join(self.areaFolderPath, fileName)
        overlayPath = os.path.join(self.overlaysFolderPath, fileName.split('.')[0]+"_overlay.png")
        image = QPixmap(imagePath)
        if os.path.exists(overlayPath):
            self.overlay = QPixmap(overlayPath)

        else:
            self.overlay = image.copy()
            self.overlay.fill(Qt.transparent)
        self.overlayItem = QGraphicsPixmapItem(self.overlay)
        self.scene.clear()
        self.scene.addPixmap(image)
        self.scene.addItem(self.overlayItem)


    def openObjectImage(self,index):
        fileName = self.ui.objectListView.currentIndex().data()
        self.imagePath = os.path.join(self.objectFolderPath, fileName)
        os.startfile(self.imagePath)

    def saveoverlay(self):
        if not os.path.exists(self.overlaysFolderPath):
            os.makedirs(self.overlaysFolderPath)
        withoutType = self.currentImageName.split('.')[0]
        self.overlayItem.pixmap().save(self.overlaysFolderPath+"/"+withoutType+"_overlay.png")

    def deleteoverlay(self):
        if os.path.exists(self.overlaysFolderPath):
            if self.overlayItem in self.scene.items():
                self.scene.removeItem(self.overlayItem)
                self.overlay.fill(Qt.transparent)
                self.overlayItem = QGraphicsPixmapItem(self.overlay)
                self.scene.addItem(self.overlayItem)
            withoutType = self.currentImageName.split('.')[0]
            if os.path.exists(self.overlaysFolderPath+"/"+withoutType+"_overlay.png"):
                os.remove(self.overlaysFolderPath + "/" + withoutType + "_overlay.png")

    def showConfirmationDialog(self):
        self.setDisabled(True)

        reply = QMessageBox.question(self, 'Подтверждение действия сборки датасета',
                                     'Вы уверены, что хотите осуществить сборку датасета?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            if self.areaFolderPath and self.objectFolderPath:
                thread = ImageProcessingThread(self.areaFolderPath, self.objectFolderPath, self.overlaysFolderPath)
                dialog = ProgressDialog()

                thread.updateProgress.connect(dialog.updateProgress)
                thread.start()
                dialog.exec_()
                thread.stop()

                if (thread.status):
                    QMessageBox.information(self, 'Подтверждение', 'Датасет готов')
                else:
                    QMessageBox.warning(self, 'Ошибка', 'Датасет не собрался')
            else:
                QMessageBox.warning(self, 'Ошибка', 'Вы не указали папки с изображениями')

        self.setEnabled(True)
