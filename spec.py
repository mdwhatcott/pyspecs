from StringIO import StringIO
import importlib
import os
import time
import traceback
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
                    # TODO: magic to get the module name right
                    importlib.import_module(f)

        self.reporter.aggregate()


class ConsoleReporter(object):
    # TODO: report each step's success/failure/error
    # TODO: report nice stack traces (remove framework entries)
    # TODO: report final stats
    # TODO: verbosity...

    def report(self, step_report):
        print step_report

    def aggregate(self):
        pass


class StepReport(object):
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

        if self.error:
            return self.name + ' (*{0}: {1})'.format(
                self.error.__class__.__name__, self.error.message).rstrip()
        elif self.failure:
            return self.name + ' (*{0}: {1})'.format(
                self.failure.__class__.__name__, self.failure.message).rstrip()

        return ''

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
provided = Step('provided', counter)
at = Step('at', counter)
when = Step('when', counter)
and_ = Step('and', counter)
then = Step('then', counter)
so = Step('so', counter)
therefore = Step('therefore', counter)
however = Step('however', counter)
as_well_as = Step('as well as', counter)

the = Should
it = Should
this = Should


# TODO: this goes in a script installed in the path
if __name__ == '__main__':
    runner.load_steps()