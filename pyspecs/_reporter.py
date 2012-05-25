from StringIO import StringIO
from collections import OrderedDict
import traceback
from abc import abstractmethod
import sys
from pyspecs._runner import SpecInitializationError
from pyspecs._steps import THEN_STEP


class Reporter(object):
    def __init__(self, capture=None):
        self.captured = capture or StringIO()

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

    @abstractmethod
    def finish(self):
        pass


ERRORS = 'Errors'
FAILED = 'Failed'
PASSED = 'Passed'



class DotReporter(Reporter):
    def __init__(self, console, capture=None):
        Reporter.__init__(self, capture)
        self.console = console
        self.specs = list() # list of 'specs', each a list of ReportableSteps
        self.results = OrderedDict.fromkeys([PASSED, FAILED, ERRORS])
        for key in self.results:
            self.results[key] = 0

    def success(self, spec_name, step, step_name):
        output = self._retrieve_captured_output()
        self._log_step(spec_name, step, step_name, output=output)
        if step == THEN_STEP:
            self.console.write('.')
            self.results[PASSED] += 1

    def failure(self, spec_name, step_name, exc_stuff):
        output = self._retrieve_captured_output()
        self._log_step(spec_name, THEN_STEP, step_name, exc_stuff, output)
        self.console.write('x')
        self.results[FAILED] += 1

    def error(self, spec_name, step, step_name, exc_stuff):
        output = self._retrieve_captured_output()
        self._log_step(spec_name, step, step_name, exc_stuff, output)
        self.console.write('e')
        self.results[ERRORS] += 1

    def _retrieve_captured_output(self):
        output = self.captured.getvalue()
        self.captured.buf = str()
        return output

    def _log_step(self, spec_name, step, step_name, exc_stuff=None, output=None):
        if not len(self.specs) or spec_name != self.specs[-1][-1].spec_name:
            self.specs.append(list())

        self.specs[-1].append(
            ReportableStep(spec_name, step, step_name, exc_stuff, output))

    def finish(self):
        self.report_problematic_specs()
        self.report_statistics()

    def report_problematic_specs(self):
        self.console.write('\n\n')
        problematic_specs = [format_spec_for_console(s) for s in self.specs
                             if any(step.exc_info for step in s)]
        for spec in problematic_specs:
            self.console.write(spec)

    def report_statistics(self):
        self.console.write('Ran {0} specs with {1} assertions.'.format(
            len(self.specs), sum(len(spec) for spec in self.specs)))
        if not self.results['Failed'] and not self.results['Errors']:
            self.console.write(' (ok)\n')
        else:
            self.console.write('\n\n')
            for key, value in self.results.iteritems():
                self.console.write('{0}: {1}\n'.format(key, value))


def format_spec_for_console(spec):
    formatted = StringIO('  SUBJECT {0}\n'.format(spec[0].spec_name))

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
        if self.exception_type != SpecInitializationError:
            exc.remove(exc[1])

        return '\n'.join(exc).replace('\n\n', '\n').strip().split('\n')