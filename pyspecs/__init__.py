import os
import sys
import time
from pyspecs._reporting import ConsoleReporter
from pyspecs._runner import _StepRunner
from pyspecs._should import _Should
from pyspecs._step import Step, _StepCounter


__version__ = '2.1'


_reporter = ConsoleReporter()
_counter = _StepCounter(_reporter, time.time)
_step_runner = _StepRunner(_reporter)


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
    sys.exc_clear()
    try:
        callable_()
    except:
        return sys.exc_info()
    else:
        return None
    finally:
        sys.exc_clear()


def main():
    working = os.getcwd()
    sys.path.append(working)
    _step_runner.load_steps(working)


if __name__ == '__main__':
    main()