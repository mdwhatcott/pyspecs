from collections import defaultdict
from inspect import getmembers, ismethod
from pyspecs.result import SpecResult
from pyspecs.should import ShouldError
from pyspecs.steps import PYSPECS_STEP, ALL_STEPS, THEN_STEP, GIVEN_STEP, WHEN_STEP, COLLECT_STEP, AFTER_STEP


class Spec(object):
    def execute(self):
        self._collect_steps()
        self._result = SpecResult(self._describe(self.__class__))
        self._execute_steps()
        return self._result

    def _collect_steps(self):
        self._steps = defaultdict.fromkeys(ALL_STEPS)
        self._steps[THEN_STEP] = list()
        for name, method in getmembers(self.__class__, ismethod):
            step = getattr(method, PYSPECS_STEP, None)
            if step is None or step not in self._steps:
                continue
            if step == THEN_STEP:
                self._steps[step].append(method)
            else:
                self._steps[step] = method

    def _execute_steps(self):
        ok = self._execute_step(GIVEN_STEP, self._steps[GIVEN_STEP])
        if ok:
            ok = self._execute_step(WHEN_STEP, self._steps[WHEN_STEP])
        if ok:
            ok = self._execute_step(COLLECT_STEP, self._steps[COLLECT_STEP])
        if ok:
            self._execute_assertions(THEN_STEP, self._steps[THEN_STEP])

        self._execute_step(AFTER_STEP, self._steps[AFTER_STEP])

    def _execute_assertions(self, name, step):
        for assertion in step:
            description = self._describe(assertion)
            try:
                with self._result:
                    assertion(self)
            except ShouldError as e:
                self._result.failures.append((description, e))
            except Exception as e:
                self._result.errors[name].append((description, e))
            else:
                self._result.names[name].append(description)

    def _execute_step(self, name, step):
        if step is None:
            return True

        description = self._describe(step)
        try:
            with self._result:
                step(self)
        except Exception as e:
            self._result.errors[name] = (description, e)
            return False
        else:
            self._result.names[name] = description
            return True

    def _describe(self, obj):
        return obj.__name__.replace('_', ' ')
