from typing import Any
from xml.etree.ElementTree import Element
from markdown import Extension
from markdown.blockprocessors import BlockProcessor

from markdown.core import Markdown

class PrePostExtension(Extension):

    def __init__(self, **kwargs: Any) -> None:
        print("Creating pre-post extesion")
        super().__init__(**kwargs)

    def extendMarkdown(self, md: Markdown) -> None:

        class CodeBlockCommentProcessor(BlockProcessor):
            def test(self, parent: Element, block: str) -> bool:
                return super().test(parent, block)
            
            def run(self, parent: Element, blocks: list[str]) -> bool | None:
                print("Running on code block")
                print(parent)
                for b in blocks:
                    print("----")
                    print(b)
                return super().run(parent, blocks)
            
        
        md.parser.blockprocessors.register(CodeBlockCommentProcessor(md.parser), "codePrePost", 1000)
        """ for index, bp in enumerate(md.parser.blockprocessors):
            print(bp)
            print(md.parser.blockprocessors._priority[index])
        """
            