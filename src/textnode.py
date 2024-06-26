"""
TextNode class represents a node in the AST that contains text content.

"""

from typing import Self
from types import NotImplementedType


class TextNode:
    """

    Attributes: 
        text: The text content of the node 
        text_type: The type of text this node contains
        url: The URL of the link or image, if the text is a link. Default to None
    """
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

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
