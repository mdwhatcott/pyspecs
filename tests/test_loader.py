from unittest.case import TestCase
from pyspecs.loader import SpecLoader, Location
from pyspecs.spec import Spec


class TestLoadSpecFromSpecModule(TestCase):
    def setUp(self):
        self.walker = FakeWalk('', [
            Location(('', [], ['file1_spec.py']))
        ])
        self.importer = FakeImporter(fake_module=FakeModule('file1_spec.py', {
            'the_spec': TheSpec,
            'not_the_spec': NotTheSpec
        }))

    def test_load_spec_and_ignore_non_spec(self):
        loader = SpecLoader(self.walker, self.importer)
        specs = list(loader.load_specs())
        self.assertEqual(1, len(specs))
        self.assertEqual(TheSpec, specs[0])


class TheSpec(Spec): pass
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