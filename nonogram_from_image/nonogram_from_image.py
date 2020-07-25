import cv2
import numpy as np


def get_image(path):
    image = cv2.imread(path)
    return image


if __name__ == "__main__":
    image_path = input("Please enter path to image file: ")
    image = get_image(image_path)
    