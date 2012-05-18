# Several flavors (
#   DotConsoleReporter,
#   StoryConsoleReporter,
#   HtmlReporter,
#
#   JsonReporter,
#   GrowlReporter,
#   etc...,
# )
# 1. Receive executed step
# 2. Formulate representation of step and its parent spec for report (text, html, etc...)
# 3. Show overview/stats

from StringIO import StringIO
from abc import abstractmethod
import sys


class Reporter(object):
    def __init__(self, io=None):
        self.captured = io or StringIO()

    def capture_stdout(self):
        return self.__enter__()

    def __enter__(self):
        sys.stdout = self.captured
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = sys.__stdout__
        return not any([exc_type, exc_val, exc_tb])

    @abstractmethod
    def success(self, spec_name, step, step_name):
        pass

    @abstractmethod
    def failure(self, step, exc_stuff):
        pass

    @abstractmethod
    def error(self, step, exc_stuff):
        pass


class DotReporter(Reporter):
    def __init__(self):
        Reporter.__init__(self)

    def success(self, spec_name, step, step_name):
        pass

    def failure(self, step, exc_stuff):
        pass

    def error(self, step, exc_stuff):
        pass