import cv2
import numpy as np
import os


def get_image(path):
    """Get image given path"""
    return cv2.imread(path)


def get_image_name(path):
    """Get image name"""
    return os.path.basename(path)


def transform_image(image, image_name):
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
    cv2.imwrite("tests/output_images/cropped/{name}".format(name=image_name), cropped_image)

    return cropped_image


def get_top_left_rectange(image, image_name):
    """Given the image of the puzzle area, return number for columns"""

    # base transformations
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_blurred = cv2.GaussianBlur(gray, (17, 7), 0)

    _, thresh_img = cv2.threshold(image_blurred, 0, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)

    kernel_opening = np.ones((5, 5), np.uint8)
    kernel_closing = np.ones((10, 15), np.uint8)
    opening = cv2.morphologyEx(thresh_img, cv2.MORPH_OPEN, kernel_opening)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel_closing)

    rho = 1
    theta = np.pi / 180
    threshold = 15
    min_line_length = 50
    max_line_gap = 20

    lines = cv2.HoughLinesP(closing, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)

    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 2)

    cv2.imwrite("tests/output_images/further_edits/{name}".format(name=image_name), image)

    return image


if __name__ == "__main__":
    image_path = input("Please enter path to image file: ")
    image = get_image(image_path)
    image_name = get_image_name(image_path)
    transformed_image = transform_image(image, image_name)
    top_left_rectangle = get_top_left_rectange(transformed_image, image_name)
