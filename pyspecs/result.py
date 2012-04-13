import datetime
from pyspecs.steps import THEN_STEP, ALL_STEPS

class SpecResult(object):
  def __init__(self):
    self.names = dict.fromkeys(ALL_STEPS)
    self.errors = dict.fromkeys(ALL_STEPS)
    self.output = dict.fromkeys(ALL_STEPS)
    self.names[THEN_STEP] = list()
    self.errors[THEN_STEP] = list()
    self.output[THEN_STEP] = list()
    self._started = None
    self._stopped = None

  @property
  def passed(self):
    return all(error is None or not error for error in self.errors.values())

  def start(self):
    self._started = datetime.datetime.utcnow()

  def stop(self):
    self._stopped = datetime.datetime.utcnow()

  @property
  def duration(self):
    return self._stopped - self._started
