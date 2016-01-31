from __future__ import absolute_import
import json
from .base import loader

@loader('.json')
def json_loader(_, module, content):
    module.__dict__.update(json.loads(content))
    return module

json_loader.register()