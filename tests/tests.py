"""Test functions from source code files.

Test functions from nonogram_full_array_from_image.
Test functions from formatted_array_from_full_array.
    """

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
        """Testing get_top_left_rectange function"""
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
            formatted_array_from_full_array.get_num_rows_cols(
                [["", "", "", "", 1, "", "", 1, ""],
                 ["", "", "", "", 1, 4, 4, 1, ""],
                 ["", "", "", 4, 2, 1, 1, 2, 4],
                 ["", "", 4, "", "", "", "", "", ""],
                 [1, 2, 1, "", "", "", "", "", ""],
                 ["", "", 6, "", "", "", "", "", ""],
                 [1, 2, 1, "", "", "", "", "", ""],
                 ["", 2, 2, "", "", "", "", "", ""],
                 ["", "", 4, "", "", "", "", "", ""]]), 3)

    def test_get_teal_string(self):
        """Test get_teal_string function"""
        grid_array = [["", "", "", "", 1, "", "", 1, ""],
                      ["", "", "", "", 1, 4, 4, 1, ""],
                      ["", "", "", 4, 2, 1, 1, 2, 4],
                      ["", "", 4, "", "", "", "", "", ""],
                      [1, 2, 1, "", "", "", "", "", ""],
                      ["", "", 6, "", "", "", "", "", ""],
                      [1, 2, 1, "", "", "", "", "", ""],
                      ["", 2, 2, "", "", "", "", "", ""],
                      ["", "", 4, "", "", "", "", "", ""]]
        transposed_array = list(map(list, zip(*grid_array)))
        num_rows = formatted_array_from_full_array.get_num_rows_cols(
            grid_array)
        num_cols = formatted_array_from_full_array.get_num_rows_cols(
            transposed_array)
        ver_array = formatted_array_from_full_array.get_row_col_array(
            grid_array, num_cols)
        hor_array = formatted_array_from_full_array.get_row_col_array(
            transposed_array, num_rows)
        self.assertEqual(
            formatted_array_from_full_array.get_teal_string(
                ver_array, hor_array),
            ('{"ver":[[4],[1,2,1],[6],[1,2,1],[2,2],[4]],'
             '"hor":[[4],[1,1,2],[4,1],[4,1],[1,1,2],[4]]}')
        )


if __name__ == "__main__":
    unittest.main()
