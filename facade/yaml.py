from __future__ import absolute_import
try:
    import yaml
except ImportError:
    print "pip install yaml"
    raise ImportError("The YAML loader cannot be used without yaml")
from .base import loader

@loader('.yaml')
def yaml_loader(_, module, content):
    module.__dict__.update(yaml.load(content))
    return module

yaml_loader.register()