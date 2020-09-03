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


def get_binary_image(image):
    """Converts image to black and white"""
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (_, black_white_image) = cv2.threshold(
        gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return black_white_image


def get_num_rows_cols_from_image(image):
    """Get cell dimensions"""
    # transform image
    black_white_image = get_binary_image(image)
    kernel = np.ones((1, 5), np.uint8)
    dilation = cv2.dilate(black_white_image, kernel, iterations=1)

    cv2.imwrite('tests/output_images/image1.jpg', dilation)

    for row in range(dilation.shape[0]):
        count = 0
        temp_color = dilation[row][0]
        for col in range(dilation.shape[1]):
            current_color = dilation[row][col]
            if temp_color != current_color:
                if temp_color == 255:
                    temp_color = 0
                else:
                    temp_color = 255
                count += 1
        if count > 2:
            break

    num_cols = int(round(count / 2))
    approximate_col_side_length = dilation.shape[1] / num_cols
    num_rows = int(round(dilation.shape[0] / approximate_col_side_length))
    return num_rows, num_cols


def remove_grid_lines(image):
    """Remove grid lines from image"""
    get_binary_image(image)
    return

if __name__ == "__main__":
    #nonogram_image_path = input("Please enter path to image file: ")
    NONOGRAM_IMAGE_PATH = "tests/input_images/image1.jpg"
    nonogram_image = get_image(NONOGRAM_IMAGE_PATH)
    nonogram_image_name = get_image_name(NONOGRAM_IMAGE_PATH)
    transformed_image = transform_image(nonogram_image)
    number_of_rows, number_of_cols = get_num_rows_cols_from_image(transformed_image)
    print(str(number_of_rows) + ", " + str(number_of_cols))
