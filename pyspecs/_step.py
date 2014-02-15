import sys
from pyspecs._reporting import _StepReport


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
        sys.stdout = report
        self._associate_report(report, self.current_step is None)
        report.started = self.timer()

    def _associate_report(self, report, top_level):
        if top_level:
            self.steps.append(report)
        else:
            self.current_step.children.append(report)
            report.parent = self.current_step

        self.current_step = report

    def finish(self):
        self.current_step.finished = self.timer()
        if self.current_step.parent is None:
            self.reporter.report(self.current_step)

        self.current_step = self.current_step.parent
        sys.stdout = sys.__stdout__

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

    >>> from pyspecs import _counter
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

    def __call__(self, *args):
        if len(args) != 1:
            raise AttributeError('You may only specify a single name')
        self._name = ''.join([x if ord(x) < 128 else '-' for x in args[0]])
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
            raise exc_val  # exit()?

        else:
            self._counter.error(exc_type, exc_val, exc_tb)

        self._name = None
        return True
