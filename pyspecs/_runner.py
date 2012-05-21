from collections import OrderedDict
from inspect import getmembers, ismethod
import inspect
from sys import exc_info
from pyspecs._should import ShouldError
from pyspecs._steps import PYSPECS_STEP, ALL_STEPS, THEN_STEP, AFTER_STEP
from pyspecs.spec import spec


SPEC_NOT_IMPLEMENTED = 'No assertions ("@then" decorators) found ' \
                       'with the current spec.'
SPEC_INITIALIZATION_ERROR = 'The spec could not be initialized ' \
                            '(error in constructor).'


class SpecRunner(object):
    def __init__(self, loader, reporter, captured_stdout):
        self.loader = loader
        self.reporter = reporter
        self.captured_stdout = captured_stdout

    def run_specs(self):
        for spec in self._spec_steps():
            for step in spec:
                with self.captured_stdout:
                    step.execute()

    def _spec_steps(self):
        for spec in self.loader.load_specs():
            yield SpecSteps(self.reporter, collect_steps(spec))


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

    def _next(self):
        self._current_index += 1

    def _error(self, exc_stuff):
        step = self._current
        self.reporter.error(step.spec_name, step.step, step.name, exc_stuff)
        if step.step in [THEN_STEP, AFTER_STEP] or step.step not in ALL_STEPS:
            self._next()
        else:
            self._advance_to_cleanup()

    def _advance_to_cleanup(self):
        cleanup_offset = 1 if self.steps[-1].step == AFTER_STEP else 0
        self._current_index = len(self.steps) - cleanup_offset

    def _failure(self, exc_stuff):
        if self._current.step != THEN_STEP:
            self._error(exc_stuff)
        else:
            step = self._current
            self.reporter.failure(step.spec_name, step.name, exc_stuff)
            self._next()

    def _success(self):
        step = self._current
        self.reporter.success(step.spec_name, step.step, step.name)
        self._next()


class Step(object):
    def __init__(self, spec, step, action):
        self.spec = spec
        self.spec_name = describe(spec)
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

    def execute(self):
        try:
            self._action(self.spec)
        except ShouldError:
            self._on_failure(exc_info())
        except Exception:
            self._on_error(exc_info())
        else:
            self._on_success()


def describe(obj):
    original = str(obj)

    if isinstance(obj, basestring):
        original = obj

    elif inspect.ismethod(obj):
        original = obj.__name__

    elif inspect.isclass(obj):
        original = obj.__name__

    elif inspect.isfunction(obj):
        original = obj.func_name

    elif isinstance(obj, spec):
        original = obj.__class__.__name__

    return original.replace('_' , ' ')


def collect_steps(spec):
    try:
        spec = spec()
    except Exception:
        return [Step(
            describe(spec), describe(collect_steps), initialization_error)]

    steps = _scan_for_steps(spec)

    if not steps[THEN_STEP]:
        return [Step(spec, describe(collect_steps), not_implemented)]

    return list(flatten(steps.values()))


def _scan_for_steps(spec):
    steps = OrderedDict.fromkeys(ALL_STEPS)
    steps[THEN_STEP] = list()

    for name, method in getmembers(spec.__class__, ismethod):
        step = getattr(method, PYSPECS_STEP, None)
        if step == THEN_STEP:
            steps[step].append(Step(spec, step, method))
        else:
            steps[step] = Step(spec, step, method)

    return steps


#noinspection PyUnusedLocal
def initialization_error(self):
    raise NotImplementedError(SPEC_INITIALIZATION_ERROR)


#noinspection PyUnusedLocal
def not_implemented(self):
    raise NotImplementedError(SPEC_NOT_IMPLEMENTED)


def flatten(list_with_lists):
    for element in list_with_lists:
        if isinstance(element, list):
            for item in element:
                if item:
                    yield item
        else:
            if element:
                yield element