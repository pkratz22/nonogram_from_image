import unittest
from .context import nonogram_from_image


class test_nonogram_from_image(unittest.TestCase):
    """Test cases for nonogram_from_image"""

    def test_get_image(self):
        self.assertIsNotNone(nonogram_from_image.get_image(
            "tests/input_images/image1.jpg"))
        self.assertIsNotNone(nonogram_from_image.get_image(
            "tests/input_images/image2.jpg"))

    def test_get_puzzle_space(self):
        image = nonogram_from_image.get_image("tests/input_images/image1.jpg")
        self.assertIsNotNone(nonogram_from_image.get_puzzle_space(image))

        image = nonogram_from_image.get_image("tests/input_images/image2.jpg")
        self.assertIsNotNone(nonogram_from_image.get_puzzle_space(image))


if __name__ == "__main__":
    unittest.main()
