import os

base_path = os.path.dirname(os.path.abspath(__file__))
def glr_path_static():
        """Returns path to packaged static files"""
        return os.path.join(base_path, "js")