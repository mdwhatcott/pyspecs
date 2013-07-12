from StringIO import StringIO
import importlib
import os
import time
import traceback
import sys
from _should import _Should


__version__ = '2.0'


class _StepRunner(object):
    def __init__(self, reporter):
        self.reporter = reporter
        self.working = os.getcwd()
        sys.path.append(self.working)  # precautionary??

    def load_steps(self):
        for root, dirs, files in os.walk(self.working):
            for f in files:
                if self._is_test_module(f):
                    name = self._derive_module_name(os.path.join(root, f))
                    self._import(name)

        self.reporter.aggregate()

    def _is_test_module(self, f):
        return f.endswith('test.py') or \
            f.endswith('tests.py') or \
            (f.startswith('test') and f.endswith('.py'))

    # noinspection PyArgumentList
    def _derive_module_name(self, path):
        common = os.path.commonprefix([self.working, path])
        slice_module_name = slice(len(common) + 1, len(path))
        return path[slice_module_name] \
            .replace('.py', '') \
            .replace('\\', '.') \
            .replace('/', '.')

    def _import(self, name):
        try:
            importlib.import_module(name)
        except (ImportError, NotImplementedError):
            return


class ConsoleReporter(object):
    # TODO: report nice stack traces (remove framework entries)
    # TODO: report final stats
    # TODO: verbosity...

    def __init__(self):
        self._total_elapsed = 0
        self._shortest_parent_step = None
        self._longest_parent_step = None
        self._average_parent_step_duration = None
        self._average_child_step_duration = None

        self._steps = 0
        self._errors = 0
        self._failures = 0
        self._passed = 0

    def report(self, step_report):
        self._steps += 1
        print step_report

    def aggregate(self):
        print '{0} passed, {1} failed, {2} errors ({3} total)'.format(
            self._passed, self._failures, self._errors, self._steps)


class _StepReport(object):
    PASSED = ''            # no news is good news
    FAILED = 'X'           # ballot 'x'
    ERROR = 'E'            # fire
    SKIPPED = 'S'          # white flag
    LIST_ITEM = u'\u2022'  # bullet
    INDENT = '  '

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
        return self._format(0) + '\n'

    def _format(self, level):
        builder = StringIO()
        message = self._compose_message(level)
        builder.write(message.encode('utf-8'))
        for c in self.children:
            builder.write(c._format(level + 1))

        return builder.getvalue()

    def _compose_message(self, level):
        status = self.PASSED if self.traceback is None else (
            self.FAILED if self.error is None else self.ERROR)
        indent = self.INDENT * level
        name = self._format_step_name()
        trace = self._format_traceback(indent)

        return u'{0:2}|{1} {2} {3}\n{4}'.format(
            status, indent, self.LIST_ITEM, name, trace)

    def _format_step_name(self):
        if not self.traceback:
            return self.name

        error = self.error or self.failure
        return self.name + ' (*{0}: {1})'.format(
            error.__class__.__name__, error.message).rstrip()

    def _format_traceback(self, indent):
        if not self.traceback:
            return ''

        trace_indent = indent + (' ' * 4)
        template = '. |{0}{{0}}\n'.format(trace_indent)
        raw_trace = traceback.format_tb(self.traceback)
        total_trace = StringIO()

        for t in raw_trace:
            line_number, code = t.strip().split('\n')
            total_trace.write(template.format(line_number))
            total_trace.write(template.format(code))

        return total_trace.getvalue()


class _StepCounter(object):
    def __init__(self, reporter, timer):
        self.reporter = reporter
        self.timer = timer
        self.current_step = None
        self.steps = []

    def start(self, name):
        report = _StepReport(name)
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


class _Step(object):
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

    def __call__(self, *args, **kwargs):
        """
        TODO: this is where a skip keyword arg could be provided
        TODO: this is where a long-running keyword arg could be provided
        """
        pass

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


_reporter = ConsoleReporter()
_runner = _StepRunner(_reporter)
_counter = _StepCounter(_reporter, time.time)

given = _Step('given', _counter)
provided = _Step('provided', _counter)
at = _Step('at', _counter)
when = _Step('when', _counter)
and_ = _Step('and', _counter)
then = _Step('then', _counter)
so = _Step('so', _counter)
therefore = _Step('therefore', _counter)
however = _Step('however', _counter)
as_well_as = _Step('as well as', _counter)

the = _Should
it = _Should
this = _Should


if __name__ == '__main__':
    _runner.load_steps()