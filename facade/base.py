import sys
from os import path
from types import ModuleType


class Finder(object):
    def __init__(self, file_ext, factory):
        self.ext = file_ext
        self.loader_factory = factory

    def find_module(self, name, m_path):
        name += self.ext
        if m_path is not None:
            name = path.join(m_path[0], name)
        if path.exists(name):
            return Loader(name, self.loader_factory)

    def register(self):
        sys.meta_path.append(self)

    def revoke(self):
        sys.meta_path = [finder for finder in sys.meta_path if finder is not self]


class Loader(object):
    def __init__(self, file_path, factory):
        self.factory = factory
        with open(file_path) as content:
            self.content = content.read()

    def load_module(self, name):
        module = ModuleType(name)
        return self.factory(name, module, self.content)


def loader(ext):
    def _outer(f):
        return Finder(ext, f)
    return _outer