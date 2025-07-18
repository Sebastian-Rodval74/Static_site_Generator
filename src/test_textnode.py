import unittest

from textnode import TextNode, TextNodeType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextNodeType.BOLD)
        node2 = TextNode("This is a text node", TextNodeType.BOLD)
        self.assertEqual(node, node2)
    def test_not_eq_different_text(self):
        node = TextNode("This is a text node", TextNodeType.BOLD)
        self.assertNotEqual(node, TextNode("Different text", TextNodeType.BOLD))
    def test_other(self):
        node1 = TextNode("Some text", TextNodeType.BOLD, "https://boot.dev")
        node2 = TextNode("Some text", TextNodeType.BOLD, None)
        self.assertNotEqual(node1, node2)
    def test_text_type(self):
        node1 = TextNode("This is a text node", TextNodeType.BOLD)
        node2 = TextNode("This is a text node", TextNodeType.TEXT)
        self.assertNotEqual(node1, node2)


        


if __name__ == "__main__":
    unittest.main()