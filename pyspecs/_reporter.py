from StringIO import StringIO
from abc import abstractmethod
import sys


class Reporter(object):
    def __init__(self, io=None):
        self.captured = io or StringIO()

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
    def failure(self, spec_name, step_name, exc_stuff):
        pass

    @abstractmethod
    def error(self, spec_name, step, step_name, exc_stuff):
        pass


class DotReporter(Reporter):
    def __init__(self, console):
        Reporter.__init__(self)
        self.console = console

    def success(self, spec_name, step, step_name):
        self.console.write('.')

    def failure(self, spec_name, step_name, exc_stuff):
        self.console.write('F')

    def error(self, spec_name, step, step_name, exc_stuff):
        self.console.write('E')