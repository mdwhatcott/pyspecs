import importlib
import os
import time
from _should import Should


class StepRunner(object):
    def __init__(self, reporter):
        self.reporter = reporter

    def load_steps(self):
        for root, dirs, files in os.walk(os.getcwd()):
            for f in files:
                if f.endswith('test.py') or \
                        f.endswith('tests.py') or \
                        f.startswith('test'):
                    # TODO: magic to get the name and stuff right
                    importlib.import_module(f)

        self.reporter.aggregate()


class ConsoleReporter(object):
    # TODO: report each step's success/failure/error
    # TODO: report nice stack traces (remove framework entries)
    # TODO: report final stats
    # TODO: verbosity...

    def aggregate(self):
        pass


class StepReport(object):
    def __init__(self, name):
        self.name = name
        self.started = None
        self.finished = None
        self.children = []
        self.parent = None
        self.failure_type = None
        self.error_type = None
        self.failure = None
        self.error = None
        self.traceback = None

    @property
    def duration(self):
        return self.finished - self.started

    def __str__(self):
        pass


class StepCounter(object):
    def __init__(self, reporter, timer):
        self.reporter = reporter
        self.timer = timer
        self.current_step = None
        self.steps = []

    def start(self, name):
        report = StepReport(name)
        self._associate_report(report, self.current_step is None)
        report.started = self.timer()

    def _associate_report(self, report, top_level):
        if top_level:
            self.steps.append(report)
        else:  # ? Is a context manager at the same scope as another a child?
            self.current_step.children.append(report)
            report.parent = self.current_step

        self.current_step = report

    def finish(self):
        self.current_step.finished = self.timer()
        if self.current_step.parent is None:
            self.reporter.report(self.current_step)

        self.current_step = self.current_step.parent

    def error(self, exception_type, exception, traceback):
        self.current_step.error_type = exception_type
        self.current_step.error = exception
        self.current_step.traceback = traceback
        self.finish()

    def fail(self, exception_type, exception, traceback):
        self.current_step.failure_type = exception_type
        self.current_step.failure = exception
        self.current_step.traceback = traceback
        self.finish()


class Step(object):
    def __init__(self, step, counter):
        self._step = step
        self._counter = counter
        self._name = None

    @property
    def name(self):
        return '{0} {1}'\
            .format(self._step, self._name or '')\
            .replace('_', ' ')\
            .strip()

    def __getattr__(self, item):
        if self._name is not None:
            raise AttributeError('You may only specify a single name.')

        self._name = item
        return self

    def __enter__(self):
        self._counter.start(self.name)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self._counter.finish()

        elif isinstance(exc_val, AssertionError):
            self._counter.fail(exc_type, exc_val, exc_tb)

        elif isinstance(exc_val, KeyboardInterrupt):
            return False

        else:
            self._counter.error(exc_type, exc_val, exc_tb)

        self._name = None
        return True


reporter = ConsoleReporter()
runner = StepRunner(reporter)
counter = StepCounter(reporter, time.time)

given = Step('given', counter)
when = Step('when', counter)
and_ = Step('and', counter)
then = Step('then', counter)

the = Should
it = Should
this = Should


# TODO: this goes in a script installed in the path
if __name__ == '__main__':
    runner.load_steps()