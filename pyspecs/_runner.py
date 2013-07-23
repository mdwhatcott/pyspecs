import importlib
import os
import traceback


class _StepRunner(object):
    """
    Imports all test files in the project scope. Specs within these files
    should either be at the top level of the module or in a function or class
    that is invoked from the top-level. This service is managed and invoked
    by the framework.
    """
    def __init__(self, reporter):
        self.reporter = reporter

    def load_steps(self, working):
        for root, dirs, files in os.walk(working):
            for f in files:
                if self._is_test_module(f):
                    name = self._derive_module_name(
                        os.path.join(root, f), working)
                    self._import(name)

        self.reporter.aggregate()

    def _is_test_module(self, f):
        return f.endswith('test.py') or \
            f.endswith('tests.py') or \
            (f.startswith('test') and f.endswith('.py'))

    # noinspection PyArgumentList
    def _derive_module_name(self, path, working):
        common = os.path.commonprefix([working, path])
        slice_module_name = slice(len(common) + 1, len(path))
        return path[slice_module_name] \
            .replace('.py', '') \
            .replace('\\', '.') \
            .replace('/', '.')

    def _import(self, name):
        try:
            importlib.import_module(name)
        except (ImportError, NotImplementedError):
            print traceback.format_exc()