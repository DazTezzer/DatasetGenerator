import os
import shutil
import subprocess
import traceback
from datetime import datetime

from PyQt5.QtCore import QThread, pyqtSignal

class ModelTestingProcessingThread(QThread):
    updateProgress = pyqtSignal(int)

    def __init__(self,testingImagesFolderPath,modelFolderPath):
        super(ModelTestingProcessingThread, self).__init__()
        self._is_running = True
        self.status = False
        self.testingImagesFolderPath = testingImagesFolderPath
        self.modelFolderPath = modelFolderPath


    def run(self):
        imagesPath = os.path.join(self.testingImagesFolderPath, "images")
        TestingsFolder = os.path.join(os.getcwd(), "Testings")
        os.makedirs(TestingsFolder, exist_ok=True)
        today = datetime.today()
        dateString = today.strftime("%d_%m_%Y_%H_%M_%S")
        newFolderName = f"Test_{dateString}"
        newFolderPath = os.path.join(TestingsFolder, newFolderName)
        os.makedirs(newFolderPath, exist_ok=True)
        metricsFolderPath = os.path.join(newFolderPath, "metrics")
        os.makedirs(metricsFolderPath, exist_ok=True)
        try:
            self.updateProgress.emit(10)
            files_to_copy = 'F1_curve.png, labels.jpg, confusion_matrix.png,labels_correlogram.jpg,P_curve.png,PR_curve.png,R_curve.png,results.csv,results.png'
            self.copy_files(self.modelFolderPath, metricsFolderPath, files_to_copy)
            self.updateProgress.emit(20)
            weightsPath = os.path.join(self.modelFolderPath, "weights", "best.pt")
            imagesPath = os.path.abspath(imagesPath)
            weightsPath = os.path.abspath(weightsPath)
            self.updateProgress.emit(45)
            command = f"python yolov5/detect.py --source {imagesPath} --weights {weightsPath} --img 896 --save-txt --save-crop"
            completed_process = subprocess.run(command, shell=True, check=True)
            self.updateProgress.emit(70)
            expPath = os.path.join(os.getcwd(), "yolov5/runs/detect/exp")
            for item in os.listdir(expPath):
                item_path = os.path.join(expPath, item)
                if os.path.isfile(item_path):
                    shutil.move(item_path, newFolderPath)
                else:
                    shutil.move(item_path, os.path.join(newFolderPath, item))
            os.rmdir(expPath)
            self.updateProgress.emit(100)
        except Exception as e:
            shutil.rmtree(os.path.join(os.getcwd(), "yolov5/runs/detect"))
            shutil.rmtree(newFolderPath)
            traceback.print_exc()
            self.status = False
            self.updateProgress.emit(100)

        self.status = True

    def copy_files(self,source_dir, destination_dir, filenames):
        if not os.path.exists(source_dir) or not os.path.exists(destination_dir):
            return
        filenames_list = filenames.split(',')
        for filename in filenames_list:
            file_path = os.path.join(source_dir, filename.strip())
            if os.path.exists(file_path):
                shutil.copy(file_path, destination_dir)

    def stop(self):
        self._is_running = False
