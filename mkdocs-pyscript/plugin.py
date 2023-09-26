import os
import sys
from timeit import default_timer as timer
from datetime import datetime, timedelta

from mkdocs import utils as mkdocs_utils
from mkdocs.config import config_options, Config, config_options
from mkdocs.plugins import BasePlugin

class MyPluginConfig(mkdocs.config.base.Config):
    version = config_options.Type(str, default='2023.09.1')

class YourPlugin(BasePlugin[MyPluginConfig]):

    def __init__(self):
        self.enabled = True
        self.total_time = 0