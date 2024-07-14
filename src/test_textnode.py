"""
Test cases for the TextNode module
"""

import unittest

from textnode import (
    TextNode,
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
)


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
        self.assertEqual(
            repr(node), "TextNode(This is a text node, bold, https://www.boot.dev)"
        )

    def test_text_node_to_html_node(self):
        node = text_node_to_html_node(TextNode("This is a paragraph", "text"))
        self.assertEqual(repr(node), "LeafNode(None, This is a paragraph, None)")

    def test_code_text_node_to_html_node(self):
        node = text_node_to_html_node(TextNode("This is a paragraph", "code"))
        self.assertEqual(repr(node), "LeafNode(code, This is a paragraph, None)")

    def test_img_text_node_to_html_node(self):
        node = text_node_to_html_node(
            TextNode("This is a paragraph", "image", "https://example.com")
        )
        self.assertEqual(repr(node), "LeafNode(img, , {'src': 'https://example.com'})")

    def test_italic_text_node_to_html_node(self):
        node = text_node_to_html_node(TextNode("This is a paragraph", "italic"))
        self.assertEqual(repr(node), "LeafNode(i, This is a paragraph, None)")

    def test_link_text_node_to_html_node(self):
        """
        Test text_node_to_html_node with a link
        """
        node = text_node_to_html_node(
            TextNode("This is a paragraph", "link", "https://example.com")
        )
        self.assertEqual(
            repr(node),
            "LeafNode(a, This is a paragraph, {'href': 'https://example.com'})",
        )

    def test_text_nodes_code_block(self):
        """
        Test split_nodes_delimiter with a code block
        """
        node = TextNode("This is text with a `code block` word", "text")
        new_nodes = split_nodes_delimiter([node], "`", "code")
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", "text"),
                TextNode("code block", "code"),
                TextNode(" word", "text"),
            ],
        )

    def test_invalid_markdown(self):
        """
        Test split_nodes_delimiter with invalid markdown
        """
        node = TextNode("This is text with a `code block word", "text")

        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", "code")

    def test_invalid_markdown2(self):
        """
        Test split_nodes_delimiter with invalid markdown
        """
        node = TextNode("This is text with a `code block word``", "text")

        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", "code")

    def test_split_modes_delimiter_invalid_type(self):
        """
        Test split_nodes_delimiter with invalid type. It should raise a ValueError
        """
        node = TextNode("This is text with a `code block` word", "text")

        with self.assertRaises(ValueError):
            split_nodes_delimiter(
                [node], "`", "invalid"  # pyright: ignore[reportArgumentType]
            )

    def test_multiple_different_blocks(self):
        """
        Test split_nodes_delimiter with multiple different blocks
        """
        node = TextNode(
            "This is text with a `code block` word and *italic* text", "text"
        )
        new_nodes = split_nodes_delimiter([node], "`", "code")
        new_nodes = split_nodes_delimiter(new_nodes, "*", "italic")
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", "text"),
                TextNode("code block", "code"),
                TextNode(" word and ", "text"),
                TextNode("italic", "italic"),
                TextNode(" text", "text"),
            ],
        )

    def test_multiple_next_to_each_other(self):
        """
        Test split_nodes_delimiter with multiple blocks next to each other
        """
        node = TextNode("This is text with a `code block``code block 2`", "text")
        new_nodes = split_nodes_delimiter([node], "`", "code")

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", "text"),
                TextNode("code block", "code"),
                TextNode("code block 2", "code"),
            ],
        )

    def test_extract_images_from_text(self):
        """
        Test extract_markdown_images
        """
        text = """This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)
         and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"""

        images = extract_markdown_images(text)
        self.assertEqual(
            images,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_extract_images_no_matches(self):
        """
        Test extract_markdown_images with no matches
        """
        text = "This is text with no images"
        images = extract_markdown_images(text)
        self.assertEqual(images, [])


    def test_extract_links_from_text(self):
        """
        Test extract_markdown_links
        """
        text = """This is text with a [link](https://www.boot.dev)
         and [another link](https://www.boot.dev)"""

        links = extract_markdown_links(text)
        self.assertEqual(
            links,
            [
                ("link", "https://www.boot.dev"),
                ("another link", "https://www.boot.dev"),
            ],
        )

    def test_extract_links_no_matches(self):
        """
        Test extract_markdown_links with no matches
        """

        text = "This is text with no links"
        links = extract_markdown_links(text)
        self.assertEqual(links, [])


    def test_do_not_match_images_in_links(self):
        """
        Test extract_markdown_images with images in links
        """
        text = """This is text with a [link](https://www.boot.dev)
         and ![image](https://i.imgur.com/aKaOqIh.gif)"""

        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        self.assertEqual(images, [("image", "https://i.imgur.com/aKaOqIh.gif")])
        self.assertEqual(links, [("link", "https://www.boot.dev")])
