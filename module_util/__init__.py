# as a marker of an unit
#import os, glob
__all__ = [
    "imp_mod_tmp",
    "imp_mod_fm_file_loc"
    #os.path.split(os.path.splitext(file)[0])[1]
    #for file in glob.glob(os.path.join(os.path.dirname(__file__), '[a-zA-Z0-9]*.py'))
]

import sys
from importlib import import_module
from importlib.abc import MetaPathFinder
from importlib.util import spec_from_file_location

def imp_mod_fm_file_loc(name, location):
    class Finder(MetaPathFinder):
        @staticmethod
        def find_spec(fullname, *_):
            if fullname == name:
                return spec_from_file_location(name, location)

    finder = Finder()
    sys.meta_path.insert(0, finder)
    try:
        return import_module(name)
    finally:
        sys.meta_path.remove(finder)
