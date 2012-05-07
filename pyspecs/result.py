from cStringIO import StringIO
import datetime
import sys
from pyspecs.steps import THEN_STEP, ALL_STEPS, SPEC


class UnimplementedSpecResult(object):
    def __init__(self, spec_name):
        self.spec_name = spec_name


class SpecResult(object):
    def __init__(self, spec_name):
        self.names = dict.fromkeys(ALL_STEPS)
        self.errors = dict.fromkeys(ALL_STEPS)
        self.failures = list()
        self._capture = StringIO()
        self.names[THEN_STEP] = list()
        self.errors[THEN_STEP] = list()
        self._started = datetime.datetime.utcnow()
        self.names[SPEC] = spec_name

    @property
    def passed(self):
        return all(error is None or not error
            for error in self.errors.values())

    def duration(self):
        return datetime.datetime.utcnow() - self._started

    @property
    def output(self):
        return self._capture.getvalue()

    def __enter__(self):
        sys.stdout = self._capture
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = sys.__stdout__
        return not any((exc_type, exc_val, exc_tb))
