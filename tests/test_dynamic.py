from playwright.sync_api import Page, expect
import pytest

from typing import Iterable
import bs4

@pytest.mark.parametrize('dir', [('./basic')])
def test_has_title(site, page: Page):
    index_file = site / "index.html"
    with open(index_file, "r") as f:
        page.set_content(f.read())
    
    expect(page).to_have_title("Example")

@pytest.mark.parametrize('dir', [('./basic')])
def test_injected_buttons(site, page: Page):
    index_file = site / "index.html"
    with open(index_file, "r") as f:
        page.set_content(f.read())

    wrappers = page.query_selector_all('.py-wrapper')
    assert len(wrappers) == 3

    loadButton = page.wait_for_selector('.hljs')
    page.wait_for_timeout(2000)
    print(f"{loadButton.text_content()=}")
