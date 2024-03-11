from PyQt5 import QtWidgets, QtGui, QtCore
import sys
from PyQt5.QtGui import QPixmap, QPainter, QColor, QImage, QPen
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsPixmapItem
from image_utils import get_coordinats

from ui.UI_MainWindow import Ui_MainWindow
class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Загрузка изображения
        image_path = "1.png"
        self.image = QPixmap(image_path)
        self.overlay = self.image.copy()
        self.overlay.fill(Qt.transparent)

        self.scene = QGraphicsScene()
        self.scene.addPixmap(self.image)
        self.overlay_item = QGraphicsPixmapItem(self.overlay)
        self.scene.addItem(self.overlay_item)
        self.ui.graphicsView.setScene(self.scene)
        self.last_pos = None
        def draw_on_overlay(event):
            pos = self.ui.graphicsView.mapToScene(event.pos())
            painter = QPainter(self.overlay)
            if event.buttons() == Qt.LeftButton:
                transparent_black = QColor(0, 0, 255, 10)
                painter.setPen(QPen(transparent_black, 100, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                if self.last_pos:
                    painter.drawLine(self.last_pos, pos)
                else:
                    painter.drawPoint(pos.toPoint())
            elif event.buttons() == Qt.RightButton:
                painter.setCompositionMode(QPainter.CompositionMode_Clear)
                painter.setPen(QPen(Qt.transparent, 100, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                painter.drawPoint(pos.toPoint())

            self.last_pos = pos
            self.overlay_item.setPixmap(self.overlay)

        def reset_last_pos(event):
            self.last_pos = None

        self.ui.graphicsView.mousePressEvent = draw_on_overlay
        self.ui.graphicsView.mouseMoveEvent = draw_on_overlay
        self.ui.graphicsView.mouseReleaseEvent = reset_last_pos
        self.ui.pushButton.clicked.connect(lambda:get_coordinats(self.overlay,"1.png","Машина.png"))

app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec())