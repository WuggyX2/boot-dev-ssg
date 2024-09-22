"""
Unit tests for markdown_utils.py

"""

from unittest import TestCase
from markdown_utils import (
    is_quote_block,
    is_unordered_list_block,
    is_ordered_list_block,
    is_heading_block,
    is_code_block,
)


class TestMarkdownUtils(TestCase):
    """
    Collection of unit tests for markdown_utils.py
    """

    def test_is_quote_block(self):
        """
        Test is_quote_block function
        """
        test_cases = [
            ("", False),
            (">", True),
            ("> this is a quote block", True),
            ("> this is a quote block\n> this is a quote block", True),
            ("> this is a quote block\nthis is not a quote block", False),
            ("> this is a quote block\n> this is a quote block\n", False),
            (
                "> this is a quote block\n> this is a quote block\n> this is a quote block",
                True,
            ),
        ]

        for block, expected in test_cases:
            with self.subTest(block=block):
                self.assertEqual(is_quote_block(block), expected)

    def test_is_unordered_list_block(self):
        """
        Test is_unordered_list_block function
        """
        test_cases = [
            ("", False),
            ("-", True),
            ("*", True),
            ("* this is a list block", True),
            ("- this is a list block", True),
            ("* this is a list block\n- this is a list block", True),
            ("* this is a list block", True),
            ("* this is a list block\n* this is a list block", True),
            ("* this is a list block\nthis is not a list block", False),
            ("* this is a list block\n* this is a list block\n", False),
        ]

        for block, expected in test_cases:
            with self.subTest(block=block):
                self.assertEqual(is_unordered_list_block(block), expected)

    def test_is_ordered_list_block(self):
        """
        Test is_ordered_list_block function
        """
        test_cases = [
            ("", False),
            ("1.", True),
            ("1. this is a list block", True),
            ("1. this is a list block\n2. this is a list block", True),
            ("1. this is a list block\nthis is not a list block", False),
            ("1. this is a list block\n1. this is a list block\n", False),
        ]

        for block, expected in test_cases:
            with self.subTest(block=block):
                self.assertEqual(is_ordered_list_block(block), expected)

    def test_heading_block(self):
        """
        Test is_heading_block function
        """
        test_cases = [
            ("", False),
            ("# heading", True),
            ("## heading", True),
            ("### heading", True),
            ("#### heading", True),
            ("##### heading", True),
            ("###### heading", True),
            ("####### heading", False),
            ("heading", False),
            ("#heading", False),
        ]

        for block, expected in test_cases:
            with self.subTest(block=block):
                self.assertEqual(is_heading_block(block), expected)


    def test_is_code_block(self):
        """
        Test is_code_block function
        """
        test_cases = [
            ("```python\nprint('hello world')\n```", True),
            ("```python\nprint('hello world')", False),
            ("print('hello world')\n```", False),
            ("```python\nprint('hello world')", False)
        ]

        for block, expected in test_cases:
            with self.subTest(block=block):
                self.assertEqual(is_code_block(block), expected)


