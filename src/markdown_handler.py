"""

TODO
"""

import re
from typing import List, get_args
from textnode import TextNode, SplittableTextType




def split_nodes_delimiter(
    old_nodes: List[TextNode], delimiter: str, text_type: SplittableTextType
) -> List[TextNode]:
    """
    Method for splitting text nodes by a delimiter. The text nodes are split
    into two types of text nodes,one with the delimiter and the other without the delimiter.
    The delimiter text nodes are of the type specified in the text_type argument.
    The specified text_type must be a valid SplittableTextType enum value otherwise a ValueError is raised.

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


def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
    """
    Method for splitting text nodes and extracting images from the text node.
    Extracted images are converted to text nodes of type image. The rest of the text
    is added to the returned list as text nodes.

    Args:
        old_nodes: List of TextNodes to be split

    Returns: List of TextNodes with images extracted

    """
    new_nodes: List[TextNode] = []

    for node in old_nodes:
        if node.text_type == "text":
            extracted_images = extract_markdown_images(node.text)

            if len(extracted_images) > 0:
                node_text = node.text
                for alt_text, url in extracted_images:
                    sections = node_text.split(f"![{alt_text}]({url})", 1)
                    if len(sections) != 2:
                        raise ValueError("Invalid markdown, link section not closed")

                    text_before = sections[0]
                    text_after = sections[1]

                    if len(text_before) > 0:
                        new_nodes.append(TextNode(text_before, "text"))

                    new_nodes.append(TextNode(alt_text, "image", url))
                    node_text = text_after

                if len(node_text) > 0:
                    new_nodes.append(TextNode(node_text, "text"))

            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)

    return new_nodes


def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    """
    Method for splitting text nodes and extracting links from the text node.
    Extracted links are converted to text nodes of type link. The rest of the text
    is added to the returned list as text nodes.

    Args:
        old_nodes: List of TextNodes to be split

    Returns: List of TextNodes with links extracted

    """
    new_nodes: List[TextNode] = []

    for node in old_nodes:
        if node.text_type == "text":
            extracted_links = extract_markdown_links(node.text)
            node_text = node.text

            if len(extracted_links) > 0:
                for text, url in extracted_links:
                    sections = node_text.split(f"[{text}]({url})", 1)
                    text_before = sections[0]
                    text_after = sections[1]

                    if len(sections) != 2:
                        raise ValueError("Invalid markdown, link section not closed")

                    if len(text_before) > 0:
                        new_nodes.append(TextNode(text_before, "text"))

                    new_nodes.append(TextNode(text, "link", url))
                    node_text = text_after

                if len(node_text) > 0:
                    new_nodes.append(TextNode(node_text, "text"))

            else:
                new_nodes.append(node)

        else:
            new_nodes.append(node)
    return new_nodes


def extract_markdown_images(text: str) -> List[tuple[str, str]]:
    """
    Method for extacting image data from markdown text.
    Markdown images are of the form ![alt text](image URL)

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
    Method for extracting link data from markdown text.
    Markdown links are of the form [link text](link URL)
    Args:
        text: text where links are to be extracted

    Returns: List of tuples containing link text and link URL

    """
    results: List[tuple[str, str]] = []

    matches = re.findall(r"(?:^|[^!])\[(.*?)\]\((.*?)\)", text)
    results.extend(matches)

    return results


def text_to_textnodes(text: str) -> List[TextNode]:
    """
    Splits mardown text into a list of text nodes. Supports text, code, bold, italic, image and link markdown.
    Returns an empty list if the text is empty.

    Args:
        text: text to be split

    Returns: list of TextNodes
        
    """
    result: List[TextNode] = [TextNode(text, "text")]

    markdown_nodes: List[tuple[str, SplittableTextType]] = [
        ("`", "code"),
        ("**", "bold"),
        ("*", "italic"),
    ]

    for delimiter, text_type in markdown_nodes:
        result = split_nodes_delimiter(result, delimiter, text_type)

    result = split_nodes_image(result)
    result = split_nodes_link(result)

    return result
