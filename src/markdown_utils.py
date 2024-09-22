"""
Collection of unitility functions for interacting with markdown text

"""

from htmlnode import HTMLNode, LeafNode, ParentNode


def is_heading_block(block: str) -> bool:
    """
    Determines if a block is a heading block.
    Checks that the block starts with a "#" character.

    Args:
        block: block being analyzed

    Returns: True if block is a heading block, False otherwise

    """

    valid = ["# ", "## ", "### ", "#### ", "##### ", "###### "]

    for v in valid:
        if block.startswith(v):
            return True

    return False


def is_code_block(block: str) -> bool:
    """
    Determines if a block is a code block.
    Checks that the block starts and ends with "```".

    Args:
        block: block being analyzed

    Returns: True if block is a code block, False otherwise

    """
    lines = block.split("\n")

    return len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```")


def is_quote_block(block: str) -> bool:
    """
    Determines if a block is a quote block.
    Checks that everyline in the block starts with a ">" character.

    Args:
        block: block being analyzed

    Returns: True if block is a quote block, False otherwise

    """

    lines = block.split("\n")

    for line in lines:
        if not line.startswith(">"):
            return False

    return True


def is_unordered_list_block(block: str) -> bool:
    """
    Determines if a block is an unordered list block.
    Checks that everyline in the block starts with a "-" or "*" character.

    Args:
        block: block being anlyzed

    Returns: True if block is an unordered list block, False otherwise

    """
    lines = block.split("\n")

    for line in lines:
        if not line.startswith("-") and not line.startswith("*"):
            return False

    return True


def is_ordered_list_block(block: str) -> bool:
    """
    Determines if a block is an ordered list block.
    Checks that everyline in the block starts with a number followed by a "." character.

    Args:
        block: block being analyzed

    Returns: True if block is an ordered list block, False otherwise

    """
    lines = block.split("\n")

    for i, line in enumerate(lines):
        if not line.startswith(f"{i+1}."):
            return False

    return True

def get_heading_level(block: str) -> int:
    """
    Determines the heading level of a block.
    The heading level is determined by the number of "#" characters at the start of the block.

    Args:
        block: block being analyzed

    Returns: heading level

    """
    level = 0

    for c in block:
        if level+1 > 6:
            raise ValueError("Invalid heading level")

        if c == "#":
            level += 1
        else:
            break

    return level
