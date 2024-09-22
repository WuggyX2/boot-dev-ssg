from unittest import TestCase
from markdown_handler import (
    split_nodes_delimiter,
    extract_markdown_links,
    extract_markdown_images,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
    block_to_block_type,
)
from textnode import TextNode


class TestMarkdownHandler(TestCase):
    """
    Test class for markdown_handler.py
    """

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

    def test_split_link_nodes(self):
        """
        Test split_nodes_image
        """
        node = TextNode(
            """This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)""",
            "text",
        )

        new_nodes = split_nodes_link([node])

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", "text"),
                TextNode("to boot dev", "link", "https://www.boot.dev"),
                TextNode(" and ", "text"),
                TextNode("to youtube", "link", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_split_link_nodes_no_links(self):
        """
        Test split_nodes_image with no links
        """
        node = TextNode("This is text with no links", "text")
        new_nodes = split_nodes_link([node])

        self.assertEqual(new_nodes, [node])

    def test_split_link_nodes_start(self):
        """
        Test split_nodes_image with a link at the start
        """
        node = TextNode("[boot dev](https://www.boot.dev) is a great website", "text")
        new_nodes = split_nodes_link([node])

        self.assertEqual(
            new_nodes,
            [
                TextNode("boot dev", "link", "https://www.boot.dev"),
                TextNode(" is a great website", "text"),
            ],
        )

    def test_split_image_nodes(self):
        """
        Test split_nodes_image
        """
        node = TextNode(
            """This is text with an image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)""",
            "text",
        )

        new_nodes = split_nodes_image([node])

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an image ", "text"),
                TextNode("rick roll", "image", "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and ", "text"),
                TextNode("obi wan", "image", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_split_image_nodes_no_images(self):
        """
        Test split_nodes_image with no images
        """
        node = TextNode("This is text with no images", "text")
        new_nodes = split_nodes_image([node])

        self.assertEqual(new_nodes, [node])

    def test_split_image_nodes_start(self):
        """
        Test split_nodes_image with an image at the start
        """
        node = TextNode(
            "![rick roll](https://i.imgur.com/aKaOqIh.gif) is a great image", "text"
        )
        new_nodes = split_nodes_image([node])

        self.assertEqual(
            new_nodes,
            [
                TextNode("rick roll", "image", "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" is a great image", "text"),
            ],
        )

    def test_text_to_textnodes(self):
        """
        Test text_to_textnodes
        """

        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)

        expected = [
            TextNode("This is ", "text"),
            TextNode("text", "bold"),
            TextNode(" with an ", "text"),
            TextNode("italic", "italic"),
            TextNode(" word and a ", "text"),
            TextNode("code block", "code"),
            TextNode(" and an ", "text"),
            TextNode("obi wan image", "image", "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", "text"),
            TextNode("link", "link", "https://boot.dev"),
        ]

        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_no_markdown(self):
        """
        Test text_to_textnodes with no markdown
        """

        text = "This is text with no markdown"
        nodes = text_to_textnodes(text)

        expected = [TextNode("This is text with no markdown", "text")]

        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_no_text(self):
        """
        Test text_to_textnodes with no text
        """

        text = ""
        nodes = text_to_textnodes(text)

        expected = []

        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_no_images_or_links(self):
        """
        Test text_to_textnodes with no images or links
        """

        text = "This is text with no **images** or *links*"
        nodes = text_to_textnodes(text)

        expected = [
            TextNode("This is text with no ", "text"),
            TextNode("images", "bold"),
            TextNode(" or ", "text"),
            TextNode("links", "italic"),
        ]

        self.assertEqual(nodes, expected)

    def test_markdown_to_blocks(self):
        """
        Test markdown_to_blocks
        """

        test = """# This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
        """

        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
        ]

        result = markdown_to_blocks(test)

        self.assertEqual(result, expected)

    def test_no_whitespace(self):
        """
        Test markdown_to_blocks so it removes leading and trailing whitespace
        """

        test = """
        # This is a heading

                 This is a paragraph of text. It has some **bold** and *italic* words inside of it.
        """

        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
        ]

        result = markdown_to_blocks(test)

        self.assertEqual(result, expected)

    def test_block_to_block_type_heading(self):
        """
        Test block_to_block_type with a heading
        """

        blocks = [
            ("# This is a heading", "heading"),
            (
                "This is a paragraph of text. It has **bold** and *italic* words inside of it.",
                "paragraph",
            ),
            (
                "* This is the first list item in a list block\n* This is a list item",
                "unordered_list",
            ),
            ("> This is a quote block", "quote"),
            ("```python\nprint('Hello, World!')\n```", "code"),
            (
                "1. This is an ordered list block\n2. This is another ordered list block",
                "ordered_list",
            ),
        ]

        for block, expected in blocks:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), expected)

    def test_paragraph(self):
        """
        Test markdown_to_html_node with a paragraph
        """
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        """
        Test markdown_to_html_node with multiple paragraphs
        """
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        """
        Test markdown_to_html_node with lists
        """
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        """
        Test markdown_to_html_node with headings
        """
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        """
        Test markdown_to_html_node with a blockquote
        """
        md = """> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_blockquote2(self):
        """
        Test markdown_to_html_node with a blockquote
        """
        md = """> This is a
> blockquote block

this is paragraph text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )
