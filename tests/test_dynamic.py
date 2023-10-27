from playwright.sync_api import Page, expect
import pytest

from http.server import HTTPServer as SuperHTTPServer
from http.server import SimpleHTTPRequestHandler
import threading
from pathlib import Path

from .support import MkdocsPyscriptTest

class TestDynamic(MkdocsPyscriptTest):

    def test_has_title(self, page: Page):
        self.load_site("basic")
        with open(self._index_file, "r") as f:
            page.set_content(f.read())
        
        expect(page).to_have_title("Example")

    #@pytest.mark.parametrize('dir', [('./basic')])
    def test_injected_buttons(self, page: Page):
        self.load_site("basic")
        with open(self._index_file, "r") as f:
            page.set_content(f.read())

        wrappers = page.query_selector_all('.py-wrapper')
        assert len(wrappers) == 3

        loadButton = page.wait_for_selector('.hljs')
        
        #TODO: Figure out why JS isn't running/finishing to make buttons appear
        #TODO: figure out why CSS isn't applying
