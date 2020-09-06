"""Test functions from source code files.

Test functions from nonogram_array_from_image.
    """

import unittest
from .context import nonogram_array_from_image


class TestNonogramFullArrayFromImage(unittest.TestCase):
    """Testing nonogram_array_from_image"""

    def test_get_image(self):
        """Testing get_image function"""
        self.assertIsNotNone(
            nonogram_array_from_image.get_image(
                "tests/input_images/image1.jpg"))
        self.assertIsNotNone(
            nonogram_array_from_image.get_image(
                "tests/input_images/image2.jpg"))

    def test_transform_image(self):
        """Testing transform_image function"""
        image = nonogram_array_from_image.get_image(
            "tests/input_images/image1.jpg")
        self.assertIsNotNone(
            nonogram_array_from_image.transform_image(image))

        image = nonogram_array_from_image.get_image(
            "tests/input_images/image2.jpg")
        self.assertIsNotNone(
            nonogram_array_from_image.transform_image(image))

        image = nonogram_array_from_image.get_image(
            "tests/input_images/image3.jpg")
        self.assertIsNotNone(
            nonogram_array_from_image.transform_image(image))

    def test_get_num_rows_cols_from_image(self):
        """Test get_num_rows_cols_from_image"""
        image = "tests/input_images/image1.jpg"
        nonogram_image = nonogram_array_from_image.get_image(image)
        transformed_image = nonogram_array_from_image.transform_image(
            nonogram_image)
        self.assertEqual(nonogram_array_from_image.get_num_rows_cols_from_image(
            transformed_image), (20, 38))

        image = "tests/input_images/image2.jpg"
        nonogram_image = nonogram_array_from_image.get_image(image)
        transformed_image = nonogram_array_from_image.transform_image(
            nonogram_image)
        self.assertEqual(nonogram_array_from_image.get_num_rows_cols_from_image(
            transformed_image), (26, 26))

        image = "tests/input_images/image3.jpg"
        nonogram_image = nonogram_array_from_image.get_image(image)
        transformed_image = nonogram_array_from_image.transform_image(
            nonogram_image)
        self.assertEqual(nonogram_array_from_image.get_num_rows_cols_from_image(
            transformed_image), (61, 61))

    def test_draw_improved_grid_lines(self):
        """Test draw_improved_grid_lines"""
        image = nonogram_array_from_image.get_image(
            "tests/input_images/image1.jpg")
        transformed_image = nonogram_array_from_image.transform_image(
            image)
        removed_grid_lines = nonogram_array_from_image.remove_grid_lines(
            transformed_image)
        number_of_rows = 20
        number_of_cols = 38
        self.assertIsNotNone(
            nonogram_array_from_image.draw_improved_grid_lines(
                removed_grid_lines, number_of_rows, number_of_cols))

        image = nonogram_array_from_image.get_image(
            "tests/input_images/image2.jpg")
        transformed_image = nonogram_array_from_image.transform_image(
            image)
        removed_grid_lines = nonogram_array_from_image.remove_grid_lines(
            transformed_image)
        number_of_rows = 26
        number_of_cols = 26
        self.assertIsNotNone(
            nonogram_array_from_image.draw_improved_grid_lines(
                removed_grid_lines, number_of_rows, number_of_cols))

        image = nonogram_array_from_image.get_image(
            "tests/input_images/image3.jpg")
        transformed_image = nonogram_array_from_image.transform_image(
            image)
        removed_grid_lines = nonogram_array_from_image.remove_grid_lines(
            transformed_image)
        number_of_rows = 61
        number_of_cols = 61
        self.assertIsNotNone(
            nonogram_array_from_image.draw_improved_grid_lines(
                removed_grid_lines, number_of_rows, number_of_cols))

    def test_get_array_from_grid(self):
        """Testing get_array_from_grid"""
        nonogram_image_path = "tests/input_images/image1.jpg"
        nonogram_image = nonogram_array_from_image.get_image(
            nonogram_image_path)
        transformed_image = nonogram_array_from_image.transform_image(
            nonogram_image)
        number_of_rows, number_of_cols = nonogram_array_from_image.get_num_rows_cols_from_image(
            transformed_image)
        finished_array = nonogram_array_from_image.get_array_from_grid(
            transformed_image, number_of_rows, number_of_cols)
        self.assertIsNotNone(finished_array)

        nonogram_image_path = "tests/input_images/image2.jpg"
        nonogram_image = nonogram_array_from_image.get_image(
            nonogram_image_path)
        transformed_image = nonogram_array_from_image.transform_image(
            nonogram_image)
        number_of_rows, number_of_cols = nonogram_array_from_image.get_num_rows_cols_from_image(
            transformed_image)
        finished_array = nonogram_array_from_image.get_array_from_grid(
            transformed_image, number_of_rows, number_of_cols)
        self.assertIsNotNone(finished_array)

        nonogram_image_path = "tests/input_images/image3.jpg"
        nonogram_image = nonogram_array_from_image.get_image(
            nonogram_image_path)
        transformed_image = nonogram_array_from_image.transform_image(
            nonogram_image)
        number_of_rows, number_of_cols = nonogram_array_from_image.get_num_rows_cols_from_image(
            transformed_image)
        finished_array = nonogram_array_from_image.get_array_from_grid(
            transformed_image, number_of_rows, number_of_cols)
        self.assertIsNotNone(finished_array)

    def test_organize_array_by_rows(self):
        """Testing organize_array_by_rows"""
        number_of_cols = 9
        array = [
            "",
            "",
            "",
            "",
            1,
            "",
            "",
            1,
            "",
            "",
            "",
            "",
            "",
            1,
            4,
            4,
            1,
            "",
            "",
            "",
            "",
            4,
            2,
            1,
            1,
            2,
            4,
            "",
            "",
            4,
            "",
            "",
            "",
            "",
            "",
            "",
            1,
            2,
            1,
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            6,
            "",
            "",
            "",
            "",
            "",
            "",
            1,
            2,
            1,
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            2,
            2,
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            4,
            "",
            "",
            "",
            "",
            "",
            ""]
        self.assertEqual(
            nonogram_array_from_image.organize_array_by_rows(
                array, number_of_cols), [
                    ["", "", "", "", 1, "", "", 1, ""],
                    ["", "", "", "", 1, 4, 4, 1, ""],
                    ["", "", "", 4, 2, 1, 1, 2, 4],
                    ["", "", 4, "", "", "", "", "", ""],
                    [1, 2, 1, "", "", "", "", "", ""],
                    ["", "", 6, "", "", "", "", "", ""],
                    [1, 2, 1, "", "", "", "", "", ""],
                    ["", 2, 2, "", "", "", "", "", ""],
                    ["", "", 4, "", "", "", "", "", ""]])

    def test_get_num_rows_cols(self):
        """Testing get_num_rows function"""
        self.assertEqual(
            nonogram_array_from_image.get_num_rows_cols(
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
        number_of_cols = 9
        array = [
            "",
            "",
            "",
            "",
            1,
            "",
            "",
            1,
            "",
            "",
            "",
            "",
            "",
            1,
            4,
            4,
            1,
            "",
            "",
            "",
            "",
            4,
            2,
            1,
            1,
            2,
            4,
            "",
            "",
            4,
            "",
            "",
            "",
            "",
            "",
            "",
            1,
            2,
            1,
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            6,
            "",
            "",
            "",
            "",
            "",
            "",
            1,
            2,
            1,
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            2,
            2,
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            4,
            "",
            "",
            "",
            "",
            "",
            ""]
        grid_array = nonogram_array_from_image.organize_array_by_rows(
            array, number_of_cols)
        transposed_array = list(map(list, zip(*grid_array)))
        num_rows = nonogram_array_from_image.get_num_rows_cols(
            grid_array)
        num_cols = nonogram_array_from_image.get_num_rows_cols(
            transposed_array)
        ver_array = nonogram_array_from_image.get_row_col_array(
            grid_array, num_cols)
        hor_array = nonogram_array_from_image.get_row_col_array(
            transposed_array, num_rows)
        self.assertEqual(
            nonogram_array_from_image.get_teal_string(
                ver_array, hor_array),
            ('{"ver":[[4],[1,2,1],[6],[1,2,1],[2,2],[4]],'
             '"hor":[[4],[1,1,2],[4,1],[4,1],[1,1,2],[4]]}')
        )


if __name__ == "__main__":
    unittest.main()
