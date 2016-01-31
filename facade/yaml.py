from __future__ import absolute_import
import yaml #pip install
from .base import loader

@loader('.yaml')
def yaml_loader(_, module, content):
    module.__dict__.update(yaml.load(content))
    return module

yaml_loader.register()