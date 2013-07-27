import StringIO
import traceback
import sys


class ConsoleReporter(object):
    """
    Makes sure spec steps and aggregated statistics are reported to the console.
    This service is managed and invoked by the framework.
    """
    def __init__(self):
        self.out = sys.__stdout__
        self._prepare_for_upcoming_run()
        self.captured = StringIO.StringIO()

    def write(self, captured):
        self.captured.write(captured)

    def _print(self, object_, newline='\n'):
        self.out.write(str(object_) + newline)
        self.out.flush()

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
            self._print(step_report)

    def _tally(self, report, selector):
        total = bool(selector(report))
        if not report.children:
            return total

        for child in report.children:
            total += self._tally(child, selector)

        return total

    def aggregate(self):
        if self._problem_reports:
            self._print('\n******* Problem Scenarios *******\n')
        for problem in self._problem_reports:
            print problem

        duration = round(self._total_duration, 4)
        if not self._failures and not self._errors:
            self._print(
                '{0} steps, {1} scenarios in {2} seconds\n\nok'.format(
                    self._steps, self._scenarios, duration))
        else:
            self._print(
                '{0} passed, {1} failed, {2} errors '
                '({3} steps, {4} scenarios in {5} seconds)'.format(
                    self._passed, self._failures, self._errors,
                    self._steps, self._scenarios, duration))

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
        self.captured_output = StringIO.StringIO()

    def write(self, value):
        self.captured_output.write(str(value))

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
        duration = self._measure_duration()
        trace = self._format_traceback(indent)

        return u'{0:2}|{1} {2} {3} {4}\n{5}'.format(
            status, indent, self.LIST_ITEM, self.name, duration, trace)

    def _format_traceback(self, indent):
        if not self.traceback:
            return ''

        trace_indent = indent + (' ' * 6)
        template = '. |{0}{{0}}\n'.format(trace_indent)
        raw_trace = traceback.format_tb(self.traceback)
        total_trace = StringIO.StringIO()

        for t in reversed(raw_trace):
            line_number, code = t.strip().split('\n')
            total_trace.write(template.format(line_number))
            total_trace.write(template.format(code))

        total_trace.write(template.format(self._format_exception_message()))

        return total_trace.getvalue() + self._collect_captured_output() + '\n'

    def _format_exception_message(self):
        error = self.error or self.failure
        return '{0}: {1}'.format(
            error.__class__.__name__, error.message).rstrip()

    def _measure_duration(self):
        duration = round(self.duration, 2)
        if duration < .1:
            return ''
        else:
            return ' (* {0} seconds *)'.format(duration)

    def _collect_captured_output(self):
        output = self.captured_output.getvalue()
        if not output:
            return output

        top_border = ('=' * 31) + ' Captured Output ' + ('=' * 31)
        bottom_border = '=' * 79
        return '\n{0}\n{1}\n{2}'.format(top_border, output, bottom_border)