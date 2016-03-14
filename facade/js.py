from __future__ import absolute_import
try:
    import jiphy
except ImportError:
    print "pip install jiphy"
    raise ImportError("The JS loader cannot be used without jiphy")

from .base import loader

@loader('.js')
def js_loader(_, module, content):
    exec(jiphy.to.python(content), module.__dict__)
    return module

js_loader.register()