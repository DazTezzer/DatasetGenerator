import os
from PIL import Image, ImageDraw
import numpy as np
import random
import time

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage

class ImageProcessingThread(QThread):
    updateProgress = pyqtSignal(int)

    def __init__(self):
        super(ImageProcessingThread, self).__init__()
        self._is_running = True
        self.status = False


    def run(self):
        while self._is_running:
            images = range(38)
            for idx, img in enumerate(images):
                time.sleep(0.5)
                progress = int((idx + 1) / len(images) * 100)
                print(progress)
                self.updateProgress.emit(progress)
            self.status = True
            pass

    def stop(self):
        self._is_running = False

def getCoordinats(overlay,imagePath,insertImagePath):
    print("bruh")
    overlayImage = overlay.toImage()
    image = overlayImage.convertToFormat(QImage.Format_ARGB32)
    width = image.width()
    height = image.height()
    # Извлекаем данные изображения как байты
    ptr = image.bits().asstring(width * height * 4)
    arr = np.frombuffer(ptr, dtype=np.uint8).reshape(height, width, 4)

    # Находим координаты ненулевых пикселей в overlay
    nonZeroCoords = np.argwhere(np.any(arr != [0, 0, 0, 0], axis=2))
    coordinates = nonZeroCoords
    for coords in coordinates:
        y, x = coords
    randomCoord = random.choice(coordinates)
    x = randomCoord[1]
    y = randomCoord[0]
    insertImage(imagePath, insertImagePath, x, y)

def drawRectangle(image, box):
    draw = ImageDraw.Draw(image)

    draw.rectangle(box, outline="red")

    return image


def insertImage(mainImagePath, insertImagePath, x, y):
    mainImagePath = os.path.abspath(mainImagePath)

    insertImagePath = os.path.abspath(insertImagePath)

    mainImage = Image.open(mainImagePath)

    insertImage = Image.open(insertImagePath).convert("RGBA")

    if (
            insertImage.size[0] > mainImage.size[0]
            or insertImage.size[1] > mainImage.size[1]
    ):
        raise ValueError("Размер вставляемого изображения превышает размер основного изображения.")

    resultImage = mainImage.copy()

    resultImage.paste(insertImage, (x, y), mask=insertImage)

    insert_box = (x, y, x + insertImage.width, y + insertImage.height)
    resultImage = drawRectangle(resultImage, insert_box)

    resultFileName = "resultImage.png"

    result_path = os.path.join(os.path.dirname(mainImagePath), resultFileName)
    resultImage.save(result_path, format="PNG")

    resultImage.show()

    print(f"Координаты вставленного изображения: (X: {x}, Y: {y})")

    print(f"Путь к результирующему изображению: {result_path}")