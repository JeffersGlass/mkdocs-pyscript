from pathlib import Path
import pytest
import os

from mkdocs.commands.build import build
from mkdocs.config.defaults import MkDocsConfig

DEBUG = True

# Based on https://github.com/mkdocs/mkdocs/blob/b5250bf9e2a58fae1dc7742d06318aae051a6303/mkdocs/tests/base.py#L26
def load_config(site_root: str | None = None, **cfg) -> MkDocsConfig:
    """Helper to build a simple config for testing."""
    path_base = Path(os.path.join(os.path.abspath(os.path.dirname(__file__))))
    print(f"{path_base=}")
    
    """if 'plugins' not in cfg:
        cfg['plugins'] = [] """
    config_file = path_base / site_root / 'mkdocs.yml'
    conf = MkDocsConfig(config_file_path=str(config_file))
    
    print(f"{config_file.absolute()=}")
    with open(config_file) as f:
        conf.load_file(f)

    if 'site_name' not in conf or not conf['site_name']:
        conf['site_name'] = 'Example'
    if 'docs_dir' not in conf or not conf['docs_dir']:
        # Point to an actual dir to avoid a 'does not exist' error on validation.
        conf['docs_dir'] = path_base / site_root / 'docs'

    print(conf)

    errors_warnings = conf.validate()
    assert errors_warnings == ([], []), errors_warnings
    return conf

@pytest.fixture
def site(dir: str | Path, tmp_path, cfg: dict=None,) -> Path:
    """Build a simple site for testing

    Args:
        dir (str | Path, optional): A directory containing the site content. Must contain a 
            mkdocs.yml and a /docs folder.
    """                
    if cfg is None: cfg = {}
    print(f"{dir=}")
    config = load_config(str(dir), **cfg)
    path = Path("_debug_site") if DEBUG else tmp_path
    config.site_dir = path
    build(config)
    return path

        