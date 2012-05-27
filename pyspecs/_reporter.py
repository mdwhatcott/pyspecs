from StringIO import StringIO
import sys
import time
import traceback
from pyspecs._spec import SpecInitializationError
from pyspecs._should import ShouldError
from pyspecs._steps import THEN_STEP, COLLECT_STEP, AFTER_STEP


class Reporter(object):
    def __init__(self, capture=None):
        self.captured = capture or StringIO()
        self.specs = list()
        self.current_spec = list()
        self.results = dict.fromkeys([PASSED, FAILED, ERRORS])
        self.finished = None
        self.started = time.time()

    def __enter__(self):
        sys.stdout = self.captured
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = sys.__stdout__
        return not any([exc_type, exc_val, exc_tb])

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
        self.current_spec = list()

    def finish(self):
        self.finished = time.time()

    def _retrieve_captured_output(self):
        output = self.captured.getvalue()
        self.captured.buf = str()
        return output

    def _log_step(self, spec_name, step, step_name, exc_stuff=None, output=None):
        self.current_spec.append(
            ReportableStep(spec_name, step, step_name, exc_stuff, output))


class ConsoleReporter(Reporter):
    def __init__(self, console, verbosity=0, capture=None):
        Reporter.__init__(self, capture)
        self.console = console
        for key in self.results:
            self.results[key] = 0
        self.verbosity = verbosity

    def success(self, spec_name, step, step_name):
        Reporter.success(self, spec_name, step, step_name)
        if not self.verbosity and step == THEN_STEP:
            self.console.write('.')

    def failure(self, spec_name, step_name, exc_stuff):
        Reporter.failure(self, spec_name, step_name, exc_stuff)
        if not self.verbosity:
            self.console.write('x')

    def error(self, spec_name, step, step_name, exc_stuff):
        Reporter.error(self, spec_name, step, step_name, exc_stuff)
        if not self.verbosity:
            self.console.write('e')

    def spec_complete(self):
        if self.verbosity:
            steps = [step for step in self.current_spec
                if step.exc_info or step.step not in [COLLECT_STEP, AFTER_STEP]]
            self.console.write(self._format_spec(steps))
        Reporter.spec_complete(self)

    def finish(self):
        Reporter.finish(self)
        self._report_problematic_specs()
        self._report_statistics()

    def _report_problematic_specs(self):
        problematic_specs = [self._format_spec(s) for s in self.specs
            if any(step.exc_info for step in s)]
        if len(problematic_specs):
            self.console.write('\n\n' + '-' * 79 + '\n\n')
        for spec in problematic_specs:
            self.console.write(spec)

    def _format_spec(self, spec):
        formatted = StringIO()
        formatted.write('"{}"\n'.format(spec[0].spec_name))

        for step in spec:
            formatted.write(self._format_step(step))

        formatted.write(self._format_captured_output(spec))

        return formatted.getvalue()

    def _format_captured_output(self, spec):
        formatted = StringIO()

        if any(s.exc_info for s in spec) and any(s.output for s in spec):
            formatted.write('-' * 31 + ' Captured Output ' + '-' * 31 + '\n')
            for step in spec:
                if step.output:
                    formatted.write('| ({} {})\n'.format(
                        step.step.upper(), step.step_name))
                    pretty_output = '\n| '.join(step.output.split('\n'))
                    formatted.write('| ' + pretty_output + '\n')
            formatted.write('-' * 79)
        formatted.write('\n\n')

        return formatted.getvalue()

    def _format_step(self, step):
        formatted = StringIO()

        step_sequence = step.step\
            if step.step != 'collect steps'\
            else '({}) - '.format(step.step)
        exc_message = '- ' + repr(step.exception_value)\
            if step.exc_info is not None\
            else str()

        formatted.write('     {} {} {}\n'.format(
            step_sequence, step.step_name, exc_message))

        if step.exc_info is None:
            return formatted.getvalue()

        formatted.write(
              '     . ' +
            '\n     . '.join(step.format_exception()) +
            '\n')

        return formatted.getvalue()

    def _report_statistics(self):
        message = StringIO()

        assertions = sum(len([step for step in spec if step.step == THEN_STEP])
                    for spec in self.specs)

        message.write('\n' + '-' * 79 + '\n')
        summary = 'Ran {} specs with {} assertions in {:.3f}s.\n\n'.format(
            len(self.specs), assertions, self.finished - self.started)
        message.write(summary)

        passed = not self.results[FAILED] and not self.results[ERRORS]
        message.write('(ok)\n' if passed else 'FAILED ({}={}, {}={})\n'.format(
                FAILED, self.results[FAILED],
                ERRORS, self.results[ERRORS]))

        self.console.write(message.getvalue())


class ReportableStep(object):
    def __init__(self, spec_name, step, step_name, exc_info=None, output=None):
        self.spec_name = spec_name
        self.step = step
        self.step_name = step_name
        self.exc_info = exc_info
        self.output = output or str()

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

        return '\n'.join(exc).replace('\n\n', '\n').strip().split('\n')

    def _remove_internal_traces(self, exc):
        if isinstance(self.exception_value, SpecInitializationError):
            exc.remove(exc[1])
        elif isinstance(self.exception_value, ShouldError):
            if len(exc) >= 5:
                exc = [exc[0]] + exc[2:-3]
        elif isinstance(self.exception_value, Exception):
            if len(exc) >= 2:
                exc.remove(exc[1])

        return exc


ERRORS = 'errors'
FAILED = 'failed'
PASSED = 'passed'