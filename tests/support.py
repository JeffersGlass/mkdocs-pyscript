

from mkdocs.commands.build import build
from mkdocs.config.defaults import MkDocsConfig

from http.server import HTTPServer as SuperHTTPServer
from http.server import SimpleHTTPRequestHandler

from .conftest import hold_at_end

import threading
from pathlib import Path
import pytest
import os
import pdb

@pytest.mark.usefixtures("hold_at_end")
class MkdocsPyscriptTest:
    EMIT_FILES = True #Build the test show to /_debug_site or a temp file

    def build_site(self, dir: str | Path, cfg: dict=None,) -> Path:
        """Build a simple site for testing

        Args:
            dir (str | Path, optional): A directory containing the site content. Must contain a 
                mkdocs.yml and a /docs folder.
        """                
        if cfg is None: cfg = {}

        config = self._load_config(str(dir), **cfg)
        path = Path(f"_debug_site_{dir.replace('/', '_')}") if self.EMIT_FILES else pytest.TempPathFactory.mktemp()
        config.site_dir = path
        build(config)
        self._index_file = path / "index.html"
        return path
    

    # Based on https://github.com/mkdocs/mkdocs/blob/b5250bf9e2a58fae1dc7742d06318aae051a6303/mkdocs/tests/base.py#L26
    def _load_config(self, site_root: str | None = None, **cfg) -> MkDocsConfig:
        """Helper to build a simple config for testing."""
        path_base = Path(os.path.join(os.path.abspath(os.path.dirname(__file__))))
        print(f"{path_base=}")
        config_file = path_base / site_root / 'mkdocs.yml'
        conf = MkDocsConfig(config_file_path=str(config_file))
        
        with open(config_file) as f:
            conf.load_file(f)

        conf.load_dict(cfg)
        
        if 'site_name' not in conf or not conf['site_name']:
            conf['site_name'] = 'Example'
        if 'docs_dir' not in conf or not conf['docs_dir']:
            # Point to an actual dir to avoid a 'does not exist' error on validation.
            conf['docs_dir'] = path_base / site_root / 'docs'

        print(conf)

        errors_warnings = conf.validate()
        assert errors_warnings == ([], []), errors_warnings
        return conf