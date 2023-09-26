import os
import sys
from timeit import default_timer as timer
from datetime import datetime, timedelta
from logging import info

from mkdocs import utils as mkdocs_utils
from mkdocs.config import config_options, Config, config_options, base
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin, get_plugin_logger
from mkdocs.utils.templates import TemplateContext


class MyPluginConfig(base.Config):
    version = config_options.Type(str, default='2023.09.1')

class Plugin(BasePlugin[MyPluginConfig]):
    logger = get_plugin_logger("mkdocs-pyscript")
    def __init__(self):
        self.enabled = True
        self.total_time = 0

    def on_template_context(self, context: TemplateContext, *, template_name: str, config: MkDocsConfig) -> TemplateContext | None:
        self.logger.info(context)