from textnode import TextNode, TextNodeType
from htmlnode import HTMLNode, LeafNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextNodeType.TEXT:
            # No lo partimos si no es texto plano
            new_nodes.append(node)
            continue

        split_pieces = node.text.split(delimiter)

        for i, piece in enumerate(split_pieces):
            if not piece:
                continue  # saltar fragmentos vacíos
            if i % 2 == 0:
                new_nodes.append(TextNode(piece, TextNodeType.TEXT))
            else:
                new_nodes.append(TextNode(piece, text_type))

    return new_nodes