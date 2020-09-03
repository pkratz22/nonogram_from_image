"""Get grid array from nonogram image"""
# imports
import os
import cv2
import numpy as np


def get_image(path):
    """Get image given path"""
    return cv2.imread(path)


def get_image_name(path):
    """Get image name"""
    return os.path.basename(path)


def base_transformation(image):
    """Complete base transformations"""
    # make image gray
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # apply Gaussian Blur to reduce noise
    image_blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    return image_blurred


def get_largest_contour_bounding_box(edges):
    """Get largest contour"""
    # find contours
    contours, _ = cv2.findContours(
        edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # finds largest contour
    max_contour = max(contours, key=cv2.contourArea)

    x_coord, y_coord, width, height = cv2.boundingRect(max_contour)
    return (x_coord, y_coord, width, height)


def transform_image(image):
    """Transform image to detect edges"""
    # apply base transformations
    image_blurred = base_transformation(image)

    # get edges using Canny method
    edges = cv2.Canny(image_blurred, 100, 300, apertureSize=3)

    # finds largest contour
    x_coord, y_coord, width, height = get_largest_contour_bounding_box(edges)

    # creates image with contour
    cropped_image = image[y_coord:y_coord + height, x_coord:x_coord + width]

    return cropped_image


def test_get_num_rows_cols_from_image(image):
    """Get cell dimensions"""
    # transform image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (_, black_white_image) = cv2.threshold(
        gray_image, 150, 255, cv2.THRESH_BINARY)
    kernel = np.ones((1, 5), np.uint8)
    erosion = cv2.erode(black_white_image, kernel, iterations=1)

    white = 255
    black = 0
    rows = erosion.shape[0]
    cols = erosion.shape[1]

    for row in range(rows):
        count = 0
        temp_color = erosion[row][0]
        for col in range(cols):
            current_color = erosion[row][col]
            if temp_color != current_color:
                if temp_color == white:
                    temp_color = black
                else:
                    temp_color = white
                count += 1
        if count > 2:
            pixel_row_for_col_counting = row + 1
            break

    temp_color = black
    count = 0
    for col in range(cols):
        current_color = erosion[pixel_row_for_col_counting][col]
        if temp_color != current_color:
            if temp_color == white:
                temp_color = black
            else:
                temp_color = white
            count += 1

    num_cols = int(round(count / 2))
    approximate_col_side_length = erosion.shape[1] / num_cols
    num_rows = int(round(erosion.shape[0] / approximate_col_side_length))
    return num_rows, num_cols


if __name__ == "__main__":
    #nonogram_image_path = input("Please enter path to image file: ")
    NONOGRAM_IMAGE_PATH = "tests/input_images/image2.jpg"
    nonogram_image = get_image(NONOGRAM_IMAGE_PATH)
    nonogram_image_name = get_image_name(NONOGRAM_IMAGE_PATH)
    transformed_image = transform_image(nonogram_image)
    COUNTER = test_get_num_rows_cols_from_image(transformed_image)
    print(COUNTER)
