"""
Unit tests for the HTMLNode and LeafNode classes.

"""

import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html(self):
        node = HTMLNode("p", "This is a paragraph", None, {"class": "paragraph"})
        self.assertEqual(node.props_to_html(), ' class="paragraph"')

    def test_props_to_html_no_props(self):
        node = HTMLNode("p", "This is a paragraph")
        self.assertEqual(node.props_to_html(), "")

    def test_print(self):
        node = HTMLNode("p", "This is a paragraph", None, {"class": "paragraph"})
        self.assertEqual(
            repr(node), "HTMLNode(p, This is a paragraph, None, {'class': 'paragraph'})"
        )


class TestLeafNode(unittest.TestCase):

    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph", {"class": "paragraph"})
        self.assertEqual(node.to_html(), '<p class="paragraph">This is a paragraph</p>')

    def test_to_html_no_props(self):
        node = LeafNode("p", "This is a paragraph")
        self.assertEqual(node.to_html(), "<p>This is a paragraph</p>")

    def test_no_tag(self):
        node = LeafNode(None, "This is a paragraph")
        self.assertEqual(node.to_html(), "This is a paragraph")

    def test_print(self):
        node = LeafNode("p", "This is a paragraph", {"class": "paragraph"})
        self.assertEqual(
            repr(node), "LeafNode(p, This is a paragraph, {'class': 'paragraph'})"
        )


class TestParentNode(unittest.TestCase):
    """Tests for the ParentNode class."""

    def test_to_html(self):
        node = ParentNode(
            "div",
            [
                LeafNode("p", "This is a paragraph"),
                LeafNode("p", "This is another paragraph"),
            ],
            {"class": "container"},
        )
        self.assertEqual(
            node.to_html(),
            '<div class="container"><p>This is a paragraph</p><p>This is another paragraph</p></div>',
        )

    def test_to_html_no_props(self):
        node = ParentNode(
            "div",
            [
                LeafNode("p", "This is a paragraph"),
                LeafNode("p", "This is another paragraph"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><p>This is a paragraph</p><p>This is another paragraph</p></div>",
        )

    def test_no_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode("div", None)
            node.to_html()

    def test_print(self):
        node = ParentNode(
            "div",
            [
                LeafNode("p", "This is a paragraph"),
                LeafNode("p", "This is another paragraph"),
            ],
            {"class": "container"},
        )
        self.assertEqual(
            repr(node),
            "ParentNode(div, [LeafNode(p, This is a paragraph, None), LeafNode(p, This is another paragraph, None)], {'class': 'container'})",
        )

    def test_nested_nodes(self):
        node = ParentNode(
            "div", [ParentNode("div", [LeafNode("p", "This is a paragraph")])]
        )
        self.assertEqual(
            node.to_html(), "<div><div><p>This is a paragraph</p></div></div>"
        )
