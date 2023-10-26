import os
import pytest
import bs4

from typing import List

@pytest.mark.parametrize('dir', [('./basic')])
def test_script_tags(site):
    index_file = site / "index.html"
    with open(index_file, "r") as f:
        soup = bs4.BeautifulSoup(f, features="html.parser")
        head = soup.find("head")
        scripts: List[bs4.element.Tag] = head.find_all("script")

        print(scripts)
        
        # check that importmap exists
        assert any(('type' in script.attrs and script['type'] == "importmap") for script in scripts)

        # check that additional script tags exist
        assert any(('src' in script.attrs and script['src'] == "makeblocks.js") for script in scripts)
        assert any(('src' in script.attrs and script['src'] == "mini-coi.js") for script in scripts)