"""Get grid array from nonogram image"""
# imports
import os
import cv2
import numpy as np
import pytesseract


CUSTOM_CONFIG = r'--oem 3 --psm 6 outputbase digits'


def get_image(path):
    """Get image given path"""
    return cv2.imread(path)


def get_image_name(path):
    """Get image name"""
    return os.path.basename(path)


def get_grayscale(image):
    """Grayscale image"""
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def base_transformation(image):
    """Complete base transformations"""
    # make image gray
    gray = get_grayscale(image)

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
    number = pytesseract.image_to_string(cell, config=CUSTOM_CONFIG)
    if number != "":
        number = int(number)
    return number


def remove_noise(image):
    """Remove noise"""
    return cv2.medianBlur(image, 3)


def opening(image):
    """Opening"""
    kernel = np.ones((1, 3), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


def get_array_from_grid(image, num_rows, num_cols):
    """Gets cells from grid"""
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.threshold(
        image, 150, 255, cv2.THRESH_BINARY)[1]
    row_height = image.shape[0] / num_rows
    col_width = image.shape[1] / num_cols
    final_array = []
    for row in range(num_rows):
        for col in range(num_cols):
            cell = image[int(row *
                             row_height):int(min((row +
                                                  1) *
                                                 row_height, image.shape[0])),
                         int(col *
                             col_width) + 4:int(min((col +
                                                     1) *
                                                    col_width, image.shape[1])) - 2]

            rnoise = remove_noise(cell)
            processed_cell = opening(rnoise)
            number = check_cell_for_number(processed_cell)
            final_array.append(number)
    return final_array


def organize_array_by_rows(unformatted_array, num_cols):
    """Take unformatted array and make grid array"""
    num_rows = int(len(unformatted_array) / num_cols)
    array = []
    for row in range(num_rows):
        array.append(unformatted_array[row * num_cols:(row + 1) * num_cols])
    return array


def fix_array(array):
    """Have user manually fix any errors from OCR"""
    fixed = False
    while not fixed:
        for row in array:
            for col in row:
                print(str(col) + (2 - len(str(col))) * " " + "|", end=" ")
            print("\n" + ((len(row) * 4) * "-") + "\n")
        is_fixed = input("Enter Y if grid is correct. Else enter N. \n")
        if is_fixed.lower() == "y":
            fixed = True
        elif is_fixed.lower() == "n":
            row = input("Enter row of incorrect cell \n")
            if not row.isdigit():
                print("Digit not entered, will start again \n")
                continue
            row = int(row)
            for index, col in enumerate(array[row - 1]):
                print("Position - " + str(index + 1) + ", Value - " + str(col))
            col = input("Enter position of incorrect cell \n")
            if not col.isdigit():
                print("Digit not entered, will start again \n")
                continue
            col = int(col)
            print("Incorrect cell currently reads: " +
                  str(array[row - 1][int(col) - 1]) + "\n")
            new_cell = input(
                "Enter correct cell entry. If blank, press enter \n")
            if not new_cell.isdigit() and new_cell != "":
                print("Entry is not digit or blank, will start again \n")
                continue
            if new_cell.isdigit():
                new_cell = int(new_cell)
            array[row - 1][int(col) - 1] = new_cell
        else:
            print("Invalid input, will start again \n")
    return array


def get_num_rows_cols(array):
    """Get number of rows that have col data"""
    row_number = 0
    is_last_row = False
    while not is_last_row:
        is_last_row = check_if_last_row(array, row_number)
        row_number += 1
    return row_number


def check_if_last_row(array, row_number):
    """Loop through row for get_num_rows_cols"""
    for cell in range(len(array[row_number])):
        if array[row_number][cell] != "":
            if array[row_number + 1][cell] != "":
                return False
    return True


def get_row_col_array(array, rows_skipped):
    """Get col array from grid"""
    ver_hor_array = []
    total_rows = len(array)
    for row in range(rows_skipped, total_rows):
        individual_row_array = []
        for cell in range(len(array[row])):
            if array[row][cell] != "":
                individual_row_array.append(array[row][cell])
        ver_hor_array.append(individual_row_array)
    return ver_hor_array


def get_ver_hor_array_as_string(ver_hor_array):
    """Gets vertical or horizontal array as string"""
    ver_hor_string = '['
    for row_num, _ in enumerate(ver_hor_array):
        ver_hor_string += '['
        for cell in range(len(ver_hor_array[row_num])):
            ver_hor_string += str(ver_hor_array[row_num][cell]) + ','
        ver_hor_string = ver_hor_string[:-1]
        ver_hor_string += '],'
    ver_hor_string = ver_hor_string[:-1]
    ver_hor_string += ']'
    return ver_hor_string


def get_teal_string(vertical, horizontal):
    """Formats string for use in teal online tool"""
    ver_string = get_ver_hor_array_as_string(vertical)
    hor_string = get_ver_hor_array_as_string(horizontal)
    return '{"ver":' + ver_string + ',"hor":' + hor_string + '}'


def main():
    """Main function"""
    # nonogram_image_path = input("Please enter path to image file: ")
    nonogram_image_path = "tests/input_images/image1.jpg"
    nonogram_image = get_image(nonogram_image_path)
    # nonogram_image_name = get_image_name(nonogram_image_path)
    transformed_image = transform_image(nonogram_image)
    number_of_rows, number_of_cols = get_num_rows_cols_from_image(
        transformed_image)
    finished_array = get_array_from_grid(
        transformed_image, number_of_rows, number_of_cols)
    grid_array = organize_array_by_rows(finished_array, number_of_cols)
    corrected_grid_array = fix_array(grid_array)
    transposed_array = list(map(list, zip(*corrected_grid_array)))
    num_rows = get_num_rows_cols(grid_array)
    num_cols = get_num_rows_cols(transposed_array)
    ver_array = get_row_col_array(grid_array, num_cols)
    hor_array = get_row_col_array(transposed_array, num_rows)
    teal_string = get_teal_string(ver_array, hor_array)
    return teal_string

if __name__ == "__main__":
    main()
