import cv2
import numpy as np


def get_image(path):
    """Get image given path"""
    return cv2.imread(path)


def transform_image(image):
    """Transform image to detect edges"""
    
    # make image gray
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # apply Gaussian Blur to reduce noise
    image_blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    # get edges using Canny method
    edges = cv2.Canny(image_blurred, 100, 300, apertureSize=3)

    # find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # finds largest contour
    c = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(c)

    # creates image with contour
    cropped_image = image[y:y+h,x:x+w]

    # write image
    cv2.imwrite("tests/output_images/edge.jpg", cropped_image)

    return image


def get_puzzle_space(img):
    """Given image, get puzzle area"""
    transformed_image = transform_image(img)
    return transformed_image

if __name__ == "__main__":
    image_path = input("Please enter path to image file: ")
    image = get_image(image_path)
    transformed_image = transform_image(image)