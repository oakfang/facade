import contextlib as ctx
import re

from base import loader

VIEW_RE = re.compile('^(\s*view \w+\(.*?\):(.|\n)*?\r?\n\s*)(\n|$)', re.MULTILINE)
VIEW_HEADER_RE = re.compile('(\s*)view (\w+)\((.*?)\):')


def tag(tag_name, bufferer):
    @ctx.contextmanager
    def factory(**attrs):
        bufferer._buffer += '<{} {}>'.format(tag_name,
                                             ' '.join(['{}="{}"'.format(key.replace('klass', 'class'), val) 
                                                       for (key, val) in attrs.iteritems()]))
        yield
        bufferer._buffer += '</{}>'.format(tag_name)
    return factory


class Page(object):
    def __init__(self):
        self._buffer = ''

    def __getattr__(self, attr):
        try:
            if attr in ('input', 'img', 'hr'):
                return lambda **attrs: self._self_closing_tag(attr, **attrs)
            return object.__getattr__(self, attr)
        except AttributeError:
            return tag(attr, self)

    def text(self, t):
        self._buffer += str(t)

    def _self_closing_tag(self, tag_name, **attrs):
        self._buffer += '<{} {}/>'.format(tag_name,
                                          ' '.join(['{}="{}"'.format(key.replace('klass', 'class'), val) 
                                                    for (key, val) in attrs.iteritems()]))

    def __str__(self):
        return self._buffer


def view(f):
    def _inner(*args, **kwargs):
        p = Page()
        f(p, *args, **kwargs)
        return str(p)
    return _inner


def view_parser(content):
    for view_block in [res[0] for res in VIEW_RE.findall(content)]:
        block = VIEW_HEADER_RE.sub(r'\1@view\n\1def \2(__p, \3):', view_block)
        block = re.sub(r'\<py\>((.|\n)*?)\</py\>', r'__p.text(\1)', block)
        temp = re.sub(r'^(\s*)?\<(\w+)\s?(.*?)\>((.|\n)*?)\1\</\2\>', r'\1with __p.\2(\3):\4', block, flags=re.M)
        while temp != block:
            block = temp
            temp = re.sub(r'^(\s*)?\<(\w+)\s?(.*?)\>((.|\n)*?)\1\</\2\>', r'\1with __p.\2(\3):\4', block, flags=re.M)
        block = re.sub(r'^(\s*)?<(\w+)\s?(.*?)\/\>\s*$', r'\1__p.\2(\3)', block, flags=re.M)
        content = content.replace(view_block, block)
    return content


@loader('.pyv')
def pyv_loader(_, module, content):
    module.view = view
    exec(view_parser(content + '\n'), module.__dict__)
    return module


pyv_loader.register()