from collections import OrderedDict
from inspect import getmembers, ismethod
from itertools import chain
from sys import exc_info as get_exception_info
from pyspecs._should import ShouldError
from pyspecs._steps import PYSPECS_STEP, ALL_STEPS, THEN_STEP, AFTER_STEP


class SpecRunner(object):
    def __init__(self, loader, reporter, captured_stdout):
        self.loader = loader
        self.reporter = reporter
        self.captured_stdout = captured_stdout

    def run_specs(self):
        steps = chain(*self._spec_steps())
        for step in steps:
            with self.captured_stdout:
                step.execute()

    def _spec_steps(self):
        for spec in self.loader.load_specs():
            yield SpecSteps(self.reporter, collect_steps(spec()))


class SpecSteps(object):
    def __init__(self, reporter, steps):
        self.reporter = reporter
        self.steps = steps
        for step in self.steps:
            step.with_callbacks(self._success, self._failure, self._error)
        self._current_index = 0

    def __iter__(self):
        return self._iterator()

    def _iterator(self):
        while self._current is not None:
            yield self._current

    @property
    def _current(self):
        return self.steps[self._current_index] \
            if len(self.steps) > self._current_index \
            else None

    def _error(self, exc_stuff):
        step = self._current
        self.reporter.error(step.spec_name, step.step, step.name, exc_stuff)
        if step.step == THEN_STEP or step.step == AFTER_STEP:
            self._current_index += 1
        else:
            self._current_index = len(self.steps) - 1

    def _failure(self, exc_stuff):
        if self._current.step != THEN_STEP:
            self._error(exc_stuff)
        else:
            step = self._current
            self.reporter.failure(step.spec_name, step.name, exc_stuff)
            self._current_index += 1

    def _success(self):
        step = self._current
        self.reporter.success(step.spec_name, step.step, step.name)
        self._current_index += 1


class Step(object):
    def __init__(self, spec, step, action):
        self.spec = spec
        self.spec_name = describe(spec.__class__)
        self.step = step
        self.name = describe(action)
        self._action = action
        self._on_success = None
        self._on_failure = None
        self._on_error = None

    def with_callbacks(self, success, failure, error):
        self._on_success = success
        self._on_failure = failure
        self._on_error = error

    #noinspection PyBroadException
    def execute(self):
        try:
            self._action(self.spec)
        except ShouldError:
            self._on_failure(get_exception_info())
        except:
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

        if step == THEN_STEP:
            steps[step].append(Step(spec, step, method))
        else:
            steps[step] = Step(spec, step, method)

    return list(flatten(steps.values()))


def describe(obj):
    return obj.__name__.replace('_', ' ')


def flatten(list_with_lists):
    for element in list_with_lists:
        if isinstance(element, list):
            for item in element:
                if item:
                    yield item
        else:
            if element:
                yield element