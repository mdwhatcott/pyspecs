from collections import OrderedDict
from inspect import getmembers, ismethod, isclass, isfunction
from sys import exc_info
from pyspecs._should import ShouldError
from pyspecs._steps import PYSPECS_STEP, ALL_STEPS, THEN_STEP, AFTER_STEP
from pyspecs.spec import spec


def run_specs(loader, reporter, captured_stdout):
    for spec in load_specs(loader, reporter):
        for step in spec:
            with captured_stdout:
                step.execute()


def load_specs(loader, reporter):
    for spec in loader.load_specs():
        yield SpecSteps(reporter, collect_steps(spec))


def collect_steps(spec):
    try:
        spec = spec()
    except Exception:
        return constructor_error_steps(spec)

    steps = scan_for_steps(spec)

    if not steps[THEN_STEP]:
        return no_assertions_steps(spec)

    extra_steps = [s for s in steps if s != THEN_STEP and len(steps[s]) > 1]
    if any(extra_steps):
        return extra_steps_steps(spec, extra_steps)

    return list(flatten(steps.values()))


def constructor_error_steps(spec):
    def initialization_error(spec):
        raise SpecInitializationError.constructor_error(spec)

    return [Step(describe(spec), describe(collect_steps), initialization_error)]


def scan_for_steps(spec):
    steps = OrderedDict.fromkeys(ALL_STEPS)
    for step in steps:
        steps[step] = list()

    for name, method in getmembers(spec.__class__, ismethod):
        step = getattr(method, PYSPECS_STEP, None)
        if step in steps:
            steps[step].append(Step(spec, step, method))

    return steps


def no_assertions_steps(spec):
    def not_implemented(spec):
        raise SpecInitializationError.no_assertions(spec)

    return [Step(spec, describe(collect_steps), not_implemented)]


def extra_steps_steps(spec, extra):
    def extra_steps(spec):
        raise SpecInitializationError.extra_steps(spec, extra)

    return [Step(spec, describe(collect_steps), extra_steps)]


def flatten(list_with_lists):
    """
    Turns a list with lists as elements into a flat list.

    flatten([1, 2, 3, [4, 5], 6]) == [1, 2, 3, 4, 5, 6]

    (Not recursive)
    """
    for element in list_with_lists:
        if isinstance(element, list):
            for item in element:
                if item:
                    yield item
        else:
            if element:
                yield element


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
    """
    Turns an object into a space-delimited description.

    describe(obj_with_underscores_in_name) == 'obj with underscores in name'
    """
    original = str(obj)

    if isinstance(obj, basestring):
        original = obj

    elif ismethod(obj):
        original = obj.__name__

    elif isclass(obj):
        original = obj.__name__

    elif isfunction(obj):
        original = obj.func_name

    elif isinstance(obj, spec):
        original = obj.__class__.__name__

    return original.replace('_' , ' ')


class SpecInitializationError(Exception):
    def __init__(self, message, *args, **kwargs):
        super(SpecInitializationError, self).__init__(*args, **kwargs)
        self.message = message

    @classmethod
    def constructor_error(cls, spec):
        message = 'The spec ({0}) could not be ' \
                  'initialized (error in constructor).'.format(describe(spec))
        return SpecInitializationError(message)

    @classmethod
    def no_assertions(cls, spec):
        message = 'No assertions ("@then" decorators) ' \
                  'found with the spec ({0}).'.format(describe(spec))
        return SpecInitializationError(message)

    @classmethod
    def extra_steps(cls, spec, extra):
        message = 'The spec ({0}) has extra steps ({1}).'\
            .format(describe(spec), extra)
        return SpecInitializationError(message)