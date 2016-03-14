from __future__ import absolute_import
try:
    from cffi import FFI
except ImportError:
    print "pip install cffi"
    raise ImportError("The DLL loader cannot be used without cffi")

from os import path
from types import ModuleType

from .base import Finder, Loader


class DllModule(ModuleType):
    def __init__(self, name, ffi, lib):
        super(DllModule, self).__init__(name)
        self._lib = lib
        self._ffi = ffi

    def declare(self, signature):
        self._ffi.cdef(signature)

    def __getattr__(self, attr):
        return getattr(self._lib, attr)


class DllFinder(Finder):
    def __init__(self):
        pass

    def find_module(self, name, m_path):
        name += '.dll'
        if m_path is not None:
            name = path.join(m_path[0], name)
        if path.exists(name):
            return DllLoader(name)


class DllLoader(Loader):
    def __init__(self, file_path):
        ffi = FFI()
        self.ffi = ffi
        self.lib = ffi.dlopen(file_path)

    def load_module(self, name):
        return DllModule(name, self.ffi, self.lib)


DllFinder().register()