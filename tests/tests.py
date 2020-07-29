"""Create portable serialized representations of Python objects.

See module copyreg for a mechanism for registering custom picklers.
See module pickletools source for extensive comments.

Classes:

    TestNonogramFullArrayFromImage

Functions:

    test_get_image(self)
    test_transform_image(self)
    test_get_top_left_rectange(self)
    test_get_num_rows(self)
    test_get_num_cols(self)

Misc variables:

    image
    image_name
    transformed_image
    column_area"""

import unittest
from .context import nonogram_full_array_from_image
from .context import formatted_array_from_full_array


class TestNonogramFullArrayFromImage(unittest.TestCase):
    """Testing various functions

    Testing formatted_array_from_full_array and
    testing nonogram_full_array_from_image"""
    def test_get_image(self):
        """Testing get_image function"""
        self.assertIsNotNone(
            nonogram_full_array_from_image.get_image(
                "tests/input_images/image1.jpg"))
        self.assertIsNotNone(
            nonogram_full_array_from_image.get_image(
                "tests/input_images/image2.jpg"))

    def test_transform_image(self):
        """Testing transform_image function"""
        image = nonogram_full_array_from_image.get_image(
            "tests/input_images/image1.jpg")
        image_name = nonogram_full_array_from_image.get_image_name(
            "tests/input_images/image1.jpg")
        self.assertIsNotNone(
            nonogram_full_array_from_image.transform_image(image, image_name))

        image = nonogram_full_array_from_image.get_image(
            "tests/input_images/image2.jpg")
        image_name = nonogram_full_array_from_image.get_image_name(
            "tests/input_images/image2.jpg")
        self.assertIsNotNone(
            nonogram_full_array_from_image.transform_image(image, image_name))

        image = nonogram_full_array_from_image.get_image(
            "tests/input_images/image3.jpg")
        image_name = nonogram_full_array_from_image.get_image_name(
            "tests/input_images/image3.jpg")
        self.assertIsNotNone(
            nonogram_full_array_from_image.transform_image(image, image_name))

    def test_get_top_left_rectange(self):
        """Testing get_top_left_rectangle function"""
        image = nonogram_full_array_from_image.get_image(
            "tests/input_images/image1.jpg")
        image_name = nonogram_full_array_from_image.get_image_name(
            "tests/input_images/image1.jpg")
        transformed_image = nonogram_full_array_from_image.transform_image(
            image, image_name)
        column_area = nonogram_full_array_from_image.get_top_left_rectange(
            transformed_image, image_name)
        self.assertIsNotNone(column_area)

        image = nonogram_full_array_from_image.get_image(
            "tests/input_images/image2.jpg")
        image_name = nonogram_full_array_from_image.get_image_name(
            "tests/input_images/image2.jpg")
        transformed_image = nonogram_full_array_from_image.transform_image(
            image, image_name)
        column_area = nonogram_full_array_from_image.get_top_left_rectange(
            transformed_image, image_name)
        self.assertIsNotNone(column_area)

        image = nonogram_full_array_from_image.get_image(
            "tests/input_images/image3.jpg")
        image_name = nonogram_full_array_from_image.get_image_name(
            "tests/input_images/image3.jpg")
        transformed_image = nonogram_full_array_from_image.transform_image(
            image, image_name)
        column_area = nonogram_full_array_from_image.get_top_left_rectange(
            transformed_image, image_name)
        self.assertIsNotNone(column_area)

    def test_get_num_rows(self):
        """Testing get_num_rows function"""
        self.assertEqual(
            formatted_array_from_full_array.get_num_rows(
                [["", "", "", "", 1, "", "", 1, ""],
                 ["", "", "", "", 1, 4, 4, 1, ""],
                 ["", "", "", 4, 2, 1, 1, 2, 4],
                 ["", "", 4, "", "", "", "", "", ""],
                 [1, 2, 1, "", "", "", "", "", ""],
                 ["", "", 6, "", "", "", "", "", ""],
                 [1, 2, 1, "", "", "", "", "", ""],
                 ["", 2, 2, "", "", "", "", "", ""],
                 ["", "", 4, "", "", "", "", "", ""]]), 3)

    def test_get_num_cols(self):
        """Testing get_num_cols function"""
        self.assertEqual(
            formatted_array_from_full_array.get_num_cols(
                [["", "", "", "", 1, "", "", 1, ""],
                 ["", "", "", "", 1, 4, 4, 1, ""],
                 ["", "", "", 4, 2, 1, 1, 2, 4],
                 ["", "", 4, "", "", "", "", "", ""],
                 [1, 2, 1, "", "", "", "", "", ""],
                 ["", "", 6, "", "", "", "", "", ""],
                 [1, 2, 1, "", "", "", "", "", ""],
                 ["", 2, 2, "", "", "", "", "", ""],
                 ["", "", 4, "", "", "", "", "", ""]]), 3)


if __name__ == "__main__":
    unittest.main()
