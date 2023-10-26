from playwright.sync_api import Page, expect
import pytest

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
    
    expect(page).to_have_title("Example")