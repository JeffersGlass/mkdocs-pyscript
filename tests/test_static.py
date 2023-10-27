import pytest
import bs4

from typing import Iterable

from .support import MkdocsPyscriptTest

class TestStatic(MkdocsPyscriptTest):
    def test_script_tags(self):
        self.build_site('basic')
        with open(self._index_file, "r") as f:
            soup = bs4.BeautifulSoup(f, features="html.parser")

        head = soup.find("head")
        scripts: Iterable[bs4.element.Tag] = head.find_all("script")

        print(scripts)
        
        # check that importmap exists
        assert any(('type' in script.attrs and script['type'] == "importmap") for script in scripts)

        # check that additional script tags exist
        assert any(('src' in script.attrs and script['src'] == "makeblocks.js") for script in scripts)
        assert any(('src' in script.attrs and script['src'] == "mini-coi.js") for script in scripts) 

    def test_code_blocks(self):
        self.build_site("basic")
        with open(self._index_file, "r") as f:
            soup = bs4.BeautifulSoup(f, features="html.parser")

        body = soup.find('body')
        wrappers: Iterable[bs4.element.Tag] = body.find_all(class_ = 'py-wrapper')

        # Make sure all three fences are convered to codeblocks
        assert len(wrappers) == 3
        for wrapper in wrappers:
            codeblock = wrapper.code

    
