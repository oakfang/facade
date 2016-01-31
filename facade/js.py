import jiphy # pip install jiphy
from base import loader

@loader('.js')
def js_loader(_, module, content):
    exec(jiphy.to.python(content), module.__dict__)
    return module

js_loader.register()