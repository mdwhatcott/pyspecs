from collections import OrderedDict
from inspect import getmembers, ismethod
from pyspecs.result import SpecResult
from pyspecs.should import ShouldError
from pyspecs.steps import PYSPECS_STEP, ALL_STEPS, THEN_STEP

class Spec(object):
  def collect_steps(self):
    steps = OrderedDict.fromkeys(ALL_STEPS)
    self._collect_steps(steps)
    return steps

  def _collect_steps(self, steps):
    steps[THEN_STEP] = list()
    for name, method in getmembers(self.__class__, ismethod):
      step = getattr(method, PYSPECS_STEP, None)
      if not step in steps:
        continue
      if step == THEN_STEP:
        steps[step].append(method)
      else:
        steps[step] = method

  def execute_steps(self, steps):
    result = SpecResult(self._describe(self.__class__))
    result.start_timer()
    self._execute_steps(steps, result)
    result.stop_timer()
    return result

  def _execute_steps(self, steps, result):
    for name, step in steps.iteritems():
      if step is None:
        continue
      if name == THEN_STEP:
        self._execute_assertions(name, result, step)
      else:
        self._execute_step(name, result, step)

  def _execute_assertions(self, name, result, step):
    for assertion in step:
      description = self._describe(assertion)
      try:
        assertion(self)
        result.names[name].append(description)
      except ShouldError as e:
        result.errors[name].append((description, e))

  def _execute_step(self, name, result, step):
    step(self)
    result.names[name] = self._describe(step)

  def _describe(self, object):
    return object.__name__.replace('_', ' ')
