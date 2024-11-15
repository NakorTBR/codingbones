import unittest

from htmlnode import LeafNode, ParentNode, HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_nodes_equal(self):
        # print("\nTesting HTML Node")
        t1 = HTMLNode()
        t2 = HTMLNode()
        self.assertEqual(t1, t2)
        t3 = HTMLNode("slot", "Test data / text")
        t4 = HTMLNode("slot", "Test data / text")
        self.assertEqual(t3, t4)
        t5 = HTMLNode("start", "Cu vi parolas?", ["one", "two", "three"])
        t6 = HTMLNode("start", "Cu vi parolas?", ["one", "two", "three"])
        self.assertEqual(t5, t6)

        n1 = HTMLNode("start", "Cu vi parolas?")
        n2 = HTMLNode("end", "Cu vi parolas?")
        self.assertNotEqual(n1, n2)
        n3 = HTMLNode("Start", "Hello")
        n4 = HTMLNode("Start", "hello")
        self.assertNotEqual(n3, n4)
        n5 = HTMLNode("end", "bye", ["boring", "test", "trial", "data"], {"monkey":"fun"})
        n6 = HTMLNode("end", "bye", ["boring", "test", "trill", "data"], {"monkey":"fun"})
        self.assertNotEqual(n5, n6)

        # print(n5.props_to_html())
        # print(n5)

    def test_leaf_nodes(self):
        leaf1 = LeafNode("just text").to_html()
        # print(leaf1)
        self.assertEqual("just text", leaf1)
        leaf2 = LeafNode("Paragraph text", "p").to_html()
        # print(leaf2)
        self.assertEqual("<p>Paragraph text</p>", leaf2)
        leaf3 = LeafNode("This is a link", "a", {"href":"https://boot.dev"}).to_html()
        # print(leaf3)
        self.assertEqual('<a href="https://boot.dev">This is a link</a>', leaf3)
        leaf4 = LeafNode("Another...link...", "a", 
                                  {"href":"whomstistesting.com?user=farkleton"}).to_html()
        # print(leaf4)
        self.assertEqual("<a href=\"whomstistesting.com?user=farkleton\">Another...link...</a>", leaf4)

    def test_basic_parent_nodes(self):
        node = ParentNode(
            tag="p",
            children=[
                LeafNode(tag="b", value="Bold text"),
                LeafNode(tag=None, value="Normal text"),
                LeafNode(tag="i", value="italic text"),
                LeafNode(tag=None, value="Normal text"),
            ],
        )

        # print("NODE TO HTML")
        # print(node.to_html())
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

        node2 = ParentNode(
            tag="p",
            children=[
                LeafNode(tag="b", value="Really important!"),
                LeafNode(tag=None, value="  Meh.  Not very important."),
                LeafNode(tag="i", value="  This is important, but don't tell anyone!"),
                LeafNode(tag=None, value="  Again, who cares about normal text?"),
                LeafNode(tag="b", value="  In closing, HTML is boring."),
            ],
        )

        # print(node2.to_html())
        self.assertEqual(
            "<p><b>Really important!</b>  Meh.  Not very important.<i>  This is important, but don't tell anyone!</i>  "
            "Again, who cares about normal text?<b>  In closing, HTML is boring.</b></p>", node2.to_html())

        # print("\n\n\n")
    
    def test_to_html_no_children(self):
        node = LeafNode(tag="p", value="Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(tag=None, value="Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_children(self):
        child_node = LeafNode(tag="span", value="child")
        parent_node = ParentNode(tag="div", children=[child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode(tag="b", value="grandchild")
        child_node = ParentNode(tag="span", children=[grandchild_node])
        parent_node = ParentNode(tag="div", children=[child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            tag="p",
            children=[
                LeafNode(tag="b", value="Bold text"),
                LeafNode(tag=None, value="Normal text"),
                LeafNode(tag="i", value="italic text"),
                LeafNode(tag=None, value="Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            tag="h2",
            children=[
                LeafNode(tag="b", value="Bold text"),
                LeafNode(tag=None, value="Normal text"),
                LeafNode(tag="i", value="italic text"),
                LeafNode(tag=None, value="Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )


if __name__ == "__main__":
    unittest.main()
