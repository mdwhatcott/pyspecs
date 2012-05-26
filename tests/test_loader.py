from exceptions import Exception, KeyError, ImportError, NotImplementedError
from unittest import TestCase
from pyspecs._loader import Location, Importer, BlankModule, load_spec_classes
from pyspecs import spec


class TestImporter(TestCase):
    def setUp(self):
        self.exception = Exception

        def import_tool(name):
            modules = {
                'module': 42,
                'package.module': 43,
            }
            try:
                return modules[name]
            except KeyError:
                raise self.exception

        self.importer = Importer('/this/is/my/working/directory', import_tool)

    def test_importer_resolves_module_names_correctly(self):
        module1_path = '/this/is/my/working/directory/module.py'
        module2_path = '/this/is/my/working/directory/package/module.py'
        self.assertEqual(42, self.importer.import_module(module1_path))
        self.assertEqual(43, self.importer.import_module(module2_path))

    def test_importer_provides_blank_module_upon_import_error(self):
        module_path = '/this/is/my/working/directory/not-there.py'

        self.exception = ImportError
        imported = self.importer.import_module(module_path)
        self.assertIsInstance(imported, BlankModule)

        self.exception = NotImplementedError
        imported = self.importer.import_module(module_path)
        self.assertIsInstance(imported, BlankModule)

    def test_importer_does_not_import_files_that_are_off_limits(self):
        off_limites = [
            '/this/is/my/working/directory/__init__.py',
            '/this/is/my/working/directory/module.pyc',
            '/this/is/my/working/directory/module.pyo',
        ]


class TestLoadSpecFromSpecModule(TestCase):
    def setUp(self):
        self.walker = FakeWalk('', [
            Location(('', [], ['file1_spec.py'])),
        ])
        self.importer = FakeImporter(fake_module=FakeModule('file1_spec.py', {
            'the_spec': TheSpec,
            'not_the_spec': NotTheSpec
        }))

    def test_load_spec_and_ignore_non_spec(self):
        specs = list(load_spec_classes(self.walker, self.importer))
        self.assertEqual(1, len(specs))
        self.assertEqual(TheSpec, specs[0])

    def test_does_not_attempt_to_import_files_that_are_off_limites(self):
        self.walker = FakeWalk('', [
            Location(('', [], ['__init__.py'])),
            Location(('', [], ['file1_spec.txt'])),
        ])
        specs = list(load_spec_classes(self.walker, self.importer))
        self.assertEqual(0, len(specs))


class TheSpec(spec): pass
class NotTheSpec(): pass


class FakeWalk(object):
    def __init__(self, start, locations):
        self.start = start
        self.locations = locations
        self.current_location = 0

    def __iter__(self):
        return self

    def next(self):
        try:
            current = self.current_location
            self.current_location += 1
            return self.locations[current]
        except IndexError:
            raise StopIteration


class FakeImporter(object):
    def __init__(self, fake_module=None):
        self.fake_module = fake_module

    def import_module(self, module_name):
        if self.fake_module.name == module_name:
            return self.fake_module


class FakeModule(object):
    def __init__(self, name, attributes=None):
        self.name = name
        self.attributes = attributes or dict()

    @property
    def __dict__(self):
        return self.attributes