import unittest
from .context import nonogram_from_image


class test_nonogram_from_image(unittest.TestCase):
    """Test cases for nonogram_from_image"""

    def test_get_image(self):
        self.assertIsNotNone(nonogram_from_image.get_image(
            "tests/input_images/image1.jpg"))
        self.assertIsNotNone(nonogram_from_image.get_image(
            "tests/input_images/image2.jpg"))

    def test_transform_image(self):
        image = nonogram_from_image.get_image("tests/input_images/image1.jpg")
        image_name = nonogram_from_image.get_image_name("tests/input_images/image1.jpg")
        self.assertIsNotNone(nonogram_from_image.transform_image(image, image_name))

        image = nonogram_from_image.get_image("tests/input_images/image2.jpg")
        image_name = nonogram_from_image.get_image_name("tests/input_images/image2.jpg")
        self.assertIsNotNone(nonogram_from_image.transform_image(image, image_name))
    
    def test_get_top_left_rectange(self):
        image = nonogram_from_image.get_image("tests/input_images/image1.jpg")
        image_name = nonogram_from_image.get_image_name("tests/input_images/image1.jpg")
        transformed_image = nonogram_from_image.transform_image(image, image_name)
        column_area = nonogram_from_image.get_top_left_rectange(transformed_image, image_name)
        self.assertIsNotNone(column_area)

        image = nonogram_from_image.get_image("tests/input_images/image2.jpg")
        image_name = nonogram_from_image.get_image_name("tests/input_images/image2.jpg")
        transformed_image = nonogram_from_image.transform_image(image, image_name)
        column_area = nonogram_from_image.get_top_left_rectange(transformed_image, image_name)
        self.assertIsNotNone(column_area)


if __name__ == "__main__":
    unittest.main()
