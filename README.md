# Facade
## Meta loaders for fun and profit

Facade builds upon a less known feature of python,
specified in [PEP 302](https://www.python.org/dev/peps/pep-0302/)
called `Import Hooks` or the `meta_path`.

Facade exports 2 main features:

- Easy creation of meta loaders/import hooks
- 5 ready-made loaders to be used as examples or for real-life challenges

### Creating a new loader

```python
# my_loader.py
from facade import loader

@loader('.xyz') # my loader's dedicated extension
def xyz_loader(module_name, module, file_content):
    module.data = file_content
    return module

xyz_loader.register() # start hooking on .xyz files


# script.py
from my_loader import xyz_loader
import foo # this is actually the file foo.xyz!

xyz_loader.revoke() # stop hooking, not mandatory
```


### Using the sample loaders

```python
from facade import pyv
import views # a .pyv file, using `pyvue`

view.index_page(...)
```


### Using the DLL loader
`facade` is bundled with a [CFFI](http://cffi.readthedocs.org/en/latest/index.html)-based DLL loader, and based on this awesome [gist](https://gist.github.com/seanjensengrey/f5d73bbdf22cfa1ad463).

It is currently only tested against DLLs created using `rustc`.

```python
from facade import dll
import triple

triple.decalre('int triple(int);')

print triple.triple(10) // 30
```
