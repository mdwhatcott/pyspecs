PYSPECS_PREFIX = '_pyspecs_'
PYSPECS_STEP = PYSPECS_PREFIX + 'step'
SPEC = 'spec'
GIVEN_STEP = 'given'
WHEN_STEP = 'when'
COLLECT_STEP = 'collect'
THEN_STEP = 'then'
AFTER_STEP = 'after'
ALL_STEPS = [
    GIVEN_STEP,
    WHEN_STEP,
    COLLECT_STEP,
    THEN_STEP,
    AFTER_STEP,
]


def _step(name):
    def decorator(object):
        setattr(object, PYSPECS_STEP, name)
        return object
    return decorator


given = _step(GIVEN_STEP)
when = _step(WHEN_STEP)
collect = _step(COLLECT_STEP)
then = _step(THEN_STEP)
after = _step(AFTER_STEP)