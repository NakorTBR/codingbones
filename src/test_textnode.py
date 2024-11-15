import unittest

from textnode import TextNode, TextType
from nodehandlers import (
    split_nodes_delimiter, 
    extract_markdown_images, 
    extract_markdown_links, 
    text_node_to_html_node,
    )


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        # print("\nTesting TextNode")
        node = TextNode(text="This is a text node", text_type=TextType.BOLD)
        node2 = TextNode(text="This is a text node", text_type=TextType.BOLD)
        self.assertEqual(node, node2)
        node3 = TextNode(text="I wrote a test", text_type=TextType.ITALIC)
        node4 = TextNode(text="I wrote a test", text_type=TextType.ITALIC)
        self.assertEqual(node3, node4)
        node5 = TextNode(text="z", text_type=TextType.NORMAL)
        node6 = TextNode(text="z", text_type=TextType.NORMAL)
        self.assertEqual(node5, node6)

        edge1 = TextNode(text="A website", text_type=TextType.LINK, url=None)
        edge2 = TextNode(text="A website", text_type=TextType.LINK, url=None)
        self.assertEqual(edge1, edge2)
        edge3 = TextNode(text="Is it different?", text_type=TextType.LINK, url=None)
        edge4 = TextNode(text="Is it different?", text_type=TextType.CODE, url=None)
        self.assertNotEqual(edge3, edge4)
        edge5 = TextNode(text="I sit different?", text_type=TextType.TEXT)
        edge6 = TextNode(text="Is it different?", text_type=TextType.TEXT)
        self.assertNotEqual(edge5, edge6)

    def test_repr(self):
        node = TextNode(text="This is a text node", text_type=TextType.TEXT, url="https://www.boot.dev")
        self.assertEqual(
            "TextNode(text=\"This is a text node\", type=text, url=https://www.boot.dev)", repr(node)
        )

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode(text="Writing tests sucks.", text_type=TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Writing tests sucks.")

    def test_image(self):
        node = TextNode(text="A picture of something interesting.", text_type=TextType.IMAGE, url="https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "A picture of something interesting."},
        )

    def test_bold(self):
        node = TextNode(text="This is bold", text_type=TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

    def test_temp_handler(self):
        node = TextNode("This is text with **bold text** words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        # print(f"NEW NODES: {new_nodes}")

    def test_extract_md_images(self):
        test = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(test, expected)
    
    def test_extract_md_links(self):
        test = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(test, expected)


if __name__ == "__main__":
    unittest.main()
