import os
from PIL import Image, ImageDraw
import numpy as np
import random
from PyQt5.QtGui import QImage


def get_coordinats(overlay,image_path,insert_image_path):
    print("bruh")
    overlay_image = overlay.toImage()
    image = overlay_image.convertToFormat(QImage.Format_ARGB32)
    width = image.width()
    height = image.height()
    # Извлекаем данные изображения как байты
    ptr = image.bits().asstring(width * height * 4)
    arr = np.frombuffer(ptr, dtype=np.uint8).reshape(height, width, 4)

    # Находим координаты ненулевых пикселей в overlay
    non_zero_coords = np.argwhere(np.any(arr != [0, 0, 0, 0], axis=2))
    coordinates = non_zero_coords
    for coords in coordinates:
        y, x = coords
    random_coord = random.choice(coordinates)
    x = random_coord[1]
    y = random_coord[0]
    insert_image(image_path, insert_image_path, x, y)

def draw_rectangle(image, box):
    draw = ImageDraw.Draw(image)

    draw.rectangle(box, outline="red")

    return image


def insert_image(main_image_path, insert_image_path, x, y):
    main_image_path = os.path.abspath(main_image_path)

    insert_image_path = os.path.abspath(insert_image_path)

    main_image = Image.open(main_image_path)

    insert_image = Image.open(insert_image_path).convert("RGBA")

    if (
            insert_image.size[0] > main_image.size[0]
            or insert_image.size[1] > main_image.size[1]
    ):
        raise ValueError("Размер вставляемого изображения превышает размер основного изображения.")

    result_image = main_image.copy()

    result_image.paste(insert_image, (x, y), mask=insert_image)

    insert_box = (x, y, x + insert_image.width, y + insert_image.height)
    result_image = draw_rectangle(result_image, insert_box)

    result_filename = "result_image.png"

    result_path = os.path.join(os.path.dirname(main_image_path), result_filename)
    result_image.save(result_path, format="PNG")

    result_image.show()

    print(f"Координаты вставленного изображения: (X: {x}, Y: {y})")

    print(f"Путь к результирующему изображению: {result_path}")