from textnode import TextNode, TextNodeType
from htmlnode import HTMLNode, LeafNode
from textnode import TextNode, TextNodeType
import re 


def main():
    my_text = TextNode("Hello, World!", TextNodeType.Plain_text)
    print(my_text)

def text_node_to_html_node(text_node):
    if text_node.text_type == TextNodeType.TEXT:
        return LeafNode(None, text_node.text)

    elif text_node.text_type == TextNodeType.BOLD:
        return LeafNode("b", text_node.text)

    elif text_node.text_type == TextNodeType.ITALIC:
        return LeafNode("i", text_node.text)

    elif text_node.text_type == TextNodeType.CODE:
        return LeafNode("code", text_node.text)

    elif text_node.text_type == TextNodeType.LINK:
        if text_node.url is None:
            raise ValueError("LINK type requires a URL.")
        return LeafNode("a", text_node.text, props={"href": text_node.url})

    elif text_node.text_type == TextNodeType.IMAGE:
        if text_node.url is None:
            raise ValueError("IMAGE type requires a URL.")
        return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})

    else:
        raise ValueError(f"Unsupported text type: {text_node.text_type}")
    #re.findall returns a list of tuples 
def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
    
def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
    

if __name__ == "__main__":
    main()
