from enum import Enum
class TextNodeType(Enum):
    BOLD = "Bold"
    TEXT = "Plain"
    ITALIC = "Italic"
    CODE = "Code"
    IMAGE = "Image"
    LINK = "Link"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url)
    def __repr__(self):
        return f"""TextNode({self.text}, {self.text_type.value}, {self.url})"""


