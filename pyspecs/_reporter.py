from StringIO import StringIO
from collections import OrderedDict
import sys
import time
import traceback
from pyspecs._spec import SpecInitializationError
from pyspecs._steps import THEN_STEP, COLLECT_STEP, AFTER_STEP, SKIPPED_SPEC


class Reporter(object):
    def __init__(self, capture=None):
        self.captured = capture or StringIO()
        self.specs = list()
        self.current_spec = list()
        self.results = OrderedDict.fromkeys(
            [SPECS, PASSED, FAILED, ERRORS, SKIPPED_SPECS, SKIPPED])
        self.finished = None
        self.started = time.time()

    def __enter__(self):
        sys.stdout = self.captured
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = sys.__stdout__
        return not any([exc_type, exc_val, exc_tb])

    def skip(self, spec_name, step, step_name):
        self._log_step(spec_name, step, step_name, skipped=True)
        if step == THEN_STEP:
            self.results[SKIPPED] += 1
        elif step == SKIPPED_SPEC:
            self.results[SKIPPED_SPECS] += 1

    def success(self, spec_name, step, step_name):
        output = self._retrieve_captured_output()
        self._log_step(spec_name, step, step_name, output=output)
        if step == THEN_STEP:
            self.results[PASSED] += 1

    def failure(self, spec_name, step_name, exc_stuff):
        output = self._retrieve_captured_output()
        self._log_step(spec_name, THEN_STEP, step_name, exc_stuff, output)
        self.results[FAILED] += 1

    def error(self, spec_name, step, step_name, exc_stuff):
        output = self._retrieve_captured_output()
        self._log_step(spec_name, step, step_name, exc_stuff, output)
        self.results[ERRORS] += 1

    def spec_complete(self):
        self.specs.append(self.current_spec)
        self.results[SPECS] += 1
        self.current_spec = list()

    def finish(self):
        self.finished = time.time()

    def _retrieve_captured_output(self):
        output = self.captured.getvalue()
        self.captured.buf = str()
        return output

    def _log_step(self, spec_name, step, step_name,
                  exc_stuff=None, output=None, skipped=False):
        self.current_spec.append(
            ReportableStep(
                spec_name, step, step_name, exc_stuff, output, skipped))


class ConsoleReporter(Reporter):
    def __init__(self, console, verbose=False, capture=None):
        Reporter.__init__(self, capture)
        self.console = console
        for key in self.results:
            self.results[key] = 0
        self.verbose = verbose
        if self.verbose:
            self.console.write(header('Specs'))

    def skip(self, spec_name, step, step_name):
        Reporter.skip(self, spec_name, step, step_name)
        if not self.verbose and step == THEN_STEP:
            self.console.write('s')

    def success(self, spec_name, step, step_name):
        Reporter.success(self, spec_name, step, step_name)
        if not self.verbose and step == THEN_STEP:
            self.console.write('.')

    def failure(self, spec_name, step_name, exc_stuff):
        Reporter.failure(self, spec_name, step_name, exc_stuff)
        if not self.verbose:
            self.console.write('x')

    def error(self, spec_name, step, step_name, exc_stuff):
        Reporter.error(self, spec_name, step, step_name, exc_stuff)
        if not self.verbose:
            self.console.write('e')

    def spec_complete(self):
        if self.verbose:
            self.console.write(self._format_spec(self.current_spec))
        Reporter.spec_complete(self)

    def finish(self):
        Reporter.finish(self)
        self._report_problematic_specs()
        self._report_statistics()

    def _report_problematic_specs(self):
        problematic_specs = [self._format_spec(s) for s in self.specs
            if any(step.exc_info for step in s)]
        if len(problematic_specs):
            self.console.write(header('Failures/Errors'))
        for spec in problematic_specs:
            self.console.write(spec)

    def _format_spec(self, spec):
        formatted = StringIO()
        formatted.write('"{}"'.format(spec[0].spec_name))
        if spec[0].skipped and len(spec) == 1:
            formatted.write(' (skipped)\n\n\n')
            return formatted.getvalue()

        formatted.write('\n')

        for step in spec:
            formatted.write(self._format_step(step))

        formatted.write(self._format_captured_output(spec))

        return formatted.getvalue()

    def _format_captured_output(self, spec):
        formatted = StringIO()

        if any(s.exc_info for s in spec) and any(s.output for s in spec):
            formatted.write(header('Captured Output', padding='\n'))
            for step in spec:
                if step.output:
                    formatted.write('| ({} {})\n'.format(
                        step.step.upper(), step.step_name))
                    pretty_output = '\n| '.join(step.output.split('\n'))
                    formatted.write('| ' + pretty_output + '\n')
            formatted.write(border())
        formatted.write('\n\n')

        return formatted.getvalue()

    def _format_step(self, step):
        if step.step in [AFTER_STEP, COLLECT_STEP] and step.exc_info is None:
            return str()

        formatted = StringIO()
        name = step.step_name + (' (skipped)' if step.skipped else str())
        message = str()
        if step.step == THEN_STEP and isinstance(step.exception_value, AssertionError):
            message = '(failed)'
        elif step.exc_info is not None:
            message = '(error)'


        padding = '   '
        if step.step == THEN_STEP:
            padding = '   > '
        formatted.write(padding + '{} {} {}\n'.format(step.step, name, message))

        if step.exc_info is None:
            return formatted.getvalue()

        padding = padding.replace('>', ' ')
        formatted.write(
                    padding + '. ' +
            ('\n' + padding + '. ').join(step.format_exception()) +
            '\n')

        return formatted.getvalue()

    def _report_statistics(self):
        self.console.write(header('Statistics'))
        for key, value in self.results.iteritems():
            if value is 0:
                continue
            self.console.write('{0} {1}\n'.format(value, key))

        self.console.write('\nDuration: {:.3f}s\n\n'.format(self.finished - self.started))

        passed = not self.results[FAILED] and not self.results[ERRORS]
        self.console.write('(ok)\n' if passed else 'FAILED\n')


class ReportableStep(object):
    def __init__(self, spec_name, step, step_name,
                 exc_info=None, output=None, skipped=False):
        self.spec_name = spec_name
        self.step = step
        self.step_name = step_name
        self.exc_info = exc_info
        self.output = output or str()
        self.skipped = skipped

    @property
    def exception_type(self):
        return None if self.exc_info is None else self.exc_info[0]

    @property
    def exception_value(self):
        return None if self.exc_info is None else self.exc_info[1]

    def format_exception(self):
        if self.exc_info is None:
            return str()

        exc = traceback.format_exception(*self.exc_info)
        exc = self._remove_internal_traces(exc)

        formatted = '\n'.join(exc).replace('\n\n', '\n').strip().split('\n')
        formatted[-1] = repr(self.exception_value)

        return formatted

    def _remove_internal_traces(self, exc):
        if isinstance(self.exception_value, SpecInitializationError):
            exc.remove(exc[1])
        elif isinstance(self.exception_value, AssertionError):
            if len(exc) >= 5:
                exc = [exc[0]] + exc[2:-3]
        elif isinstance(self.exception_value, Exception):
            if len(exc) >= 2:
                exc.remove(exc[1])

        return exc


SPECS = 'specs'
ERRORS = 'errors'
FAILED = 'assertions failed'
PASSED = 'assertions passed'
SKIPPED = 'assertions skipped'
SKIPPED_SPECS = 'specs skipped'


def header(message, delimiter='-', padding='\n\n'):
    length = len(message) + len('  ')
    border = delimiter * ((80 - length) / 2)
    return '{0}{1} {2} {1}{0}'.format(padding, border, message)


def border(delimiter='-', padding='\n'):
    return '{0}{1}{0}'.format(padding, delimiter * 79)