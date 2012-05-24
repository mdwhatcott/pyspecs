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


class DotReporter(Reporter):
    def __init__(self, console, capture=None):
        Reporter.__init__(self, capture)
        self.console = console
        self.specs = list() # list of 'specs', each a list of ReportableSteps
        self.results = OrderedDict.fromkeys(['Passed', 'Failed', 'Errors'])
        for key in self.results:
            self.results[key] = 0

    def success(self, spec_name, step, step_name):
        self._log_step(spec_name, step, step_name)
        if step == THEN_STEP:
            self.console.write('.')
            self.results['Passed'] += 1

    def failure(self, spec_name, step_name, exc_stuff):
        self._log_step(spec_name, THEN_STEP, step_name, exc_stuff)
        self.console.write('x')
        self.results['Failed'] += 1

    def error(self, spec_name, step, step_name, exc_stuff):
        self._log_step(spec_name, step, step_name, exc_stuff)
        self.console.write('e')
        self.results['Errors'] += 1

    def _log_step(self, spec_name, step, step_name, exc_stuff=None):
        if not len(self.specs) or spec_name != self.specs[-1][-1].spec_name:
            self.specs.append(list())

        self.specs[-1].append(
            ReportableStep(spec_name, step, step_name, exc_stuff))

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
    formatted = StringIO()

    formatted.write(str('  SUBJECT {0}\n'.format(spec[0].spec_name)))
    for step in spec:
        format_step_for_console(formatted, step)

    formatted.write('\n\n')

    return formatted.getvalue()


def format_step_for_console(formatted, step):
    step_name = step.step.upper()\
        if step.step != 'collect steps'\
        else '.'
    exc_message = '- ' + repr(step.exception_value)\
        if step.exc_info is not None\
        else ''

    formatted.write(str('{0:>9} {1} {2}\n'.format(
        step_name, step.step_name, exc_message)))

    if step.exc_info is None:
        return

    formatted.write(
          '        . ' +
        '\n        . '.join(step.format_exception()) +
        '\n')


class ReportableStep(object):
    def __init__(self, spec_name, step, step_name, exc_info):
        self.spec_name = spec_name
        self.step = step
        self.step_name = step_name
        self.exc_info = exc_info

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