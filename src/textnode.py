"""
TextNode class represents a node in the AST that contains text content.

"""

from typing import Self, TypeAlias, Literal
from types import NotImplementedType
from htmlnode import LeafNode


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

def text_node_to_html_node(text_node: TextNode ) -> LeafNode:

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

TextType: TypeAlias = Literal["text", "bold", "italic", "code", "link", "image"]
Url: TypeAlias = str | None
