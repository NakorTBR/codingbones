from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    HTML = "html"
    LEAF = "leaf"
    TEXT = "text"
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    ULIST = "ul"
    OLIST = "ol"
    LITEM = "li"
    DIV = "div"
    QUOTE = "blockquote"


class TextNode():
    """A "TextNode" is an intermediate representation between Markdown and HTML, and is specific to inline markup.
    """
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type.value
        self.url = url

    def __eq__(self, other):
        if self.text != other.text:
            return False
        if self.text_type != other.text_type:
            return False
        if self.url != other.url:
            return False
        
        return True
    
    def __repr__(self):
        return f"TextNode(text=\"{self.text}\", type={self.text_type}, url={self.url})"


