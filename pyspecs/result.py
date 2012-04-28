from cStringIO import StringIO
import datetime
import sys
from pyspecs.steps import THEN_STEP, ALL_STEPS, SPEC


class SpecResult(object):
  def __init__(self, spec_name):
    self.names = dict.fromkeys(ALL_STEPS)
    self.errors = dict.fromkeys(ALL_STEPS)
    self.failures = list()
    self._output = StringIO()
    self.names[THEN_STEP] = list()
    self.errors[THEN_STEP] = list()
    self._started = None
    self._stopped = None
    self.names[SPEC] = spec_name
    self._stdout = None

  @property
  def passed(self):
    return all(error is None or not error for error in self.errors.values())

  def start_timer(self):
    self._stdout = sys.stdout
    sys.stdout = self._output
    self._started = datetime.datetime.utcnow()

  def stop_timer(self):
    sys.stdout = self._stdout
    self._stopped = datetime.datetime.utcnow()

  @property
  def duration(self):
    return self._stopped - self._started

  @property
  def output(self):
    return self._output.getvalue()
