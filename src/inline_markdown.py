import re
from textnode import TextNode, TextNodeType
from split_nodes import split_nodes_delimiter

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextNodeType.TEXT:
            images = extract_markdown_images(node.text)
            if images:
                remaining = node.text
                for alt_text, url in images:
                    markdown_image = f"![{alt_text}]({url})"
                    parts = remaining.split(markdown_image, 1)
                    if parts[0]:
                        new_nodes.append(TextNode(parts[0], TextNodeType.TEXT))
                    new_nodes.append(TextNode(alt_text, TextNodeType.IMAGE, url))
                    remaining = parts[1]
                if remaining:
                    new_nodes.append(TextNode(remaining, TextNodeType.TEXT))
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextNodeType.TEXT:
            links = extract_markdown_links(node.text)
            if links:
                remaining = node.text
                for link_text, url in links:
                    markdown_link = f"[{link_text}]({url})"
                    parts = remaining.split(markdown_link, 1)
                    if parts[0]:
                        new_nodes.append(TextNode(parts[0], TextNodeType.TEXT))
                    new_nodes.append(TextNode(link_text, TextNodeType.LINK, url))
                    remaining = parts[1]
                if remaining:
                    new_nodes.append(TextNode(remaining, TextNodeType.TEXT))
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes

def split_only_text_nodes(nodes, splitter):
    result = []
    for node in nodes:
        if isinstance(node, TextNode) and node.text_type == TextNodeType.TEXT:
            result.extend(splitter([node]))
        else:
            result.append(node)
    return result

def text_to_textnodes(text):
    nodes = [TextNode(text, TextNodeType.TEXT)]
    nodes = split_only_text_nodes(nodes, split_nodes_image)
    nodes = split_only_text_nodes(nodes, split_nodes_link)
    nodes = split_only_text_nodes(nodes, lambda n: split_nodes_delimiter(n, "`", TextNodeType.CODE))
    nodes = split_only_text_nodes(nodes, lambda n: split_nodes_delimiter(n, "**", TextNodeType.BOLD))
    nodes = split_only_text_nodes(nodes, lambda n: split_nodes_delimiter(n, "_", TextNodeType.ITALIC))
    return nodes