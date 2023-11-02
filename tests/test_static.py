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
        scripts: Iterable[bs4.element.Tag] = soup.find_all("script")
      
        # check that importmap exists
        assert any(('type' in script.attrs and script['type'] == "importmap") for script in scripts)

        # check that additional script tags exist
        assert any(('src' in script.attrs and "makeblocks.js" in script['src']) for script in scripts)
        assert any(('src' in script.attrs and "mini-coi.js" in script['src']) for script in scripts) 

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
        
        #TODO Check contents of codeblocks
            
    def test_pre_post(self):
        self.build_site("prepost")
        with open(self._index_file, "r") as f:
            soup = bs4.BeautifulSoup(f, features="html.parser")

        body = soup.find('body')
        wrappers: Iterable[bs4.element.Tag] = body.find_all(class_ = 'py-wrapper')

        # Make sure all one one codeblock is emitted are convered to codeblocks
        assert len(wrappers) == 1
        for wrapper in wrappers:
            codeblock = wrapper.code

        pre_tags = soup.find_all('script', attrs={"type": "py-pre"})
        assert len(pre_tags) == 1
        assert pre_tags[0].text.strip() == 'print("This is some pre-code")'

        post_tags = soup.find_all('script', attrs={"type": "py-post"}) 
        assert len(post_tags) == 1
        assert post_tags[0].text.strip() == 'print("This is some post code")'

        #TODO check contents of code block, pre and post tags

        

    
