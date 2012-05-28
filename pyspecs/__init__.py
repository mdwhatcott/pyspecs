from pyspecs._steps import _step, _skip
from pyspecs import _steps
from pyspecs._should import This as _This


this = the = that = it = then_ = _This

given = _step(_steps.GIVEN_STEP)
when = _step(_steps.WHEN_STEP)
collect = _step(_steps.COLLECT_STEP)
then = _step(_steps.THEN_STEP)
after = _step(_steps.AFTER_STEP)
skip = _skip


class spec(object):
    """
    Subclass your spec classes from this class to identify them as specs.
    """