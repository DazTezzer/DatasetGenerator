import os
import shutil
import traceback

import cv2
from datetime import datetime
from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np

import pandas as pd
from keras.src.applications.resnet import ResNet50
from keras.src.legacy.preprocessing.image import ImageDataGenerator
from tensorflow.python.keras import Model
from tensorflow.python.keras.layers import Dense, Flatten
from tensorflow.python.keras.models import save_model
from tensorflow.python.keras.optimizer_v1 import Adam




class ModelTrainingProcessingThread(QThread):
    updateProgress = pyqtSignal(int)

    def __init__(self, datasetFolderPath):
        super(ModelTrainingProcessingThread, self).__init__()
        self._is_running = True
        self.status = False
        self.datasetFolderPath = datasetFolderPath
        self.coordinatsFolderPath = os.path.join(datasetFolderPath,"resultCoordinats")
        self.imagesFolderPath = os.path.join(datasetFolderPath,"resultImages")
        self.coordinatesData = self.loadCoordinatesData(self.coordinatsFolderPath)

    def run(self):
        today = datetime.today()
        dateString = today.strftime("%d_%m_%Y_%H_%M_%S")
        newFolderName = f"Model_{dateString}"
        newFolderPath = os.path.join(os.getcwd(), newFolderName)
        os.makedirs(newFolderPath, exist_ok=True)
        try:
            train_datagen = ImageDataGenerator(rescale=1. / 255, rotation_range=20, width_shift_range=0.1,
                                               height_shift_range=0.1, shear_range=0.1, zoom_range=0.1,
                                               horizontal_flip=True)

            base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
            x = base_model.output
            x = Dense(1, activation='sigmoid')(Flatten()(x))
            model = Model(inputs=base_model.input, outputs=x)
            model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])

            batch_size = 32
            maxepoch = 10
            for epoch in range(maxepoch):
                for batch_images, batch_coordinates in self.customImageGenerator(batch_size):
                    model.train_on_batch(batch_images, batch_coordinates)
                    progress = int(((epoch + 1) / maxepoch) * 100)
                    print("Epoch:", epoch + 1, "Progress:", progress, "%")
                    self.updateProgress.emit(progress)

            model_checkpoint_path = os.path.join(newFolderPath, 'trained_model.h5')
            save_model(model, model_checkpoint_path)
            self.status = True

        except Exception as e:
            shutil.rmtree(newFolderPath)
            traceback.print_exc()
            self.status = False


    def stop(self):
        self._is_running = False

    def loadCoordinatesData(self,coordinatesDir):
        coordinatesData = pd.DataFrame()
        for filename in os.listdir(coordinatesDir):
            if filename.endswith('.csv'):
                data = pd.read_csv(os.path.join(coordinatesDir, filename))
                coordinatesData = pd.concat([coordinatesData, data], ignore_index=True)
        return coordinatesData

    def customImageGenerator(self, batch_size):
        while True:
            for i in range(0, len(self.coordinatesData), batch_size):
                batch_data = self.coordinatesData.iloc[i:i + batch_size]
                batch_images = []
                batch_coordinates = []
                for _, row in batch_data.iterrows():
                    image_path = os.path.join(self.imagesFolderPath, row['filename'])
                    image = cv2.imread(image_path)
                    image = cv2.resize(image, (224, 224)) / 255.0
                    batch_images.append(image)
                    coordinates = [row['x_min'], row['y_min'], row['x_max'], row['y_max']]
                    batch_coordinates.append(coordinates)
                yield np.array(batch_images), np.array(batch_coordinates)