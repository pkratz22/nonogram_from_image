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
    contours, _ = cv2.findContours(
        edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # finds largest contour
    c = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(c)

    # creates image with contour
    cropped_image = image[y:y + h, x:x + w]

    # write image
    cv2.imwrite("tests/output_images/edge.jpg", cropped_image)

    return cropped_image


def get_column_region(image):
    """Given the image of the puzzle area, return number for columns"""

    # base transformations
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    _, thresh_img = cv2.threshold(image_blurred, 0, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)

    kernel_opening = np.ones((5, 5), np.uint8)
    kernel_closing = np.ones((5, 20), np.uint8)
    opening = cv2.morphologyEx(thresh_img, cv2.MORPH_OPEN, kernel_opening)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel_closing)

    binary = cv2.bitwise_not(closing)

    (contours, _) = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    (x, y, w, h) = cv2.boundingRect(contours[0])

    for contour in contours:
        (temp_x, temp_y, temp_w, temp_h) = cv2.boundingRect(contour)
        if temp_x < x:
            x = temp_x
        if temp_y < y:
            y = temp_y
    
    for contour in contours:
        (temp_x, temp_y, temp_w, temp_h) = cv2.boundingRect(contour)
        if(temp_x == x and temp_y == y):
            cv2.rectangle(image, (temp_x, temp_y), (temp_x+temp_w, temp_y+temp_h), (0, 255, 0), 2)

    cv2.imwrite("tests/output_images/columns.jpg", image)

    return image


def get_row_region(image):
    """Given the image of the puzzle area, return number for rows"""
    pass


if __name__ == "__main__":
    image_path = input("Please enter path to image file: ")
    image = get_image(image_path)
    transformed_image = transform_image(image)
    column_region = get_column_region(transformed_image)
