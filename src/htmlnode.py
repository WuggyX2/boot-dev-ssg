"""
HTMLNode class reprisents a node in the HTML tree.

"""

from typing import Self, TypeAlias, List

class HTMLNode:

    """

    Attributes: 
        tag: The tag of the node
        value: The value of the node 
        children: The children of the node 
        props: The properties of the node 
    """
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag: Value = tag
        self.value: Value = value
        self.children: Children = children
        self.props: Props = props

    def to_html(self: Self) -> str:
        """
        Not going to be implemented. Implementet by the subclasses.

        Args:
            self: Self 
        """
        raise NotImplementedError

    def props_to_html(self: Self) -> str:
        """
        Convert the props dictionary to a string of HTML attributes.
        Args:
            self: Self 

        Returns: str
            
        """
        result = ""

        if self.props:

            for key, value in self.props.items():
                result += f' {key}="{value}"'

        return result

    def __repr__(self: Self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    """
    Child class of HTMLNode that represents a single HTML node without children.

    """
    def __init__(self, tag,  value:str, props=None,) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self: Self) -> str:
        """
        Convert the node to an HTML string.

        Args:
            self: Self 

        Returns: str
            
        """

        if not self.value:
            raise ValueError("LeafNode must have a value")

        if not self.tag:
            return  self.value

        return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self: Self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):

    """
    Child class of HTMLNode that represents a single HTML node with children.
    """
    def __init__(self, tag, children,  props=None) -> None:
        super().__init__(tag, None, children, props)


    def to_html(self: Self) -> str:
        children_html = ""

        if not self.children:
            raise ValueError("ParentNode must have children")

        for child in self.children:
            children_html += child.to_html()

        return f"<{self.tag}{super().props_to_html()}>{children_html}</{self.tag}>"


    def __repr__(self: Self) -> str:
        return f"ParentNode({self.tag}, {self.children}, {self.props})"

# Type aliases for the HTMLNode class

Value: TypeAlias = str | None
Tag: TypeAlias = str | None
Children: TypeAlias = List[HTMLNode] | None
Props: TypeAlias = dict[str, str] | None
