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


def get_grid_fillable_area(image):
    """Get dimensions of fillable area"""
    # get pytesseract
    pytesseract.pytesseract.tesseract_cmd = "Tesseract-OCR/tesseract"

    text = pytesseract.image_to_string(image)

    text = text.replace("l", "1")

    separator = "#"
    grid_size = text.split(separator, 1)[0].strip()

    grid_width, grid_height = grid_size.split('x')

    return (grid_width, grid_height)


def get_fillable_area_dimensions(image):
    """Get grid dimensions"""
    # apply base transformations
    image_blurred = base_transformation(image)

    # get edges using Canny method
    edges = cv2.Canny(image_blurred, 100, 300, apertureSize=3)

    # get largest contour
    x_coord, y_coord, width, _ = get_largest_contour_bounding_box(edges)

    # creates image with contour
    cropped_image = image[y_coord - 40:y_coord,
                          (x_coord + width) // 2:x_coord + width]

    # get fillable area width and height in number of cells
    grid_width, grid_height = get_grid_fillable_area(cropped_image)

    return (grid_width, grid_height)


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


def get_individual_cell_dimensions(image):
    """Get cell dimensions"""
    # crop image to grid
    cropped_image = transform_image(image)

    # get grid width and height in number of cells
    grid_width, grid_height = get_fillable_area_dimensions(image)

    cell_width_restriction = cropped_image.shape[1] / int(grid_width)
    cell_height_restriction = cropped_image.shape[0] / int(grid_height)

    cell_size_restriction = cell_width_restriction * cell_height_restriction

    return (cell_width_restriction, cell_height_restriction, cell_size_restriction)


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
    NONOGRAM_IMAGE_PATH = "tests/input_images/image1.jpg"
    nonogram_image = get_image(NONOGRAM_IMAGE_PATH)
    nonogram_image_name = get_image_name(NONOGRAM_IMAGE_PATH)
    get_individual_cell_dimensions(nonogram_image)
    