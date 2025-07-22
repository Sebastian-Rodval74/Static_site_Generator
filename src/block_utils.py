# block_utils.py
from enum import Enum, auto

class BlockType(Enum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERED_LIST = auto()
    ORDERED_LIST = auto()

def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    return [block.strip() for block in raw_blocks if block.strip()]

def block_to_block_type(block):
    lines = block.strip().splitlines()

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    if lines[0].startswith("#"):
        import re
        if re.match(r"^(#{1,6})\s", lines[0]):
            return BlockType.HEADING

    if all(line.strip().startswith(">") for line in lines):
        return BlockType.QUOTE

    if all_valid_ordered_list(lines):
        return BlockType.ORDERED_LIST

    if all(line.strip().startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    return BlockType.PARAGRAPH

def all_valid_ordered_list(lines):
    for i, line in enumerate(lines):
        if not line.strip().startswith(f"{i+1}. "):
            return False
    return True