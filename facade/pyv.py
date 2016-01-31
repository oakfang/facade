from pyvue import view, view_parser

from base import loader


@loader('.pyv')
def pyv_loader(_, module, content):
    module.view = view
    exec(view_parser(content + '\n'), module.__dict__)
    return module


pyv_loader.register()