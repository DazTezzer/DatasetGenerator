import os
import shutil
import traceback

import pandas as pd
from PIL import Image, ImageDraw
import numpy as np
import random
from datetime import datetime

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
import csv

from PyQt5.QtWidgets import QMessageBox


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
        DatesetsFolder = os.path.join(os.getcwd(),"Datasets")
        os.makedirs(DatesetsFolder, exist_ok=True)
        today = datetime.today()
        dateString = today.strftime("%d_%m_%Y_%H_%M_%S")
        newFolderName = f"Dataset_{dateString}"
        newFolderPath = os.path.join(DatesetsFolder, newFolderName)
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
                                overlay = QPixmap(areaFilePath).toImage()
                                getCoordinats(overlay, areaFilePath, objectFilePath, newFolderPath)

                    print("Processing image:", areaFilePath)
                    processedFiles += 1
                    progress = int((processedFiles / totalFiles) * 100)
                    print("Progress:", progress)
                    self.status = True
                    self.updateProgress.emit(progress)
        except Exception as e:
            shutil.rmtree(newFolderPath)
            traceback.print_exc()
            self.status = False
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
    #resultImage = drawRectangle(resultImage, insert_box)

    resultFileName = os.path.basename(mainImagePath.split('.')[0])+"_"+os.path.basename(insertImagePath.split('.')[0])
    resultImagesFolderPath = os.path.join(FolderPath, "images")
    os.makedirs(resultImagesFolderPath, exist_ok=True)
    resultImagesPath = os.path.join(resultImagesFolderPath,resultFileName+".png")
    resultImage.save(resultImagesPath, format="PNG")
    resultCoordinatsPath = os.path.join(FolderPath,"annotations.csv")
    x_top_left = x
    y_top_left = y
    insertImageWidth, insertImageHeight = insertImage.size
    x_bottom_right = x_top_left + insertImageWidth
    y_bottom_right = y_top_left + insertImageHeight
    data = {
        'image_id': [resultFileName+".png"],
        'geometry': f"[({x_top_left},{y_bottom_right}),({x_bottom_right},{y_bottom_right}),({x_bottom_right},{y_top_left}),({x_top_left},{y_top_left})]",
        'class': ["Car"]
    }
    if os.path.isfile(resultCoordinatsPath):
        with open(resultCoordinatsPath, 'a') as f:
            df = pd.DataFrame(data)
            f.write(df.to_csv(header=False, index=False).strip() + '\n')
    else:
        df = pd.DataFrame(data)
        df.to_csv(resultCoordinatsPath, index=False)

    print(f"Координаты вставленного изображения: (X: {x}, Y: {y})")
    print(f"Путь к результирующему изображению: {resultImagesPath}")
