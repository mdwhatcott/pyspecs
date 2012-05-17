from collections import OrderedDict
from inspect import getmembers, ismethod
from itertools import chain
from sys import exc_info as get_exception_info
from pyspecs._should import ShouldError
from pyspecs._steps import PYSPECS_STEP, ALL_STEPS, THEN_STEP


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


class SpecSteps(object):
    def __init__(self, reporter, steps):
        self.reporter = reporter
        self.steps = steps
        for step in self.steps:
            step.with_callbacks(self._success, self._failure, self._error)
        self._current_index = 0

    def __iter__(self):
        return self._iterator()

    @property
    def _current(self):
        return self.steps[self._current_index] \
            if len(self.steps) > self._current_index \
            else None

    def _iterator(self):
        while self._current is not None:
            yield self._current

    def _error(self, exc_stuff):
        self.reporter.error(self._current, exc_stuff)
        if self._current.step != THEN_STEP:
            self._current_index = len(self.steps)

    def _failure(self, exc_stuff):
        if self._current.step == THEN_STEP:
            self.reporter.failure(self._current, exc_stuff)
            self._current_index += 1
        else:
            self._error(exc_stuff)

    def _success(self):
        self.reporter.success(self._current)
        self._current_index += 1


class Step(object):
    def __init__(self, spec, step, name, action):
        self.spec = spec
        self.step = step
        self.name = name
        self._action = action
        self._on_success = None
        self._on_failure = None
        self._on_error = None

    def with_callbacks(self, success, failure, error):
        self._on_success = success
        self._on_failure = failure
        self._on_error = error

    def execute(self):
        try:
            self._action(self.spec)
        except ShouldError:
            self._on_failure(get_exception_info())
        except Exception:
            self._on_error(get_exception_info())
        else:
            self._on_success()


def collect_steps(spec):
    steps = OrderedDict.fromkeys(ALL_STEPS)
    steps[THEN_STEP] = list()

    for name, method in getmembers(spec.__class__, ismethod):
        step = getattr(method, PYSPECS_STEP, None)
        if step is None or step not in steps:
            continue

        spec_name = describe(spec.__class__)
        description = describe(name)
        if step == THEN_STEP:
            steps[step].append(Step(spec_name, step, description, method))
        else:
            steps[step] = Step(spec_name, step, description, method)

    return steps.values()


def describe(obj):
    return obj.__name__.replace('_', ' ')