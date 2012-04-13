import inspect
from pyspecs.result import SpecResult
from pyspecs.steps import PYSPECS_STEP, ALL_STEPS, THEN_STEP, SPEC

class Spec(object):
  def collect_steps(self):
    self.steps = dict.fromkeys(ALL_STEPS)
    self.steps[THEN_STEP] = list()
    methods = inspect.getmembers(self.__class__, inspect.ismethod)
    for name, method in methods:
      step = getattr(method, PYSPECS_STEP, None)
      if step in self.steps:
        if step == THEN_STEP:
          self.steps[step].append(method)
        else:
          self.steps[step] = method

  def execute_steps(self):
    result = SpecResult()
    result.names[SPEC] = self.__class__.__name__

    result.start()

    for step_name in [s for s in ALL_STEPS if s in self.steps]:
      step = self.steps[step_name]
      if step_name == THEN_STEP:
        for assertion in step:
          assertion(self)
          result.names[step_name].append(assertion._pyspecs_description)
      else:
        step(self)
        result.names[step_name] = step._pyspecs_description

    result.stop()

    return result