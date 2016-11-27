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
    def load_steps(self, working, registry):
        for root, dirs, files in os.walk(working):
            for f in files:
                if self._is_test_module(f):
                    path = os.path.join(root, f)
                    self._exec_in(path, registry)

    def _is_test_module(self, f):
        return f.endswith('.pyspecs')

    def _exec_in(self, path, registry):
        log.debug('Procesing file %s', path)

        config = framework(registry)
        with open(path) as fd:
            code = compile(fd.read(), path, 'exec', optimize=0)
            exec(code, config)
        return config
