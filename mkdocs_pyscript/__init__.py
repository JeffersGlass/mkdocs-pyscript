import os

base_path = os.path.dirname(os.path.abspath(__file__))

def glr_path_static(pathname):
        """Returns path to packaged static files"""
        return os.path.join(base_path, pathname)