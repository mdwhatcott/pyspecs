PYSPECS_PREFIX = '_pyspecs_'
PYSPECS_STEP = PYSPECS_PREFIX + 'step'
SPEC_DESCRIPTION = PYSPECS_PREFIX + 'description'
GIVEN_STEP = 'given'
WHEN_STEP = 'when'
COLLECT_STEP = 'collect'
THEN_STEP = 'then'
AFTER_STEP = 'after'


def _step(name):
    def decorator(object):
        description = object.__name__.replace('_', ' ')
        setattr(object, SPEC_DESCRIPTION, description)
        setattr(object, PYSPECS_STEP, name)
        return object
    return decorator


given = _step(GIVEN_STEP)
when = _step(WHEN_STEP)
collect = _step(COLLECT_STEP)
then = _step(THEN_STEP)
after = _step(AFTER_STEP)