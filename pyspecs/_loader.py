import importlib
import inspect
import os
from os.path import commonprefix
from pyspecs.spec import spec


def load_spec_classes(walker, importer):
    for location in walker:
        for path in location.py_spec_modules:
            module = importer.import_module(path)
            for cls in extract_spec_classes(module):
                yield cls

def extract_spec_classes(module):
    return (c for c in vars(module).itervalues()
        if inspect.isclass(c) and issubclass(c, spec))


class Importer(object):
    def __init__(self, working, import_tool=None):
        self.working = working
        self.import_tool = import_tool or importlib.import_module

    def import_module(self, path):
        module_name = self._derive_module_name(path)
        return self._imported_module(module_name)

    def _derive_module_name(self, path):
        common = commonprefix([self.working, path])
        slice_module_name = slice(len(common) + 1, len(path))
        return path[slice_module_name]\
            .replace('.py', '')\
            .replace('\\', '.')\
            .replace('/', '.')

    def _imported_module(self, module_name):
        try:
            return self.import_tool(module_name)
        except (ImportError, NotImplementedError):
            return BlankModule()


class BlankModule(object):
    def __init__(self):
        self.__dir__ = list()


class Location(object):
    def __init__(self, step):
        root, files = step[0], step[2]
        self._files = [os.path.join(root, f) for f in files]

    @property
    def py_spec_modules(self):
        return [f for f in self._files
                if not f.startswith('__') and
                   (f.endswith('spec.py') or f.endswith('specs.py'))]