import cv2
from PIL import Image, ImageDraw
import numpy as np
import os

def draw_or_erase(event, x, y, flags, param):
    global drawing, erasing

    # Рисование круга или стирание
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        cv2.circle(overlay, (x, y), 10, (0, 0, 255), -1)
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.circle(overlay, (x, y), 10, (0, 0, 255), -1)
        if erasing == True:
            cv2.circle(overlay, (x, y), 10, (0, 0, 0), -1)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
    elif event == cv2.EVENT_RBUTTONDOWN:
        erasing = True
        cv2.circle(overlay, (x, y), 10, (0, 0, 0), -1)
    elif event == cv2.EVENT_RBUTTONUP:
        erasing = False

main_image_path = "2.png"
main_image_path = os.path.abspath(main_image_path)
img = np.array(Image.open(main_image_path))
overlay = np.zeros_like(img)
alpha = 0.4
cv2.namedWindow('Image')
cv2.setMouseCallback('Image', draw_or_erase)
drawing = False
erasing = False

while True:
    img_new = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
    cv2.imshow('Image', img_new)
    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()
non_zero_coords = np.argwhere(np.any(overlay != [0, 0, 0], axis=2))
def get_coordinats():
    return non_zero_coords
