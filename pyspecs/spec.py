from pyspecs._steps import _step
from pyspecs import _steps
from pyspecs._should import This


this = This
given = _step(_steps.GIVEN_STEP)
when = _step(_steps.WHEN_STEP)
collect = _step(_steps.COLLECT_STEP)
then = _step(_steps.THEN_STEP)
after = _step(_steps.AFTER_STEP)


class spec(object):
    """
    Subclass your spec classes from this class to identify them as specs.
    """