import os
import shutil

from PIL import Image, ImageDraw
import numpy as np
import random
from datetime import datetime

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
import csv

class ImageProcessingThread(QThread):
    updateProgress = pyqtSignal(int)

    def __init__(self, areaFolderPath, objectFolderPath, overlaysFolderPath):
        super(ImageProcessingThread, self).__init__()
        self._is_running = True
        self.status = False
        self.areaFolderPath = areaFolderPath
        self.objectFolderPath = objectFolderPath
        self.overlaysFolderPath = overlaysFolderPath

    def run(self):
        today = datetime.today()
        dateString = today.strftime("%d_%m_%Y_%H_%M_%S")
        newFolderName = f"Dataset_{dateString}"
        newFolderPath = os.path.join(os.getcwd(), newFolderName)
        os.makedirs(newFolderPath, exist_ok=True)
        try:
            areaFiles = os.listdir(self.areaFolderPath)
            objectFiles = os.listdir(self.objectFolderPath)
            processedFiles = 0
            totalFiles = len(areaFiles)
            for areaFile in areaFiles:
                areaFilePath = os.path.join(self.areaFolderPath, areaFile)
                if os.path.isfile(areaFilePath) and areaFile.lower().endswith(('.png', '.jpg', '.jpeg')):
                    for objectFile in objectFiles:
                        objectFilePath = os.path.join(self.objectFolderPath, objectFile)
                        if os.path.isfile(objectFilePath) and objectFile.lower().endswith(('.png', '.jpg', '.jpeg')):
                            withoutType = areaFile.split('.')[0]
                            overlayPath = os.path.join(self.overlaysFolderPath, withoutType + "_overlay.png")
                            if os.path.exists(overlayPath):
                                overlay = QPixmap(overlayPath).toImage()
                                getCoordinats(overlay, areaFilePath, objectFilePath,newFolderPath)
                            else:
                                print("File '1_overlay.png' not found in 'overlays' folder.")

                    print("Processing image:", areaFilePath)
                    processedFiles += 1
                    progress = int((processedFiles / totalFiles) * 100)
                    print("Progress:", progress)
                    self.updateProgress.emit(progress)
        except Exception as e:
            shutil.rmtree(newFolderPath)
            print(e)


        self.status = True

    def stop(self):
        self._is_running = False


def getCoordinats(overlay, imagePath, insertImagePath,FolderPath):
    overlayImage = overlay.convertToFormat(QImage.Format_ARGB32)
    width = overlayImage.width()
    height = overlayImage.height()

    ptr = overlayImage.bits().asstring(width * height * 4)
    arr = np.frombuffer(ptr, dtype=np.uint8).reshape(height, width, 4)

    nonZeroCoords = np.argwhere(np.any(arr != [0, 0, 0, 0], axis=2))
    coordinates = nonZeroCoords
    for coords in coordinates:
        y, x = coords
    randomCoord = random.choice(coordinates)
    x = randomCoord[1]
    y = randomCoord[0]
    insertImage(imagePath, insertImagePath, x, y,FolderPath)


def drawRectangle(image, box):
    draw = ImageDraw.Draw(image)

    draw.rectangle(box, outline="red")

    return image


def insertImage(mainImagePath, insertImagePath, x, y,FolderPath):
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

    resultFileName = os.path.basename(mainImagePath.split('.')[0])+"_"+os.path.basename(insertImagePath.split('.')[0])
    resultImagesFolderPath = os.path.join(FolderPath, "resultImages")
    resultCoordinatsFolderPath = os.path.join(FolderPath, "resultCoordinats")
    os.makedirs(resultImagesFolderPath, exist_ok=True)
    os.makedirs(resultCoordinatsFolderPath, exist_ok=True)
    resultImagesPath = os.path.join(resultImagesFolderPath,resultFileName+".png")
    resultImage.save(resultImagesPath, format="PNG")
    resultCoordinatsPath = os.path.join(resultCoordinatsFolderPath,resultFileName+".csv")
    coordinates = [(x,y)]
    with open(resultCoordinatsPath, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(coordinates)

    print(f"Координаты вставленного изображения: (X: {x}, Y: {y})")
    print(f"Путь к результирующему изображению: {resultImagesPath}")
