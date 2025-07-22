
from textnode import TextNode, TextNodeType
from inline_markdown import text_to_textnodes
from block_utils import markdown_to_blocks, block_to_block_type

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag.")
        if not self.children:
            raise ValueError("ParentNode must have at least one child.")
        return f"<{self.tag}{self.props_to_html()}>{''.join(child.to_html() for child in self.children)}</{self.tag}>"
    
    def props_to_html(self):
        if not self.props:
            return ''
        return " " + ' '.join(f'{key}="{value}"' for key, value in self.props.items())
    def __repr__(self):
        return f'HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})'

    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("LeafNode must have a value.")
        super().__init__(tag, value, children= None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value.")

        if self.tag is None:
            return self.value

        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)



def text_to_children(text):
    """Converts a string into a list of HTMLNode children by processing inline markdown."""
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]

def text_node_to_html_node(text_node):
    """Converts a TextNode into a corresponding LeafNode."""
    if text_node.text_type == TextNodeType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextNodeType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextNodeType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextNodeType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextNodeType.LINK:
        return LeafNode("a", text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextNodeType.IMAGE:
        return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Unknown TextNodeType: {text_node.text_type}")

def block_to_html_node(block):
    from block_type import BlockType
    block_type = block_to_block_type(block)

    if block_type == BlockType.HEADING:
        import re
        match = re.match(r"^(#{1,6})\s+(.*)", block)
        level = len(match.group(1))
        content = match.group(2).strip()
        return HTMLNode(tag=f"h{level}", children=text_to_children(content))

    elif block_type == BlockType.PARAGRAPH:
        return HTMLNode(tag="p", children=text_to_children(block))

    elif block_type == BlockType.QUOTE:
        lines = [line.lstrip("> ").strip() for line in block.splitlines()]
        content = " ".join(lines)
        return HTMLNode(tag="blockquote", children=text_to_children(content))

    elif block_type == BlockType.UNORDERED_LIST:
        list_items = []
        for line in block.splitlines():
            text = line.lstrip("- ").strip()
            list_items.append(HTMLNode(tag="li", children=text_to_children(text)))
        return HTMLNode(tag="ul", children=list_items)

    elif block_type == BlockType.ORDERED_LIST:
        list_items = []
        for line in block.splitlines():
            _, text = line.split(". ", 1)
            list_items.append(HTMLNode(tag="li", children=text_to_children(text.strip())))
        return HTMLNode(tag="ol", children=list_items)

    elif block_type == BlockType.CODE:
        code_lines = block.splitlines()[1:-1]  # remove triple backticks
        code_text = "\n".join(code_lines)
        code_node = text_node_to_html_node(TextNode(code_text, TextNodeType.TEXT))
        return HTMLNode(tag="pre", children=[
            HTMLNode(tag="code", children=[code_node])
        ])

    else:
        raise ValueError(f"Unsupported block type: {block_type}")

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return HTMLNode(tag="div", children=children)



