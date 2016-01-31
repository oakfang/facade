from __future__ import absolute_import

import ConfigParser
import io

from .base import loader

@loader('.ini')
def ini_loader(_, module, content):
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.readfp(io.BytesIO(content))
    for attr in dir(config):
        setattr(module, attr, getattr(config, attr))
    return module

ini_loader.register()