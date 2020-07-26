import cv2
import numpy as np


def get_image(path):
    """Get image given path"""
    return cv2.imread(path)


def transform_image(image):
    """Transform image to detect edges"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    kernel = np.ones((5, 5), np.uint8)
    opening = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
    
    image_blurred = cv2.GaussianBlur(opening, (3, 3), 0)

    edges = cv2.Canny(image_blurred, 100, 300, apertureSize=3)

    contours, hierarchy = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]

    biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]

    cv2.drawContours(image, contours, -1, 255, 3)

    c = max(contours, key = cv2.contourArea)
    x,y,w,h = cv2.boundingRect(c)

    image_with_contour = cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)

    cv2.imwrite("tests/output_images/edge.jpg", image_with_contour)

    return image


def get_puzzle_space(img):
    """Given image, get puzzle area"""
    transformed_image = transform_image(img)
    return transformed_image

if __name__ == "__main__":
    image_path = input("Please enter path to image file: ")
    image = get_image(image_path)
    transformed_image = transform_image(image)