"""
TextNode class represents a node in the AST that contains text content.

"""

import re
from typing import Self, TypeAlias, Literal, List, get_args
from types import NotImplementedType
from htmlnode import LeafNode

TextType: TypeAlias = Literal["text", "bold", "italic", "code", "link", "image"]
SplittableTextType: TypeAlias = Literal["bold", "italic", "code"]
Url: TypeAlias = str | None


class TextNode:
    """

    Attributes:
        text: The text content of the node
        text_type: The type of text this node contains
        url: The URL of the link or image, if the text is a link. Default to None
    """

    def __init__(self, text, text_type, url=None):
        self.text: str = text
        self.text_type: TextType = text_type
        self.url: Url = url

    def __eq__(self: Self, other: object) -> bool | NotImplementedType:

        if not isinstance(other, TextNode):
            return NotImplemented

        if (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        ):
            return True

        return False

    def __repr__(self: Self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    """
        Transforms a TextNode to a LeafNode or HTMLNode.
        If type is image HTML node is returned, otherwise LeafNode is returned.

    Args:
        text_node: TextNode to be transformed

    Raises:
        ValueError: if text type does not match values defined in TextType alias

    Returns:

    """
    match text_node.text_type:
        case "text":
            return LeafNode(None, text_node.text)
        case "bold":
            return LeafNode("b", text_node.text)
        case "italic":
            return LeafNode("i", text_node.text)
        case "code":
            return LeafNode("code", text_node.text)
        case "link":
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case "image":
            return LeafNode("img", "", {"src": text_node.url})
        case _:
            raise ValueError("TextNode has an invalid text type")


def split_nodes_delimiter(
    old_nodes: List[TextNode], delimiter: str, text_type: SplittableTextType
) -> List[TextNode]:
    """
    Method for splitting text nodes by a delimiter. The text nodes are split
    into two types of text nodes,one with the delimiter and the other without the delimiter.
    The delimiter text nodes are of the type specified in the text_type argument.

    Args:
        old_nodes: List of TextNodes to be split
        delimiter: Delimiter to split the text
        text_type: Type of text to be split

    Returns:

    """
    new_nodes: List[TextNode] = []

    if not text_type in get_args(SplittableTextType):
        raise ValueError("Invalid text type")

    for node in old_nodes:
        if node.text_type == "text":
            splitted_text = node.text.split(delimiter)
            if len(splitted_text) % 2 == 0:
                raise Exception("Invalid markdown syntax, delimiter not closed")

            for i, text in enumerate(splitted_text):
                if len(text) == 0:
                    continue

                if i % 2 == 0:
                    new_nodes.append(TextNode(text, "text"))
                else:
                    new_nodes.append(TextNode(text, text_type))

        else:
            new_nodes.append(node)

    return new_nodes


def extract_markdown_images(text: str) -> List[tuple[str, str]]:
    """
    Method for extacting image data from markdown text

    Args:
        text: text where images are to be extracted

    Returns: List of tuples containing image alt text and image URL

    """
    results: List[tuple[str, str]] = []

    matches = re.findall(r"!\[(.*?)]\((.+?)\)", text)
    results.extend(matches)

    return results


def extract_markdown_links(text: str) -> List[tuple[str, str]]:
    """
    Method for extracting link data from markdown text
    Args:
        text: text where links are to be extracted

    Returns: List of tuples containing link text and link URL
        
    """
    results: List[tuple[str, str]] = []

    matches = re.findall(r"[^!]\[(.*?)]\((.+?)\)", text)
    results.extend(matches)

    return results
