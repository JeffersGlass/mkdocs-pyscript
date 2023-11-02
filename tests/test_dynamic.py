from playwright.sync_api import Page, expect

from pathlib import Path

from .conftest import DevServer

from .support import MkdocsPyscriptTest

class TestDynamic(MkdocsPyscriptTest):
    def test_has_title(self, page: Page, dev_server: DevServer):
        # This mostly checks that the page build and config injection works
        filepath = self.build_site("basic")
        with open(self._index_file, "r") as f:
            page.goto(str(Path(dev_server.base_url) / filepath / "index.html"))
        
        expect(page).to_have_title("basic")

    #@pytest.mark.parametrize('dir', [('./basic')])
    def test_codemirror_and_run(self, page: Page, dev_server):
        filepath = self.build_site("basic")
        with open(self._index_file, "r") as f:
            page.goto(str(Path(dev_server.base_url) / filepath / "index.html"))

        wrappers = page.query_selector_all('.py-wrapper')
        assert len(wrappers) == 3

        # Check that all buttons load
        button_selector = '[data-pyscript="button"]'
        page.wait_for_selector(button_selector)
        buttons = page.query_selector_all(button_selector)
        assert len(buttons) == 3
        # Check that button loads the code in a codemirror
        buttons[0].click()
        codemirror = page.locator("div .cm-editor")
        assert """# This is a 'py' blockprint("hello_py")""" in codemirror.text_content()

        # Check that py-repl actually runs and emits output
        page.locator(".py-repl-run-button").click()
        page.wait_for_selector(".py-repl-output")
        assert page.locator(".py-repl-output").text_content() == "hello_py"

    def test_pre_post(self, page: Page, dev_server):
        filepath = self.build_site("prepost")
        with open(self._index_file, "r") as f:
            page.goto(str(Path(dev_server.base_url) / filepath / "index.html"))

        wrappers = page.query_selector_all('.py-wrapper')
        assert len(wrappers) == 1

        button_selector = '[data-pyscript="button"]'
        page.wait_for_selector(button_selector)
        buttons = page.query_selector_all(button_selector)
        assert len(buttons) == 1

        buttons[0].click()
        codemirror = page.locator("div .cm-editor")
        assert """print("This is the main tag")""" in codemirror.text_content()

        # Check that py-repl actually runs and emits output
        page.locator(".py-repl-run-button").click()
        page.wait_for_selector(".py-repl-output")
        assert page.locator(".py-repl-output").text_content() == "This is some pre-codeThis is the main tagThis is some post code"


