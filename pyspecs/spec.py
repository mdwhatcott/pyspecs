from collections import OrderedDict
from inspect import getmembers, ismethod
from pyspecs.result import SpecResult
from pyspecs.should import ShouldError
from pyspecs.steps import PYSPECS_STEP, ALL_STEPS, THEN_STEP


class Spec(object):
    def execute(self):
        self._collect_steps()
        self._result = SpecResult(self._describe(self.__class__))
        self._result.start_timer()
        self._execute_steps()
        self._result.stop_timer()
        return self._result

    def _collect_steps(self):
        self._steps = OrderedDict.fromkeys(ALL_STEPS)
        self._steps[THEN_STEP] = list()
        for name, method in getmembers(self.__class__, ismethod):
            step = getattr(method, PYSPECS_STEP, None)
            if not step in self._steps:
                continue
            if step == THEN_STEP:
                self._steps[step].append(method)
            else:
                self._steps[step] = method

    def _execute_steps(self):
        for name, step in self._steps.iteritems():
            if step is None:
                continue
            if name == THEN_STEP:
                self._execute_assertions(name, step)
            else:
                self._execute_step(name, step)

    def _execute_assertions(self, name, step):
        for assertion in step:
            description = self._describe(assertion)
            try:
                assertion(self)
                self._result.names[name].append(description)
            except ShouldError as e:
                self._result.failures.append((description, e))
            except Exception as e:
                self._result.errors[name].append((description, e))

    def _execute_step(self, name, step):
        step(self)
        self._result.names[name] = self._describe(step)

    def _describe(self, object):
        return object.__name__.replace('_', ' ')
