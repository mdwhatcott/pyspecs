from StringIO import StringIO
from collections import OrderedDict
import traceback
from abc import abstractmethod
import sys
from pyspecs._spec import SpecInitializationError
from pyspecs._should import ShouldError
from pyspecs._steps import THEN_STEP, COLLECT_STEP, AFTER_STEP


class Reporter(object):
    def __init__(self, capture=None):
        self.captured = capture or StringIO()
        self.specs = list() # list of 'specs', each a list of ReportableSteps
        self.current = list()
        self.results = dict(Passed=0, Failed=0, Errors=0)

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
        self.specs.append(self.current)
        self.current = list()

    @abstractmethod
    def finish(self):
        pass

    def _retrieve_captured_output(self):
        output = self.captured.getvalue()
        self.captured.buf = str()
        return output

    def _log_step(self, spec_name, step, step_name, exc_stuff=None, output=None):
        self.current.append(
            ReportableStep(spec_name, step, step_name, exc_stuff, output))


class StoryReporter(Reporter):
    def __init__(self, console, capture=None):
        Reporter.__init__(self, capture)
        self.console = console
        self.results = OrderedDict.fromkeys([PASSED, FAILED, ERRORS])
        for key in self.results:
            self.results[key] = 0

    def success(self, spec_name, step, step_name):
        Reporter.success(self, spec_name, step, step_name)

    def failure(self, spec_name, step_name, exc_stuff):
        Reporter.failure(self, spec_name, step_name, exc_stuff)

    def error(self, spec_name, step, step_name, exc_stuff):
        Reporter.error(self, spec_name, step, step_name, exc_stuff)

    def spec_complete(self):
        steps = [step for step in self.current
                 if step.exc_info or step.step not in [COLLECT_STEP, AFTER_STEP]]
        self.console.write(format_spec_for_console(steps))
        Reporter.spec_complete(self)

    def finish(self):
        report_problematic_specs_to_console(self.console, self.specs)
        report_statistics_to_console(self.console, self.specs, self.results)


class DotReporter(Reporter):
    def __init__(self, console, capture=None):
        Reporter.__init__(self, capture)
        self.console = console
        self.results = OrderedDict.fromkeys([PASSED, FAILED, ERRORS])
        for key in self.results:
            self.results[key] = 0

    def success(self, spec_name, step, step_name):
        Reporter.success(self, spec_name, step, step_name)
        if step == THEN_STEP:
            self.console.write('.')

    def failure(self, spec_name, step_name, exc_stuff):
        Reporter.failure(self, spec_name, step_name, exc_stuff)
        self.console.write('x')

    def error(self, spec_name, step, step_name, exc_stuff):
        Reporter.error(self, spec_name, step, step_name, exc_stuff)
        self.console.write('e')

    def spec_complete(self):
        Reporter.spec_complete(self)

    def finish(self):
        report_problematic_specs_to_console(self.console, self.specs)
        report_statistics_to_console(self.console, self.specs, self.results)


def report_problematic_specs_to_console(console, specs):
    console.write('\n\n')
    problematic_specs = [format_spec_for_console(s) for s in specs
                         if any(step.exc_info for step in s)]
    for spec in problematic_specs:
        console.write(spec)


def format_spec_for_console(spec):
    formatted = StringIO()
    formatted.write(str('     SPEC {0}\n'.format(spec[0].spec_name)))

    for step in spec:
        formatted.write(format_step_for_console(step))

    formatted.write(format_captured_output_for_console(spec))

    return formatted.getvalue()


def format_captured_output_for_console(spec):
    formatted = StringIO()

    if any(s.exc_info for s in spec) and any(s.output for s in spec):
        formatted.write('-' * 31 + ' Captured Output ' + '-' * 31 + '\n')
        for step in spec:
            if step.output:
                formatted.write(str('| ({0} {1})\n'.format(
                    step.step.upper(), step.step_name)))
                pretty_output = '\n| '.join(step.output.split('\n'))
                formatted.write('| ' + pretty_output + '\n')
        formatted.write('-' * 79)
    formatted.write('\n\n')

    return formatted.getvalue()


def format_step_for_console(step):
    formatted = StringIO()

    step_sequence = step.step.upper()\
        if step.step != 'collect steps'\
        else '.'
    exc_message = '- ' + repr(step.exception_value)\
        if step.exc_info is not None\
        else ''

    formatted.write(str('{0:>9} {1} {2}\n'.format(
        step_sequence, step.step_name, exc_message)))

    if step.exc_info is None:
        return formatted.getvalue()

    formatted.write(
          '        . ' +
        '\n        . '.join(step.format_exception()) +
        '\n')

    return formatted.getvalue()


def report_statistics_to_console(console, specs, results):
    assertions = sum(len([step for step in spec if step.step == THEN_STEP])
        for spec in specs)

    console.write('Ran {0} specs with {1} assertions.'.format(
        len(specs), assertions))

    if not results['Failed'] and not results['Errors']:
        console.write(' (ok)\n')
    else:
        console.write('\n\n')
        for key, value in results.iteritems():
            console.write('{0}: {1}\n'.format(key, value))


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
        if isinstance(self.exception_value, SpecInitializationError):
            exc.remove(exc[1])
        elif isinstance(self.exception_value, ShouldError):
            if len(exc) >= 3:
                exc = exc[:-3]

        return '\n'.join(exc).replace('\n\n', '\n').strip().split('\n')


ERRORS = 'Errors'
FAILED = 'Failed'
PASSED = 'Passed'