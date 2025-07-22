from textnode import TextNode, TextNodeType
from htmlnode import HTMLNode, LeafNode
from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from block_utils import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
)
from split_nodes import split_nodes_delimiter


def main():
    my_text = TextNode("Hello, World!", TextNodeType.TEXT)
    print(my_text)


if __name__ == "__main__":
    main()