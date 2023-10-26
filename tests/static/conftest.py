from pathlib import Path
import pytest
import os

from mkdocs.commands.build import build
from mkdocs.config.defaults import MkDocsConfig

DEBUG = True

# Based on https://github.com/mkdocs/mkdocs/blob/b5250bf9e2a58fae1dc7742d06318aae051a6303/mkdocs/tests/base.py#L26
def load_config(config_file_path: str | None = None, **cfg) -> MkDocsConfig:
    """Helper to build a simple config for testing."""
    path_base = os.path.join(os.path.abspath(os.path.dirname(__file__)))
    if 'site_name' not in cfg:
        cfg['site_name'] = 'Example'
    if 'docs_dir' not in cfg:
        # Point to an actual dir to avoid a 'does not exist' error on validation.
        cfg['docs_dir'] = os.path.join(path_base, config_file_path, 'docs')
    if 'plugins' not in cfg:
        cfg['plugins'] = []
    print(f"{config_file_path=}")
    conf = MkDocsConfig(config_file_path=config_file_path or os.path.join(path_base, 'mkdocs.yml'))
    conf.load_dict(cfg)

    print(conf)

    errors_warnings = conf.validate()
    assert errors_warnings == ([], []), errors_warnings
    return conf

@pytest.fixture
def site(dir: str | Path, tmp_path) -> Path:
    """Build a simple site for testing

    Args:
        dir (str | Path, optional): A directory containing the site content. Must contain a 
            mkdocs.yml and a /docs folder.
    """                
    config = load_config(str(dir), plugins= ['mkdocs-pyscript'])
    path = Path("_debug_site") if DEBUG else tmp_path
    config.site_dir = path
    build(config)
    return path

        