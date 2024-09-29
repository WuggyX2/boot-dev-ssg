from unittest import TestCase
from main import extract_title


class TestMain(TestCase):

    """
    Test cases for the main module
    """
    def test_extract_title_success(self):
        """
        Test that the title is extracted successfully
        """
        title = extract_title("# My Title")
        self.assertEqual(title, "My Title")

    def test_no_title(self):
        """
        Test that an exception is raised when no title is found
        """
        with self.assertRaises(Exception):
            extract_title("No title here")


    def test_multiple_titles(self):
        """
        Test that the first title is extracted if there are multiple titles
        """
        test_input = """# Title 1\n# Title 2"""
        self.assertEqual(extract_title(test_input), "Title 1")


    def test_multiple_titles_with_different_levels(self):
        """
        Test that the first title is extracted if there are multiple titles with different levels
        """
        test_input = """# Title 1\n## Title 2"""
        self.assertEqual(extract_title(test_input), "Title 1")
