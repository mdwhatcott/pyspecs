import sys
import time
from pyspecs._reporting import ConsoleReporter
from pyspecs._runner import _StepRunner
from pyspecs._should import _Should
from pyspecs._step import Step, _StepCounter


__version__ = '2.2'


_reporter = ConsoleReporter()
_counter = _StepCounter(_reporter, time.time)
_step_runner = _StepRunner()
_reporter.aggregate()

given = Step('given', _counter)
provided = Step('provided', _counter)
at = Step('at', _counter)
when = Step('when', _counter)
and_ = Step('and', _counter)
then = Step('then', _counter)
so = Step('so', _counter)
therefore = Step('therefore', _counter)
however = Step('however', _counter)
as_well_as = Step('as well as', _counter)

the = _Should
it = _Should
this = _Should
that = _Should


# noinspection PyBroadException
def catch(callable_):
    """
    Utility method for saving any exceptions raised from a callable.
    """
    def exc_clear():
        if sys.version < '3':
            sys.exc_clear()
    exc_clear()
    try:
        callable_()
    except:
        return sys.exc_info()[1]
    else:
        return None
    finally:
        exc_clear()


def finish():
    """
    Call this method from your test script after all scenarios like so:

    if __name__ == '__main__':
        pyspecs.finish()

    This allows you to invoke your test file as a main module, limiting
    the scenarios executed to those in the file in question.
    """
    _reporter.aggregate()
