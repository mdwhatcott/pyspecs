import importlib
import os
import time
import StringIO
import traceback


class _StepRunner(object):
    """
    Imports all test files in the project scope. Specs within these files
    should either be at the top level of the module or in a function or class
    that is invoked from the top-level. This service is managed and invoked
    by the framework.
    """
    def __init__(self, reporter):
        self.reporter = reporter

    def load_steps(self, working):
        for root, dirs, files in os.walk(working):
            for f in files:
                if self._is_test_module(f):
                    name = self._derive_module_name(
                        os.path.join(root, f), working)
                    self._import(name)

        self.reporter.aggregate()

    def _is_test_module(self, f):
        return f.endswith('test.py') or \
            f.endswith('tests.py') or \
            (f.startswith('test') and f.endswith('.py'))

    # noinspection PyArgumentList
    def _derive_module_name(self, path, working):
        common = os.path.commonprefix([working, path])
        slice_module_name = slice(len(common) + 1, len(path))
        return path[slice_module_name] \
            .replace('.py', '') \
            .replace('\\', '.') \
            .replace('/', '.')

    def _import(self, name):
        try:
            importlib.import_module(name)
        except (ImportError, NotImplementedError):
            print traceback.format_exc()
            return


class ConsoleReporter(object):
    """
    Makes sure spec steps and aggregated statistics are reported to the console.
    This service is managed and invoked by the framework.
    """
    def __init__(self):
        self._prepare_for_upcoming_run()

    def _prepare_for_upcoming_run(self):
        self._total_duration = 0
        self._scenarios = 0
        self._steps = 0
        self._errors = 0
        self._failures = 0
        self._passed = 0
        self._problem_reports = []

    def report(self, step_report):
        self._scenarios += 1
        self._total_duration += step_report.duration
        self._errors += self._tally(step_report, lambda r: r.error)
        self._failures += self._tally(step_report, lambda r: r.failure)
        all_passed = self._tally(step_report, lambda r: r.traceback is None)
        all_steps = self._tally(step_report, lambda r: r)
        self._steps += all_steps
        self._passed += all_passed

        if all_passed < all_steps:
            self._problem_reports.append(step_report)
        else:
            print step_report

    def _tally(self, report, selector):
        total = bool(selector(report))
        if not report.children:
            return total

        for child in report.children:
            total += self._tally(child, selector)

        return total

    def aggregate(self):
        if self._problem_reports:
            print '\n******* Problem Scenarios *******\n'
        for problem in self._problem_reports:
            print problem

        duration = round(self._total_duration, 4)
        if not self._failures and not self._errors:
            print 'ok ({0} steps, {1} scenarios in {2} seconds)'.format(
                self._steps, self._scenarios, duration)
        else:
            print '{0} passed, {1} failed, {2} errors ' \
                  '({3} steps, {4} scenarios in {5} seconds)'.format(
                  self._passed, self._failures, self._errors,
                  self._steps, self._scenarios, duration)

        self._prepare_for_upcoming_run()


class _StepReport(object):
    """
    Each instance is a node in a doubly-linked tree, making aggregation of
    formatting via recursion elegant. These instances are created and managed
    by the framework.
    """
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
        builder = StringIO.StringIO()
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
        duration = self._measure_duration()

        return u'{0:2}|{1} {2} {3} {4}\n{5}'.format(
            status, indent, self.LIST_ITEM, name, duration, trace)

    def _format_step_name(self):
        if not self.traceback:
            return self.name

        error = self.error or self.failure
        return self.name + ' <----{0}: {1}---->'.format(
            error.__class__.__name__, error.message).rstrip()

    def _format_traceback(self, indent):
        if not self.traceback:
            return ''

        trace_indent = indent + (' ' * 4)
        template = '. |{0}{{0}}\n'.format(trace_indent)
        raw_trace = traceback.format_tb(self.traceback)
        total_trace = StringIO.StringIO()

        for t in raw_trace:
            line_number, code = t.strip().split('\n')
            total_trace.write(template.format(line_number))
            total_trace.write(template.format(code))

        return total_trace.getvalue()

    def _measure_duration(self):
        duration = round(self.duration, 2)
        if duration < .1:
            return ''
        else:
            return ' (* {0} seconds *)'.format(duration)


class _StepCounter(object):
    """
    This service is responsible for:
        - creation of individual steps and their resultant exceptions
        - timing of individual steps
        - maintaining the scope of the steps that make up a spec
        - assigning the relations between steps (parent, children)

    This service is managed and invoked by the framework.
    """
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


class Step(object):
    """
    Context-manager-based construct that houses the code that makes up
    one of many dynamically named steps within a spec. While several default
    steps are provided by the framework, developers may create others to suit
    their grammatical constructs and tastes.

    >>> by_the_way = Step('by the way', _counter)
    >>> with by_the_way.this_framework_is_awesome:
    ...     pass  # code for the step here...
      | - by the way this framework is awesome
    """
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


_reporter = ConsoleReporter()
_step_runner = _StepRunner(_reporter)
_counter = _StepCounter(_reporter, time.time)