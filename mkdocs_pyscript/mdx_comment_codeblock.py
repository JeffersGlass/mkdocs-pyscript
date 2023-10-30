from xml.etree.ElementTree import Element
from markdown import Extension
from markdown.treeprocessors import Treeprocessor
from markdown.core import Markdown

from typing import Sequence

class PyScriptBlockProcessor(Treeprocessor):
    def __init__(self, comment_types: Sequence[str] | None = None, md: Markdown | None = None) -> None:
        # A list of strings, the types of code block to be commented out
        self.comment_types = comment_types
        super().__init__(md)

    def run(self, root: Element) -> Element | None:
        return super().run(root)

class CommentCodeblockExtension(Extension):

    def extendMarkdown(self, md: Markdown) -> None:
        md.tree