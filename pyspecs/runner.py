from itertools import chain
from pyspecs.spec import SpecSteps


class SpecRunner(object):
    def __init__(self, loader, reporter):
        self.loader = loader
        self.reporter = reporter

    def run_specs(self):
        for step in chain(self._spec_steps()):
            step.execute()

    def _spec_steps(self):
        for spec in self.loader.load_specs():
            yield SpecSteps(self.reporter, spec().___collect_steps()) # TODO: initialization error