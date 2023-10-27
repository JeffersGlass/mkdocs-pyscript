from http.server import HTTPServer as SuperHTTPServer
from http.server import SimpleHTTPRequestHandler

import threading
from pathlib import Path
import pytest
import os

import pdb

from mkdocs.commands.build import build
from mkdocs.config.defaults import MkDocsConfig

EMIT_FILES = True

# Based on https://github.com/mkdocs/mkdocs/blob/b5250bf9e2a58fae1dc7742d06318aae051a6303/mkdocs/tests/base.py#L26
def load_config(site_root: str | None = None, **cfg) -> MkDocsConfig:
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


## ----- Servers and Support ------

def pytest_configure(config):
    if config.option.dev:
        config.option.headed = True

def pytest_addoption(parser):
    parser.addoption(
        "--dev",
        action="store_true",
        help="Automatically open a devtools panel. Implies --headed and --no-fake-server",
    )

@pytest.fixture(scope="session")
def browser_type_launch_args(request):
    """
    Override the browser_type_launch_args defined by pytest-playwright to
    support --devtools.

    NOTE: this has been tested with pytest-playwright==0.3.0. It might break
    with newer versions of it.
    """
    # this calls the "original" fixture defined by pytest_playwright.py
    launch_options = request.getfixturevalue("browser_type_launch_args")
    if request.config.option.dev:
        launch_options["devtools"] = True
    return launch_options

class DevServer(SuperHTTPServer):
    """
    Class for wrapper to run SimpleHTTPServer on Thread.
    Ctrl +Only Thread remains dead when terminated with C.
    Keyboard Interrupt passes.
    """

    def __init__(self, base_url, *args, **kwargs):
        self.base_url = base_url
        super().__init__(*args, **kwargs)

    def run(self):
        try:
            self.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.server_close()

@pytest.fixture(scope="session")
def dev_server(request):
    class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
        enable_cors_headers = True

        @classmethod
        def my_headers(cls):
            if cls.enable_cors_headers:
                return {
                    "Cross-Origin-Embedder-Policy": "require-corp",
                    "Cross-Origin-Opener-Policy": "same-origin",
                }
            return {}

        def end_headers(self):
            self.send_my_headers()
            SimpleHTTPRequestHandler.end_headers(self)

        def send_my_headers(self):
            for k, v in self.my_headers().items():
                self.send_header(k, v)

        def log_message(self, fmt, *args):
            print("http_server", fmt % args)
            #print("http_server", fmt % args, color="blue")

    host, port = "localhost", 8080
    base_url = f"http://{host}:{port}"

    # serve_Run forever under thread
    server = DevServer(base_url, (host, port), MyHTTPRequestHandler)

    thread = threading.Thread(None, server.run)
    thread.start()

    yield server  # Transition to test here

    # End thread
    server.shutdown()
    thread.join()

@pytest.fixture()
def hold_at_end(request):
    if request.config.option.headed:
        pdb.Pdb.intro = (
            "\n"
            "This (Pdb) was started automatically because you passed --headed:\n"
            "the execution of the test pauses here to give you the time to inspect\n"
            "the browser. When you are done, type one of the following commands:\n"
            "    (Pdb) continue\n"
            "    (Pdb) cont\n"
            "    (Pdb) c\n"
        )
        pdb.set_trace()
    yield