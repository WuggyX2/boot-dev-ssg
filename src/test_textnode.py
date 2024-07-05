"""
Test cases for the TextNode module
"""

import unittest

from textnode import TextNode, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)

    def test_repr_without_url(self):
        node = TextNode("This is a text node", "bold")
        self.assertEqual(repr(node), "TextNode(This is a text node, bold, None)")

    def test_repr_with_url(self):
        node = TextNode("This is a text node", "bold", "https://www.boot.dev")
        self.assertEqual(repr(node), "TextNode(This is a text node, bold, https://www.boot.dev)")

    def test_text_node_to_html_node(self):
        node = text_node_to_html_node(TextNode("This is a paragraph", "text"))
        self.assertEqual(repr(node), "LeafNode(None, This is a paragraph, None)")

    def test_code_text_node_to_html_node(self):
        node = text_node_to_html_node(TextNode("This is a paragraph", "code"))
        self.assertEqual(repr(node), "LeafNode(code, This is a paragraph, None)")

    def test_img_text_node_to_html_node(self):
        node = text_node_to_html_node(TextNode("This is a paragraph", "image", "https://example.com"))
        self.assertEqual(repr(node), "LeafNode(img, , {'src': 'https://example.com'})")

    def test_italic_text_node_to_html_node(self):
        node = text_node_to_html_node(TextNode("This is a paragraph", "italic"))
        self.assertEqual(repr(node), "LeafNode(i, This is a paragraph, None)")

    def test_link_text_node_to_html_node(self):
        node = text_node_to_html_node(TextNode("This is a paragraph", "link", "https://example.com"))
        self.assertEqual(repr(node), "LeafNode(a, This is a paragraph, {'href': 'https://example.com'})")
