# Done: setup.py
# Done: test installation and usage (bowling game)
# TODO: catalog bowling game example
# TODO: documentation
# TODO: decide on name and location on github
# TODO: publish to pypi


import sys
from pyspecs._runner import _Step, _counter, _step_runner
from pyspecs._should import _Should


__version__ = '2.0'


given = _Step('given', _counter)
provided = _Step('provided', _counter)
at = _Step('at', _counter)
when = _Step('when', _counter)
and_ = _Step('and', _counter)
then = _Step('then', _counter)
so = _Step('so', _counter)
therefore = _Step('therefore', _counter)
however = _Step('however', _counter)
as_well_as = _Step('as well as', _counter)

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