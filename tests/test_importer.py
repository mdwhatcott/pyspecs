from unittest.case import TestCase
from pyspecs._loader import Importer, BlankModule


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