import sys
import traceback
import logging
from ._registry import Registry

log = logging.getLogger(__name__)
if sys.version < '3':
    from StringIO import StringIO
else:
    from io import StringIO
    unichr = chr
    unicode = str


class ConsoleReporter(object):
    """
    Makes sure spec steps and aggregated statistics are reported to the
    console.
    This service is managed and invoked by the framework.
    """
    LIST_ITEM = unichr(0x2022)  # bullet
    INDENT = '  '

    def __init__(self):
        self.out = sys.__stdout__
        self.duration = 0
        self.steps = 0
        self._errors = 0
        self._failures = 0
        self._passed = 0
        self._problem_reports = []
        self.captured = StringIO()

    def render(self, step_runner):
        registry = Registry()
        steps = registry.root_steps

        for step in steps:
            self._gather_stats(step)

        success_steps = [x for x in steps if x.result.is_success]
        failed_steps = [x for x in steps if not x.result.is_success]

        for step in success_steps:
            self.render_step(step)
            print('')

        if len(failed_steps):
            print('\n********************* FAILURES *****************\n')

        for step in failed_steps:
            self.render_step(step)
            print('')

        print('{steps} steps, {scenarios} scenarios in {duration} seconds'
              .format(scenarios=len(steps), steps=registry.total_steps, duration=self.duration))

    def _gather_stats(self, step):
        self.steps += 1
        self.duration += step.duration
        self._errors += 1 if step.result.is_error else 0
        self._failures += 1 if step.result.is_failure else 0
        self._passed += 1 if step.result.is_success else 0

    def render_step(self, step, level=0):
        if step.result.is_success or step.result.has_children_errors:
            self.render_successful_step(step, level)
        else:
            self.render_step_error(step, level)

    def render_successful_step(self, step, level=0):
        indent = self.INDENT * level
        print('  | %s%s %s' % (indent, self.LIST_ITEM, step))
        for child in step.steps:
            self.render_step(child, level+1)

    def render_step_error(self, step, level):
        indent = self.INDENT * level
        letter = self.get_letter(step)
        print('%s | %s%s' % (letter, indent, step))
        print('%s | %sERROR:   %s'
              % (letter, indent, step.result.exc_type.__name__))
        print('%s | %sMESSAGE: %s' % (letter, indent, step.result.exc_val))
        print(self._format_traceback(step.result.exc_tb, letter, level))

        if step.output:
            print('----- output -----')
            print(step.output)
            print('------------------\n')

    def _format_traceback(self, tb, letter, level):
        if not tb:
            return ''
        indent = self.INDENT * level
        raw_trace = traceback.format_tb(tb)
        template = '{0} |{1} TRACE>{{0}}\n'.format(letter, indent)
        result = '{0} |\n'.format(letter)

        for t in reversed(raw_trace):
            line_number, code = t.strip().split('\n')
            result += template.format(line_number)
            result += template.format(code)

        return result

    def get_letter(self, step):
        return (
            ' ' if step.result.is_success else
            'F' if step.result.is_failure else
            '.' if step.result.is_abort else
            'E'
            )
