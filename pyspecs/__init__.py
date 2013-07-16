# Done: setup.py
# Done: test installation and usage (bowling game)
# Done: catalog bowling game example
# TODO: documentation (README, readthedocs?)
# TODO: decide on name and location on github
# TODO: publish to pypi


import sys
from pyspecs._runner import Step, _counter, _step_runner
from pyspecs._should import _Should


__version__ = '2.0'


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