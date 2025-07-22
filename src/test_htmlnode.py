import unittest
from main import extract_markdown_images, extract_markdown_links
from htmlnode import *


class TestHtml(unittest.TestCase):
    def test_props(self):
        node = HTMLNode("div", "Hello World", props={"class": "container", "id": "main"})
        self.assertEqual(node.props_to_html(), ' class="container" id="main"')
    def test_no_props(self):
        node = HTMLNode("div", "Hello World")
        self.assertEqual(node.props_to_html(), '')
    def test_repr(self):
        node = HTMLNode("div", "Hello World", children=[HTMLNode("span", "Child")], props={"class": "container"})
        expected_repr = 'HTMLNode(tag=div, value=Hello World, children=[HTMLNode(tag=span, value=Child, children=[], props={})], props={\'class\': \'container\'})'
        self.assertEqual(repr(node), expected_repr)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_Tag_None(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")
    def test_leaf_no_value(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None)
    def test_leaf_props(self):
        node = LeafNode("img", " ", props={"src": "image.png", "alt": "An image"})
        self.assertEqual(
            node.to_html(),
            '<img src="image.png" alt="An image"> </img>'
        )
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is a link to [linkedin](https://www.linkedin.com/in/david-sebastian-rodríguez-valencia-017541207/)"
        )
        self.assertListEqual([("linkedin", "https://www.linkedin.com/in/david-sebastian-rodríguez-valencia-017541207/")], matches)

    
if __name__ == "__main__":
    unittest.main()