"""Get grid array from nonogram image"""
# imports
import os
import cv2
import pytesseract


def get_image(path):
    """Get image given path"""
    return cv2.imread(path)


def get_image_name(path):
    """Get image name"""
    return os.path.basename(path)


def get_grid_size(image, image_name):
    """Get grid dimensions"""
    # get pytesseract
    pytesseract.pytesseract.tesseract_cmd = "Tesseract-OCR/tesseract"

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
    cropped_image = image[y_coord - 40:y_coord,
                          (x_coord + width) // 2:x_coord + width]

    text = pytesseract.image_to_string(cropped_image)

    text = text.replace("l", "1")

    separator = "#"
    grid_size = text.split(separator, 1)[0].strip()

    grid_width, grid_height = grid_size.split('x')

    cropped_image = image[y_coord:y_coord + height,
                          x_coord:x_coord + width]

    cell_width_restriction = cropped_image.shape[1] / int(grid_width)
    cell_height_restriction = cropped_image.shape[0] / int(grid_height)

    cell_size_restriction = cell_width_restriction * cell_height_restriction

    cropped_gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
    cropped_blurred = cv2.GaussianBlur(cropped_gray, (3, 3), 0)
    cropped_edges = cv2.Canny(cropped_blurred, 100, 300, apertureSize=3)

    contours, _ = cv2.findContours(
        cropped_edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        x_coord, y_coord, width, height = cv2.boundingRect(contour)
        if (abs(cropped_image.shape[0] - y_coord) <
                cell_height_restriction) and (x_coord < cell_width_restriction):
            area = cv2.contourArea(contour)
            if area * 1.1 < cell_size_restriction:
                cv2.drawContours(cropped_image, contour, 0, (255, 255, 0), 3)
                break
            
    cv2.imwrite(
        "tests/output_images/further_edits/{name}".format(name=image_name), cropped_image)

    return cropped_image


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
    cv2.imwrite(
        "tests/output_images/cropped/{name}".format(name=image_name), cropped_image)

    return cropped_image


def get_top_left_rectange(image, image_name):
    """Given the image of the puzzle area, return number for columns"""

    # base transformations
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    _, thresh_img = cv2.threshold(
        image_blurred, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    # filter out numbers
    contours = cv2.findContours(
        thresh_img,
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 1000:
            cv2.drawContours(thresh_img, [contour], -1, (0, 0, 0), -1)

    cv2.imwrite(
        "tests/output_images/further_edits/{name}".format(name=image_name), thresh_img)

    return thresh_img


if __name__ == "__main__":
    #nonogram_image_path = input("Please enter path to image file: ")
    nonogram_image_path = "C:/Users/Peter/Documents/GitHub/nonogram_from_image/tests/input_images/image1.jpg"
    nonogram_image = get_image(nonogram_image_path)
    nonogram_image_name = get_image_name(nonogram_image_path)
    get_grid_size(nonogram_image, nonogram_image_name)
