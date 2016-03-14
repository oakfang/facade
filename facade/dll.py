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
    def __init__(self, name, ffi, lib, headers):
        super(DllModule, self).__init__(name)
        self._lib = lib
        self._ffi = ffi
        for header in headers:
            self.declare(header)

    def declare(self, signature):
        self._ffi.cdef(signature)

    def __getattr__(self, attr):
        return getattr(self._lib, attr)


class DllFinder(Finder):
    def __init__(self):
        pass

    def find_module(self, name, m_path):
        if m_path is not None:
            name = path.join(m_path[0], name)
        source = name + '.dll'
        headers = name + '.h'
        if path.exists(source):
            return DllLoader(source, headers if path.exists(headers) else None)


class DllLoader(Loader):
    def __init__(self, file_path, headers_path):
        ffi = FFI()
        self.ffi = ffi
        self.lib = ffi.dlopen(file_path)
        self.headers = []
        if headers_path is not None:
            with open(headers_path) as headers:
                self.headers = headers.readlines()

    def load_module(self, name):
        return DllModule(name, self.ffi, self.lib, self.headers)


DllFinder().register()