from mkdocs import utils as mkdocs_utils
from mkdocs.config import config_options, Config, config_options, base
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin, get_plugin_logger
from mkdocs.structure.files import Files, File
from mkdocs.structure.pages import Page
from mkdocs.utils.templates import TemplateContext

from typing import Any, Union
import os

from bs4 import BeautifulSoup

DEFAULT_VERSION = "snapshots/2023.09.1.RC2"
SCRIPT = 'https://pyscript.net/{version}/core.js'

from . import glr_path_static

class MyPluginConfig(base.Config):
    pyscript_version = config_options.Type(str, default=DEFAULT_VERSION)
    selective = config_options.Type(bool, default=False)

class Plugin(BasePlugin[MyPluginConfig]):
    logger = get_plugin_logger("mkdocs-pyscript")
    def __init__(self):
        self.enabled = True
        self.total_time = 0
        

    def on_config(self, config: MkDocsConfig) -> Union[MkDocsConfig, None]:
        # Append static resources
        config["theme"].dirs.append(glr_path_static("dist/js"))
        config["theme"].dirs.append(glr_path_static("dist/css"))
        for file in os.listdir(glr_path_static("dist/css")):
            if file.endswith(".css"):
                config["extra_css"].append(file)

        for file in os.listdir(glr_path_static("dist/js")):
            if file.endswith(".js"):
                print(f"Adding {file} ")
                config["extra_javascript"].append(file)

        print(f"{config=}")

        # Set version
        self.SCRIPT_LINK = SCRIPT.format(version=self.config.pyscript_version)

        # Disable navigation.instant
        if 'features' in config['theme'] and 'navigation.instant' in config['theme']['features']:
            self.logger.warning("mkdocs-pyscript is not compatible with navigation.instant; instant navigation will be disabled.")
            config['theme']['features'].remove('navigation.instant')
        
        return config

    def on_page_content(self, html: str, *, page: Page, config: MkDocsConfig, files: Files) -> Union[str, None]:
        soup = BeautifulSoup(html, features="html.parser")
        if self.config.selective:
            code_blocks = soup.findAll(name=['code', 'div'], attrs={'class': 'pyscript'})
        else:
            code_blocks = soup.findAll(name=['code', 'div'], attrs={'class': ['language-py', 'language-python']})
        for block in code_blocks:
            #self.logger.info(f"Adding button to {page.canonical_url}")
            #Wrap codeblock in a new div
            div = soup.new_tag('div')
            div['class'] = "py-wrapper"
            div['style'] = "position:relative"

            block.wrap(div) # Wrap codeblock with div
        return str(soup)
    
    def on_post_page(self, output: str, *, page: Page, config: MkDocsConfig) -> Union[str, None]:

        soup = BeautifulSoup(output, features="html.parser")
        codeblocks = soup.find_all(attrs={"class": "py-wrapper" },)
        if (len(codeblocks)):
            # Add importmap
            imp_map = soup.new_tag("script")
            imp_map['type'] = "importmap"
            imp_map.string = f"""
            {{
                "imports": {{ 
                    "@pyscript/core": "{self.SCRIPT_LINK}"
                }}
            }}
            """
            soup.head.append(imp_map)

            # PyScript is imported in makeblocks.js via the import map

            # Make makeblock script a module
            makeblocks = [s for s in soup.find_all("script") if 'src' in s.attrs and "makeblocks" in s['src']][0]
            makeblocks['type'] = "module"
        return str(soup)
    
