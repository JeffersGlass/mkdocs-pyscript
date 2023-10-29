from mkdocs import utils as mkdocs_utils
from mkdocs.config import config_options, Config, config_options, base
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin, get_plugin_logger
from mkdocs.structure.files import Files, File
from mkdocs.structure.pages import Page
from mkdocs.utils.templates import TemplateContext

from typing import Any, Union
import os
from itertools import chain

from typing import Iterable, List

from bs4 import BeautifulSoup, Comment, Tag

from .prePostExtension import PrePostExtension

import logging

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
        self.logger.setLevel(logging.DEBUG)
        

    def on_config(self, config: MkDocsConfig) -> Union[MkDocsConfig, None]:
        # Append static resources
        config["theme"].dirs.append(glr_path_static("dist/js"))
        config["theme"].dirs.append(glr_path_static("dist/css"))
        for css_file in os.listdir(glr_path_static("dist/css")):
            if css_file.endswith(".css"):
                config["extra_css"].append(css_file)

        # Set version
        self.SCRIPT_LINK = SCRIPT.format(version=self.config.pyscript_version)

        # Disable navigation.instant
        if 'features' in config['theme'] and 'navigation.instant' in config['theme']['features']:
            self.logger.warning("mkdocs-pyscript is not compatible with navigation.instant; instant navigation will be disabled.")
            config['theme']['features'].remove('navigation.instant')

        # Inject pre-post Markdown plugin
        #config['markdown_extensions'].append(PrePostExtension())
        
        return config
    
    def scriptize(self, soup: BeautifulSoup, block: Tag, *, script_type="unmanaged-pyscript-mkdocs", label=None,):
        #Remove linenumber links:
        lineno_links = block.find_all('a')
        for a in lineno_links:
            if 'href' in a.attrs and "codelineno" in a['href']: a.extract()

        script = soup.new_tag("script")
        script['type'] = script_type
        script['id'] = label
        script.string = block.text
        return script


    def on_page_content(self, html: str, *, page: Page, config: MkDocsConfig, files: Files) -> Union[str, None]:
        soup = BeautifulSoup(html, features="html.parser")

        # Get all potential codeblocks in order:
        code_blocks: List[Tag] = []
        tag = soup.find(name=['code', 'div'])
        if tag:
            code_blocks.append(tag)
            while tag:= tag.find_next(name=['code', 'div']):
                # Only include "top level" code tags
                if not any((tag in existing_tag.descendants) for existing_tag in code_blocks): code_blocks.append(tag)

        # exit early if no codeblocks on page
        if not code_blocks: return html

        # When we process a 'py-pre' tag, we'll turn it into a comment and extract it from the document,
        # only saving the most recent one seen. Then, when we process an actual code tag, we'll inject 
        # that py-pre tag before it with a matching ID

        # Similarly, when we see an actual code tag, we'll save a reference to it; when we process a 'py-post'
        # tag, we'll inject it after the most recent code tag with a matching ID
        last_seen_pre_tag = None
        last_seen_primary_tag = None
        primary_block_index = -1

        # Process all blocks
        for block in code_blocks:
            try:
                #Classless blocks cannot be handled
                classes = block.attrs['class']
            except KeyError:
                continue

            if 'py-pre' in classes:
                if last_seen_pre_tag:
                    self.logger.warning("Multiple py-pre tags encountered with no primary tag between them")
                last_seen_pre_tag = block.extract()

            elif 'py-post' in classes:
                block.extract()
                if last_seen_primary_tag:
                    last_seen_primary_tag.insert_after(self.scriptize(soup, block, script_type="py-post", label=f"py-post-{primary_block_index}"))
                    last_seen_primary_tag = None
                else: self.logger.warning('Encountered py-post tag with no valid primary tag preceding it')

            elif (self.config.selective and 'pyscript' in classes) or \
                    ((not self.config.selective) and ('language-python' in classes or 'language-py' in classes)):
                #Wrap codeblock in a new div
                div = soup.new_tag('div')
                div['class'] = "py-wrapper"
                div['style'] = "position:relative"
                div['id'] = f"py-main-{(primary_block_index := primary_block_index + 1)}"

                block.wrap(div) # Wrap codeblock with div
                last_seen_primary_tag = div

                #Inject a pre-tag if necessary
                if last_seen_pre_tag:
                    block.insert_before(self.scriptize(soup, last_seen_pre_tag, script_type="py-pre", label=f"py-pre-{primary_block_index}"))
                    last_seen_pre_tag = None                    
            
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

            # Add Plugin JS
            mkdocs_script = soup.new_tag("script")
            mkdocs_script['type'] = "module"
            mkdocs_script['src'] = "/makeblocks.js"
            soup.head.append(mkdocs_script)

            #Add tag to point to mini-coi.js
            coi_script = soup.new_tag("script")
            coi_script['src'] = '/mini-coi.js'
            soup.head.append(coi_script)
        return str(soup)
    
