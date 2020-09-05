"""Get grid array from nonogram image"""
# imports
import os
import cv2
import numpy as np
import pytesseract


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
    (thresh, black_white_image) = cv2.threshold(
        gray_image, 150, 255, cv2.THRESH_BINARY_INV)
    return thresh, black_white_image


def get_num_rows_cols_from_image(image):
    """Get cell dimensions"""
    # transform image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (_, black_white_image) = cv2.threshold(
        gray_image, 150, 255, cv2.THRESH_BINARY)
    kernel = np.ones((1, 5), np.uint8)
    erosion = cv2.erode(black_white_image, kernel, iterations=1)

    for row in range(erosion.shape[0]):
        count = 0
        temp_color = erosion[row][0]
        for col in range(erosion.shape[1]):
            current_color = erosion[row][col]
            if temp_color != current_color:
                if temp_color == 255:
                    temp_color = 0
                else:
                    temp_color = 255
                count += 1
        if count > 2:
            pixel_row_for_col_counting = row + 1
            break

    temp_color = 0
    count = 0
    for col in range(erosion.shape[1]):
        current_color = erosion[pixel_row_for_col_counting][col]
        if temp_color != current_color:
            if temp_color == 255:
                temp_color = 0
            else:
                temp_color = 255
            count += 1

    num_cols = int(round(count / 2))
    approximate_col_side_length = erosion.shape[1] / num_cols
    num_rows = int(round(erosion.shape[0] / approximate_col_side_length))
    return num_rows, num_cols


def remove_horizontal_grid_lines(image):
    """Remove horizontal grid lines from image"""
    thresh = get_binary_image(image)[1]

    # Remove horizontal
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
    detected_lines = cv2.morphologyEx(
        thresh,
        cv2.MORPH_OPEN,
        horizontal_kernel,
        iterations=2)
    contours = cv2.findContours(
        detected_lines,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    for contour in contours:
        cv2.drawContours(image, [contour], -1, (255, 255, 255), 2)

    # Repair image
    repair_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 6))
    result = 255 - cv2.morphologyEx(255 - image,
                                    cv2.MORPH_CLOSE,
                                    repair_kernel,
                                    iterations=1)

    return result


def remove_vertical_grid_lines(image):
    """Remove vertical grid lines from image"""
    thresh = get_binary_image(image)[1]

    # Remove vertical
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25))
    detected_lines = cv2.morphologyEx(
        thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
    contours = cv2.findContours(
        detected_lines,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    for contour in contours:
        cv2.drawContours(image, [contour], -1, (255, 255, 255), 2)

    # Repair image
    repair_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (6, 1))
    result = 255 - cv2.morphologyEx(255 - image,
                                    cv2.MORPH_CLOSE,
                                    repair_kernel,
                                    iterations=1)
    return result


def remove_grid_lines(image):
    """Remove all grid lines"""
    image_minus_horizontal = remove_horizontal_grid_lines(image)
    image_minus_gridlines = remove_vertical_grid_lines(image_minus_horizontal)
    return image_minus_gridlines


def draw_improved_grid_lines(image, num_rows, num_cols):
    """Draws single pixel grid lines with no noise to get contours from"""
    row_height = image.shape[0] / num_rows
    col_width = image.shape[1] / num_cols

    for row in range(num_rows + 1):
        cv2.line(image, (0, int(row * row_height)),
                 (image.shape[1], int(row * row_height)), (255, 0, 0), 1, 1)

    for col in range(num_cols + 1):
        cv2.line(image, (int(col * col_width), 0),
                 (int(col * col_width), image.shape[0]), (255, 0, 0), 1, 1)

    cv2.line(image, (0, image.shape[0] -
                     1), (image.shape[1], image.shape[0] -
                          1), (255, 0, 0), 1, 1)
    cv2.line(image, (image.shape[1] -
                     1, 0), (image.shape[1] -
                             1, image.shape[0]), (255, 0, 0), 1, 1)

    return image


def check_cell_for_number(cell):
    """Checks cell for number"""
    pytesseract.pytesseract.tesseract_cmd = "Tesseract-OCR/tesseract"
    number = pytesseract.image_to_string(cell)
    return number


def get_array_from_grid(image, num_rows, num_cols):
    """Gets cells from grid"""
    row_height = image.shape[0] / num_rows
    col_width = image.shape[1] / num_cols
    final_array = []
    for row in range(num_rows):
        for col in range(num_cols):
            cell = image[int(row *
                             row_height):int(min((row +
                                                  1) *
                                                 row_height, image.shape[1])),
                         int(col *
                             col_width):int(min((col +
                                                 1) *
                                                col_width, image.shape[0]))]
            number = check_cell_for_number(cell)
            final_array.append(number)
    return final_array


if __name__ == "__main__":
    #nonogram_image_path = input("Please enter path to image file: ")
    NONOGRAM_IMAGE_PATH = "tests/input_images/image1.jpg"
    nonogram_image = get_image(NONOGRAM_IMAGE_PATH)
    nonogram_image_name = get_image_name(NONOGRAM_IMAGE_PATH)
    transformed_image = transform_image(nonogram_image)
    removed_grid_lines = remove_grid_lines(transformed_image)
    number_of_rows, number_of_cols = get_num_rows_cols_from_image(
        transformed_image)
    finished_array = get_array_from_grid(
        transformed_image, number_of_rows, number_of_cols)
    print(finished_array)
