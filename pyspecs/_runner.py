import os
import logging

from .framework import framework


log = logging.getLogger(__name__)


class _StepRunner(object):
    """
    Imports all test files in the project scope. Specs within these files
    should either be at the top level of the module or in a function or class
    that is invoked from the top-level. This service is managed and invoked
    by the framework.
    """
    def load_steps(self, working):
        for root, dirs, files in os.walk(working):
            for f in files:
                if self._is_test_module(f):
                    path = os.path.join(root, f)
                    self._exec_in(path)

    def _is_test_module(self, f):
        return f.endswith('.pyspecs')

    def _exec_in(self, path):
        log.debug('Procesing file %s', path)

        config = framework()
        with open(path) as fd:
            source = ''
            for line in fd.readlines():
                source += line
        code = compile(source, path, 'exec')
        exec(code, config)
        return config
