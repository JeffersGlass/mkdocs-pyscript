import os
import sys
from timeit import default_timer as timer
from datetime import datetime, timedelta
from logging import info

from mkdocs import utils as mkdocs_utils
from mkdocs.config import config_options, Config, config_options, base
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin, get_plugin_logger
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page
from mkdocs.utils.templates import TemplateContext

from bs4 import BeautifulSoup

class MyPluginConfig(base.Config):
    version = config_options.Type(str, default='2023.09.1')

class Plugin(BasePlugin[MyPluginConfig]):
    logger = get_plugin_logger("mkdocs-pyscript")

    def __init__(self):
        self.enabled = True
        self.total_time = 0

    def on_page_markdown(self, markdown: str, *, page: Page, config: MkDocsConfig, files: Files) -> str | None:
        pass#self.logger.info(markdown)

    def on_page_content(self, html: str, *, page: Page, config: MkDocsConfig, files: Files) -> str | None:
        soup = BeautifulSoup(html)
        codeblocks = soup.select('div[class*="language-py"]')
        for block in codeblocks:
            tag = soup.new_tag("p")
            tag.string = "This is before the code block?"
            block.insert_before(tag)
        self.logger.info(str(soup))
        return str(soup)