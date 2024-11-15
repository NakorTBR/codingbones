import unittest

from nodehandlers import (
    markdown_to_blocks,
    markdown_to_html_node,
    block_to_block_type,
    extract_title,
    block_type_heading,
    block_type_code,
    block_type_paragraph,
    block_type_quote,
    block_type_olist,
    block_type_ulist,
)

from io_handler import get_content_path, get_static_path, get_public_path, get_template_path

from generator import generate_page, generate_pages_recursive

# from io_handler import get_file_contents

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
TMTB This is a **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "TMTB This is a **bolded** paragraph<br />",
                "This is another paragraph with *italic* text and `code` here<br />This is the same paragraph on a new line<br />",
                "* This is a list<br />* with items<br />",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
TMTBN This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "TMTBN This is **bolded** paragraph<br /><br />",
                "This is another paragraph with *italic* text and `code` here<br />This is the same paragraph on a new line<br />",
                "* This is a list<br />* with items<br />",
            ],
        )

    def test_markdown_to_blocks_newlines2(self):
        md = """
TMTBN2 This is **bolded** paragraph




RAND OM  T  E XT         

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "TMTBN2 This is **bolded** paragraph<br /><br />",
                "RAND OM  T  E XT<br />",
                "This is another paragraph with *italic* text and `code` here<br />This is the same paragraph on a new line<br />",
                "* This is a list<br />* with items<br />",
            ],
        )

class TestMarkdownBlockTypes(unittest.TestCase):
    def test_block_to_block_types(self):
        block = "# Awesome header"
        self.assertEqual(block_to_block_type(block), block_type_heading)
        block = "```<br />int main()<br />```<br />"
        self.assertEqual(block_to_block_type(block), block_type_code)
        block = "> Something quotable\n> continued here"
        self.assertEqual(block_to_block_type(block), block_type_quote)
        block = "* A list\n* With multiple\n* List items"
        self.assertEqual(block_to_block_type(block), block_type_ulist)
        block = "1. Ordered\n2. List"
        self.assertEqual(block_to_block_type(block), block_type_olist)
        block = "Wow.  An entire paragraph?  Not even special.  Just the default case."
        self.assertEqual(block_to_block_type(block), block_type_paragraph)

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_HTML(self):
        md = """
TMTHTML This is a **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items

1. Different lists,
2. Might be ordered.
3. This one is.
"""
        result = markdown_to_html_node(md)
        # print(f"FINAL RESULT:\n{result}")
        self.assertEqual(
            result, 
            "<div>TMTHTML This is a <b>bolded</b> paragraph<br />This is another paragraph with "
            "<i>italic</i> text and <code>code</code> here<br />This is the same paragraph on a "
            "new line<br /><ul><li>This is a list</li><li>with items</li></ul><ol><li>Different "
            "lists,</li><li>Might be ordered.</li><li>This one is.</li></ol></div>")
        
        
class TestMarkdownToHTML(unittest.TestCase):
    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        self.assertEqual(
            node,
            "<div><h1>this is an h1<br /></h1><p>this is paragraph text</p><h2>this is an h2<br /></h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        self.assertEqual(
            node,
            "<div><blockquote>This is a blockquote block</blockquote><br /><p>this is paragraph text</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is a code block
```

this is paragraph text

"""

        node = markdown_to_html_node(md)
        self.assertEqual(
            node,
            "<div><pre><code><br />This is a code block<br /></code></pre><p>this is paragraph text</p></div>",
        )

    def test_etract_title(self):
        # result = extract_title(get_file_contents("index.md"))
        result = extract_title("# Title here")
        self.assertEqual(result, "Title here")

        result = extract_title("#       It's still a title")
        self.assertEqual(result, "It's still a title")

        result = extract_title("# <><>Title h_ere")
        self.assertEqual(result, "<><>Title h_ere")

        result = extract_title("# Who shot first?\nYou did.  Stop trying to blame Han.\nJerk.")
        self.assertEqual(result, "Who shot first?")

    def test_generator(self):
        content = get_content_path() / "index.md"
        dest = get_static_path() / "index.html"
        generate_page(from_path=content, dest_path=dest, template_path=get_template_path())

        generate_pages_recursive()

if __name__ == "__main__":
    unittest.main()