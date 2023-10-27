from playwright.sync_api import Page, expect

from pathlib import Path

from .conftest import DevServer

from .support import MkdocsPyscriptTest

class TestDynamic(MkdocsPyscriptTest):
    def test_has_title(self, page: Page, dev_server: DevServer):
        filepath = self.build_site("basic")
        with open(self._index_file, "r") as f:
            page.goto(str(Path(dev_server.base_url) / filepath / "index.html"))
        
        expect(page).to_have_title("Example")

    #@pytest.mark.parametrize('dir', [('./basic')])
    def test_injected_buttons(self, page: Page, dev_server):
        filepath = self.build_site("basic")
        with open(self._index_file, "r") as f:
            page.goto(str(Path(dev_server.base_url) / filepath / "index.html"))

        wrappers = page.query_selector_all('.py-wrapper')
        assert len(wrappers) == 3

        button_selector = '[data-pyscript="button"]'
        page.wait_for_selector(button_selector)
        buttons = page.query_selector_all(button_selector)
        assert len(buttons) == 3
