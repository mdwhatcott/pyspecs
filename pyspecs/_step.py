import sys
import time
import logging
log = logging.getLogger(__name__)
if sys.version < '3':
    from StringIO import StringIO
else:
    from io import StringIO


class Result(object):
    SUCCESS = 'success'
    ERROR = 'error'
    ERROR = 'error'
    FAILURE = 'failure'
    ABORT = 'abort'
    NOT_EXECUTED = 'not executed'
    CHILD_ERROR = 'child error'

    def __init__(self):
        self.kind = self.NOT_EXECUTED
        self.exc_type = None
        self.exc_val = None
        self.exc_tb = None

    def set_exception(self, exc_type, exc_val, exc_tb):
        self.exc_type = exc_type
        self.exc_val = exc_val
        self.exc_tb = exc_tb

        if exc_type is None:
            self.kind = self.SUCCESS
        elif isinstance(exc_val, AssertionError):
            self.kind = self.FAILURE
        elif isinstance(exc_val, KeyboardInterrupt):
            self.kind = self.ABORT
        else:
            self.kind = self.ERROR

    @property
    def is_success(self):
        return self.kind == self.SUCCESS

    @property
    def is_error(self):
        return self.kind == self.ERROR

    @property
    def is_failure(self):
        return self.kind == self.FAILURE

    @property
    def is_abort(self):
        return self.kind == self.ABORT

    @property
    def has_children_errors(self):
        return self.kind == self.CHILD_ERROR

    def __str__(self):
        return self.kind


class Step(object):
    def __init__(self, kind, name, registry, timer=time.time):
        self.kind = kind
        self.name = name
        self.registry = registry
        self.timer = timer
        self.start = timer()
        self.stop = None
        self.parent = None
        self.steps = []
        self.result = Result()
        self.previous_stdout = sys.stdout
        self.stdout = StringIO()

    @property
    def duration(self):
        return self.stop - self.start

    @property
    def output(self):
        return (
            self.stdout.buf +
            ''.join([x.output for x in self.steps])
            )

    def write(self, stream):
        self.stdout.write(stream)

    def __enter__(self):
        log.debug('Entering in %s', self.name)
        self.parent = self.registry.push(self)
        sys.stdout = self.stdout

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop = self.timer()
        log.debug('Exiting from %s with %s,%s,%s', self.name, exc_type, exc_val, exc_tb)

        self.registry.pop()
        sys.stdout = self.previous_stdout

        self._set_result(exc_type, exc_val, exc_tb)
        return True

    def __str__(self):
        return '%s %s' % (self.kind, self.name)

    def _set_result(self, exc_type, exc_val, exc_tb):
        if self.result.has_children_errors:
            return
        self.result.set_exception(exc_type, exc_val, exc_tb)
        if self.result.is_abort:
            log.debug('Aborting')
            raise exc_val
        if not self.result.is_success and self.parent:
            log.debug('Sending error to parent')
            self.parent.set_child_error()

    def set_child_error(self):
        self.result.kind = Result.CHILD_ERROR
        if self.parent:
            self.parent.set_child_error()


class StepFactory(object):
    def __init__(self, kind, registry):
        self.kind = kind
        self.registry = registry

    def __getattr__(self, name):
        return self._create_step(name)

    def __call__(self, *args):
        if len(args) != 1:
            raise AttributeError('You may only specify a single name')
        name = ''.join([x if ord(x) < 128 else '-' for x in args[0]])
        return self._create_step(name)

    def _create_step(self, name):
        step = Step(self.kind, name.replace('_', ' '), self.registry)
        return step
