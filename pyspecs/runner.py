from pyspecs.result import BrokenSpecResult
from pyspecs.spec import Spec

class SpecRunner(object):
    def __init__(self, loader, reporter):
        self.loader = loader
        self.reporter = reporter

    def run_specs(self):
        for spec in self.loader.load_specs():
            result = self._execute(spec)
            self.reporter.report(result)

    def _execute(self, spec):
        try:
            spec = spec()
        except Exception:
            return BrokenSpecResult(Spec.describe(spec))
        else:
            return spec.execute()
