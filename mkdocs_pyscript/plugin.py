import jinja2
from mkdocs import utils as mkdocs_utils
from mkdocs.config import config_options, Config, config_options, base
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin, get_plugin_logger
from mkdocs.structure.files import Files, File
from mkdocs.structure.pages import Page
from mkdocs.utils.templates import TemplateContext

from typing import Any

from bs4 import BeautifulSoup
import tempfile
from pathlib import Path
import os
from .minicoi import mini_coi_content

DEFAULT_VERSION = "2023.09.1.RC1"
SCRIPT = 'https://pyscript.net/snapshots/{version}/core.js'

class MyPluginConfig(base.Config):
    version = config_options.Type(str, default='2023.09.1')

class Plugin(BasePlugin[MyPluginConfig]):
    logger = get_plugin_logger("mkdocs-pyscript")
    def __init__(self):
        self.enabled = True
        self.total_time = 0
        self.temp_path = "./_mkdocs_pyscript_tmp/mini_coi.js"
        if not os.path.exists("./_mkdocs_pyscript_tmp"): os.mkdir("./_mkdocs_pyscript_tmp/")
        with open(self.temp_path, "w+") as f:
            f.write(mini_coi_content)

    def on_page_content(self, html: str, *, page: Page, config: MkDocsConfig, files: Files) -> str | None:
        soup = BeautifulSoup(html, features="html.parser")
        code_blocks = soup.findAll(name=['code', 'div'], attrs={'class', 'language-py'})
        for block in code_blocks:
            #self.logger.info(f"Adding button to {page.canonical_url}")
            #Wrap codeblock in a new div
            div = soup.new_tag('div')
            div['class'] = "py-wrapper"
            div['style'] = "position:relative"

            #Add run button
            button = soup.new_tag('a')
            button['style'] =  "position:absolute; width:60px; height:30px; bottom:3px; right:3px; background-color:#7773f7; color:#FFF; border-radius:5px; text-align:center; box-shadow: 2px 2px 3px #999; cursor:pointer"
            button['onclick'] = "console.log('clicked!')"

            label = soup.new_tag('i')
            label['style'] = "color:white;position:absolute; top:4px; left: 14px "
            label.string = "RUN"

            block.wrap(div) # Wrap codeblock with div
            div.append(button) #Add button to div
            button.append(label) # Wrap label in button
        return str(soup)
    
    def on_post_page(self, output: str, *, page: Page, config: MkDocsConfig) -> str | None:
        soup = BeautifulSoup(output, features="html.parser")
        codeblocks = soup.find_all(attrs={"class": "py-wrapper" },)
        if (len(codeblocks)):
            #self.logger.info(f"Page at {page.canonical_url} will get script in head")
            # Add PySript
            py_script = soup.new_tag("script")
            py_script['type'] = "module"
            py_script['src'] = SCRIPT.format(version=DEFAULT_VERSION)
            soup.head.append(py_script)

            coi_script = soup.new_tag("script")
            coi_script['src'] = '/mini-coi.js'
            soup.head.append(coi_script)
        return str(soup)
    
    def on_files(self, files: Files, *, config: MkDocsConfig) -> Files | None:
        #Add mini-coi to enable webworkers  

        new_file = File(
                path = self.temp_path,
                src_dir = './',
                dest_dir= config.site_dir,
                use_directory_urls=False,
                dest_uri="./mini-coi.js"
            )
        print(new_file)
        files.append(new_file)

        return files

    def on_post_build(self, *, config: MkDocsConfig) -> None:
        #self.temp_coi_file.close()
        self.logger.info("foo")
        os.remove("./_mkdocs_pyscript_tmp/mini_coi.js")
        os.rmdir("./_mkdocs_pyscript_tmp/")
        
            