import traceback
from datetime import datetime
from PyQt5.QtCore import QThread, pyqtSignal
import ast
from pathlib import Path
import numpy as np
import pandas as pd
import PIL
from PIL import Image
import torch
from tqdm.auto import tqdm
import tqdm.notebook
import matplotlib.pyplot as plt
import os
import subprocess
import shutil

class ModelTrainingProcessingThread(QThread):
    updateProgress = pyqtSignal(int)

    def __init__(self, datasetFolderPath,cfg,imgsz,batch,epochs,weights):
        super(ModelTrainingProcessingThread, self).__init__()
        self._is_running = True
        self.status = False
        self.datasetFolderPath = datasetFolderPath
        self.annotations_file = Path(self.datasetFolderPath) / "annotations.csv"
        self.imagesFolderPath = os.path.join(datasetFolderPath,"images")
        self.DATA_DIR = Path(self.datasetFolderPath)
        self.cfg = cfg
        self.imgsz = imgsz
        self.batch = batch
        self.epochs = epochs
        self.weights = weights
        df_annotations = pd.read_csv(self.annotations_file)
        self.most_common_class = df_annotations['class'].mode()[0]

    def run(self):
        ModelsFolder = os.path.join(os.getcwd(), "Models")
        os.makedirs(ModelsFolder, exist_ok=True)
        today = datetime.today()
        dateString = today.strftime("%d_%m_%Y_%H_%M_%S")
        newFolderName = f"Model_{dateString}"
        newFolderPath = os.path.join(ModelsFolder, newFolderName)
        os.makedirs(newFolderPath, exist_ok=True)
        try:
            self.updateProgress.emit(1)
            img_list = list(self.DATA_DIR.glob('images/*.*'))
            if not img_list:
                print("В директории нет изображений формата .jpg, .png или .jpeg")
            only_files = [f for f in img_list if f.is_file() and f.suffix.lower() in [".jpg", ".png", ".jpeg"]]

            if only_files:
                first_image = Image.open(only_files[0])
                IMAGE_HEIGHT, IMAGE_WIDTH = first_image.size
                num_channels = len(first_image.getbands())
                print("Image size: {}".format((IMAGE_HEIGHT, IMAGE_WIDTH)))
                print("Num channels: {}".format(num_channels))
            self.updateProgress.emit(10)
            print(self.DATA_DIR)
            df = pd.read_csv(self.DATA_DIR / "annotations.csv",
                             converters={'geometry': self.f, 'class': lambda o: "'" + self.most_common_class + "'"})
            df.loc[:, 'bounds'] = df.loc[:, 'geometry'].apply(self.getBounds)
            df.loc[:, 'width'] = df.loc[:, 'bounds'].apply(self.getWidth)
            df.loc[:, 'height'] = df.loc[:, 'bounds'].apply(self.getHeight)
            self.updateProgress.emit(20)

            fold = 1
            num_fold = 5
            index = df['image_id'].unique()
            val_indexes = index[len(index) * fold // num_fold:len(index) * (fold + 1) // num_fold]
            print(val_indexes)

            TILE_WIDTH = 512
            TILE_HEIGHT = 512
            TILE_OVERLAP = 64
            TRUNCATED_PERCENT = 0.3
            _overwriteFiles = True

            working_dir = self.DATA_DIR
            working_dir.mkdir(parents=True, exist_ok=True)

            TILES_DIR = {
                'train': working_dir / 'train' / 'images',
                'val': working_dir / 'val' / 'images'
            }
            for _, folder in TILES_DIR.items():
                folder.mkdir(parents=True, exist_ok=True)

            LABELS_DIR = {
                'train': working_dir / 'train' / 'labels',
                'val': working_dir / 'val' / 'labels'
            }
            for _, folder in LABELS_DIR.items():
                folder.mkdir(parents=True, exist_ok=True)
            self.updateProgress.emit(30)
            for img_path in tqdm.tqdm(img_list):
                pil_img = PIL.Image.open(img_path, mode='r')
                np_img = np.array(pil_img, dtype=np.uint8)

                img_labels = df[df["image_id"] == img_path.name]

                X_TILES = (IMAGE_WIDTH + TILE_WIDTH - TILE_OVERLAP - 1) // (TILE_WIDTH - TILE_OVERLAP)
                Y_TILES = (IMAGE_HEIGHT + TILE_HEIGHT - TILE_OVERLAP - 1) // (TILE_HEIGHT - TILE_OVERLAP)


                for x in range(X_TILES):
                    for y in range(Y_TILES):

                        x_end = min((x + 1) * TILE_WIDTH - TILE_OVERLAP * (x != 0), IMAGE_WIDTH)
                        x_start = x_end - TILE_WIDTH
                        y_end = min((y + 1) * TILE_HEIGHT - TILE_OVERLAP * (y != 0), IMAGE_HEIGHT)
                        y_start = y_end - TILE_HEIGHT

                        folder = 'val' if img_path.name in val_indexes else 'train'
                        save_tile_path = TILES_DIR[folder].joinpath(
                            img_path.stem + "_" + str(x_start) + "_" + str(y_start) + ".jpg")
                        save_label_path = LABELS_DIR[folder].joinpath(
                            img_path.stem + "_" + str(x_start) + "_" + str(y_start) + ".txt")

                        # Save if file doesn't exit
                        if _overwriteFiles or not os.path.isfile(save_tile_path):
                            cut_tile = np.zeros(shape=(TILE_WIDTH, TILE_HEIGHT, 3), dtype=np.uint8)
                            cut_tile[0:TILE_HEIGHT, 0:TILE_WIDTH, :] = np_img[y_start:y_end, x_start:x_end, :]
                            cut_tile_img = PIL.Image.fromarray(cut_tile)
                            cut_tile_img.save(save_tile_path)

                        found_tags = [
                            self.tag_is_inside_tile(bounds, x_start, y_start, TILE_WIDTH, TILE_HEIGHT,
                                                    TRUNCATED_PERCENT)
                            for i, bounds in enumerate(img_labels['bounds'])]
                        found_tags = [el for el in found_tags if el is not None]

                        # save labels
                        with open(save_label_path, 'w+') as f:
                            for tags in found_tags:
                                f.write(' '.join(str(x) for x in tags) + '\n')
            self.updateProgress.emit(40)
            CONFIG = f"""
                            # train and val datasets (image directory or *.txt file with image paths)
                            train: {working_dir}/train/
                            val: {working_dir}/val/

                            # number of classes
                            nc: 1

                            # class names
                            names: ['{self.most_common_class}']
                            """

            with open(f"{working_dir}/dataset.yaml", "w") as f:
                f.write(CONFIG)

            print('Setup complete. Using torch %s %s' % (
                torch.__version__, torch.cuda.get_device_properties(0) if torch.cuda.is_available() else 'CPU'))
            self.updateProgress.emit(50)
            yolovPath = os.path.join(os.getcwd(), "yolov5/train.py")
            dataPath = os.path.join(working_dir, "dataset.yaml")
            command = f"python {yolovPath} --cfg {self.cfg} --imgsz {self.imgsz} --batch-size {self.batch} --epochs {self.epochs} --data {dataPath} --weights {self.weights} --device 0"
            completed_process = subprocess.run(command, shell=True, check=True)
            self.updateProgress.emit(80)
            expPath = os.path.join(os.getcwd(), "yolov5/runs/train/exp")
            for item in os.listdir(expPath):
                item_path = os.path.join(expPath, item)
                if os.path.isfile(item_path):
                    shutil.move(item_path, newFolderPath)
                else:
                    shutil.move(item_path, os.path.join(newFolderPath, item))
            os.rmdir(expPath)
            self.status = True
            self.updateProgress.emit(100)
        except Exception as e:
            shutil.rmtree(os.path.join(os.getcwd(), "yolov5/runs/train"))
            shutil.rmtree(newFolderPath)
            traceback.print_exc()
            self.status = False
            self.updateProgress.emit(100)
        self.status = True

    def stop(self):
        self._is_running = False


    def f(self,x):
        return ast.literal_eval(x.rstrip('\r\n'))

    def getBounds(self,geometry):
        try:
            arr = np.array(geometry).T
            xmin = np.min(arr[0])
            ymin = np.min(arr[1])
            xmax = np.max(arr[0])
            ymax = np.max(arr[1])
            return (xmin, ymin, xmax, ymax)
        except:
            return np.nan

    def getWidth(self,bounds):
        try:
            (xmin, ymin, xmax, ymax) = bounds
            return np.abs(xmax - xmin)
        except:
            return np.nan

    def getHeight(self,bounds):
        try:
            (xmin, ymin, xmax, ymax) = bounds
            return np.abs(ymax - ymin)
        except:
            return np.nan
    def tag_is_inside_tile(self,bounds, x_start, y_start, width, height, truncated_percent):
        x_min, y_min, x_max, y_max = bounds
        x_min, y_min, x_max, y_max = x_min - x_start, y_min - y_start, x_max - x_start, y_max - y_start

        if (x_min > width) or (x_max < 0.0) or (y_min > height) or (y_max < 0.0):
            return None

        x_max_trunc = min(x_max, width)
        x_min_trunc = max(x_min, 0)
        if (x_max_trunc - x_min_trunc) / (x_max - x_min) < truncated_percent:
            return None

        y_max_trunc = min(y_max, width)
        y_min_trunc = max(y_min, 0)
        if (y_max_trunc - y_min_trunc) / (y_max - y_min) < truncated_percent:
            return None

        x_center = (x_min_trunc + x_max_trunc) / 2.0 / width
        y_center = (y_min_trunc + y_max_trunc) / 2.0 / height
        x_extend = (x_max_trunc - x_min_trunc) / width
        y_extend = (y_max_trunc - y_min_trunc) / height

        return (0, x_center, y_center, x_extend, y_extend)



