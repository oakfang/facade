from __future__ import absolute_import
try:
    from pyvue import view, view_parser
except ImportError:
    print "pip install pyvue"
    raise ImportError("The pyv loader cannot be used without pyvue")

from .base import loader


@loader('.pyv')
def pyv_loader(_, module, content):
    module.view = view
    exec(view_parser(content + '\n'), module.__dict__)
    return module


pyv_loader.register()