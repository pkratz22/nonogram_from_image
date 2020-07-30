"""Get grid array from nonogram image

Functions:
    get_image(path)
    get_image_name(path)
    transform_image(image, image_name)
    get_top_left_rectange(image, image_name)
"""
# imports
import os
import cv2


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
    max_contour = max(contours, key=cv2.contourArea)
    x_coord, y_coord, width, height = cv2.boundingRect(max_contour)

    # creates image with contour
    cropped_image = image[y_coord:y_coord + height, x_coord:x_coord + width]

    # write image
    cv2.imwrite("tests/output_images/cropped/{name}".format(name=image_name), cropped_image)

    return cropped_image


def get_top_left_rectange(image, image_name):
    """Given the image of the puzzle area, return number for columns"""

    # base transformations
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    _, thresh_img = cv2.threshold(image_blurred, 0, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)

    cv2.imwrite("tests/output_images/further_edits/{name}".format(name=image_name), thresh_img)

    return thresh_img


if __name__ == "__main__":
    nonogram_image_path = input("Please enter path to image file: ")
    nonogram_image = get_image(nonogram_image_path)
    nonogram_image_name = get_image_name(nonogram_image_path)
    transformed_image = transform_image(nonogram_image, nonogram_image_name)
    top_left_rectangle = get_top_left_rectange(transformed_image, nonogram_image_name)
